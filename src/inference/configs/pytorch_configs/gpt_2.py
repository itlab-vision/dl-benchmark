from causal_lm_base import CausalLMBase


class Gpt2(CausalLMBase):
    def __init__(self):
        super().__init__('gpt2')
