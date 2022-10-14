import re
from model.quantization_config.compression_parameters import CompressionParameters

from tags import (CONFIG_MODEL_PARAMS_MODEL_TAGS, HEADER_POT_PARAMS_TAGS, HEADER_MODEL_PARAMS_MODEL_TAGS,
    HEADER_MODEL_PARAMS_ENGINE_TAGS, CONFIG_MODEL_TAG, CONFIG_ENGINE_TAG,
    CONFIG_COMPRESSION_TAG, CONFIG_POT_PARAMETERS_TAG, CONFIG_Q_CONFIG_TAG,
    CONFIG_MODEL_PARAMETERS_TAG, CONFIG_MODEL_NAME_TAG, CONFIG_WEIGHTS_TAG,
    CONFIG_STAT_REQUESTS_NUMBER_TAG, CONFIG_EVAL_REQUESTS_NUMBER_TAG, CONFIG_CONFIG_TAG,
    CONFIG_CONFIG_TYPE_TAG, CONFIG_DATA_SOURCE_TAG, CONFIG_CONFIG_ID_TAG)


class QModel:
    def __init__(self, pot_params, model_params, dependent_params):
        self.__pot_params = [*pot_params]

        COUNT_OF_CONFIG_MODEL_PARAMS = len(HEADER_MODEL_PARAMS_MODEL_TAGS)
        COUNt_OF_CONFIG_ENGINE_PARAMS = len(HEADER_MODEL_PARAMS_ENGINE_TAGS)

        idx_0 = 0
        idx_1 = idx_0 + COUNT_OF_CONFIG_MODEL_PARAMS
        idx_2 = idx_1 + COUNt_OF_CONFIG_ENGINE_PARAMS

        model_params_list = [
            model_params[:idx_1],       # config_model_params (model_name, model)
            model_params[idx_1:idx_2],  # config_engine_params
            model_params[idx_2:],       # config_common_compression_params (target_device, algorithm, preset,
                                        #   stat_subset_size, weights, activations)
        ]

        self.parameters = {}
        """
        self.parameters
                |
                |-- pot_params_dict
                |       |-- CONFIG_POT_CONFIG_TAG (HEADER_POT_PARAMS_TAGS)
                |       |-- CONFIG_EVALUATION_TAG (HEADER_POT_PARAMS_TAGS)
                |       |-- ...
                |
                |-- config_params_dict
                        |-- model_params_dict
                        |       |-- CONFIG_MODEL_NAME_TAG (HEADER_MODEL_PARAMS_MODEL_TAGS)
                        |       |-- CONFIG_MODEL_TAG (HEADER_MODEL_PARAMS_MODEL_TAGS)
                        |       |-- CONFIG_WEIGHTS_TAG (HEADER_MODEL_PARAMS_MODEL_TAGS)
                        |
                        |-- engine_params_dict
                        |       |-- CONFIG_STAT_REQUESTS_NUMBER_TAG (HEADER_MODEL_PARAMS_ENGINE_TAGS)
                        |       |-- CONFIG_EVAL_REQUESTS_NUMBER_TAG (HEADER_MODEL_PARAMS_MODEL_TAGS)
                        |       |-- ...
                        |
                        |-- compression_params_dict
                                |-- ... (CompressionParameters.parameters)
        """
        pot_params_dict = {}
        for i, param_name in enumerate(HEADER_POT_PARAMS_TAGS):
            pot_params_dict[param_name] = self.__pot_params[i]

        model_params_dict = {}
        model_params_dict[CONFIG_MODEL_NAME_TAG] = model_params_list[0][0]
        parent_model_params_list = model_params_list[0][1].split(';')
        self.__parent_model = {
            'task': parent_model_params_list[0],
            'name': parent_model_params_list[1],
            'precision': parent_model_params_list[2],
            'framework': parent_model_params_list[3],
            'model_path': parent_model_params_list[4],
            'weights_path': parent_model_params_list[5],
        }
        model_params_dict[CONFIG_MODEL_TAG] = self.__parent_model['model_path']
        model_params_dict[CONFIG_WEIGHTS_TAG] = self.__parent_model['weights_path']

        self.__model_params = [
            [model_params_dict[tag] for tag in CONFIG_MODEL_PARAMS_MODEL_TAGS],
            model_params_list[1],
            model_params_list[2],
        ]

        engine_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_ENGINE_TAGS):
            engine_params_dict[param_name] = self.__model_params[1][i]

        self.__compression_params = CompressionParameters(self.__model_params[2], dependent_params)
        compression_params_dict = self.__compression_params.get_parameters_dict()

        config_params_dict = {
            CONFIG_MODEL_TAG: model_params_dict,
            CONFIG_ENGINE_TAG: engine_params_dict,
            CONFIG_COMPRESSION_TAG: compression_params_dict,
        }

        self.parameters[CONFIG_POT_PARAMETERS_TAG] = pot_params_dict
        self.parameters[CONFIG_Q_CONFIG_TAG] = config_params_dict

        self.__engine_type = self.__model_params[1][3]
        self.__quantization_method = self.__compression_params.get_quantization_method_name()

        self.__dependent_params = dependent_params
        self.__independent_params = [
            *self.__pot_params,
            *self.__model_params[0],
            *self.__model_params[1],
            *self.__model_params[2],
        ]

    def get_quantization_method(self):
        return self.__quantization_method

    def get_independent_params_list(self):
        return self.__independent_params

    def get_params(self):
        return self.__independent_params, self.__dependent_params

    def create_dom(self, file, i):
        DOM_CONFIG_ID_TAG = self.__create_dom_config_id(file, i)
        DOM_POT_PARAMETERS_TAG = self.__create_dom_pot_params(file)
        DOM_MODEL_PARAMETERS_TAG = self.__create_dom_model_params(file)
        return DOM_CONFIG_ID_TAG, DOM_POT_PARAMETERS_TAG, DOM_MODEL_PARAMETERS_TAG

    def __create_dom_model_params(self, file):
        DOM_MODEL_PARAMETERS_TAG = file.createElement(CONFIG_MODEL_PARAMETERS_TAG)

        DOM_MODEL_TAG = self.__create_dom_model_params_model(file)
        DOM_ENGINE_TAG = self.__create_dom_model_params_engine(file)
        DOM_COMPRESSION_TAG = self.__create_dom_model_params_compression(file)

        DOM_MODEL_PARAMETERS_TAG.appendChild(DOM_MODEL_TAG)
        DOM_MODEL_PARAMETERS_TAG.appendChild(DOM_ENGINE_TAG)
        DOM_MODEL_PARAMETERS_TAG.appendChild(DOM_COMPRESSION_TAG)

        return DOM_MODEL_PARAMETERS_TAG

    def __create_dom_model_params_model(self, file):
        DOM_MODEL_TAG = file.createElement(CONFIG_MODEL_TAG)

        DOM_MODEL_NAME_TAG = file.createElement(CONFIG_MODEL_NAME_TAG)
        DOM_MODEL_MODEL_TAG = file.createElement(CONFIG_MODEL_TAG)
        DOM_MODEL_WEIGHTS_TAG = file.createElement(CONFIG_WEIGHTS_TAG)

        DOM_MODEL_NAME_TAG.appendChild(file.createTextNode(self.__model_params[0][0]))
        DOM_MODEL_MODEL_TAG.appendChild(file.createTextNode(self.__model_params[0][1]))
        DOM_MODEL_WEIGHTS_TAG.appendChild(file.createTextNode(self.__model_params[0][2]))

        DOM_MODEL_TAG.appendChild(DOM_MODEL_NAME_TAG)
        DOM_MODEL_TAG.appendChild(DOM_MODEL_MODEL_TAG)
        DOM_MODEL_TAG.appendChild(DOM_MODEL_WEIGHTS_TAG)

        return DOM_MODEL_TAG

    def __create_dom_model_params_compression(self, file):
        return self.__compression_params.create_dom(file, self.__model_params[2])

    def __create_dom_model_params_engine(self, file):
        DOM_ENGINE_TAG = file.createElement(CONFIG_ENGINE_TAG)
        if self.__model_params[1][0] is not None and self.__model_params[1][0] != '':
            self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_STAT_REQUESTS_NUMBER_TAG, self.__model_params[1][0])
        if self.__model_params[1][1] is not None and self.__model_params[1][1] != '':
            self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_EVAL_REQUESTS_NUMBER_TAG, self.__model_params[1][1])
        if (self.__quantization_method == 'AccuracyAwareQuantization'):
            self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_CONFIG_TAG, self.__model_params[1][2])
        else:
            self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_CONFIG_TYPE_TAG, self.__engine_type)
            if (self.__engine_type == 'accuracy_checker'):
                self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_CONFIG_TAG, self.__model_params[1][2])
            else:
                self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_DATA_SOURCE_TAG, self.__model_params[1][4])
        return DOM_ENGINE_TAG

    def __create_dom_config_id(self, file, i):
        DOM_CONFIG_ID_TAG = file.createElement(CONFIG_CONFIG_ID_TAG)
        q_type = 'DQ' if (self.__quantization_method == 'DefaultQuantization') else 'AAQ'
        config_id = self.__model_params[0][0] + '_' + q_type + '_' + str(i)
        DOM_CONFIG_ID_TAG.appendChild(file.createTextNode(config_id))
        return DOM_CONFIG_ID_TAG

    def __create_dom_pot_params(self, file):
        DOM_POT_PARAMETERS_TAG = file.createElement(CONFIG_POT_PARAMETERS_TAG)
        for i, param_name in enumerate(HEADER_POT_PARAMS_TAGS):
            if self.__pot_params[i] != '' and self.__pot_params[i] is not None:
                self.create_dom_node(file, DOM_POT_PARAMETERS_TAG, param_name, self.__pot_params[i])
        return DOM_POT_PARAMETERS_TAG

    @staticmethod
    def create_dom_node(file, parent, child_name, text=None):
        child = file.createElement(child_name)
        if text is not None:
            child.appendChild(file.createTextNode(text))
        parent.appendChild(child)
        return child

    @staticmethod
    def parse(dom):
        pot_params = []
        dom_pot_params = dom.getElementsByTagName(CONFIG_POT_PARAMETERS_TAG)[0]
        pot_params = QModel.parse_pot_params(dom_pot_params)
        dom_model_params = dom.getElementsByTagName(CONFIG_MODEL_PARAMETERS_TAG)[0]
        m_params_dom = QModel.parse_model_params(dom_model_params.getElementsByTagName(CONFIG_MODEL_TAG)[0])
        m_params = [
            m_params_dom[0],
            '-;-;INT8;OpenVINO_DLDT;' + m_params_dom[1] + ';' + m_params_dom[2],
        ]
        e_params = QModel.parse_engine_params(dom_model_params.getElementsByTagName(CONFIG_ENGINE_TAG)[0])
        dependent_params, common_c_params = QModel.parse_compression_params(
            dom_model_params.getElementsByTagName(CONFIG_COMPRESSION_TAG)[0])
        model_params = m_params + e_params + common_c_params
        return QModel(pot_params, model_params, dependent_params)

    @staticmethod
    def parse_pot_params(dom):
        pot_params = []
        for tag in HEADER_POT_PARAMS_TAGS:
            pot_params.append(QModel.get_element_by_tag(dom, tag))
        return pot_params

    @staticmethod
    def parse_model_params(dom):
        model_params = []
        for tag in CONFIG_MODEL_PARAMS_MODEL_TAGS:
            model_params.append(QModel.get_element_by_tag(dom, tag))
        return model_params

    @staticmethod
    def parse_engine_params(dom):
        engine_params = [
            QModel.get_element_by_tag(dom, CONFIG_STAT_REQUESTS_NUMBER_TAG),
            QModel.get_element_by_tag(dom, CONFIG_EVAL_REQUESTS_NUMBER_TAG),
            QModel.get_element_by_tag(dom, CONFIG_CONFIG_TAG),
            QModel.get_element_by_tag(dom, CONFIG_CONFIG_TYPE_TAG),
            QModel.get_element_by_tag(dom, CONFIG_DATA_SOURCE_TAG),
        ]
        return engine_params

    @staticmethod
    def get_element_by_tag(dom, tag):
        nodes = dom.getElementsByTagName(tag)
        return nodes[0].firstChild.data if len(nodes) != 0 else None

    @staticmethod
    def parse_compression_params(dom):
        return CompressionParameters.parse(dom)

    @staticmethod
    def camel_to_snake(string):
        groups = re.findall('([A-z][a-z0-9]*)', string)
        return '_'.join([i.lower() for i in groups])
