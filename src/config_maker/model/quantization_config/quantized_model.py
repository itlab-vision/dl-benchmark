# import os
import abc
import re
from xml.dom.minidom import Node
# pylint: disable-next=E0401
from tags import CONFIG_ALGORITHM_NAME_TAG, CONFIG_ALGORITHMS_TAG, CONFIG_COMPRESSION_PARAMS, CONFIG_COMPRESSION_PARAMS_TAG, CONFIG_MODEL_TAG, CONFIG_PRESET_TAG, CONFIG_STAT_SUBSET_SIZE_TAG, CONFIG_TARGET_DEVICE_TAG, CONFIG_TASK_TAG, CONFIG_NAME_TAG, CONFIG_PRECISION_TAG, \
    CONFIG_SOURCE_FRAMEWORK_TAG, CONFIG_MODEL_PATH_TAG, CONFIG_WEIGHTS_PATH_TAG, CONFIG_DIRECTORY_TAG, DEFAULT_QUANTIZATION_PARAMS_COUNT, HEADER_AAQ_PARAMS_TAGS, HEADER_DQ_PARAMS_TAGS
from tags import CONFIG_POT_CONFIG_TAG, CONFIG_EVALUATION_TAG, CONFIG_OUTPUT_DIR_TAG, \
    CONFIG_DIRECT_DUMP_TAG, CONFIG_LOG_LEVEL_TAG, CONFIG_PROGRESS_BAR_TAG, \
    CONFIG_STREAM_OUTPUT_TAG, CONFIG_KEEP_WEIGHTS_TAG
from tags import CONFIG_POT_PARAMETERS_TAG, CONFIG_MODEL_PARAMETERS_TAG, CONFIG_ENGINE_TAG, CONFIG_COMPRESSION_TAG, \
    CONFIG_CONFIG_TAG, CONFIG_CONFIG_ID_TAG
from tags import CONFIG_MODEL_NAME_TAG, CONFIG_MODEL_PARAMETERS_TAG, CONFIG_ENGINE_TAG, CONFIG_COMPRESSION_TAG, \
    CONFIG_WEIGHTS_TAG
from tags import CONFIG_STAT_REQUESTS_NUMBER_TAG, CONFIG_EVAL_REQUESTS_NUMBER_TAG, CONFIG_CONFIG_TAG, \
    CONFIG_DATA_SOURCE_TAG, CONFIG_CONFIG_TYPE_TAG
from tags import HEADER_POT_PARAMS_TAGS, HEADER_MODEL_PARAMS_MODEL_TAGS, HEADER_MODEL_PARAMS_ENGINE_TAGS


