# import os
import abc
import re
from xml.dom.minidom import Node
from model.quantization_config.compression_parameters import CompressionParameters
# pylint: disable-next=E0401
from tags import CONFIG_ACTIVATIONS_BITS_TAG, CONFIG_ACTIVATIONS_GRANULARITY_TAG, CONFIG_ACTIVATIONS_MAX_AGGREGATOR_TAG, CONFIG_ACTIVATIONS_MAX_CLIPPING_VALUE_TAG, CONFIG_ACTIVATIONS_MAX_OUTLIER_PROB_TAG, CONFIG_ACTIVATIONS_MAX_TAG, CONFIG_ACTIVATIONS_MAX_TYPE_TAG, CONFIG_ACTIVATIONS_MIN_AGGREGATOR_TAG, CONFIG_ACTIVATIONS_MIN_CLIPPING_VALUE_TAG, CONFIG_ACTIVATIONS_MIN_OUTLIER_PROB_TAG, CONFIG_ACTIVATIONS_MIN_TAG, CONFIG_ACTIVATIONS_MIN_TYPE_TAG, CONFIG_ACTIVATIONS_MODE_TAG, CONFIG_ACTIVATIONS_PRESET_TAG, CONFIG_ACTIVATIONS_RANGE_ESTIMATOR_TAG, CONFIG_ACTIVATIONS_TAG, CONFIG_ALGORITHM_NAME_TAG, CONFIG_ALGORITHMS_TAG, CONFIG_COMPRESSION_PARAMS_TAG, CONFIG_MODEL_TAG, CONFIG_PRESET_TAG, CONFIG_Q_CONFIG_TAG, CONFIG_STAT_SUBSET_SIZE_TAG, CONFIG_TARGET_DEVICE_TAG, CONFIG_TASK_TAG, CONFIG_NAME_TAG, CONFIG_PRECISION_TAG, \
    CONFIG_SOURCE_FRAMEWORK_TAG, CONFIG_MODEL_PATH_TAG, CONFIG_WEIGHTS_BITS_TAG, CONFIG_WEIGHTS_GRANULARITY_TAG, CONFIG_WEIGHTS_LEVEL_HIGH_TAG, CONFIG_WEIGHTS_LEVEL_LOW_TAG, CONFIG_WEIGHTS_MAX_OUTLIER_PROB_TAG, CONFIG_WEIGHTS_MAX_TAG, CONFIG_WEIGHTS_MAX_TYPE_TAG, CONFIG_WEIGHTS_MODE_TAG, CONFIG_WEIGHTS_PATH_TAG, CONFIG_DIRECTORY_TAG, CONFIG_WEIGHTS_RANGE_ESTIMATOR_TAG, DEFAULT_QUANTIZATION_PARAMS_COUNT, DEPENDENT_PARAMETERS_TAG, HEADER_AAQ_PARAMS_TAGS, HEADER_DQ_PARAMS_TAGS, HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS
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
            model_params[:idx_1],  # config_model_params (model_name, model (.xml), weights (.bin))
            model_params[idx_1:idx_2],  # config_engine_params
            model_params[idx_2:],       # config_common_compression_params (target_device, algorithm, preset,
                                        #   stat_subset_size, weights, activations)
        ]

        # self.parameters = Parameters(self.__pot_params, self.__model_params, dependent_params)

        '''
        self.parameters = {}
        pot_params_dict = {}
        for i, param_name in enumerate(HEADER_POT_PARAMS_TAGS):
            pot_params_dict[param_name] = self.__pot_params[i]
        self.parameters[CONFIG_POT_PARAMETERS_TAG] = pot_params_dict

        config_params_dict
        model_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_MODEL_TAGS):
            model_params_dict[param_name] = self.__model_params[0][i]

        for i, param_name in enumerate(HEADER_MODEL_PARAMS_ENGINE_TAGS):
            self.parameters[param_name] = self.__model_params[1][i]
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS):
            self.parameters[param_name] = self.__model_params[2][i]

        self.parameters[CONFIG_Q_CONFIG_TAG] = {}

        self.parameters[DEPENDENT_PARAMETERS_TAG] = CompressionParameters.get_parameters(
            self.__quantization_method,
            dependent_params
        )
        '''

        self.parameters = {}
        '''
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
        '''
        pot_params_dict = {}
        for i, param_name in enumerate(HEADER_POT_PARAMS_TAGS):
            pot_params_dict[param_name] = self.__pot_params[i]

        model_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_MODEL_TAGS):
            model_params_dict[param_name] = self.__model_params[0][i]

        engine_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_ENGINE_TAGS):
            engine_params_dict[param_name] = self.__model_params[1][i]

        self.__compression_params = CompressionParameters(self.__model_params[2], dependent_params)
        compression_params_dict = self.__compression_params.get_parameters_dict()

        '''
        compression_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS):
            compression_params_dict[param_name] = model_params[2][i]

        compression_params_dict[DEPENDENT_PARAMETERS_TAG] = CompressionParameters.get_parameters(
            self.__quantization_method,
            dependent_params
        )
        '''

        config_params_dict = {
            CONFIG_MODEL_TAG : model_params_dict,
            CONFIG_ENGINE_TAG : engine_params_dict,
            CONFIG_COMPRESSION_TAG : compression_params_dict
        }

        self.parameters[CONFIG_POT_PARAMETERS_TAG] = pot_params_dict
        self.parameters[CONFIG_Q_CONFIG_TAG] = config_params_dict

        self.__engine_type = self.__model_params[1][3]
        self.__quantization_method = self.__compression_params.get_quantization_method_name()
        # self.__quantization_method = 'DefaultQuantization' # self.__model_params[2][1]

        self.__dependent_params = dependent_params
        self.__independent_params = [
            *self.__pot_params,
            *self.__model_params[0],
            *self.__model_params[1],
            *self.__model_params[2]
        ]


    # def get_all_params(self):
    #     return self.__pot_params + self.__model_params[0] + self.__model_params[1] + self.__model_params[2]


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
        # return self.parameters.get_compression_params().create_dom(file)
        return self.__compression_params.create_dom(file, self.__model_params[2])
        '''
        DOM_COMPRESSION_TAG = file.createElement(CONFIG_COMPRESSION_TAG)
        target_device = self.__model_params[2][0]
        if target_device:
            self.create_dom_node(file, DOM_COMPRESSION_TAG, CONFIG_TARGET_DEVICE_TAG, target_device)
        DOM_ALGORITHMS_TAG = self.create_dom_node(file, DOM_COMPRESSION_TAG, CONFIG_ALGORITHMS_TAG)
        self.create_dom_node(file, DOM_ALGORITHMS_TAG, CONFIG_ALGORITHM_NAME_TAG, self.__model_params[2][1])
        DOM_PARAMS_TAG = self.create_dom_node(file, DOM_ALGORITHMS_TAG, CONFIG_COMPRESSION_PARAMS_TAG)
        self.parameters[DEPENDENT_PARAMETERS_TAG].create_dependent_params_dom(file, DOM_PARAMS_TAG)
        CompressionParameters.create_independent_params_dom(file, self.__model_params[2], DOM_PARAMS_TAG)
        # -TODO: compression_parser (weights, activations, ignored)
        # pass
        return DOM_COMPRESSION_TAG
        '''


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
            self.create_dom_node(file, DOM_POT_PARAMETERS_TAG, param_name, self.__pot_params[i])
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
        dependent_params, common_c_params = QModel.parse_compression_params(
            dom_model_params.getElementsByTagName(CONFIG_COMPRESSION_TAG)[0]
        )
        model_params = m_params + e_params + common_c_params
        return QModel(pot_params, model_params, dependent_params)


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
        return CompressionParameters.parse(dom)
        '''
        compression_params = [QModel.get_element_by_tag(dom, CONFIG_TARGET_DEVICE_TAG)]
        # target_device = dom.getElementsByTagName(CONFIG_TARGET_DEVICE_TAG)
        # compression_params.append(target_device[0].firstChild.data if len(target_device) != 0 else None)
        algo_node = dom.getElementsByTagName(CONFIG_ALGORITHMS_TAG)[0]

        algorithm_name = algo_node.getElementsByTagName(CONFIG_ALGORITHM_NAME_TAG)[0].firstChild.data
        compression_params.append(algorithm_name)

        algo_params_node = algo_node.getElementsByTagName(CONFIG_COMPRESSION_PARAMS_TAG)[0]

        dependent_params = CompressionParameters.parse_dependent_params(algorithm_name, algo_params_node)
        independent_params = CompressionParameters.parse_independent_params(algo_params_node)
        compression_params.extend(independent_params)
        # compression_params.append(*dependent_params)
        # -TODO: compression_parser for weights, activations, ignored
        # pass
        return dependent_params, compression_params
        '''


    @staticmethod
    def camel_to_snake(string):
        groups = re.findall('([A-z][a-z0-9]*)', string)
        return '_'.join([i.lower() for i in groups])

