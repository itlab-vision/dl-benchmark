import abc

from tags import (HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS, CONFIG_WEIGHTS_MAX_TAG,
                  CONFIG_WEIGHTS_RANGE_ESTIMATOR_TAG, CONFIG_ACTIVATIONS_PRESET_TAG, CONFIG_ACTIVATIONS_MIN_TAG,
                  CONFIG_ACTIVATIONS_MAX_TAG, CONFIG_ACTIVATIONS_RANGE_ESTIMATOR_TAG, CONFIG_WEIGHTS_TAG,
                  CONFIG_ACTIVATIONS_TAG, CONFIG_TARGET_DEVICE_TAG, CONFIG_ALGORITHMS_TAG, CONFIG_ALGORITHM_NAME_TAG,
                  CONFIG_COMPRESSION_PARAMS_TAG, CONFIG_PRESET_TAG, CONFIG_STAT_SUBSET_SIZE_TAG,
                  CONFIG_WEIGHTS_BITS_TAG, CONFIG_WEIGHTS_MODE_TAG, CONFIG_WEIGHTS_GRANULARITY_TAG,
                  CONFIG_WEIGHTS_LEVEL_LOW_TAG, CONFIG_WEIGHTS_LEVEL_HIGH_TAG, CONFIG_WEIGHTS_MAX_TYPE_TAG,
                  CONFIG_WEIGHTS_MAX_OUTLIER_PROB_TAG, CONFIG_ACTIVATIONS_BITS_TAG, CONFIG_ACTIVATIONS_MODE_TAG,
                  CONFIG_ACTIVATIONS_GRANULARITY_TAG, CONFIG_ACTIVATIONS_MIN_CLIPPING_VALUE_TAG,
                  CONFIG_ACTIVATIONS_MIN_AGGREGATOR_TAG, CONFIG_ACTIVATIONS_MIN_TYPE_TAG,
                  CONFIG_ACTIVATIONS_MIN_OUTLIER_PROB_TAG, CONFIG_ACTIVATIONS_MAX_CLIPPING_VALUE_TAG,
                  CONFIG_ACTIVATIONS_MAX_AGGREGATOR_TAG, CONFIG_ACTIVATIONS_MAX_TYPE_TAG,
                  CONFIG_ACTIVATIONS_MAX_OUTLIER_PROB_TAG, CONFIG_COMPRESSION_TAG,
                  HEADER_DQ_PARAMS_TAGS, HEADER_AAQ_PARAMS_TAGS)


