from transformers import ViTForImageClassification

from model_handler import ModelHandler


class VitBasePatch16224(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self, **kwargs):
        return ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')
