from transformers import Wav2Vec2ForCTC

from model_handler import ModelHandler


class Wav2vec2Base(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self, **kwargs):
        return Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-base-960h')
