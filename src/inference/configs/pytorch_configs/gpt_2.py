import torch

from transformers import AutoConfig, AutoModelForCausalLM
from causal_lm_base import CausalLMBase


class Gpt2(CausalLMBase):
    def __init__(self):
        super().__init__('gpt2')

    def create_model(self, should_be_traced, trust_remote_code=False, **kwargs):
        config = AutoConfig.from_pretrained(self.model_name)

        trace_args = self.get_traced_loading_flags() if should_be_traced else {}

        params = dict(pretrained_model_name_or_path=self.model_name,
                      trust_remote_code=trust_remote_code,
                      config=config, **trace_args)

        if kwargs['precision'] == 'BF16':
            params.update({'torch_dtype': torch.bfloat16})
        elif kwargs['precision'] == 'FP16':
            params.update({'torch_dtype': torch.float16})

        return AutoModelForCausalLM.from_pretrained(**params)
