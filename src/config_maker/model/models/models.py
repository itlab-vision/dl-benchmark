import os
from xml.dom import minidom
from .model import Model  # pylint: disable=E0402
from tags import CONFIG_MODELS_TAG  # pylint: disable-next=E0401


class Models:
    def __init__(self):
        self.__models = []

    def get_models(self):
        return self.__models

    def get_model_list_in_strings(self):
        models_list = []
        for model in self.__models:
            models_list.append(model.get_str())
        return models_list

    def set_models(self, models):
        self.__models.clear()
        for model in models:
            if model not in self.__models:
                self.__models.append(model)

    def add_model(self, task, name, precision, framework, model_path, weights_path):
        self.__models.append(Model(task, name, precision, framework, model_path, weights_path))

    def change_model(self, row, task, name, precision, framework, model_path, weights_path):
        self.__models[row] = Model(task, name, precision, framework, model_path, weights_path)

    def delete_model(self, index):
        self.__models.pop(index)

    def delete_models(self, indexes):
        for index in indexes:
            if index < len(self.__models):
                self.delete_model(index)

    def copy_models(self, indexes):
        for index in indexes:
            if index < len(self.__models):
                self.__models.append(self.__models[index])

    def clear(self):
        self.__models.clear()

    def parse_config(self, path_to_config):
        parsed_config = minidom.parse(path_to_config)
        self.__models = Model.parse(parsed_config)

    def create_config(self, path_to_config):
        if len(self.__models) == 0:
            return False
        file = minidom.Document()
        DOM_ROOT_TAG = file.createElement(CONFIG_MODELS_TAG)
        file.appendChild(DOM_ROOT_TAG)
        for model in self.__models:
            DOM_ROOT_TAG.appendChild(model.create_dom(file))
        xml_str = file.toprettyxml(indent="\t", encoding="utf-8")
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        return os.path.exists(path_to_config)
