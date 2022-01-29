import os
# pylint: disable-next=E0401
from tags import CONFIG_MODEL_TAG, CONFIG_TASK_TAG, CONFIG_NAME_TAG, CONFIG_PRECISION_TAG, \
    CONFIG_SOURCE_FRAMEWORK_TAG, CONFIG_MODEL_PATH_TAG, CONFIG_WEIGHTS_PATH_TAG, CONFIG_DIRECTORY_TAG


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
               self.framework == other.framework and self.model_path == other.model_path and \
               self.weights_path == other.weights_path

    def get_str(self):
        return ';'.join([self.task, self.name, self.precision, self.framework, self.model_path, self.weights_path])

    @staticmethod
    def directory2IR(model, directory):
        model_path = os.path.join(directory, model + '.xml')
        weights_path = os.path.join(directory, model + '.bin')
        return model_path, weights_path

    @staticmethod
    def IR2directory(model_path):
        return os.path.dirname(os.path.normpath(model_path))

    def create_dom(self, file, directory=False):
        DOM_MODEL_TAG = file.createElement(CONFIG_MODEL_TAG)
        DOM_TASK_TAG = file.createElement(CONFIG_TASK_TAG)
        DOM_NAME_TAG = file.createElement(CONFIG_NAME_TAG)
        DOM_PRECISION_TAG = file.createElement(CONFIG_PRECISION_TAG)
        DOM_SOURCE_FRAMEWORK_TAG = file.createElement(CONFIG_SOURCE_FRAMEWORK_TAG)

        DOM_TASK_TAG.appendChild(file.createTextNode(self.task))
        DOM_NAME_TAG.appendChild(file.createTextNode(self.name))
        DOM_PRECISION_TAG.appendChild(file.createTextNode(self.precision))
        DOM_SOURCE_FRAMEWORK_TAG.appendChild(file.createTextNode(self.framework))
        DOM_MODEL_TAG.appendChild(DOM_TASK_TAG)
        DOM_MODEL_TAG.appendChild(DOM_NAME_TAG)
        DOM_MODEL_TAG.appendChild(DOM_PRECISION_TAG)
        DOM_MODEL_TAG.appendChild(DOM_SOURCE_FRAMEWORK_TAG)

        if directory:
            DOM_DIRECTORY_TAG = file.createElement(CONFIG_DIRECTORY_TAG)
            DOM_DIRECTORY_TAG.appendChild(file.createTextNode(Model.IR2directory(self.model_path)))
            DOM_MODEL_TAG.appendChild(DOM_DIRECTORY_TAG)
        else:
            DOM_MODEL_PATH_TAG = file.createElement(CONFIG_MODEL_PATH_TAG)
            DOM_WEIGHTS_PATH_TAG = file.createElement(CONFIG_WEIGHTS_PATH_TAG)
            DOM_MODEL_PATH_TAG.appendChild(file.createTextNode(self.model_path))
            DOM_WEIGHTS_PATH_TAG.appendChild(file.createTextNode(self.weights_path))
            DOM_MODEL_TAG.appendChild(DOM_MODEL_PATH_TAG)
            DOM_MODEL_TAG.appendChild(DOM_WEIGHTS_PATH_TAG)

        return DOM_MODEL_TAG

    @staticmethod
    def parse(dom, directory=False):
        parsed_models = dom.getElementsByTagName(CONFIG_MODEL_TAG)
        models = []
        for parsed_model in parsed_models:
            task = parsed_model.getElementsByTagName(CONFIG_TASK_TAG)[0].firstChild.data
            name = parsed_model.getElementsByTagName(CONFIG_NAME_TAG)[0].firstChild.data
            precision = parsed_model.getElementsByTagName(CONFIG_PRECISION_TAG)[0].firstChild.data
            framework = parsed_model.getElementsByTagName(CONFIG_SOURCE_FRAMEWORK_TAG)[0].firstChild.data
            if directory:
                model_path, weights_path = Model.directory2IR(name, parsed_model.getElementsByTagName(
                    CONFIG_DIRECTORY_TAG)[0].firstChild.data)
            else:
                model_path = parsed_model.getElementsByTagName(CONFIG_MODEL_PATH_TAG)[0].firstChild.data
                weights_path = parsed_model.getElementsByTagName(CONFIG_WEIGHTS_PATH_TAG)[0].firstChild.data
            models.append(Model(task, name, precision, framework, model_path, weights_path))
        return models
