import abc
from model.models.model import Model  # pylint: disable=E0401
from model.data.dataset import Dataset  # pylint: disable=E0401
# pylint: disable-next=E0401
from tags import CONFIG_TEST_TAG, CONFIG_MODEL_TAG, CONFIG_DATASET_TAG, CONFIG_FRAMEWORK_INDEPENDENT_TAG, \
    CONFIG_FRAMEWORK_TAG, CONFIG_BATCH_SIZE_TAG, CONFIG_DEVICE_TAG, CONFIG_ITERATION_COUNT_TAG, \
    CONFIG_TEST_TIME_LIMIT_TAG, CONFIG_FRAMEWORK_DEPENDENT_TAG, INDEPENDENT_PARAMETER_COUNT
# pylint: disable-next=E0401
from tags import OPENVINO_DLDT_PARAMETER_COUNT, CAFFE_PARAMETER_COUNT, TENSORFLOW_PARAMETER_COUNT, CONFIG_MODE_TAG, \
    CONFIG_EXTENSION_TAG, CONFIG_ASYNC_REQ_COUNT_TAG, CONFIG_THREAD_COUNT_TAG, CONFIG_STREAM_COUNT_TAG, \
    CONFIG_CHANNEL_SWAP_TAG, CONFIG_MEAN_TAG, CONFIG_INPUT_SCALE_TAG, CONFIG_INPUT_SHAPE_TAG, CONFIG_INPUT_NAME_TAG, \
    CONFIG_OUTPUT_NAMES_TAG, CONFIG_KMP_AFFINITY_TAG, CONFIG_INTER_OP_THREADS_TAG, \
    CONFIG_INTRA_OP_THREADS_TAG


