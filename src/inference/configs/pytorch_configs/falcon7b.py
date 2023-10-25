import logging as log

from causal_lm_base import CausalLMBase


class Falcon7b(CausalLMBase):
    def __init__(self):
        super().__init__('tiiuae/falcon-7b')

    def create_model(self, should_be_traced, trust_remote_code=True, **kwargs):
        revision = '378337427557d1df3e742264a2901a49f25d4eb1'
        log.info('Model revision: ' + revision)
        return super().create_model(should_be_traced, trust_remote_code=True, revision=revision, **kwargs)
