import sys
import subprocess
import logging as log
from pathlib import Path

import torch
from transformers import FalconForCausalLM, FalconConfig

from causal_lm_base import CausalLMBase


CONFIG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CONFIG_DIR))


class Falcon7bQ(CausalLMBase):
    def __init__(self):
        super().__init__('falcon7b_quant')
        self.model_dir = CONFIG_DIR.joinpath('pytorch_configs', self.model_name)

    def download_model_weigths(self, custom_models_links, precision='INT4', device='gpu'):
        log.info(f'Downloading weights for {precision} precision')
        if not Path(self.model_dir / precision).exists():
            subprocess.run(['wget', '-np', '-q', '-nH', '--cut-dirs', '4', '-R', 'index.html*', '-r',
                            '-P', str(self.model_dir), f'{custom_models_links["model"]}/{precision}/'])
        log.info('Download finished')
        self.model_dir = self.model_dir / precision

    def create_model(self, custom_models_links, precision='INT4', device='gpu', **kwargs):
        self.download_model_weigths(custom_models_links, precision, device)
        self.falcon_config = FalconConfig.from_pretrained(self.model_dir)
        self.falcon_model = FalconForCausalLM.from_pretrained(
            self.model_dir,
            config=self.falcon_config,
            torch_dtype=torch.float32,
            device_map=device,
        )
        return self.falcon_model