class Test:
    def __init__(self, model, dataset, framework, batch_size, device, iter_count, test_time_limit, *args):
        self.parameters = {
            CONFIG_MODEL_TAG: Model(*model.split(';')) if isinstance(model, str) else model,
            CONFIG_DATASET_TAG: Dataset(*dataset.split(';')) if isinstance(dataset, str) else dataset,
            CONFIG_FRAMEWORK_TAG: framework,
            CONFIG_BATCH_SIZE_TAG: batch_size,
            CONFIG_DEVICE_TAG: device,
            CONFIG_ITERATION_COUNT_TAG: iter_count,
            CONFIG_TEST_TIME_LIMIT_TAG: test_time_limit,
            CONFIG_FRAMEWORK_DEPENDENT_TAG: args[0] if isinstance(args[0], DependentParameters) else
            DependentParameters.get_parameters(framework, args)
        }

    def get_values_list(self):
        return list(self.parameters.values())

    def get_values_dict(self):
        return self.parameters

    def grouping_dependent_values_check(self, other):
        self_values = self.get_values_list()
        other_values = other.get_values_list()
        if self_values[:-1] != other_values[:-1]:
            return -1
        return self.parameters[CONFIG_FRAMEWORK_DEPENDENT_TAG].get_grouping_parameter(other_values[-1])

    def grouping_independent_values_check(self, other):
        if self.parameters[CONFIG_FRAMEWORK_DEPENDENT_TAG] != other.parameters[CONFIG_FRAMEWORK_DEPENDENT_TAG]:
            return -1
        count = 0
        self_values = self.get_values_list()
        other_values = other.get_values_list()
        for i in range(INDEPENDENT_PARAMETER_COUNT):
            if self_values[i] != other_values[i]:
                parameter = i
                count += 1
        if count != 1 or parameter < 3:
            return -1
        else:
            return parameter

    @staticmethod
    def grouping_by_independent(self, other, parameter):
        self_parameters = self.get_values_list()
        value = other.get_values_list()[parameter]
        self_parameters[parameter] = ';'.join([self_parameters[parameter], value])
        return Test(*self_parameters)

    @staticmethod
    def grouping_by_dependent(self, other, parameter):
        self_parameters = self.get_values_list()
        self_dependent_parameters = self_parameters[-1]
        other_dependent_parameters = other.get_values_list()[-1]
        new_dependent_parameters = DependentParameters.grouping(self_dependent_parameters, other_dependent_parameters,
                                                                parameter)
        return Test(*self_parameters[:-1], new_dependent_parameters)

    @staticmethod
    def parse(dom):
        model = Model.parse(dom)[0]
        dataset = Dataset.parse(dom)

        parsed_framework_independent = dom.getElementsByTagName(CONFIG_FRAMEWORK_INDEPENDENT_TAG)[0]
        framework = parsed_framework_independent.getElementsByTagName(CONFIG_FRAMEWORK_TAG)[0].firstChild.data
        batch_size = parsed_framework_independent.getElementsByTagName(CONFIG_BATCH_SIZE_TAG)[0].firstChild.data
        device = parsed_framework_independent.getElementsByTagName(CONFIG_DEVICE_TAG)[0].firstChild.data
        iter_count = parsed_framework_independent.getElementsByTagName(CONFIG_ITERATION_COUNT_TAG)[0].firstChild.data
        test_time_limit = parsed_framework_independent.getElementsByTagName(CONFIG_TEST_TIME_LIMIT_TAG)[
            0].firstChild.data

        framework_parameters = DependentParameters.parse(framework, dom)

        return Test(model, dataset, framework, batch_size, device, iter_count, test_time_limit, framework_parameters)

    def create_dom(self, file):
        DOM_TEST_TAG = file.createElement(CONFIG_TEST_TAG)
        DOM_MODEL_TAG = self.parameters[CONFIG_MODEL_TAG].create_dom(file)
        DOM_DATASET_TAG = self.parameters[CONFIG_DATASET_TAG].create_dom(file)
        DOM_FRAMEWORK_INDEPENDENT_TAG = self.__create_dom_framework_independent(file)
        DOM_FRAMEWORK_DEPENDENT_TAG = self.parameters[CONFIG_FRAMEWORK_DEPENDENT_TAG].create_dom(file)

        DOM_TEST_TAG.appendChild(DOM_MODEL_TAG)
        DOM_TEST_TAG.appendChild(DOM_DATASET_TAG)
        DOM_TEST_TAG.appendChild(DOM_FRAMEWORK_INDEPENDENT_TAG)
        DOM_TEST_TAG.appendChild(DOM_FRAMEWORK_DEPENDENT_TAG)

        return DOM_TEST_TAG

    def test_splitting(self):
        new_tests = []
        model = self.parameters[CONFIG_MODEL_TAG]
        dataset = self.parameters[CONFIG_DATASET_TAG]
        framework = self.parameters[CONFIG_FRAMEWORK_TAG]
        batch_sizes = self.parameters[CONFIG_BATCH_SIZE_TAG].split(';')
        devices = self.parameters[CONFIG_DEVICE_TAG].split(';')
        iteration_counts = self.parameters[CONFIG_ITERATION_COUNT_TAG].split(';')
        test_time_limits = self.parameters[CONFIG_TEST_TIME_LIMIT_TAG].split(';')
        dependent_parameters = self.parameters[CONFIG_FRAMEWORK_DEPENDENT_TAG].test_splitting()

        for batch_size in batch_sizes:
            for device in devices:
                for iteration_count in iteration_counts:
                    for test_time_limit in test_time_limits:
                        for dependent_parameter in dependent_parameters:
                            new_tests.append(Test(model, dataset, framework, batch_size, device, iteration_count,
                                                  test_time_limit, dependent_parameter))
        return new_tests

    def __create_dom_framework_independent(self, file):
        DOM_FRAMEWORK_INDEPENDENT_TAG = file.createElement(CONFIG_FRAMEWORK_INDEPENDENT_TAG)
        DOM_INFERENCE_FRAMEWORK_TAG = file.createElement(CONFIG_FRAMEWORK_TAG)
        DOM_BATCH_SIZE_TAG = file.createElement(CONFIG_BATCH_SIZE_TAG)
        DOM_DEVICE_TAG = file.createElement(CONFIG_DEVICE_TAG)
        DOM_ITERATION_COUNT_TAG = file.createElement(CONFIG_ITERATION_COUNT_TAG)
        DOM_TEST_TIME_LIMIT_TAG = file.createElement(CONFIG_TEST_TIME_LIMIT_TAG)

        DOM_INFERENCE_FRAMEWORK_TAG.appendChild(file.createTextNode(self.parameters[CONFIG_FRAMEWORK_TAG]))
        DOM_BATCH_SIZE_TAG.appendChild(file.createTextNode(self.parameters[CONFIG_BATCH_SIZE_TAG]))
        DOM_DEVICE_TAG.appendChild(file.createTextNode(self.parameters[CONFIG_DEVICE_TAG]))
        DOM_ITERATION_COUNT_TAG.appendChild(file.createTextNode(self.parameters[CONFIG_ITERATION_COUNT_TAG]))
        DOM_TEST_TIME_LIMIT_TAG.appendChild(file.createTextNode(self.parameters[CONFIG_TEST_TIME_LIMIT_TAG]))
        DOM_FRAMEWORK_INDEPENDENT_TAG.appendChild(DOM_INFERENCE_FRAMEWORK_TAG)
        DOM_FRAMEWORK_INDEPENDENT_TAG.appendChild(DOM_BATCH_SIZE_TAG)
        DOM_FRAMEWORK_INDEPENDENT_TAG.appendChild(DOM_DEVICE_TAG)
        DOM_FRAMEWORK_INDEPENDENT_TAG.appendChild(DOM_ITERATION_COUNT_TAG)
        DOM_FRAMEWORK_INDEPENDENT_TAG.appendChild(DOM_TEST_TIME_LIMIT_TAG)

        return DOM_FRAMEWORK_INDEPENDENT_TAG