class CompressionParameters:
    def __init__(self, independent_params, dependent_params):
        self.__quantization_method = independent_params[1]
        self.__dependent_params = DependentParameters.get_parameters(
            self.__quantization_method,
            dependent_params)
        dependent_params_dict = self.__dependent_params.get_parameters_dict()
        independent_params_dict = self.__create_independent_parameters_dict(independent_params)
        self.parameters = {**independent_params_dict, **dependent_params_dict}

    def get_quantization_method_name(self):
        return self.__quantization_method

    def get_parameters_dict(self):
        return self.parameters

    def __create_independent_parameters_dict(self, independent_params):
        weights_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[4:9]):
            weights_params_dict[param_name] = independent_params[i]
        w_re_params_dict = {CONFIG_WEIGHTS_MAX_TAG: {}}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[9:11]):
            w_re_params_dict[CONFIG_WEIGHTS_MAX_TAG][param_name] = independent_params[i]
        weights_params_dict[CONFIG_WEIGHTS_RANGE_ESTIMATOR_TAG] = w_re_params_dict

        activations_params_dict = {}
        for i, param_name in enumerate(HEADER_MODEL_PARAMS_COMPRESSION_COMMON_TAGS[11:14]):
            activations_params_dict[param_name] = independent_params[i]
        a_re_params_dict = {CONFIG_ACTIVATIONS_PRESET_TAG: independent_params[14],
                            CONFIG_ACTIVATIONS_MIN_TAG: {}, CONFIG_ACTIVATIONS_MAX_TAG: {}}
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
        common_compression_params = [CompressionParameters.get_element_by_tag(dom, CONFIG_TARGET_DEVICE_TAG)]
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
        return DependentParameters.parse(quantization_method, dom).get_parameters_list()

    @staticmethod
    def __parse_independent_params(dom):
        independent_params = [
            CompressionParameters.get_element_by_tag(dom, CONFIG_PRESET_TAG),
            CompressionParameters.get_element_by_tag(dom, CONFIG_STAT_SUBSET_SIZE_TAG),
        ]

        weights_params = dom.getElementsByTagName(CONFIG_WEIGHTS_TAG)
        weights_params_tags = [
            CONFIG_WEIGHTS_BITS_TAG, CONFIG_WEIGHTS_MODE_TAG, CONFIG_WEIGHTS_GRANULARITY_TAG,
            CONFIG_WEIGHTS_LEVEL_LOW_TAG, CONFIG_WEIGHTS_LEVEL_HIGH_TAG,
        ]
        if weights_params != []:
            weights_params = weights_params[0]
            for param_name in weights_params_tags:
                independent_params.append(CompressionParameters.get_element_by_tag(weights_params, param_name))

            weights_re = weights_params.getElementsByTagName(CONFIG_WEIGHTS_RANGE_ESTIMATOR_TAG)
            if weights_re != []:
                weights_re = weights_re[0]
                weights_max_params = weights_re.getElementsByTagName(CONFIG_WEIGHTS_MAX_TAG)
                weights_max_params = weights_max_params[0] if weights_max_params != [] else None
            else:   # weights_re == []
                weights_max_params = None

            for param_name in [CONFIG_WEIGHTS_MAX_TYPE_TAG, CONFIG_WEIGHTS_MAX_OUTLIER_PROB_TAG]:
                independent_params.append(CompressionParameters.get_element_by_tag(weights_max_params, param_name))

        else:   # weights_params == []
            for _ in weights_params_tags + [CONFIG_WEIGHTS_MAX_TYPE_TAG, CONFIG_WEIGHTS_MAX_OUTLIER_PROB_TAG]:
                independent_params.append(None)

        activations_params = dom.getElementsByTagName(CONFIG_ACTIVATIONS_TAG)
        activations_params_tags = [
            CONFIG_ACTIVATIONS_BITS_TAG, CONFIG_ACTIVATIONS_MODE_TAG, CONFIG_ACTIVATIONS_GRANULARITY_TAG,
        ]
        activations_min_params_tags = [
            CONFIG_ACTIVATIONS_MIN_CLIPPING_VALUE_TAG, CONFIG_ACTIVATIONS_MIN_AGGREGATOR_TAG,
            CONFIG_ACTIVATIONS_MIN_TYPE_TAG, CONFIG_ACTIVATIONS_MIN_OUTLIER_PROB_TAG,
        ]
        activations_max_params_tags = [
            CONFIG_ACTIVATIONS_MAX_CLIPPING_VALUE_TAG, CONFIG_ACTIVATIONS_MAX_AGGREGATOR_TAG,
            CONFIG_ACTIVATIONS_MAX_TYPE_TAG, CONFIG_ACTIVATIONS_MAX_OUTLIER_PROB_TAG,
        ]

        if activations_params != []:
            activations_params = activations_params[0]
            for param_name in activations_params_tags:
                independent_params.append(CompressionParameters.get_element_by_tag(activations_params, param_name))

            activations_re = activations_params.getElementsByTagName(CONFIG_ACTIVATIONS_RANGE_ESTIMATOR_TAG)
            if activations_re != []:
                activations_re = activations_re[0]
                independent_params.append(CompressionParameters.get_element_by_tag(
                    activations_re,
                    CONFIG_ACTIVATIONS_PRESET_TAG))

                activations_min_params = activations_re.getElementsByTagName(CONFIG_ACTIVATIONS_MIN_TAG)
                activations_min_params = activations_min_params[0] if activations_min_params != [] else None
                for param_name in activations_min_params_tags:
                    independent_params.append(
                        CompressionParameters.get_element_by_tag(activations_min_params, param_name))

                activations_max_params = activations_re.getElementsByTagName(CONFIG_ACTIVATIONS_MAX_TAG)
                activations_max_params = activations_max_params[0] if activations_max_params != [] else None
                for param_name in activations_max_params_tags:
                    independent_params.append(
                        CompressionParameters.get_element_by_tag(activations_max_params, param_name))

            else:   # activations_re == []
                independent_params.append(None)  # CONFIG_ACTIVATIONS_PRESET_TAG
                for _ in activations_min_params_tags + activations_max_params_tags:
                    independent_params.append(None)

        else:   # activations_params == []
            for _ in activations_params_tags:
                independent_params.append(None)
            independent_params.append(None)  # CONFIG_ACTIVATIONS_PRESET_TAG
            for _ in activations_min_params_tags + activations_max_params_tags:
                independent_params.append(None)

        return independent_params

    def create_dom(self, file, params, parent_node=None):
        if parent_node is not None:
            DOM_COMPRESSION_TAG = parent_node
        else:
            file.createElement(CONFIG_COMPRESSION_TAG)
        target_device = params[0]
        if target_device is not None and target_device != '':
            self.create_dom_node(file, DOM_COMPRESSION_TAG, CONFIG_TARGET_DEVICE_TAG, target_device)
        DOM_ALGORITHMS_TAG = self.create_dom_node(file, DOM_COMPRESSION_TAG, CONFIG_ALGORITHMS_TAG)
        self.create_dom_node(file, DOM_ALGORITHMS_TAG, CONFIG_ALGORITHM_NAME_TAG, params[1])
        DOM_PARAMS_TAG = self.create_dom_node(file, DOM_ALGORITHMS_TAG, CONFIG_COMPRESSION_PARAMS_TAG)
        self.__create_dependent_params_dom(file, DOM_PARAMS_TAG)
        self.__create_independent_params_dom(file, params, DOM_PARAMS_TAG)
        return DOM_COMPRESSION_TAG

    def __create_dependent_params_dom(self, file, parent_node=None):
        self.__dependent_params.create_dom(file, parent_node)

    def __create_independent_params_dom(self, file, params, parent_node=None):
        if parent_node is not None:
            DOM_PARAMS_TAG = parent_node
        else:
            file.createElement(CONFIG_COMPRESSION_PARAMS_TAG)

        if params[2] is not None and params[2] != '':
            self.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_PRESET_TAG, params[2])
        if params[3] is not None and params[3] != '':
            self.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_STAT_SUBSET_SIZE_TAG, params[3])

        if any(p is not None and p != '' for p in params[4:11]):
            DOM_WEIGHTS_TAG = self.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_WEIGHTS_TAG)

            self.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_BITS_TAG, params[4])
            self.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_MODE_TAG, params[5])
            self.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_GRANULARITY_TAG, params[6])
            self.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_LEVEL_LOW_TAG, params[7])
            self.create_dom_node(file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_LEVEL_HIGH_TAG, params[8])

            if any(p is not None and p != '' for p in params[9:11]):
                DOM_WEIGHTS_RE_TAG = self.create_dom_node(
                    file, DOM_WEIGHTS_TAG, CONFIG_WEIGHTS_RANGE_ESTIMATOR_TAG)
                DOM_WEIGHTS_MAX_TAG = self.create_dom_node(file, DOM_WEIGHTS_RE_TAG, CONFIG_WEIGHTS_MAX_TAG)
                self.create_dom_node(file, DOM_WEIGHTS_MAX_TAG, CONFIG_WEIGHTS_MAX_TYPE_TAG, params[9])
                self.create_dom_node(file, DOM_WEIGHTS_MAX_TAG, CONFIG_WEIGHTS_MAX_OUTLIER_PROB_TAG, params[10])

        if any(p is not None and p != '' for p in params[11:23]):
            DOM_ACTIVATIONS_TAG = self.create_dom_node(file, DOM_PARAMS_TAG, CONFIG_ACTIVATIONS_TAG)
            self.create_dom_node(file, DOM_ACTIVATIONS_TAG, CONFIG_ACTIVATIONS_BITS_TAG, params[11])
            self.create_dom_node(file, DOM_ACTIVATIONS_TAG, CONFIG_ACTIVATIONS_MODE_TAG, params[12])
            self.create_dom_node(file, DOM_ACTIVATIONS_TAG, CONFIG_ACTIVATIONS_GRANULARITY_TAG, params[13])

            if any(p is not None and p != '' for p in params[14:23]):
                DOM_ACTIVATIONS_RE_TAG = self.create_dom_node(
                    file, DOM_ACTIVATIONS_TAG, CONFIG_ACTIVATIONS_RANGE_ESTIMATOR_TAG)
                self.create_dom_node(file, DOM_ACTIVATIONS_RE_TAG, CONFIG_ACTIVATIONS_PRESET_TAG, params[14])

                if any(p is not None and p != '' for p in params[15:19]):
                    DOM_ACTIVATIONS_MIN_TAG = self.create_dom_node(
                        file, DOM_ACTIVATIONS_RE_TAG, CONFIG_ACTIVATIONS_MIN_TAG)
                    self.create_dom_node(
                        file, DOM_ACTIVATIONS_MIN_TAG, CONFIG_ACTIVATIONS_MIN_CLIPPING_VALUE_TAG, params[15])
                    self.create_dom_node(
                        file, DOM_ACTIVATIONS_MIN_TAG, CONFIG_ACTIVATIONS_MIN_AGGREGATOR_TAG, params[16])
                    self.create_dom_node(
                        file, DOM_ACTIVATIONS_MIN_TAG, CONFIG_ACTIVATIONS_MIN_TYPE_TAG, params[17])
                    self.create_dom_node(
                        file, DOM_ACTIVATIONS_MIN_TAG, CONFIG_ACTIVATIONS_MIN_OUTLIER_PROB_TAG, params[18])

                if any(p is not None and p != '' for p in params[19:23]):
                    DOM_ACTIVATIONS_MAX_TAG = self.create_dom_node(
                        file, DOM_ACTIVATIONS_RE_TAG, CONFIG_ACTIVATIONS_MAX_TAG)
                    self.create_dom_node(
                        file, DOM_ACTIVATIONS_MAX_TAG, CONFIG_ACTIVATIONS_MAX_CLIPPING_VALUE_TAG, params[19])
                    self.create_dom_node(
                        file, DOM_ACTIVATIONS_MAX_TAG, CONFIG_ACTIVATIONS_MAX_AGGREGATOR_TAG, params[20])
                    self.create_dom_node(
                        file, DOM_ACTIVATIONS_MAX_TAG, CONFIG_ACTIVATIONS_MAX_TYPE_TAG, params[21])
                    self.create_dom_node(
                        file, DOM_ACTIVATIONS_MAX_TAG, CONFIG_ACTIVATIONS_MAX_OUTLIER_PROB_TAG, params[22])

        return DOM_PARAMS_TAG

    @staticmethod
    def get_element_by_tag(dom, tag):
        if dom is None:
            return None
        nodes = dom.getElementsByTagName(tag)
        return nodes[0].firstChild.data if len(nodes) != 0 else None

    @staticmethod
    def create_dom_node(file, parent, child_name, text=None):
        child = file.createElement(child_name)
        if (text is not None) and (text != ''):
            child.appendChild(file.createTextNode(text))
        parent.appendChild(child)
        return child


