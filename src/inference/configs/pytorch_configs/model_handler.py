import abc


class ModelHandler(abc.ABC):
    def __init__(self):
        self.model_name = None
        self.model_dir = None
        self.weights = None
        self.module = None
        self.pretrained = False

    def set_model_name(self, model_name):
        if self.model_name is None:
            self.model_name = model_name

    @abc.abstractmethod
    def set_model_weights(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def create_model(self, **kwargs):
        raise NotImplementedError
