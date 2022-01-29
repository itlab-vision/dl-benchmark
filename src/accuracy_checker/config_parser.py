import yaml
from xml.dom import minidom


class model:
    def __init__(self, name, directory, precision, task, framework):
        self.name = name
        self.directory = directory
        self.precision = precision
        self.task = task
        self.framework = framework

    @staticmethod
    def parse(dom):
        CONFIG_MODEL_TAG = 'Model'
        CONFIG_MODEL_TASK_TAG = 'Task'
        CONFIG_MODEL_NAME_TAG = 'Name'
        CONFIG_MODEL_PRECISION_TAG = 'Precision'
        CONFIG_MODEL_SOURCE_FRAMEWORK_TAG = 'SourceFramework'
        CONFIG_MODEL_DIRECTORY_TAG = 'Directory'

        model_tag = dom.getElementsByTagName(CONFIG_MODEL_TAG)[0]
        return model(
            task=model_tag.getElementsByTagName(CONFIG_MODEL_TASK_TAG)[0].firstChild.data,
            name=model_tag.getElementsByTagName(CONFIG_MODEL_NAME_TAG)[0].firstChild.data,
            precision=model_tag.getElementsByTagName(CONFIG_MODEL_PRECISION_TAG)[0].firstChild.data,
            framework=model_tag.getElementsByTagName(CONFIG_MODEL_SOURCE_FRAMEWORK_TAG)[0].firstChild.data,
            directory=model_tag.getElementsByTagName(CONFIG_MODEL_DIRECTORY_TAG)[0].firstChild.data
        )


class test:
    def __init__(self, model=None,  device=None, framework=None, config=None, parameters=None):
        self.model = model
        self.device = device
        self.framework = framework
        self.config = config
        self.parameters = parameters
        self.metrics = self.__init_metrics_from_config(model.config)

    def __init_metrics_from_config(self, config):
        MODELS_TAG = 'models'
        LAUNCHERS_TAG = 'launchers'
        FRAMEWORK_TAG = 'framework'
        DATASETS_TAG = 'datasets'
        METRICS_TAG = 'metrics'

        metrics = []
        with open(config, 'r') as f:
            test_dict = yaml.safe_load(f)
        models = test_dict[MODELS_TAG]
        for model in models:
            model_metric = []
            launchers = model[LAUNCHERS_TAG]
            for launcher in launchers:
                if self.__convert_framework_from_config(launcher[FRAMEWORK_TAG]) == self.framework:
                    dataset = model[DATASETS_TAG][0]
                    if METRICS_TAG in dataset:
                        config_metrics = dataset[METRICS_TAG]
                        for metric in config_metrics:
                            if 'name' in metric.keys():
                                model_metric.append(metric['name'])
                            else:
                                model_metric.append('_'.join(metric.values()))
            if len(model_metric) == 0:
                for launcher in launchers:
                    if self.__convert_framework_from_config(launcher[FRAMEWORK_TAG]) == self.framework:
                        needed_dataset = model[DATASETS_TAG][0]
                        for index, dataset in enumerate(self.parameters.list_of_datasets):
                            if 'name' in dataset and dataset['name'] == needed_dataset['name']:
                                if METRICS_TAG in dataset:
                                    config_metrics = dataset[METRICS_TAG]
                                    for metric in config_metrics:
                                        if 'name' in metric.keys():
                                            model_metric.append(metric['name'])
                                        else:
                                            model_metric.append('_'.join(metric.values()))
            metrics.extend(model_metric)
        return metrics

    @staticmethod
    def __convert_framework_from_config(framework):
        if framework == 'dlsdk':
            return 'OpenVINO DLDT'
        elif framework == 'caffe':
            return 'Caffe'
        elif framework == 'tf':
            return 'TensorFlow'
        else:
            raise ValueError('Framework {} is not supported!'.format(framework))

    @staticmethod
    def parse(dom, test_parameters=None):
        CONFIG_PARAMETERS_TAG = 'Parameters'
        CONFIG_PARAMETERS_DEVICE_TAG = 'Device'
        CONFIG_PARAMETERS_FRAMEWORK_TAG = 'InferenceFramework'
        CONFIG_PARAMETERS_CONFIG_TAG = 'Config'

        parameters_tag = dom.getElementsByTagName(CONFIG_PARAMETERS_TAG)[0]
        return test(
            model=model.parse(dom),
            device=parameters_tag.getElementsByTagName(CONFIG_PARAMETERS_DEVICE_TAG)[0].firstChild.data,
            framework=parameters_tag.getElementsByTagName(CONFIG_PARAMETERS_FRAMEWORK_TAG)[0].firstChild.data,
            config=parameters_tag.getElementsByTagName(CONFIG_PARAMETERS_CONFIG_TAG)[0].firstChild.data,
            parameters=test_parameters
        )


class parser:
    @staticmethod
    def get_test_list(config, test_parameters):
        CONFIG_ROOT_TAG = 'Test'

        test_list = []
        parsed_config = minidom.parse(config)
        tests_tag = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
        for current_test in tests_tag:
            t = test.parse(current_test, test_parameters)
            test_list.append(t)
        return test_list