class DependentParameters(metaclass=abc.ABCMeta):
    def __init__(self):
        self.parameters = {}

    @staticmethod
    def get_parameters(quantization_method, args):
        if quantization_method == 'DefaultQuantization':
            return DefaultQuantizationParameters(args)
        elif quantization_method == 'AccuracyAwareQuantization':
            return AccuracyAwareQuantizationParameters(args)
        else:
            raise ValueError('Unknown quantization method: {0} !'.format(quantization_method))

    def get_parameters_dict(self):
        return self.parameters

    def __check_subtree(self, param_tree_node):
        params = []
        if not isinstance(param_tree_node, dict):
            params.append(param_tree_node)
        else:
            for key in param_tree_node.keys():
                params.extend(self.__check_subtree(param_tree_node[key]))
        return params

    def get_parameters_list(self):
        params_list = []
        for key in self.parameters.keys():
            params_list.extend(self.__check_subtree(self.parameters[key]))
        return params_list

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
        self.parameters = {}
        for i, param_name in enumerate(HEADER_DQ_PARAMS_TAGS):
            self.parameters[param_name] = params[i]

    @staticmethod
    def _parse_params(dom):
        params = []
        for param_name in HEADER_DQ_PARAMS_TAGS:
            param_node = dom.getElementsByTagName(param_name)
            params.append(param_node[0].firstChild.data if param_node else '')
        return DefaultQuantizationParameters(params)

    def create_dom(self, file, parent_node=None):
        if parent_node is not None:
            DOM_COMPRESSION_PARAMS_TAG = parent_node
        else:
            file.createElement(CONFIG_COMPRESSION_PARAMS_TAG)
        for key in self.parameters:
            if self.parameters[key] != '' and self.parameters[key] is not None:
                CompressionParameters.create_dom_node(file, DOM_COMPRESSION_PARAMS_TAG, key, self.parameters[key])
        return DOM_COMPRESSION_PARAMS_TAG


class AccuracyAwareQuantizationParameters(DependentParameters):
    def __init__(self, params):
        self.parameters = {}
        for i, param_name in enumerate(HEADER_AAQ_PARAMS_TAGS):
            self.parameters[param_name] = params[i]

    @staticmethod
    def _parse_params(dom):
        params = []
        for param_name in HEADER_AAQ_PARAMS_TAGS:
            param_node = dom.getElementsByTagName(param_name)
            params.append(param_node[0].firstChild.data if param_node else '')
        return AccuracyAwareQuantizationParameters(params)

    def create_dom(self, file, parent_node=None):
        if parent_node is not None:
            DOM_COMPRESSION_PARAMS_TAG = parent_node
        else:
            file.createElement(CONFIG_COMPRESSION_PARAMS_TAG)
        for key in self.parameters:
            if self.parameters[key] != '' and self.parameters[key] is not None:
                CompressionParameters.create_dom_node(file, DOM_COMPRESSION_PARAMS_TAG, key, self.parameters[key])
        return DOM_COMPRESSION_PARAMS_TAG
