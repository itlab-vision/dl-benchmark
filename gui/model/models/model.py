class Model:
    def __init__(self, task=None, name=None, precision=None, framework=None, model_path=None, weights_path=None):
        self.task = task
        self.name = name
        self.precision = precision
        self.framework = framework
        self.model_path = model_path
        self.weights_path = weights_path

    def __eq__(self, other):
        return self.task == other.task and self.name == other.name and self.precision == other.precision and \
               self.framework == other.framework and self.model_path == other.model_path and self.weights_path == other.weights_path

    def get_str(self):
        return ';'.join([self.task, self.name, self.precision, self.framework, self.model_path, self.weights_path])
