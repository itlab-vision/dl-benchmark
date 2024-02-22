import logging as log

from causal_lm_base import CausalLMBase


class Mistral7bV01(CausalLMBase):
    def __init__(self):
        super().__init__('mistralai/Mistral-7B-v0.1')

    def create_model(self, should_be_traced, trust_remote_code=True, **kwargs):
        revision = '26bca36bde8333b5d7f72e9ed20ccda6a618af24'
        log.info('Model revision: ' + revision)
        return super().create_model(should_be_traced, trust_remote_code=True, revision=revision, **kwargs)