class DependentParameters(metaclass=abc.ABCMeta):
    def __init__(self):
        self.framework = None
        self.parameter_count = -1
        self.parameters = {}

    @staticmethod
    def get_parameters(framework, args):
        if framework == 'OpenVINO DLDT':
            return OpenVINOParameters(*args)
        elif framework == 'Caffe':
            return CaffeParameters(*args)
        elif framework == 'TensorFlow':
            return TensorFlowParameters(*args)
        else:
            raise ValueError('Unknown framework: {0} !'.format(framework))

    def __eq__(self, other):
        if self.framework != other.framework:
            return False
        self_parameters = self.get_parameter_list()
        other_parameters = other.get_parameter_list()
        for i in range(self.parameter_count):
            if self_parameters[i] != other_parameters[i]:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def get_parameter_list(self):
        return list(self.parameters.values())

    def get_parameter_dict(self):
        return self.parameters

    @staticmethod
    def parse(framework, dom):
        framework_dom = dom.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]
        if framework == 'OpenVINO DLDT':
            return OpenVINOParameters._parse_framework(framework_dom)
        elif framework == 'Caffe':
            return CaffeParameters._parse_framework(framework_dom)
        elif framework == 'TensorFlow':
            return TensorFlowParameters._parse_framework(framework_dom)

    @abc.abstractmethod
    def _parse_framework(self):
        pass

    def create_dom(self, file):
        DOM_FRAMEWORK_DEPENDENT_TAG = file.createElement(CONFIG_FRAMEWORK_DEPENDENT_TAG)

        for key in self.parameters:
            DOM_PARAMETER = file.createElement(key)
            DOM_PARAMETER.appendChild(file.createTextNode(self.parameters[key]))
            DOM_FRAMEWORK_DEPENDENT_TAG.appendChild(DOM_PARAMETER)

        return DOM_FRAMEWORK_DEPENDENT_TAG

    def get_grouping_parameter(self, other):
        if self.framework != other.framework:
            return -1
        count = 0
        self_parameters = self.get_parameter_list()
        other_parameters = other.get_parameter_list()
        for i in range(self.parameter_count):
            if self_parameters[i] != other_parameters[i]:
                parameter = i
                count += 1
        if count != 1:
            return -1
        else:
            return parameter

    @staticmethod
    def grouping(self, other, parameter):
        self_parameters = self.get_parameter_list()
        value = other.get_parameter_list()[parameter]
        self_parameters[parameter] = ';'.join([self_parameters[parameter], value])
        return self.get_parameters(self.framework, self_parameters)

    @abc.abstractmethod
    def test_splitting(self):
        pass


