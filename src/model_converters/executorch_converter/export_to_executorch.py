import sys
import argparse
import traceback
from pathlib import Path

import torch
from torchvision.models import get_model

from executorch.backends.vulkan.partitioner.vulkan_partitioner import VulkanPartitioner
from executorch.backends.xnnpack.partition.xnnpack_partitioner import XnnpackPartitioner
from executorch.exir import to_edge_transform_and_lower

sys.path.append(str(Path(__file__).parent.parent))

from logger_conf import configure_logger  # noqa: E402
from src.xfeat import XFeat as XFeatWrapper  # noqa: E402
from src.tfeat_descriptor import TFeat  # noqa: E402
from src.hardnet_descriptor import HardNet  # noqa: E402
from src.lightglue_pipeline import LightGlueFeatureExtractor  # noqa: E402
from lightglue import LightGlue  # noqa: E402
from lightglue.lightglue import filter_matches, normalize_keypoints  # noqa: E402

logger = configure_logger()

PARTITIONERS = {
    "xnnpack": XnnpackPartitioner(),
    "vulkan": VulkanPartitioner(),
    "none": None,
}

CUSTOM_MODELS = {"tfeat", "hardnet", "d2net", "disk_lightglue", "superpoint_lightglue",
                 "lightglue", "superglue", "xfeat"}


class DiskDenseWrapper(torch.nn.Module):
    def __init__(self, disk_model):
        super().__init__()
        self.model = disk_model

    def forward(self, image):
        heatmaps, descriptors = self.model.heatmap_and_dense_descriptors(image)
        return heatmaps.contiguous(), descriptors.contiguous()


class XFeatDenseWrapper(torch.nn.Module):
    def __init__(self, xfeat_model):
        super().__init__()
        self.model = xfeat_model.net

    def forward(self, image):
        out = self.model(image)
        if not isinstance(out, (list, tuple)):
            return out.contiguous()
        descriptors, reliability = out[0].contiguous(), out[1].contiguous()
        return reliability, descriptors


class D2NetDenseWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model.dense_feature_extraction

    def forward(self, image):
        return self.model(image)


class SuperPointDenseWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, image):
        if image.shape[1] == 3:
            image = image[:, 0:1] * 0.2989 + image[:, 1:2] * 0.5870 + image[:, 2:3] * 0.1140

        m = self.model
        x = m.relu(m.conv1a(image))
        x = m.pool(m.relu(m.conv1b(x)))
        x = m.relu(m.conv2a(x))
        x = m.pool(m.relu(m.conv2b(x)))
        x = m.relu(m.conv3a(x))
        x = m.pool(m.relu(m.conv3b(x)))
        x = m.relu(m.conv4a(x))
        x = m.relu(m.conv4b(x))

        score_logits = m.convPb(m.relu(m.convPa(x)))
        descriptors = m.convDb(m.relu(m.convDa(x)))
        descriptors = torch.nn.functional.normalize(descriptors, p=2, dim=1)
        return score_logits, torch.softmax(score_logits, dim=1), descriptors


class LightGlueFixedWrapper(torch.nn.Module):
    def __init__(self, model, image_height, image_width):
        super().__init__()
        self.model = model
        self.register_buffer("image_size", torch.tensor([image_width, image_height], dtype=torch.float32))

    def forward(self, keypoints0, keypoints1, descriptors0, descriptors1):
        kpts0 = normalize_keypoints(keypoints0, self.image_size).clone()
        kpts1 = normalize_keypoints(keypoints1, self.image_size).clone()

        desc0 = self.model.input_proj(descriptors0.contiguous())
        desc1 = self.model.input_proj(descriptors1.contiguous())
        encoding0 = self.model.posenc(kpts0)
        encoding1 = self.model.posenc(kpts1)

        for layer in self.model.transformers:
            desc0, desc1 = layer(desc0, desc1, encoding0, encoding1)

        scores, _ = self.model.log_assignment[-1](desc0, desc1)
        return filter_matches(scores, self.model.conf.filter_threshold)


def load_model(model_name, weights, input_shape, matcher_features):
    if model_name.lower() in CUSTOM_MODELS:
        logger.info("Loading project model %s", model_name)
        return load_custom_model(model_name, input_shape, matcher_features)

    logger.info("Loading torchvision model %s", model_name)
    model = get_model(model_name, weights=weights)
    return model, model_name


