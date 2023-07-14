from transformers import AutoModelForTokenClassification

from model_handler import ModelHandler


class BertBaseNer(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self, **kwargs):
        return AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER')
