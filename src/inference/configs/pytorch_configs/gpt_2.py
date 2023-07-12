from transformers import GPT2Model

from model_handler import ModelHandler


class Gpt2(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self):
        return GPT2Model.from_pretrained('gpt2')
