import os
from xml.dom import minidom
from .quantized_model import QModel  # pylint: disable=E0402
from tags import CONFIG_QUANTIZATION_ALL_PARAMETERS_TAG, CONFIG_Q_CONFIG_TAG  # pylint: disable=E0401

# import json
# pylint: disable-next=E0401
# from tags import CONFIG_QUANTIZATION_METHOD_TAG, CONFIG_NAME_TAG, CONFIG_MODEL_PATH_TAG, \
#     CONFIG_WEIGHTS_PATH_TAG, CONFIG_PRESET_TAG, CONFIG_AC_CONFIG_TAG, CONFIG_MAX_DROP_TAG, \
#     CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, CONFIG_DIRECT_DUMP_TAG, CONFIG_LOG_LEVEL_TAG, \
#     CONFIG_PROGRESS_BAR_TAG, CONFIG_STREAM_OUTPUT_TAG, CONFIG_KEEP_WEIGHTS_TAG

class QuantizationConfig:
    def __init__(self):
        self.__q_models = []

    def get_q_models(self):
        return self.__q_models

    # TODO: fix
    # def add_q_model(self, *args):
    #     self.__q_models.append(QModel(*args))
    # def change_q_model(self, row, *args):
    #     self.__q_models[row] = QModel(*args)

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

    # TODO: json -> xml
    '''
    def parse_config(self, path_to_config):
        with open(path_to_config, 'r') as q_config_file:
            q_config = json.load(q_config_file)
            # q_global_pot_params = q_config["global_pot_parameters"]
        for q_model in q_config["parameters"]:
            self.__q_models.append(QModel.parse(q_model))
        # self.__q_models = q_config
        return self.get_q_models()
    '''

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
        xml_str = file.toprettyxml(indent='\t', encoding='utf-8')
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        return os.path.exists(path_to_config)
        '''
        if len(self.__q_models) == 0:
            return False
        # file = minidom.Document()
        # DOM_ROOT_TAG = file.createElement(CONFIG_TESTS_TAG)
        # file.appendChild(DOM_ROOT_TAG)
        # tests = self.__prepare_tests()
        # for test in tests:
        #     DOM_TEST_TAG = test.create_dom(file)
        #     DOM_ROOT_TAG.appendChild(DOM_TEST_TAG)
        # xml_str = file.toprettyxml(indent='\t', encoding='utf-8')
        with open(path_to_config, 'wb') as f:
            json.dump(
                self.get_models(),
                path_to_config,
                indent='\t',
                encoding='utf-8'
            )
            # f.write(xml_str)
        return os.path.exists(path_to_config)
        '''