class QModel:
    def __init__(self, pot_params, model_params, dependent_params):
        self.__pot_params = [*pot_params]

        COUNT_OF_CONFIG_MODEL_PARAMS = 3
        COUNt_OF_CONFIG_ENGINE_PARAMS = 5

        idx_0 = 0
        idx_1 = idx_0 + COUNT_OF_CONFIG_MODEL_PARAMS
        idx_2 = idx_1 + COUNt_OF_CONFIG_ENGINE_PARAMS
        idx_3 = -1

        self.__model_params = [
            model_params[idx_0:idx_1], # config_model_params (model_name, model (.xml), weights (.bin))
            model_params[idx_1:idx_2], # config_engine_params
            model_params[idx_2:idx_3],  # config_compression_params
        ]

        self.__engine_type = self.__model_params[1][3]
        self.__quantization_method = 'DefaultQuantization' # self.__model_params[2][1]

        self.parameters = {}
        for i, param_name in enumerate(HEADER_POT_PARAMS_TAGS):
            self.parameters[param_name] = self.__pot_params[i]
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_MODEL_TAGS):
            self.parameters[param_name] = self.__model_params[0][i]
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_ENGINE_TAGS):
            self.parameters[param_name] = self.__model_params[1][i]

        self.parameters['DependentParams'] = CompressionParameters.get_parameters(
            self.__quantization_method,
            dependent_params
        )


    # def get_all_params(self):
    #     return self.__pot_params + self.__model_params[0] + self.__model_params[1] + self.__model_params[2]


    # @staticmethod
    # def camel_to_snake(string):
    #     groups = re.findall('([A-z][a-z0-9]*)', string)
    #     return '_'.join([i.lower() for i in groups])


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
        DOM_COMPRESSION_TAG = file.createElement(CONFIG_COMPRESSION_TAG)
        target_device = self.__model_params[2][0]
        if target_device:
            self.create_dom_node(file, DOM_COMPRESSION_TAG, CONFIG_TARGET_DEVICE_TAG, target_device)
        DOM_ALGORITHMS_TAG = self.create_dom_node(file, DOM_COMPRESSION_TAG, CONFIG_ALGORITHMS_TAG)
        self.create_dom_node(file, DOM_ALGORITHMS_TAG, CONFIG_ALGORITHM_NAME_TAG, self.__model_params[2][1])
        DOM_PARAMS_TAG = self.create_dom_node(file, DOM_ALGORITHMS_TAG, CONFIG_COMPRESSION_PARAMS_TAG)
        self.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_PRESET_TAG, self.__model_params[2][2])
        self.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_STAT_SUBSET_SIZE_TAG, self.__model_params[2][3])
        self.parameters['DependentParams'].create_dom(file, DOM_PARAMS_TAG)
        # TODO: compression_parser (weights, activations, ignored)
        pass
        return DOM_COMPRESSION_TAG


    def __create_dom_model_params_engine(self, file):
        DOM_ENGINE_TAG = file.createElement(CONFIG_ENGINE_TAG)
        '''
        DOM_STAT_REQUESTS_NUMBER_TAG = file.createElement(CONFIG_STAT_REQUESTS_NUMBER_TAG)
        DOM_STAT_REQUESTS_NUMBER_TAG.appendChild(file.createTextNode(self.__model_params[1][0]))
        DOM_ENGINE_TAG.appendChild(DOM_STAT_REQUESTS_NUMBER_TAG)
        DOM_EVAL_REQUESTS_NUMBER_TAG.appendChild(file.createTextNode(self.__model_params[1][1]))
        DOM_EVAL_REQUESTS_NUMBER_TAG = file.createElement(CONFIG_EVAL_REQUESTS_NUMBER_TAG)
        DOM_ENGINE_TAG.appendChild(DOM_EVAL_REQUESTS_NUMBER_TAG)
        '''
        self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_STAT_REQUESTS_NUMBER_TAG, self.__model_params[1][0])
        self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_EVAL_REQUESTS_NUMBER_TAG, self.__model_params[1][1])
        if (self.__quantization_method == 'AccuracyAwareQuantization'):
            self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_CONFIG_TAG, self.__model_params[1][2])
        # if (self.__quantization_method == 'DefaultQuantization'):
        else:
            self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_CONFIG_TYPE_TAG, self.__engine_type)
            if (self.__engine_type == 'accuracy_checker'):
                self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_CONFIG_TAG, self.__model_params[1][2])
            # if (self.__engine_type == 'simplified'):
            else:
                self.create_dom_node(file, DOM_ENGINE_TAG, CONFIG_DATA_SOURCE_TAG, self.__model_params[1][4])
        return DOM_ENGINE_TAG


    def __create_dom_config_id(self, file, i):
        DOM_CONFIG_ID_TAG = file.createElement(CONFIG_CONFIG_ID_TAG)
        # config_id = self.__model_params[0][0] + '_' + self.__quantization_method + '_' + str(i)
        q_type = 'DQ' if (self.__quantization_method == 'DefaultQuantization') else 'AAQ'
        config_id = self.__model_params[0][0] + '_' + q_type + '_' + str(i)
        DOM_CONFIG_ID_TAG.appendChild(file.createTextNode(config_id))
        return DOM_CONFIG_ID_TAG


    def __create_dom_pot_params(self, file):
        DOM_POT_PARAMETERS_TAG = file.createElement(CONFIG_POT_PARAMETERS_TAG)

        for i, param_name in enumerate(HEADER_POT_PARAMS_TAGS):
            self.create_dom_node(file, DOM_POT_PARAMETERS_TAG, param_name, self.__pot_params[0])
        '''
        DOM_POT_CONFIG_TAG = file.createElement(CONFIG_POT_CONFIG_TAG)
        DOM_EVALUATION_TAG = file.createElement(CONFIG_EVALUATION_TAG)
        DOM_OUTPUT_DIR_TAG = file.createElement(CONFIG_OUTPUT_DIR_TAG)
        DOM_DIRECT_DUMP_TAG = file.createElement(CONFIG_DIRECT_DUMP_TAG)
        DOM_LOG_LEVEL_TAG = file.createElement(CONFIG_LOG_LEVEL_TAG)
        DOM_PROGRESS_BAR_TAG = file.createElement(CONFIG_PROGRESS_BAR_TAG)
        DOM_STREAM_OUTPUT_TAG = file.createElement(CONFIG_STREAM_OUTPUT_TAG)
        DOM_KEEP_WEIGHTS_TAG = file.createElement(CONFIG_KEEP_WEIGHTS_TAG)

        DOM_POT_CONFIG_TAG.appendChild(file.createTextNode(self.__pot_params[0]))
        DOM_EVALUATION_TAG.appendChild(file.createTextNode(self.__pot_params[1]))
        DOM_OUTPUT_DIR_TAG.appendChild(file.createTextNode(self.__pot_params[2]))
        DOM_DIRECT_DUMP_TAG.appendChild(file.createTextNode(self.__pot_params[3]))
        DOM_LOG_LEVEL_TAG.appendChild(file.createTextNode(self.__pot_params[4]))
        DOM_PROGRESS_BAR_TAG.appendChild(file.createTextNode(self.__pot_params[5]))
        DOM_STREAM_OUTPUT_TAG.appendChild(file.createTextNode(self.__pot_params[6]))
        DOM_KEEP_WEIGHTS_TAG.appendChild(file.createTextNode(self.__pot_params[7]))

        DOM_POT_PARAMETERS_TAG.appendChild(DOM_POT_CONFIG_TAG)
        DOM_POT_PARAMETERS_TAG.appendChild(DOM_EVALUATION_TAG)
        DOM_POT_PARAMETERS_TAG.appendChild(DOM_OUTPUT_DIR_TAG)
        DOM_POT_PARAMETERS_TAG.appendChild(DOM_DIRECT_DUMP_TAG)
        DOM_POT_PARAMETERS_TAG.appendChild(DOM_LOG_LEVEL_TAG)
        DOM_POT_PARAMETERS_TAG.appendChild(DOM_PROGRESS_BAR_TAG)
        DOM_POT_PARAMETERS_TAG.appendChild(DOM_STREAM_OUTPUT_TAG)
        DOM_POT_PARAMETERS_TAG.appendChild(DOM_KEEP_WEIGHTS_TAG)
        '''
        return DOM_POT_PARAMETERS_TAG

    @staticmethod
    def create_dom_node(file, parent, child_name, text=None):
        child = file.createElement(child_name)
        if text != None:
            child.appendChild(file.createTextNode(text))
        parent.appendChild(child)
        return child


    @staticmethod
    def parse(dom):
        pot_params = []
        dom_pot_params = dom.getElementsByTagName(CONFIG_POT_PARAMETERS_TAG)[0]
        for params in dom_pot_params.childNodes:
            if params.nodeType == Node.ELEMENT_NODE:
                pot_params.append(params.firstChild.data)
        '''
        model_params = []
        dom_model_params = dom.getElementsByTagName(CONFIG_MODEL_PARAMETERS)[0]
        model_params.extend(
            QModel.parse_model_params(dom_model_params.getElementsByTagName(CONFIG_MODEL_TAG)[0]),
            QModel.parse_engine_params(dom_model_params.getElementsByTagName(CONFIG_ENGINE_TAG)[0]),
            QModel.parse_compression_params(dom_model_params.getElementsByTagName(CONFIG_COMPRESSION_TAG)[0])
        )
        '''
        dom_model_params = dom.getElementsByTagName(CONFIG_MODEL_PARAMETERS_TAG)[0]
        m_params = QModel.parse_model_params(dom_model_params.getElementsByTagName(CONFIG_MODEL_TAG)[0])
        e_params = QModel.parse_engine_params(dom_model_params.getElementsByTagName(CONFIG_ENGINE_TAG)[0])
        c_params = QModel.parse_compression_params(dom_model_params.getElementsByTagName(CONFIG_COMPRESSION_TAG)[0])
        model_params = m_params + e_params + c_params
        return QModel(pot_params, model_params)


    @staticmethod
    def parse_model_params(dom):
        model_params = []
        for params in dom.childNodes:
            if params.nodeType == Node.ELEMENT_NODE:
                model_params.append(params.firstChild.data)
        return model_params


    @staticmethod
    def parse_engine_params(dom):
        engine_params = [
            QModel.get_element_by_tag(dom, CONFIG_STAT_REQUESTS_NUMBER_TAG),
            QModel.get_element_by_tag(dom, CONFIG_EVAL_REQUESTS_NUMBER_TAG),
            QModel.get_element_by_tag(dom, CONFIG_CONFIG_TAG),
            QModel.get_element_by_tag(dom, CONFIG_CONFIG_TYPE_TAG),
            QModel.get_element_by_tag(dom, CONFIG_DATA_SOURCE_TAG)
            # dom.getElementsByTagName(CONFIG_STAT_REQUESTS_NUMBER_TAG)[0].firstChild.data,
            # dom.getElementsByTagName(CONFIG_EVAL_REQUESTS_NUMBER_TAG)[0].firstChild.data
        ]

        # config = dom.getElementsByTagName(CONFIG_CONFIG_TAG)
        # engine_params.append(config[0].firstChild.data if len(config) != 0 else None)

        # config_type = dom.getElementsByTagName(CONFIG_CONFIG_TYPE_TAG)
        # engine_params.append(config_type[0].firstChild.data if len(config_type) != 0 else None)

        # config_data = dom.getElementsByTagName(CONFIG_DATA_SOURCE_TAG)
        # engine_params.append(config_data[0].firstChild.data if len(config_data) != 0 else None)

        return engine_params


    @staticmethod
    def get_element_by_tag(dom, tag):
        nodes = dom.getElementsByTagName(tag)
        return nodes[0].firstChild.data if len(nodes) != 0 else None


    @staticmethod
    def parse_compression_params(dom):
        compression_params = [QModel.get_element_by_tag(dom, CONFIG_TARGET_DEVICE_TAG)]
        # target_device = dom.getElementsByTagName(CONFIG_TARGET_DEVICE_TAG)
        # compression_params.append(target_device[0].firstChild.data if len(target_device) != 0 else None)
        algo_node = dom.getElementsByTagName(CONFIG_ALGORITHMS_TAG)[0]
        algorithm = algo_node.getElementsByTagName(CONFIG_ALGORITHM_NAME_TAG)[0]
        compression_params.append(algorithm.firstChild.data)
        dependent_params = CompressionParameters.parse(algorithm, algo_node)
        compression_params.append(*dependent_params)
        # TODO: compression_parser for weights, activations, ignored
        pass
        return compression_params