class OpenVINOParameters(DependentParameters):
    def __init__(self, mode, extension, async_req_count, thread_count, stream_count):
        self.framework = 'OpenVINO DLDT'
        self.parameter_count = OPENVINO_DLDT_PARAMETER_COUNT
        self.parameters = {
            CONFIG_MODE_TAG: mode,
            CONFIG_EXTENSION_TAG: extension,
            CONFIG_ASYNC_REQ_COUNT_TAG: async_req_count,
            CONFIG_THREAD_COUNT_TAG: thread_count,
            CONFIG_STREAM_COUNT_TAG: stream_count

        }

    @staticmethod
    def _parse_framework(dom):
        extension = ''
        asynq_req_count = ''
        thread_count = ''
        stream_count = ''

        mode_node = dom.getElementsByTagName(CONFIG_MODE_TAG)[0].firstChild
        if not mode_node:
            raise ValueError('Tag <Mode> is mandatory!')
        mode = mode_node.data
        extension_node = dom.getElementsByTagName(CONFIG_EXTENSION_TAG)[0].firstChild
        if extension_node:
            extension = extension_node.data
        asynq_req_count_node = dom.getElementsByTagName(CONFIG_ASYNC_REQ_COUNT_TAG)[0].firstChild
        if asynq_req_count_node:
            asynq_req_count = asynq_req_count_node.data
        thread_count_node = dom.getElementsByTagName(CONFIG_THREAD_COUNT_TAG)[0].firstChild
        if thread_count_node:
            thread_count = thread_count_node.data
        stream_count_node = dom.getElementsByTagName(CONFIG_STREAM_COUNT_TAG)[0].firstChild
        if stream_count_node:
            stream_count = stream_count_node.data

        return OpenVINOParameters(mode, extension, asynq_req_count, thread_count, stream_count)

    def test_splitting(self):
        modes = self.parameters[CONFIG_MODE_TAG].split(';')
        extensions = self.parameters[CONFIG_EXTENSION_TAG].split(';')
        async_req_counts = self.parameters[CONFIG_ASYNC_REQ_COUNT_TAG].split(';')
        thread_counts = self.parameters[CONFIG_THREAD_COUNT_TAG].split(';')
        stream_counts = self.parameters[CONFIG_STREAM_COUNT_TAG].split(';')

        new_parameters = []
        for mode in modes:
            for extension in extensions:
                for async_req_count in async_req_counts:
                    for thread_count in thread_counts:
                        for stream_count in stream_counts:
                            new_parameters.append(OpenVINOParameters(mode, extension, async_req_count, thread_count,
                                                                     stream_count))
        return new_parameters


class CaffeParameters(DependentParameters):
    def __init__(self, channel_swap, mean, input_scale, thread_count, kmp_affinity):
        self.framework = 'Caffe'
        self.parameter_count = CAFFE_PARAMETER_COUNT
        self.parameters = {
            CONFIG_CHANNEL_SWAP_TAG: channel_swap,
            CONFIG_MEAN_TAG: mean,
            CONFIG_INPUT_SCALE_TAG: input_scale,
            CONFIG_THREAD_COUNT_TAG: thread_count,
            CONFIG_KMP_AFFINITY_TAG: kmp_affinity
        }

    @staticmethod
    def _parse_framework(dom):
        channel_swap = ''
        mean = ''
        input_scale = ''
        thread_count = ''
        kmp_affinity = ''

        channel_swap_node = dom.getElementsByTagName(CONFIG_CHANNEL_SWAP_TAG)[0].firstChild
        if channel_swap_node:
            channel_swap = channel_swap_node.data
        mean_node = dom.getElementsByTagName(CONFIG_MEAN_TAG)[0].firstChild
        if mean_node:
            mean = mean_node.data
        input_scale_node = dom.getElementsByTagName(CONFIG_INPUT_SCALE_TAG)[0].firstChild
        if input_scale_node:
            input_scale = input_scale_node.data
        thread_count_node = dom.getElementsByTagName(CONFIG_THREAD_COUNT_TAG)[0].firstChild
        if thread_count_node:
            thread_count = thread_count_node.data
        kmp_affinity_node = dom.getElementsByTagName(CONFIG_KMP_AFFINITY_TAG)[0].firstChild
        if kmp_affinity_node:
            kmp_affinity = kmp_affinity_node.data

        return CaffeParameters(channel_swap, mean, input_scale, thread_count, kmp_affinity)

    def test_splitting(self):
        channel_swaps = self.parameters[CONFIG_CHANNEL_SWAP_TAG].split(';')
        means = self.parameters[CONFIG_MEAN_TAG].split(';')
        input_scales = self.parameters[CONFIG_INPUT_SCALE_TAG].split(';')
        thread_counts = self.parameters[CONFIG_THREAD_COUNT_TAG].split(';')
        kmp_affinities = self.parameters[CONFIG_KMP_AFFINITY_TAG].split(';')

        new_parameters = []
        for channel_swap in channel_swaps:
            for mean in means:
                for input_scale in input_scales:
                    for thread_count in thread_counts:
                        for kmp_affinity in kmp_affinities:
                            new_parameters.append(CaffeParameters(channel_swap, mean, input_scale,
                                                                  thread_count, kmp_affinity))
        return new_parameters


