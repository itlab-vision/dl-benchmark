import subprocess
import sys
from pathlib import Path

from model_handler import ModelHandler

CONFIG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CONFIG_DIR))
from config_utils import github_clone, prepend_to_path, regex_replace_in_file, apply_patch  # noqa: E402


class YoloV7(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.pretrained = True
        self.download_model_repo()
        self.download_model_weigths()

    def download_model_repo(self):
        self.model_dir = CONFIG_DIR.joinpath('pytorch_configs', self.model_name)
        github_clone(repo_name='WongKinYiu/yolov7', dist=str(self.model_dir))

        patch = CONFIG_DIR.joinpath('pytorch_configs', 'patches', '1167.patch')
        apply_patch(folder=str(self.model_dir), patch=str(patch))

        replace_unused_imports_in_repo(repo_dir=self.model_dir)

    def download_model_weigths(self):
        weights_name = 'yolov7.pt'
        weights_path = f'https://github.com/WongKinYiu/yolov7/releases/download/v0.1/{weights_name}'

        self.weights = Path(self.model_dir).joinpath(weights_name)

        if not self.weights.exists():
            subprocess.run(['wget', '-O', str(self.weights), weights_path])

    def create_model(self, device, **kwargs):
        with prepend_to_path([str(self.model_dir)]):
            from models.experimental import attempt_load  # noqa: E402
            return attempt_load(self.weights, map_location=device)


def replace_unused_imports_in_repo(repo_dir: Path):
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


def non_max_suppression(prediction, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False, multi_label=False,
                        labels=()):
    model_dir = CONFIG_DIR.joinpath('pytorch_configs', 'yolo-v7')
    with prepend_to_path([str(model_dir)]):
        from utils.general import non_max_suppression  # noqa: E402
        return non_max_suppression(prediction, conf_thres, iou_thres, classes, agnostic, multi_label)


def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    model_dir = CONFIG_DIR.joinpath('pytorch_configs', 'yolo-v7')
    with prepend_to_path([str(model_dir)]):
        from utils.plots import plot_one_box  # noqa: E402
        return plot_one_box(x, img, color, label, line_thickness)
