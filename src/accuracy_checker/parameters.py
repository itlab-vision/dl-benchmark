import yaml
from config.tests import test


class parameters:
    def __init__(self, config, models, source, annotations=None, definitions=None, extensions=None):
        self.configs = {}
        self.models = self.__is_correct_path(models)
        self.source = self.__is_correct_path(source)
        self.annotations = self.__is_correct_path(annotations)
        self.definitions = self.__is_correct_path(definitions)
        self.extensions = self.__is_correct_path(extensions)
        self.tests_for_config_by_framework = {}
        config = self.__is_correct_path(config)
        self.__config_concatenation(config)

    @staticmethod
    def __is_correct_path(path):
        if path is not None and ' ' in path and '"' not in path:
            path = '"' + path + '"'
        return path

    def __config_concatenation(self, config_path):
        MODELS_TAG = 'models'
        LAUNCHERS_TAG = 'launchers'
        FRAMEWORK_TAG = 'framework'
        with open(config_path, 'r') as f:
            test_dict = yaml.safe_load(f)
        models = test_dict[MODELS_TAG]
        for model in models:
            framework = model[LAUNCHERS_TAG][0][FRAMEWORK_TAG]
            try:
                self.tests_for_config_by_framework[framework]
            except KeyError:
                self.tests_for_config_by_framework[framework] = []
            self.tests_for_config_by_framework[framework].append(model)
        for framework in self.tests_for_config_by_framework:
            config = 'config_{}.yml'.format(framework)
            with open(config, 'w') as f:
                yaml.dump({MODELS_TAG: self.tests_for_config_by_framework[framework]}, f, default_flow_style=False)
            self.configs[framework] = config

    def get_config_data_by_framework(self, framework):
        tests = []
        for model in self.tests_for_config_by_framework[framework]:
            tests.append(test(model))
        return tests
