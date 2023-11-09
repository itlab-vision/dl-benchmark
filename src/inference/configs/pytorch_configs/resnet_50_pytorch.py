import importlib

from model_handler import ModelHandler


class Resnet50Pytorch(ModelHandler):
    def __init__(self):
        super().__init__()
        self.model_name = 'resnet50'
        self.module = 'torchvision.models'

    def set_model_weights(self, module, **kwargs):
        weights = importlib.import_module(module).__getattribute__('ResNet50_Weights')
        self.weights = weights.DEFAULT

    def create_model(self, **kwargs):
        return importlib.import_module(self.module).__getattribute__(self.model_name)
