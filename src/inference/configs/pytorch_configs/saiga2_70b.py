import os
import sys
import logging as log
from pathlib import Path

from transformers import AutoModelForCausalLM, GenerationConfig
import torch

from causal_lm_base import CausalLMBase


CONFIG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CONFIG_DIR))


class Saiga270b(CausalLMBase):
    def __init__(self):
        super().__init__('saiga2_70b')
        self.model_dir = None

    def download_model_weigths(self, custom_models_links, precision='FP16'):
        self.model_dir = f'{custom_models_links["models_dir"]}/saiga2_70b/safetensors/{precision}/'

    def set_devices(self, num_gpu_devices=2):
        log.info(f'Using {num_gpu_devices} GPUs')
        os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(map(str, range(num_gpu_devices)))

    def create_model(self, custom_models_links, precision='FP16', num_gpu_devices=2, **kwargs):
        self.download_model_weigths(custom_models_links, precision)
        self.set_devices(num_gpu_devices)
        self.saiga_config = GenerationConfig.from_pretrained(self.model_dir)
        self.saiga_model = AutoModelForCausalLM.from_pretrained(
            self.model_dir,
            device_map='auto',
            torch_dtype=torch.float16,
        )
        return self.saiga_model
