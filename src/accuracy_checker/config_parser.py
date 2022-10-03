from xml.dom import minidom


class Model:
    def __init__(self, name, directory, precision, task, framework):
        """
        :param name:
        :type name:
        :param directory:
        :type directory:
        :param precision:
        :type precision:
        :param task:
        :type task:
        :param framework:
        :type framework:
        """
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
        return Model(
            task=model_tag.getElementsByTagName(CONFIG_MODEL_TASK_TAG)[0].firstChild.data,
            name=model_tag.getElementsByTagName(CONFIG_MODEL_NAME_TAG)[0].firstChild.data,
            precision=model_tag.getElementsByTagName(CONFIG_MODEL_PRECISION_TAG)[0].firstChild.data,
            framework=model_tag.getElementsByTagName(CONFIG_MODEL_SOURCE_FRAMEWORK_TAG)[0].firstChild.data,
            directory=model_tag.getElementsByTagName(CONFIG_MODEL_DIRECTORY_TAG)[0].firstChild.data,
        )


class Test:
    def __init__(self, model=None, device=None, framework=None, config=None, parameters=None):
        self.model = model
        self.device = device
        self.framework = framework
        self.config = config
        self.parameters = parameters

    @staticmethod
    def __convert_framework_from_config(framework):
        if framework == 'dlsdk':
            return 'OpenVINO DLDT'
        elif framework == 'caffe':
            return 'Caffe'
        elif framework == 'tf':
            return 'TensorFlow'
        else:
            return 'Unsupported framework'

    @staticmethod
    def parse(dom, test_parameters=None):
        CONFIG_PARAMETERS_TAG = 'Parameters'
        CONFIG_PARAMETERS_DEVICE_TAG = 'Device'
        CONFIG_PARAMETERS_FRAMEWORK_TAG = 'InferenceFramework'
        CONFIG_PARAMETERS_CONFIG_TAG = 'Config'

        parameters_tag = dom.getElementsByTagName(CONFIG_PARAMETERS_TAG)[0]
        return Test(
            model=Model.parse(dom),
            device=parameters_tag.getElementsByTagName(CONFIG_PARAMETERS_DEVICE_TAG)[0].firstChild.data,
            framework=parameters_tag.getElementsByTagName(CONFIG_PARAMETERS_FRAMEWORK_TAG)[0].firstChild.data,
            config=parameters_tag.getElementsByTagName(CONFIG_PARAMETERS_CONFIG_TAG)[0].firstChild.data,
            parameters=test_parameters,
        )


class TestResultParser:
    @staticmethod
    def get_test_list(config, test_parameters):
        CONFIG_ROOT_TAG = 'Test'

        test_list = []
        parsed_config = minidom.parse(config)
        tests_tag = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
        for current_test in tests_tag:
            test = Test.parse(current_test, test_parameters)
            test_list.append(test)
        return test_list