class TensorFlowParameters(DependentParameters):
    def __init__(self, channel_swap, mean, input_scale, input_shape, input_name, output_names, thread_count,
                 inter_op_threads, intra_op_threads, kmp_affinity):
        self.framework = 'TensorFlow'
        self.parameter_count = TENSORFLOW_PARAMETER_COUNT
        self.parameters = {
            CONFIG_CHANNEL_SWAP_TAG: channel_swap,
            CONFIG_MEAN_TAG: mean,
            CONFIG_INPUT_SCALE_TAG: input_scale,
            CONFIG_INPUT_SHAPE_TAG: input_shape,
            CONFIG_INPUT_NAME_TAG: input_name,
            CONFIG_OUTPUT_NAMES_TAG: output_names,
            CONFIG_THREAD_COUNT_TAG: thread_count,
            CONFIG_INTER_OP_THREADS_TAG: inter_op_threads,
            CONFIG_INTRA_OP_THREADS_TAG: intra_op_threads,
            CONFIG_KMP_AFFINITY_TAG: kmp_affinity
        }

    @staticmethod
    def _parse_framework(dom):
        channel_swap = ''
        mean = ''
        input_scale = ''
        input_shape = ''
        input_name = ''
        output_names = ''
        thread_count = ''
        inter_op_threads = ''
        intra_op_threads = ''
        kmp_affinity = ''

        channel_swap_node = dom.getElementsByTagName(CONFIG_CHANNEL_SWAP_TAG)[0].firstChild
        if channel_swap_node:
            channel_swap = channel_swap_node.data
        mean_node = dom.getElementsByTagName(CONFIG_MEAN_TAG)[0].firstChild
        if mean_node:
            mean = mean_node.data
        input_scale_node = dom.getElementsByTagName(CONFIG_INPUT_SCALE_TAG)[0].firstChild
        if input_scale_node:
            input_scale = input_scale_node.data
        input_shape_node = dom.getElementsByTagName(CONFIG_INPUT_SHAPE_TAG)[0].firstChild
        if input_shape_node:
            input_shape = input_shape_node.data
        input_name_node = dom.getElementsByTagName(CONFIG_INPUT_NAME_TAG)[0].firstChild
        if input_name_node:
            input_name = input_name_node.data
        output_names_node = dom.getElementsByTagName(CONFIG_OUTPUT_NAMES_TAG)[0].firstChild
        if output_names_node:
            output_names = output_names_node.data
        thread_count_node = dom.getElementsByTagName(CONFIG_THREAD_COUNT_TAG)[0].firstChild
        if thread_count_node:
            thread_count = thread_count_node.data
        inter_op_threads_node = dom.getElementsByTagName(CONFIG_INTER_OP_THREADS_TAG)[0].firstChild
        if inter_op_threads_node:
            inter_op_threads = inter_op_threads_node.data
        intra_op_threads_node = dom.getElementsByTagName(CONFIG_INTRA_OP_THREADS_TAG)[0].firstChild
        if intra_op_threads_node:
            intra_op_threads = intra_op_threads_node.data
        kmp_affinity_node = dom.getElementsByTagName(CONFIG_KMP_AFFINITY_TAG)[0].firstChild
        if kmp_affinity_node:
            kmp_affinity = kmp_affinity_node.data

        return TensorFlowParameters(channel_swap, mean, input_scale, input_shape, input_name, output_names,
                                    thread_count, inter_op_threads, intra_op_threads, kmp_affinity)

    def test_splitting(self):
        channel_swaps = self.parameters[CONFIG_CHANNEL_SWAP_TAG].split(';')
        means = self.parameters[CONFIG_MEAN_TAG].split(';')
        input_scales = self.parameters[CONFIG_INPUT_SCALE_TAG].split(';')
        input_shapes = self.parameters[CONFIG_INPUT_SHAPE_TAG].split(';')
        input_names = self.parameters[CONFIG_INPUT_NAME_TAG].split(';')
        output_names = self.parameters[CONFIG_OUTPUT_NAMES_TAG].split(';')
        thread_counts = self.parameters[CONFIG_THREAD_COUNT_TAG].split(';')
        inter_op_threads = self.parameters[CONFIG_INTER_OP_THREADS_TAG].split(';')
        intra_op_threads = self.parameters[CONFIG_INTRA_OP_THREADS_TAG].split(';')
        kmp_affinities = self.parameters[CONFIG_KMP_AFFINITY_TAG].split(';')

        new_parameters = []
        for channel_swap in channel_swaps:
            for mean in means:
                for input_scale in input_scales:
                    for input_shape in input_shapes:
                        for input_name in input_names:
                            for output_name in output_names:
                                for thread_count in thread_counts:
                                    for inter_op_thread in inter_op_threads:
                                        for intra_op_thread in intra_op_threads:
                                            for kmp_affinity in kmp_affinities:
                                                new_parameters.append(TensorFlowParameters(channel_swap, mean,
                                                                                           input_scale, input_shape,
                                                                                           input_name, output_name,
                                                                                           thread_count,
                                                                                           inter_op_thread,
                                                                                           intra_op_thread,
                                                                                           kmp_affinity))
        return new_parameters
