class Dataset:
    def __init__(self, name, path):
        self.name = None
        self.path = None
        if self._parameter_is_not_none(name):
            self.name = name
        else:
            raise ValueError('Dataset name is required parameter.')
        if self._parameter_is_not_none(path):
            self.path = path
        else:
            raise ValueError('Path to dataset is required parameter.')

    @staticmethod
    def _parameter_is_not_none(parameter):
        return True if parameter is not None else False
