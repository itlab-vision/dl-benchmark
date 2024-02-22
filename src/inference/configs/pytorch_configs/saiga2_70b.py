import sys
import subprocess
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, GenerationConfig

from causal_lm_base import CausalLMBase


CONFIG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CONFIG_DIR))


class Saiga270b(CausalLMBase):
    def __init__(self):
        super().__init__('saiga2_70b')
        self.model_dir = None

    def download_model_weigths(self, log, custom_models_links, precision='FP16'):
        self.model_dir = f'{custom_models_links["models_dir"]}/saiga2_70b/safetensors/'

        if not Path(self.model_dir).exists():
            subprocess.run(['wget', '-np', '-q', '-nH', '--cut-dirs', '4', '-R', 'index.html*', '-r',
                            '-P', str(self.model_dir), f'{custom_models_links["model"]}/safetensors/{precision}/'])
            log.info('Download finished')
        self.model_dir += precision

    def get_cuda_memory_map(self, log, num_gpu_devices=2, single_gpu_memory='80GB'):
        """
        Used for setting maximum amount of GPUs available to model.
        """

        log.info(f'Using {num_gpu_devices} GPUs')
        return {gpu_num: single_gpu_memory for gpu_num in range(num_gpu_devices)}

    def create_model(self, custom_models_links, log, precision='FP16', num_gpu_devices=2, **kwargs):
        self.download_model_weigths(log, custom_models_links, precision)
        self.saiga_config = GenerationConfig.from_pretrained(self.model_dir)

        model_kwargs = {'device_map': 'auto', 'max_memory': self.get_cuda_memory_map(log=log,
                                                                                     num_gpu_devices=num_gpu_devices)}
        if precision == 'FP16':
            model_kwargs['torch_dtype'] = torch.float16
        self.saiga_model = AutoModelForCausalLM.from_pretrained(self.model_dir, **model_kwargs)
        log.info('Model loaded on devices: ' + ', '.join(map(str, set(self.saiga_model.hf_device_map.values()))))

        return self.saiga_model
