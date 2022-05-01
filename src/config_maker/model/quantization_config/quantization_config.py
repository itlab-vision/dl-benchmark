import os
from xml.dom import minidom
from .quantized_model import QModel  # pylint: disable=E0402
from tags import CONFIG_QUANTIZATION_ALL_PARAMETERS_TAG, CONFIG_Q_CONFIG_TAG  # pylint: disable=E0401


class QuantizationConfig:
    def __init__(self):
        self.__q_models = []

    def get_q_models(self):
        return self.__q_models

    def add_q_model(self, pot_params, model_params, dependent_params):
        self.__q_models.append(QModel(pot_params, model_params, dependent_params))

    def change_q_model(self, row, pot_params, model_params, dependent_params):
        self.__q_models[row] = QModel(pot_params, model_params, dependent_params)

    def delete_q_model(self, index):
        self.__q_models.pop(index)

    def delete_q_models(self, indexes):
        for index in indexes:
            if index < len(self.__q_models):
                self.delete_q_model(index)

    def copy_q_models(self, indexes):
        for index in indexes:
            if index < len(self.__q_models):
                self.__q_models.append(self.__q_models[index])

    def clear(self):
        self.__q_models.clear()

    def parse_config(self, path_to_config):
        config = minidom.parse(path_to_config)
        parsed_config = config.getElementsByTagName(CONFIG_QUANTIZATION_ALL_PARAMETERS_TAG)[0]
        parameters = parsed_config.getElementsByTagName(CONFIG_Q_CONFIG_TAG)
        self.clear()
        for dom in parameters:
            q_model = QModel.parse(dom)
            self.__q_models.append(q_model)
        return self.get_q_models()

    def create_config(self, path_to_config):
        if len(self.__q_models) == 0:
            return False
        file = minidom.Document()
        DOM_ROOT_TAG = file.createElement(CONFIG_QUANTIZATION_ALL_PARAMETERS_TAG)
        file.appendChild(DOM_ROOT_TAG)
        for i, q_model in enumerate(self.__q_models):
            DOM_Q_CONFIG_TAG = file.createElement(CONFIG_Q_CONFIG_TAG)
            DOM_ROOT_TAG.appendChild(DOM_Q_CONFIG_TAG)
            DOM_CONFIG_ID, DOM_POT_PARAMETERS, DOM_MODEL_PARAMETERS = q_model.create_dom(file, i)
            DOM_Q_CONFIG_TAG.appendChild(DOM_CONFIG_ID)
            DOM_Q_CONFIG_TAG.appendChild(DOM_POT_PARAMETERS)
            DOM_Q_CONFIG_TAG.appendChild(DOM_MODEL_PARAMETERS)
        xml_str = file.toprettyxml(indent='    ', encoding='utf-8')
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        return os.path.exists(path_to_config)
