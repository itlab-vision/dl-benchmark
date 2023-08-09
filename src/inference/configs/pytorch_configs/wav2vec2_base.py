from transformers import Wav2Vec2ForCTC

from model_handler import ModelHandler


class Wav2vec2Base(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self, should_be_traced, **kwargs):
        trace_args = self.get_traced_loading_flags() if should_be_traced else {}
        return Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-base-960h', **trace_args)
