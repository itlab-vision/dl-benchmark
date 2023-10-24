class Model:
    def __init__(self, task, name, model_path, weights_path, precision, source_framework, module=None):
        """
        :param task:
        :type task:
        :param name:
        :type name:
        :param model_path:
        :type model_path:
        :param weights_path:
        :type weights_path:
        :param precision:
        :type precision:
        :param source_framework:
        :type source_framework:
        :param module:
        :type module:
        """
        self.source_framework = None
        self.task = task
        self.name = None
        self.model = None
        self.weight = None
        self.precision = None
        self.module = module

        if self._parameter_is_not_none(source_framework):
            self.source_framework = source_framework
        else:
            raise ValueError('Source framework is required parameter.')
        if self._parameter_is_not_none(name):
            self.name = name
        else:
            raise ValueError('Model name is required parameter.')
        if self._parameter_is_not_none(model_path):
            self.model = model_path
        else:
            raise ValueError('Path to model is required parameter.')
        if self._parameter_is_not_none(weights_path):
            self.weight = weights_path
        else:
            raise ValueError('Path to model weights is required parameter.')
        if self._parameter_is_not_none(precision):
            self.precision = precision
        else:
            raise ValueError('Precision is required parameter.')

    @staticmethod
    def _parameter_is_not_none(parameter):
        return parameter is not None
