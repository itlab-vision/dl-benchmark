import logging as log

from speech_to_sequence_base import Speech2SequenceBase


class WhisperV3Large(Speech2SequenceBase):
    def __init__(self):
        super().__init__('openai/whisper-large-v3')

    def create_model(self, trust_remote_code=True, **kwargs):
        revision = '1ecca609f9a5ae2cd97a576a9725bc714c022a93'
        log.info('Model revision: ' + revision)
        return super().create_model(trust_remote_code=True, revision=revision, **kwargs)
