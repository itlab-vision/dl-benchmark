import sys
from pathlib import Path

from huggingface_hub import hf_hub_download
from transformers.models.clip import CLIPTextModelWithProjection

from model_handler import ModelHandler

CONFIG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CONFIG_DIR))
from config_utils import create_folder  # noqa: E402


class ClipVitB32Text(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True
        self.download_model_weigths()

    def download_model_weigths(self):
        self.model_name = 'clip_vit_b_32'
        self.model_dir = CONFIG_DIR.joinpath('pytorch_configs', self.model_name)
        create_folder(self.model_dir)

        hf_hub_download(repo_id='openai/clip-vit-base-patch32', filename='config.json', local_dir=self.model_dir)
        hf_hub_download(repo_id='openai/clip-vit-base-patch32', filename='pytorch_model.bin', local_dir=self.model_dir)

    def create_model(self, **kwargs):
        return CLIPTextModelWithProjection.from_pretrained(self.model_dir)