class CompressionParameters(metaclass=abc.ABCMeta):
    def __init__(self):
        # self.parameter_count = -1
        self.parameters = {}

    @staticmethod
    def get_parameters(quantization_method, args):
        if quantization_method == 'DefaultQuantization':
            return DefaultQuantizationParameters(*args)
        elif quantization_method == 'AccuracyAwareQuantization':
            return AccuracyAwareQuantizationParameters(*args)
        else:
            raise ValueError('Unknown quantization method: {0} !'.format(quantization_method))

    def get_parameter_list(self):
        return list(self.parameters.values())

    def get_parameter_dict(self):
        return self.parameters

    @staticmethod
    def parse(quantization_method, dom):
        params_dom = dom.getElementsByTagName(CONFIG_COMPRESSION_PARAMS_TAG)[0]
        if quantization_method == 'DefaultQuantization':
            return DefaultQuantizationParameters._parse_params(params_dom)
        elif quantization_method == 'AccuracyAwareQuantization':
            return AccuracyAwareQuantizationParameters._parse_params(params_dom)

    @abc.abstractmethod
    def _parse_params(self):
        pass

    @abc.abstractmethod
    def create_dom(self, file, parent_node=None):
        pass


class DefaultQuantizationParameters(CompressionParameters):
    def __init__(self, params):
        # self.parameter_count = DEFAULT_QUANTIZATION_PARAMS_COUNT
        for i, param in enumerate(params):
            self.__model_params[2][i] = param
        for i, param_name in enumerate(HEADER_DQ_PARAMS_TAGS):
            self.parameters[param_name] = self.__model_params[2][i]

    @staticmethod
    def _parse_params(dom):
        # TODO: compression_parser metrics?
        params = []
        for param_name in HEADER_DQ_PARAMS_TAGS:
            # param_node = dom.getElementsByTagName(param_name)[0].firstChild
            param_node = dom.getElementsByTagName(param_name)
            params.append(param_node[0].firstChild.data if param_node else '')
        return DefaultQuantizationParameters(params)

    def create_dom(self, file, parent_node=None):
        DOM_COMPRESSION_PARAMS_TAG = parent_node if parent_node != None \
            else file.createElement(CONFIG_COMPRESSION_PARAMS_TAG)

        for key in self.parameters:
            QModel.create_dom_node(file, DOM_COMPRESSION_PARAMS_TAG, key, self.parameters[key])
            # DOM_PARAMETER = file.createElement(key)
            # DOM_PARAMETER.appendChild(file.createTextNode(self.parameters[key]))
            # DOM_COMPRESSION_PARAMS_TAG.appendChild(DOM_PARAMETER)

        return DOM_COMPRESSION_PARAMS_TAG


class AccuracyAwareQuantizationParameters(CompressionParameters):
    def __init__(self, params):
        # self.parameter_count = ACCURACY_AWARE_QUANTIZATION_PARAMS_COUNT
        for i, param in enumerate(params):
            self.__model_params[2][i] = param
        for i, param_name in enumerate(HEADER_AAQ_PARAMS_TAGS):
            self.parameters[param_name] = self.__model_params[2][i]

    @staticmethod
    def _parse_params(dom):
        params = []
        for param_name in HEADER_AAQ_PARAMS_TAGS:
            # param_node = dom.getElementsByTagName(param_name)[0].firstChild
            param_node = dom.getElementsByTagName(param_name)
            params.append(param_node[0].firstChild.data if param_node else '')
        return AccuracyAwareQuantizationParameters(params)

    def create_dom(self, file, parent_node=None):
        DOM_COMPRESSION_PARAMS_TAG = parent_node if parent_node != None \
            else file.createElement(CONFIG_COMPRESSION_PARAMS_TAG)

        for key in self.parameters:
            QModel.create_dom_node(file, DOM_COMPRESSION_PARAMS_TAG, key, self.parameters[key])
