import subprocess
import sys
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as f

from model_handler import ModelHandler

CONFIG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CONFIG_DIR))
from config_utils import github_clone, prepend_to_path, regex_replace_in_file, apply_patch  # noqa: E402


class Ensemble(nn.ModuleList):
    def __init__(self):
        super(Ensemble, self).__init__()

    def forward(self, x, augment=False):
        y = []
        for module in self:
            y.append(module(x, augment)[0])
        y = torch.cat(y, 1)  # nms ensemble

        return y, None  # inference, train output


class Hardswish(nn.Module):
    @staticmethod
    def forward(x):
        return x * f.hardtanh(x + 3, 0.0, 6.0) / 6.0


class SiLU(nn.Module):
    @staticmethod
    def forward(x):
        return x * torch.sigmoid(x)


class YoloV7(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.pretrained = True
        self.download_model_repo()
        self.download_model_weigths()

    def download_model_repo(self):
        self.model_dir = CONFIG_DIR.joinpath('pytorch_configs', self.model_name)
        github_clone(repo_name='WongKinYiu/yolov7', dist=str(self.model_dir))

        self.patch = CONFIG_DIR.joinpath('pytorch_configs', '1167.patch')
        apply_patch(folder=str(self.model_dir), patch=str(self.patch))

        replace_unused_imports_in_repo(repo_dir=self.model_dir)

    def download_model_weigths(self):
        weights_name = 'yolov7.pt'
        weights_path = f'https://github.com/WongKinYiu/yolov7/releases/download/v0.1/{weights_name}'

        self.weights = Path(self.model_dir).joinpath(weights_name)

        subprocess.run(['wget', '-O', str(self.weights), weights_path])

    def create_model(self, device):
        with prepend_to_path([str(self.model_dir)]):
            from models.experimental import End2End  # noqa: E402
            from models.common import Conv  # noqa: E402

            model = Ensemble()
            ckpt = torch.load(self.weights, map_location=device)
            model.append(ckpt['ema' if ckpt.get('ema') else 'model'].float().fuse().eval())

            # Compatibility updates
            for m in model.modules():
                if type(m) is nn.Upsample:
                    m.recompute_scale_factor = None  # torch 1.11.0 compatibility
            model = model[-1]

            for _, m in model.named_modules():
                if isinstance(m, Conv):
                    if isinstance(m.act, nn.Hardswish):
                        m.act = Hardswish()
                    elif isinstance(m.act, nn.SiLU):
                        m.act = SiLU()

            model.model[-1].export = False

            return End2End(model, iou_thres=0.65, score_thres=0.35, max_wh=640, device=device)


def replace_unused_imports_in_repo(repo_dir: Path):
    regex_replace_in_file(file=repo_dir.joinpath('models/experimental.py'),
                          regex='from utils', replacement=r'# \g<0>')
    regex_replace_in_file(file=repo_dir.joinpath('models/yolo.py'),
                          regex=r'from utils.autoanchor', replacement=r'# \g<0>')
    regex_replace_in_file(file=repo_dir.joinpath('models/yolo.py'),
                          regex=r'from utils.general', replacement=r'# \g<0>')
    regex_replace_in_file(file=repo_dir.joinpath('models/yolo.py'),
                          regex=r'from utils.loss', replacement=r'# \g<0>')
    regex_replace_in_file(file=repo_dir.joinpath('models/common.py'),
                          regex=r'from utils.datasets', replacement=r'# \g<0>')
    regex_replace_in_file(file=repo_dir.joinpath('models/common.py'),
                          regex=r'from utils.general', replacement=r'# \g<0>')
    regex_replace_in_file(file=repo_dir.joinpath('models/common.py'),
                          regex=r'from utils.plots', replacement=r'# \g<0>')
