import yaml
from config.tests import Test


class Parameters:
    def __init__(self, config, models, source, annotations=None, definitions=None, extensions=None):
        self.config = self.__is_correct_path(config)
        self.models = self.__is_correct_path(models)
        self.source = self.__is_correct_path(source)
        self.annotations = self.__is_correct_path(annotations)
        self.definitions = self.__is_correct_path(definitions)
        self.extensions = self.__is_correct_path(extensions)

    def __is_correct_path(self, path):
        if path is None:
            return None
        if ' ' in path and '"' not in path:
            return '"' + path + '"'
        else:
            return path

    def get_config_data(self):
        tests = []
        with open(self.config, 'r') as f:
            tests_dict = yaml.safe_load(f)

        MODELS_TAG = 'models'
        models = tests_dict[MODELS_TAG]
        for model in models:
            tests.append(Test(model))
        return tests
