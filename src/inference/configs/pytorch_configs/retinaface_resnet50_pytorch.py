import subprocess
import sys
from pathlib import Path

from torch import load

from model_handler import ModelHandler

CONFIG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CONFIG_DIR))
from config_utils import github_clone, prepend_to_path  # noqa: E402


class RetinafaceResnet50Pytorch(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.pretrained = True
        self.download_model_repo()
        self.download_model_weigths()

    def download_model_repo(self):
        self.model_dir = CONFIG_DIR.joinpath('pytorch_configs', self.model_name)
        github_clone(repo_name='biubug6/Pytorch_Retinaface', dist=str(self.model_dir))

    def download_model_weigths(self):
        weights_name = 'Resnet50_Final.pth'
        repo_name = 'https://github.com/elliottzheng/face-detection/releases/download/0.0.1'
        weights_path = f'{repo_name}/{weights_name}'

        self.weights = Path(self.model_dir).joinpath(weights_name)

        subprocess.run(['wget', '-O', str(self.weights), weights_path])

    def create_model(self, **kwargs):
        with prepend_to_path([str(self.model_dir)]):
            from data.config import cfg_re50  # noqa: E402
            from models.retinaface import RetinaFace  # noqa: E402

            model = RetinaFace(cfg=cfg_re50, phase='test')

            checkpoint = load(self.weights, map_location='cpu')
            ckpt = {k.replace('module.', ''): v for k, v in checkpoint.items()}

            model.load_state_dict(ckpt)
            return model
