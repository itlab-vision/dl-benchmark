import sys
import argparse
import torch
from pathlib import Path
from torchvision.models import get_model
from executorch.backends.xnnpack.partition.xnnpack_partitioner import XnnpackPartitioner
from executorch.backends.vulkan.partitioner.vulkan_partitioner import VulkanPartitioner
from executorch.exir import to_edge_transform_and_lower

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from utils.logger_conf import configure_logger  # noqa: E402

log = configure_logger()

PARTITIONER = {
    'xnnpack': XnnpackPartitioner(),
    'vulkan': VulkanPartitioner(),
    'None': None,
}


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-mn', '--model_name',
                        help='Model name from the module.',
                        required=True,
                        type=str,
                        dest='model_name')
    parser.add_argument('-w', '--weights',
                        help='Name of weights to use from module.',
                        type=str,
                        default='DEFAULT',
                        dest='weights')
    parser.add_argument('-is', '--input_shapes',
                        help='Input tensor shapes.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shapes')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-p', '--partitioner',
                        help='Partitioner to export model.',
                        default='None',
                        choices=['xnnpack', 'vulkan', 'arm', None],
                        type=str,
                        dest='partitioner')
    args = parser.parse_args()

    return args


def export_to_executorch(model_name, weights,
                         input_shape, partitioner, batch):
    log.info(f'Getting the model {model_name} from torchvision.')
    model = get_model(model_name, weights=weights)
    model = model.eval()
    sample_inputs = (torch.randn(list(input_shape)), )

    log.info('Export model to ExecuTorch format.')
    et_program = to_edge_transform_and_lower(
        torch.export.export(model, sample_inputs),
        partitioner=PARTITIONER[partitioner],
    ).to_executorch()

    save_name = f'{model_name}_{partitioner}_batch_{batch}.pte'
    log.info(f'Save model as {save_name}.')
    with open(save_name, 'wb') as file:
        et_program.write_to_file(file)


def main():
    log.info('Parsing command line arguments.')
    args = cli_argument_parser()
    export_to_executorch(args.model_name, args.weights,
                         args.input_shapes, args.partitioner,
                         args.batch_size)


if __name__ == '__main__':
    sys.exit(main() or 0)
