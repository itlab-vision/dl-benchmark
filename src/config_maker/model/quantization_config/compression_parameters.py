import abc
from model.benchmark_config.test import DependentParameters
from tags import *
from model.quantization_config.quantized_model import QModel

class CompressionParameters:
    def __init__(self, independent_params, dependent_params):
        self.__quantization_method = independent_params[1]
        self.__dependent_params = DependentParameters.get_parameters(
            self.__quantization_method,
            dependent_params
        )
        dependent_params_dict = self.__dependent_params.get_parameters_dict()
        independent_params_dict = self.__create_independent_parameters_dict(independent_params)
        self.parameters = {**independent_params_dict, **dependent_params_dict}

    def get_quantization_method_name(self):
        return self.quantization_method

    def get_parameters_dict(self):
        return self.parameters

    def __create_independent_parameters_dict(self, independent_params):
        '''
        independent_params = [
            [00]<TargetDevice>,
            [01]<Algorithm>,
            [02]<Preset>,
            [03]<StatSubsetSize>,

            [04]<Weights::Bits>,
            [05]<Weights::Mode>,
            [06]<Weights::Granularity>,
            [07]<Weights::LevelLow>,
            [08]<Weights::LevelHigh>,

            [09]<Weights::RangeEstimator::Max::Type>,
            [10]<Weights::RangeEstimator::Max::OutlierProb>,

            [11]<Activations::Bits>,
            [12]<Activations::Mode>,
            [13]<Activations::Granularity>,

            [14]<Activations::RangeEstimator::Preset>,

            [15]<Activations::RangeEstimator::Min::ClippingValue>,
            [16]<Activations::RangeEstimator::Min::Aggregator>,
            [17]<Activations::RangeEstimator::Min::Type>,
            [18]<Activations::RangeEstimator::Min::OutlierProb>,

            [19]<Activations::RangeEstimator::Max::ClippingValue>,
            [20]<Activations::RangeEstimator::Max::Aggregator>,
            [21]<Activations::RangeEstimator::Max::Type>,
            [22]<Activations::RangeEstimator::Max::OutlierProb>
        ]
        '''
        weights_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[4:9]):
            weights_params_dict[param_name] = independent_params[i]
        w_re_params_dict = { CONFIG_WEIGHTS_MAX_TAG : {} }
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[9:11]):
            w_re_params_dict[CONFIG_WEIGHTS_MAX_TAG][param_name] = independent_params[i]
        weights_params_dict[CONFIG_WEIGHTS_RANGE_ESTIMATOR_TAG] = w_re_params_dict

        activations_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[11:14]):
            activations_params_dict[param_name] = independent_params[i]
        a_re_params_dict = { CONFIG_ACTIVATIONS_PRESET_TAG : independent_params[14],
            CONFIG_ACTIVATIONS_MIN_TAG : {}, CONFIG_ACTIVATIONS_MAX_TAG : {} }
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[15:19]):
            a_re_params_dict[CONFIG_ACTIVATIONS_MIN_TAG][param_name] = independent_params[i]
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[19:23]):
            a_re_params_dict[CONFIG_ACTIVATIONS_MAX_TAG][param_name] = independent_params[i]
        activations_params_dict[CONFIG_ACTIVATIONS_RANGE_ESTIMATOR_TAG] = a_re_params_dict

        parameters_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[0:4]):
            parameters_dict[param_name] = independent_params[i]
        parameters_dict[CONFIG_WEIGHTS_TAG] = weights_params_dict
        parameters_dict[CONFIG_ACTIVATIONS_TAG] = activations_params_dict

        return parameters_dict

    @staticmethod
    def parse(dom):
        common_compression_params = [QModel.get_element_by_tag(dom, CONFIG_TARGET_DEVICE_TAG)]
        algo_node = dom.getElementsByTagName(CONFIG_ALGORITHMS_TAG)[0]

        algorithm_name = algo_node.getElementsByTagName(CONFIG_ALGORITHM_NAME_TAG)[0].firstChild.data
        common_compression_params.append(algorithm_name)

        algo_params_node = algo_node.getElementsByTagName(CONFIG_COMPRESSION_PARAMS_TAG)[0]

        dependent_params = CompressionParameters.__parse_dependent_params(algorithm_name, algo_params_node)
        independent_params = CompressionParameters.__parse_independent_params(algo_params_node)
        common_compression_params.extend(independent_params)

        return dependent_params, common_compression_params

    @staticmethod
    def __parse_dependent_params(quantization_method, dom):
        DependentParameters.parse(quantization_method, dom)

    @staticmethod
    def __parse_independent_params(dom):
        independent_params = [
            QModel.get_element_by_tag(dom, CONFIG_PRESET_TAG),
            QModel.get_element_by_tag(dom, CONFIG_STAT_SUBSET_SIZE_TAG)
        ]

        weights_params = dom.getElementsByTagName(CONFIG_WEIGHTS_TAG)[0]
        for param_name in [CONFIG_WEIGHTS_BITS_TAG, CONFIG_WEIGHTS_MODE_TAG, CONFIG_WEIGHTS_GRANULARITY_TAG,
            CONFIG_WEIGHTS_LEVEL_LOW_TAG, CONFIG_WEIGHTS_LEVEL_HIGH_TAG]:
            independent_params.append(QModel.get_element_by_tag(weights_params, param_name))

        weights_re = dom.getElementsByTagName(CONFIG_WEIGHTS_RANGE_ESTIMATOR_TAG)[0]
        weights_max_params = weights_re.getElementsByTagName(CONFIG_WEIGHTS_MAX_TAG)[0]
        for param_name in [CONFIG_WEIGHTS_MAX_TYPE_TAG, CONFIG_WEIGHTS_MAX_OUTLIER_PROB_TAG]:
            independent_params.append(QModel.get_element_by_tag(weights_max_params, param_name))

        activations_params = dom.getElementsByTagName(CONFIG_WEIGHTS_TAG)[0]
        for param_name in [CONFIG_ACTIVATIONS_BITS_TAG, CONFIG_ACTIVATIONS_MODE_TAG,
            CONFIG_ACTIVATIONS_GRANULARITY_TAG, CONFIG_ACTIVATIONS_PRESET_TAG]:
            independent_params.append(QModel.get_element_by_tag(activations_params, param_name))

        activations_re = dom.getElementsByTagName(CONFIG_ACTIVATIONS_RANGE_ESTIMATOR_TAG)[0]
        independent_params.append(QModel.get_element_by_tag(activations_re, CONFIG_ACTIVATIONS_PRESET_TAG))

        activations_min_params = activations_re.getElementsByTagName(CONFIG_ACTIVATIONS_MIN_TAG)[0]
        for param_name in [CONFIG_ACTIVATIONS_MIN_CLIPPING_VALUE_TAG, CONFIG_ACTIVATIONS_MIN_AGGREGATOR_TAG,
            CONFIG_ACTIVATIONS_MIN_TYPE_TAG, CONFIG_ACTIVATIONS_MIN_OUTLIER_PROB_TAG]:
            independent_params.append(QModel.get_element_by_tag(activations_min_params, param_name))

        activations_max_params = activations_re.getElementsByTagName(CONFIG_ACTIVATIONS_MAX_TAG)[0]
        for param_name in [CONFIG_ACTIVATIONS_MAX_CLIPPING_VALUE_TAG, CONFIG_ACTIVATIONS_MAX_AGGREGATOR_TAG,
            CONFIG_ACTIVATIONS_MAX_TYPE_TAG, CONFIG_ACTIVATIONS_MAX_OUTLIER_PROB_TAG]:
            independent_params.append(QModel.get_element_by_tag(activations_max_params, param_name))

        return independent_params

    def create_dom(self, file, params, parent_node=None):
        DOM_COMPRESSION_TAG = parent_node if parent_node != None \
            else file.createElement(CONFIG_COMPRESSION_TAG)
        target_device = params[0]
        if target_device:
            QModel.create_dom_node(file, DOM_COMPRESSION_TAG, CONFIG_TARGET_DEVICE_TAG, target_device)
        DOM_ALGORITHMS_TAG = QModel.create_dom_node(file, DOM_COMPRESSION_TAG, CONFIG_ALGORITHMS_TAG)
        QModel.create_dom_node(file, DOM_ALGORITHMS_TAG, CONFIG_ALGORITHM_NAME_TAG, params[1])
        DOM_PARAMS_TAG = QModel.create_dom_node(file, DOM_ALGORITHMS_TAG, CONFIG_COMPRESSION_PARAMS_TAG)
        self.__create_dependent_params_dom(file, DOM_PARAMS_TAG)
        self.__create_independent_params_dom(file, params, DOM_PARAMS_TAG)
        return DOM_COMPRESSION_TAG

    def __create_dependent_params_dom(self, file, parent_node=None):
        self.__dependent_params.create_dom(file, parent_node)

    def __create_independent_params_dom(self, file, params, parent_node=None):
        DOM_PARAMS_TAG = parent_node if parent_node != None \
            else file.createElement(CONFIG_COMPRESSION_PARAMS_TAG)
        
        QModel.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_PRESET_TAG, params[2])
        QModel.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_STAT_SUBSET_SIZE_TAG, params[3])

        DOM_WEIGHTS_TAG = QModel.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_WEIGHTS_TAG)

        QModel.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_BITS_TAG, params[4])
        QModel.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_MODE_TAG, params[5])
        QModel.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_GRANULARITY_TAG, params[6])
        QModel.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_LEVEL_LOW_TAG, params[7])
        QModel.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_LEVEL_HIGH_TAG, params[8])

        DOM_WEIGHTS_RE_TAG = QModel.create_dom_node(
            file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_RANGE_ESTIMATOR_TAG)
        DOM_WEIGHTS_MAX_TAG = QModel.create_dom_node(file, DOM_WEIGHTS_RE_TAG, CONFIG_WEIGHTS_MAX_TAG)
        QModel.create_dom_node(file, DOM_WEIGHTS_MAX_TAG, CONFIG_WEIGHTS_MAX_TYPE_TAG, params[9])
        QModel.create_dom_node(file, DOM_WEIGHTS_MAX_TAG, CONFIG_WEIGHTS_MAX_OUTLIER_PROB_TAG, params[10])

        DOM_ACTIVATIONS_TAG = QModel.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_ACTIVATIONS_TAG)
        QModel.create_dom_node(file, DOM_ACTIVATIONS_TAG, CONFIG_ACTIVATIONS_BITS_TAG, params[11])
        QModel.create_dom_node(file, DOM_ACTIVATIONS_TAG, CONFIG_ACTIVATIONS_MODE_TAG, params[12])
        QModel.create_dom_node(file, DOM_ACTIVATIONS_TAG, CONFIG_ACTIVATIONS_GRANULARITY_TAG, params[13])

        DOM_ACTIVATIONS_RE_TAG = QModel.create_dom_node(
            file, DOM_ACTIVATIONS_TAG, CONFIG_ACTIVATIONS_RANGE_ESTIMATOR_TAG)
        QModel.create_dom_node(file, DOM_ACTIVATIONS_RE_TAG, CONFIG_ACTIVATIONS_PRESET_TAG, params[14])

        DOM_ACTIVATIONS_MIN_TAG = QModel.create_dom_node(
            file, DOM_ACTIVATIONS_RE_TAG, CONFIG_ACTIVATIONS_MIN_TAG)
        QModel.create_dom_node(file, DOM_ACTIVATIONS_MIN_TAG,
            CONFIG_ACTIVATIONS_MIN_CLIPPING_VALUE_TAG, params[15])
        QModel.create_dom_node(file, DOM_ACTIVATIONS_MIN_TAG,
            CONFIG_ACTIVATIONS_MIN_AGGREGATOR_TAG, params[16])
        QModel.create_dom_node(file, DOM_ACTIVATIONS_MIN_TAG,
            CONFIG_ACTIVATIONS_MIN_TYPE_TAG, params[17])
        QModel.create_dom_node(file, DOM_ACTIVATIONS_MIN_TAG,
            CONFIG_ACTIVATIONS_MIN_OUTLIER_PROB_TAG, params[18])

        DOM_ACTIVATIONS_MAX_TAG = QModel.create_dom_node(
            file, DOM_ACTIVATIONS_RE_TAG, CONFIG_ACTIVATIONS_MAX_TAG)
        QModel.create_dom_node(file, DOM_ACTIVATIONS_MAX_TAG,
            CONFIG_ACTIVATIONS_MAX_CLIPPING_VALUE_TAG, params[19])
        QModel.create_dom_node(file, DOM_ACTIVATIONS_MAX_TAG,
            CONFIG_ACTIVATIONS_MAX_AGGREGATOR_TAG, params[20])
        QModel.create_dom_node(file, DOM_ACTIVATIONS_MAX_TAG,
            CONFIG_ACTIVATIONS_MAX_TYPE_TAG, params[21])
        QModel.create_dom_node(file, DOM_ACTIVATIONS_MAX_TAG,
            CONFIG_ACTIVATIONS_MAX_OUTLIER_PROB_TAG, params[22])

        return DOM_PARAMS_TAG