def load_custom_model(name, input_shape, matcher_features):
    name = name.lower()

    if name == "tfeat":
        return TFeat("tfeat", logger, {"device": "cpu"}).model, name

    if name == "hardnet":
        return HardNet("hardnet", logger, {"device": "cpu"}).model, name

    if name == "d2net":
        from src.d2net import D2Net
        extractor = D2Net("d2net", logger, {"device": "cpu"})
        return D2NetDenseWrapper(extractor._model), name

    if name == "xfeat":
        extractor = XFeatWrapper("xfeat", logger, config={"device": "cpu"})
        return XFeatDenseWrapper(extractor._model), name

    if name == "superpoint_lightglue":
        extractor = LightGlueFeatureExtractor(name, logger, {"device": "cpu"})
        return SuperPointDenseWrapper(extractor._extractor.model), name

    if name == "disk_lightglue":
        extractor = LightGlueFeatureExtractor(name, logger, {"device": "cpu"})
        return DiskDenseWrapper(extractor._extractor.model), name

    if name == "lightglue":
        model = LightGlue(features=matcher_features, flash=False, depth_confidence=-1, width_confidence=-1).eval()
        stem = f"lightglue_{matcher_features}"
        return LightGlueFixedWrapper(model, input_shape[2], input_shape[3]), stem

    raise ValueError(f"Unknown model '{name}'")


def fix_batchnorm_for_xnnpack(model):
    for name, module in model.named_children():
        if isinstance(module, torch.nn.BatchNorm2d) and not module.affine:
            new_bn = torch.nn.BatchNorm2d(module.num_features, eps=module.eps, momentum=module.momentum, affine=True,
                                          track_running_stats=module.track_running_stats)
            with torch.no_grad():
                new_bn.weight.fill_(1.0)
                new_bn.bias.fill_(0.0)
                if module.running_mean is not None:
                    new_bn.running_mean.copy_(module.running_mean)
                if module.running_var is not None:
                    new_bn.running_var.copy_(module.running_var)
                new_bn.num_batches_tracked.copy_(module.num_batches_tracked)
            new_bn.eval()
            setattr(model, name, new_bn)
        else:
            fix_batchnorm_for_xnnpack(module)
    return model


def build_lightglue_inputs(matcher_features):
    num_keypoints = 256
    descriptor_dim = 256 if matcher_features == "superpoint" else 128

    sample_inputs = (torch.randn(1, num_keypoints, 2), torch.randn(1, num_keypoints, 2),
                     torch.randn(1, num_keypoints, descriptor_dim), torch.randn(1, num_keypoints, descriptor_dim))

    n_kp0 = torch.export.Dim("n_kp0", min=1, max=4096)
    n_kp1 = torch.export.Dim("n_kp1", min=1, max=4096)
    dynamic_shapes = {"keypoints0": {1: n_kp0}, "keypoints1": {1: n_kp1},
                      "descriptors0": {1: n_kp0}, "descriptors1": {1: n_kp1}}
    return sample_inputs, dynamic_shapes


def export_to_executorch(model_name, weights, input_shape, partitioner_name, output_dir, matcher_features="superpoint"):
    model, output_stem = load_model(model_name, weights, input_shape, matcher_features)
    model = model.cpu().eval()

    if partitioner_name == "xnnpack":
        model = fix_batchnorm_for_xnnpack(model)

    if model_name == "lightglue":
        sample_inputs, dynamic_shapes = build_lightglue_inputs(matcher_features)
    else:
        sample_inputs = (torch.randn(tuple(input_shape), dtype=torch.float32),)
        dynamic_shapes = None

    exported_program = torch.export.export(model, sample_inputs, dynamic_shapes=dynamic_shapes, strict=True)

    partitioner = PARTITIONERS.get(partitioner_name)
    if partitioner is not None:
        partitioners = [partitioner]
    else:
        partitioners = None

    edge_program = to_edge_transform_and_lower(exported_program, partitioner=partitioners)
    et_program = edge_program.to_executorch()

    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / f"{output_stem}_{partitioner_name}_{'x'.join(map(str, input_shape))}.pte"
    with model_path.open("wb") as file:
        et_program.write_to_file(file)

    logger.info("Saved ExecuTorch program: %s", model_path.resolve())
    return model_path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-mn", "--model-name", required=True, help="torchvision or custom model name")
    parser.add_argument("-is", "--input-shape", required=True, type=int, nargs=4, metavar=("N", "C", "H", "W"))
    parser.add_argument("-w", "--weights", default="DEFAULT", help="torchvision weights enum, or 'none'")
    parser.add_argument("-p", "--partitioner", default="none", choices=("none", "xnnpack", "vulkan"))
    parser.add_argument("-o", "--output-dir", type=Path, default=Path("exported"))
    parser.add_argument("--matcher-features", default="superpoint",
                        choices=("superpoint", "disk", "aliked", "sift", "doghardnet"))
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        export_to_executorch(args.model_name, args.weights, args.input_shape, args.partitioner, args.output_dir,
                             matcher_features=args.matcher_features)
    except Exception:
        logger.error(traceback.format_exc())
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)