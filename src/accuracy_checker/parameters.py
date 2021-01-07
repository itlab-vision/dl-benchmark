import yaml
from config.tests import test


class parameters:
    def __init__(self, config, models, source, annotations=None, definitions=None, extensions=None):
        self.config = self.__is_correct_path(config)
        self.models = self.__is_correct_path(models)
        self.source = self.__is_correct_path(source)
        self.annotations = self.__is_correct_path(annotations)
        self.definitions = self.__is_correct_path(definitions)
        self.extensions = self.__is_correct_path(extensions)

    def __is_correct_path(self, path):
        if path is not None and ' ' in path and '"' not in path:
            path = '"' + path + '"'
        return path

    def get_config_data(self):
        MODELS_TAG = 'models'
        tests = []
        with open(self.config, 'r') as f:
            test_dict = yaml.safe_load(f)
        models = test_dict[MODELS_TAG]
        for model in models:
            tests.append(test(model))
        return tests