class DependentParameters(metaclass=abc.ABCMeta):
    def __init__(self):
        self.parameters = {}

    @staticmethod
    def get_parameters(quantization_method, args):
        if quantization_method == 'DefaultQuantization':
            return DefaultQuantizationParameters(*args)
        elif quantization_method == 'AccuracyAwareQuantization':
            return AccuracyAwareQuantizationParameters(*args)
        else:
            raise ValueError('Unknown quantization method: {0} !'.format(quantization_method))

    # def get_parameter_list(self):
    #     return list(self.parameters.values())

    def get_parameters_dict(self):
        return self.parameters

    @staticmethod
    def parse(quantization_method, dom):
        if quantization_method == 'DefaultQuantization':
            return DefaultQuantizationParameters._parse_params(dom)
        elif quantization_method == 'AccuracyAwareQuantization':
            return AccuracyAwareQuantizationParameters._parse_params(dom)

    @abc.abstractmethod
    def _parse_params(self):
        pass

    @abc.abstractmethod
    def create_dom(self, file, parent_node=None):
        pass


class DefaultQuantizationParameters(DependentParameters):
    def __init__(self, params):
        # self.parameter_count = DEFAULT_QUANTIZATION_PARAMS_COUNT
        # for i, param in enumerate(params):
        #     self.__model_params[2][i] = param
        # for i, param_name in enumerate(HEADER_DQ_PARAMS_TAGS):
        #     self.parameters[param_name] = self.__model_params[2][i]
        for i, param_name in enumerate(HEADER_DQ_PARAMS_TAGS):
            self.parameters[param_name] = params[i]

    @staticmethod
    def _parse_params(dom):
        # -TODO: compression_parser metrics?
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


class AccuracyAwareQuantizationParameters(DependentParameters):
    def __init__(self, params):
        # self.parameter_count = ACCURACY_AWARE_QUANTIZATION_PARAMS_COUNT
        # for i, param in enumerate(params):
        #     self.__model_params[2][i] = param
        # for i, param_name in enumerate(HEADER_AAQ_PARAMS_TAGS):
        #     self.parameters[param_name] = self.__model_params[2][i]
        for i, param_name in enumerate(HEADER_AAQ_PARAMS_TAGS):
            self.parameters[param_name] = params[i]

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

        return DOM_COMPRESSION_PARAMS_TAG