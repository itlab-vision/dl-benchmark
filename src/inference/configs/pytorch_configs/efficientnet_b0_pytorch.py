import importlib

from model_handler import ModelHandler


class EfficientnetB0Pytorch(ModelHandler):
    def __init__(self):
        super().__init__()
        self.model_name = 'efficientnet_b0'
        self.module = 'torchvision.models'

    def set_model_weights(self, module, **kwargs):
        weights = importlib.import_module(module).__getattribute__('EfficientNet_B0_Weights')
        self.weights = weights.DEFAULT

    def create_model(self):
        return getattr(importlib.import_module(self.module), self.model_name)
