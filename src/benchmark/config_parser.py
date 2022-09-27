import abc
import os
from collections import OrderedDict
from xml.dom import minidom


class Parser:
    def get_tests_list(self, config):
        CONFIG_ROOT_TAG = 'Test'
        return minidom.parse(config).getElementsByTagName(CONFIG_ROOT_TAG)

    def parse_model(self, curr_test):
        CONFIG_MODEL_TAG = 'Model'
        CONFIG_MODEL_TASK_TAG = 'Task'
        CONFIG_MODEL_NAME_TAG = 'Name'
        CONFIG_MODEL_PRECISION_TAG = 'Precision'
        CONFIG_MODEL_SOURCE_FRAMEWORK_TAG = 'SourceFramework'
        CONFIG_MODEL_MODEL_PATH_TAG = 'ModelPath'
        CONFIG_MODEL_WEIGHTS_PATH_TAG = 'WeightsPath'

        model_tag = curr_test.getElementsByTagName(CONFIG_MODEL_TAG)[0]

        return Model(
            task=model_tag.getElementsByTagName(CONFIG_MODEL_TASK_TAG)[0].firstChild.data,
            name=model_tag.getElementsByTagName(CONFIG_MODEL_NAME_TAG)[0].firstChild.data,
            precision=model_tag.getElementsByTagName(CONFIG_MODEL_PRECISION_TAG)[0].firstChild.data,
            source_framework=model_tag.getElementsByTagName(CONFIG_MODEL_SOURCE_FRAMEWORK_TAG)[0].firstChild.data,
            model_path=model_tag.getElementsByTagName(CONFIG_MODEL_MODEL_PATH_TAG)[0].firstChild.data,
            weights_path=model_tag.getElementsByTagName(CONFIG_MODEL_WEIGHTS_PATH_TAG)[0].firstChild.data
        )

    def parse_dataset(self, curr_test):
        CONFIG_DATASET_TAG = 'Dataset'
        CONFIG_DATASET_NAME_TAG = 'Name'
        CONFIG_DATASET_PATH_TAG = 'Path'

        dataset_tag = curr_test.getElementsByTagName(CONFIG_DATASET_TAG)[0]

        return Dataset(
            name=dataset_tag.getElementsByTagName(CONFIG_DATASET_NAME_TAG)[0].firstChild.data,
            path=dataset_tag.getElementsByTagName(CONFIG_DATASET_PATH_TAG)[0].firstChild.data
        )

    def parse_independent_parameters(self, curr_test):
        CONFIG_FRAMEWORK_INDEPENDENT_TAG = 'FrameworkIndependent'
        CONFIG_FRAMEWORK_INDEPENDENT_INFERENCE_FRAMEWORK_TAG = 'InferenceFramework'
        CONFIG_FRAMEWORK_INDEPENDENT_BATCH_SIZE_TAG = 'BatchSize'
        CONFIG_FRAMEWORK_INDEPENDENT_DEVICE_TAG = 'Device'
        CONFIG_FRAMEWORK_INDEPENDENT_ITERATION_COUNT_TAG = 'IterationCount'
        CONFIG_FRAMEWORK_INDEPENDENT_TEST_TIME_LIMIT_TAG = 'TestTimeLimit'

        indep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_INDEPENDENT_TAG)[0]

        return FrameworkIndependentParameters(
            inference_framework=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_INFERENCE_FRAMEWORK_TAG)[0].firstChild.data,
            batch_size=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_BATCH_SIZE_TAG)[0].firstChild.data,
            device=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_DEVICE_TAG)[0].firstChild.data,
            iterarion_count=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_ITERATION_COUNT_TAG)[0].firstChild.data,
            test_time_limit=indep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_INDEPENDENT_TEST_TIME_LIMIT_TAG)[0].firstChild.data
        )

    def parse_dependent_parameters(self, curr_test, framework):
        dep_parser = DependentParametersParser.get_parser(framework)
        return dep_parser.parse_parameters(curr_test)


class DependentParametersParser(metaclass=abc.ABCMeta):
    @staticmethod
    def get_parser(framework):
        if framework == 'OpenVINO DLDT':
            return OpenVINOParametersParser()
        elif framework == 'Caffe':
            return IntelCaffeParametersParser()
        elif framework == 'TensorFlow':
            return TensorFlowParametersParser()
        else:
            raise ValueError(
                'Invalid framework name: only \'OpenVINO DLDT\', \'Caffe\' and \'TensorFlow\' are available')

    @abc.abstractmethod
    def parse_parameters(self, curr_test):
        pass


class OpenVINOParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_MODE_TAG = 'Mode'
        CONFIG_FRAMEWORK_DEPENDENT_EXTENSION_TAG = 'Extension'
        CONFIG_FRAMEWORK_DEPENDENT_ASYNC_REQUEST_COUNT_TAG = 'AsyncRequestCount'
        CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG = 'ThreadCount'
        CONFIG_FRAMEWORK_DEPENDENT_STREAM_COUNT_TAG = 'StreamCount'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _mode = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MODE_TAG)[0].firstChild
        _extension = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_EXTENSION_TAG)[0].firstChild
        _async_request_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_ASYNC_REQUEST_COUNT_TAG)[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG)[0].firstChild
        _stream_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_STREAM_COUNT_TAG)[0].firstChild

        return OpenVINOParameters(
            mode=_mode.data if _mode else None,
            extension=_extension.data if _extension else None,
            async_request_count=_async_request_count.data if _async_request_count else None,
            thread_count=_thread_count.data if _thread_count else None,
            stream_count=_stream_count.data if _stream_count else None
        )


class IntelCaffeParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_CHANNEL_SWAP_TAG = 'ChannelSwap'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG = 'InputScale'
        CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG = 'ThreadCount'
        CONFIG_FRAMEWORK_DEPENDENT_KMP_AFFINITY_TAG = 'KmpAffinity'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _channel_swap = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_CHANNEL_SWAP_TAG)[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        _input_scale = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG)[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG)[0].firstChild
        _kmp_affinity = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_KMP_AFFINITY_TAG)[0].firstChild

        return IntelCaffeParameters(
            channel_swap=_channel_swap.data if _channel_swap else None,
            mean=_mean.data if _mean else None,
            input_scale=_input_scale.data if _input_scale else None,
            thread_count=_thread_count.data if _thread_count else None,
            kmp_affinity=_kmp_affinity.data if _kmp_affinity else None
        )


class TensorFlowParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_CHANNEL_SWAP_TAG = 'ChannelSwap'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG = 'InputScale'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SHAPE_TAG = 'InputShape'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_NAME_TAG = 'InputName'
        CONFIG_FRAMEWORK_DEPENDENT_OUTPUT_NAMES_TAG = 'OutputNames'
        CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG = 'ThreadCount'
        CONFIG_FRAMEWORK_DEPENDENT_INTER_OP_PARALLELISM_THREADS_TAG = 'InterOpParallelismThreads'
        CONFIG_FRAMEWORK_DEPENDENT_INTRA_OP_PARALLELISM_THREADS_TAG = 'IntraOpParallelismThreads'
        CONFIG_FRAMEWORK_DEPENDENT_KMP_AFFINITY_TAG = 'KmpAffinity'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _channel_swap = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_CHANNEL_SWAP_TAG)[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        _input_scale = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG)[0].firstChild
        _input_shape = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SHAPE_TAG)[0].firstChild
        _input_name = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_NAME_TAG)[0].firstChild
        _output_names = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_OUTPUT_NAMES_TAG)[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG)[0].firstChild
        _inter_op_parallelism_threads = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INTER_OP_PARALLELISM_THREADS_TAG)[0].firstChild
        _intra_op_parallelism_threads = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INTRA_OP_PARALLELISM_THREADS_TAG)[0].firstChild
        _kmp_affinity = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_KMP_AFFINITY_TAG)[0].firstChild

        return TensorFlowParameters(
            channel_swap=_channel_swap.data if _channel_swap else None,
            mean=_mean.data if _mean else None,
            input_scale=_input_scale.data if _input_scale else None,
            input_shape=_input_shape.data if _input_shape else None,
            input_name=_input_name.data if _input_name else None,
            output_names=_output_names.data if _output_names else None,
            thread_count=_thread_count.data if _thread_count else None,
            inter_op_parallelism_threads=_inter_op_parallelism_threads.data if _inter_op_parallelism_threads else None,
            intra_op_parallelism_threads=_intra_op_parallelism_threads.data if _intra_op_parallelism_threads else None,
            kmp_affinity=_kmp_affinity.data if _kmp_affinity else None
        )


class Model:
    @staticmethod
    def _parameter_not_is_none(parameter):
        return True if parameter is not None else False

    def __init__(self, task, name, model_path, weights_path, precision, source_framework):
        self.source_framework = None
        self.task = task
        self.name = None
        self.model = None
        self.weight = None
        self.precision = None
        if self._parameter_not_is_none(source_framework):
            self.source_framework = source_framework
        else:
            raise ValueError('Source framework is required parameter.')
        if self._parameter_not_is_none(name):
            self.name = name
        else:
            raise ValueError('Model name is required parameter.')
        if self._parameter_not_is_none(model_path):
            self.model = model_path
        else:
            raise ValueError('Path to model is required parameter.')
        if self._parameter_not_is_none(weights_path):
            self.weight = weights_path
        else:
            raise ValueError('Path to model weights is required parameter.')
        if self._parameter_not_is_none(precision):
            self.precision = precision
        else:
            raise ValueError('Precision is required parameter.')


class Dataset:
    @staticmethod
    def _parameter_not_is_none(parameter):
        return True if parameter is not None else False

    def __init__(self, name, path):
        self.name = None
        self.path = None
        if self._parameter_not_is_none(name):
            self.name = name
        else:
            raise ValueError('Dataset name is required parameter.')
        if self._parameter_not_is_none(path):
            self.path = path
        else:
            raise ValueError('Path to dataset is required parameter.')


class ParametersMethods:
    @staticmethod
    def _parameter_not_is_none(parameter):
        return True if parameter is not None else False

    @staticmethod
    def _int_value_is_correct(int_value):
        for i in range(len(int_value)):
            if (i < 0) or (9 < i):
                return False
        return True

    def _float_value_is_correct(self, float_value):
        for i in float_value.split('.'):
            if not self._int_value_is_correct(i):
                return False
        return True


class FrameworkIndependentParameters(ParametersMethods):
    @staticmethod
    def _device_is_correct(device):
        const_correct_devices = ['CPU', 'GPU', 'MYRIAD', 'FPGA']
        if device.upper() in const_correct_devices:
            return True
        return False

    def __init__(self, inference_framework, batch_size, device, iterarion_count, test_time_limit):
        self.inference_framework = None
        self.batch_size = None
        self.device = None
        self.iteration = None
        self.test_time_limit = None
        if self._parameter_not_is_none(inference_framework):
            self.inference_framework = inference_framework
        else:
            raise ValueError('Inference framework is required parameter.')
        if self._parameter_not_is_none(batch_size) and self._int_value_is_correct(batch_size):
            self.batch_size = int(batch_size)
        else:
            raise ValueError('Batch size is required parameter. '
                             'Batch size can only take values: integer greater than zero.')
        if self._device_is_correct(device):
            self.device = device.upper()
        else:
            raise ValueError('Device is required parameter. '
                             'Device can only take values: CPU, GPU, FPGA, MYRIAD.')
        if self._parameter_not_is_none(iterarion_count) and self._int_value_is_correct(iterarion_count):
            self.iteration = int(iterarion_count)
        else:
            raise ValueError('Iteration count is required parameter. '
                             'Iteration count can only take values: integer greater than zero.')
        if self._parameter_not_is_none(test_time_limit) and self._float_value_is_correct(test_time_limit):
            self.test_time_limit = float(test_time_limit)
        else:
            raise ValueError('Test time limit is required parameter. '
                             'Test time limit can only `take values: float greater than zero.')


class OpenVINOParameters(ParametersMethods):
    @staticmethod
    def _mode_is_correct(mode):
        const_correct_mode = ['sync', 'async']
        if mode.lower() in const_correct_mode:
            return True
        return False

    def _extension_path_is_correct(self, extension):
        if not self._parameter_not_is_none(extension) or os.path.exists(extension):
            return True
        return False

    def __init__(self, mode, extension, async_request_count, thread_count, stream_count):
        self.mode = None
        self.extension = None
        self.async_request = None
        self.nthreads = None
        self.nstreams = None

        if self._mode_is_correct(mode):
            self.mode = mode.title()
        else:
            raise ValueError('Mode is required parameter. \
                Mode can only take values: Sync, Async.')
        if self._extension_path_is_correct(extension):
            self.extension = extension
        else:
            raise ValueError('Wrong extension path for device. File not found.')
        if self.mode == 'Sync':
            if self._parameter_not_is_none(thread_count):
                if self._int_value_is_correct(thread_count):
                    self.nthreads = int(thread_count)
                else:
                    raise ValueError('Thread count can only take values: integer greater than zero.')
        if self.mode == 'Async':
            if self._parameter_not_is_none(async_request_count):
                if self._int_value_is_correct(async_request_count):
                    self.async_request = async_request_count
                else:
                    raise ValueError('Async requiest count can only take values: integer greater than zero.')
            if self._parameter_not_is_none(stream_count):
                if self._int_value_is_correct(stream_count):
                    self.nstreams = stream_count
                else:
                    raise ValueError('Stream count can only take values: integer greater than zero.')


class IntelCaffeParameters(ParametersMethods):
    @staticmethod
    def _channel_swap_is_correct(channel_swap):
        set_check = {'0', '1', '2'}
        set_in = set(channel_swap.split())
        return set_in == set_check

    def _mean_is_correct(self, mean):
        mean_check = mean.split()
        if len(mean_check) != 3:
            return False
        for i in mean_check:
            if not self._float_value_is_correct(i):
                return False
        return True

    def __init__(self, channel_swap, mean, input_scale, thread_count, kmp_affinity):
        self.channel_swap = None
        self.mean = None
        self.input_scale = None
        self.nthreads = None
        self.kmp_affinity = None

        if self._parameter_not_is_none(channel_swap):
            if self._channel_swap_is_correct(channel_swap):
                self.channel_swap = channel_swap
            else:
                raise ValueError('Channel swap can only take values: list of unique values 0, 1, 2.')
        if self._parameter_not_is_none(mean):
            if self._mean_is_correct(mean):
                self.mean = mean
            else:
                raise ValueError('Mean can only take values: list of 3 float elements.')
        if self._parameter_not_is_none(input_scale):
            if self._float_value_is_correct(input_scale):
                self.input_scale = input_scale
            else:
                raise ValueError('Input scale can only take values: float greater than zero.')
        if self._parameter_not_is_none(thread_count):
            if self._int_value_is_correct(thread_count):
                self.nthreads = thread_count
            else:
                raise ValueError('Threads count can only take integer value')
        if self._parameter_not_is_none(kmp_affinity):
            self.kmp_affinity = kmp_affinity


class TensorFlowParameters(ParametersMethods):
    @staticmethod
    def _channel_swap_is_correct(channel_swap):
        set_check = {'0', '1', '2'}
        set_in = set(channel_swap.split())
        return set_in == set_check

    def _mean_is_correct(self, mean):
        mean_check = mean.split()
        if len(mean_check) != 3:
            return False
        for i in mean_check:
            if not self._float_value_is_correct(i):
                return False
        return True

    def _input_shape_is_correct(self, input_shape):
        shape_check = input_shape.split()
        if len(shape_check) != 3:
            return False
        for i in shape_check:
            if not self._int_value_is_correct(i):
                return False
        return True

    def __init__(self, channel_swap, mean, input_scale, input_shape, input_name, output_names, thread_count,
                 inter_op_parallelism_threads, intra_op_parallelism_threads, kmp_affinity):
        self.channel_swap = None
        self.mean = None
        self.input_scale = None
        self.input_shape = None
        self.input_name = None
        self.output_names = None
        self.nthreads = None
        self.num_inter_threads = None
        self.num_intra_threads = None
        self.kmp_affinity = None

        if self._parameter_not_is_none(channel_swap):
            if self._channel_swap_is_correct(channel_swap):
                self.channel_swap = channel_swap
            else:
                raise ValueError('Channel swap can only take values: list of unique values 0, 1, 2.')
        if self._parameter_not_is_none(mean):
            if self._mean_is_correct(mean):
                self.mean = mean
            else:
                raise ValueError('Mean can only take values: list of 3 float elements.')
        if self._parameter_not_is_none(input_scale):
            if self._float_value_is_correct(input_scale):
                self.input_scale = input_scale
            else:
                raise ValueError('Input scale can only take values: float greater than zero.')
        if self._parameter_not_is_none(input_shape):
            if self._input_shape_is_correct(input_shape):
                self.input_shape = input_shape
            else:
                raise ValueError('Input shape can only take values: list of 3 integer elements greater than zero.')
        if self._parameter_not_is_none(input_name):
            self.input_name = input_name
        if self._parameter_not_is_none(output_names):
            self.output_names = output_names
        if self._parameter_not_is_none(thread_count):
            if self._int_value_is_correct(thread_count):
                self.nthreads = thread_count
            else:
                raise ValueError('Threads count can only take integer value')
        if self._parameter_not_is_none(inter_op_parallelism_threads):
            if self._int_value_is_correct(inter_op_parallelism_threads):
                self.num_inter_threads = inter_op_parallelism_threads
            else:
                raise ValueError('Inter op parallelism threads can only take integer value')
        if self._parameter_not_is_none(intra_op_parallelism_threads):
            if self._int_value_is_correct(intra_op_parallelism_threads):
                self.num_intra_threads = intra_op_parallelism_threads
            else:
                raise ValueError('Intra op parallelism threads can only take integer value')
        if self._parameter_not_is_none(kmp_affinity):
            self.kmp_affinity = kmp_affinity


class Test(metaclass=abc.ABCMeta):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        self.model = model
        self.dataset = dataset
        self.indep_parameters = indep_parameters
        self.dep_parameters = dep_parameters

    @staticmethod
    def get_test(framework, model, dataset, indep_parameters, dep_parameters):
        if framework == 'OpenVINO DLDT':
            return OpenVINOTest(model, dataset, indep_parameters, dep_parameters)
        elif framework == 'Caffe':
            return IntelCaffeTest(model, dataset, indep_parameters, dep_parameters)
        elif framework == 'TensorFlow':
            return TensorFlowTest(model, dataset, indep_parameters, dep_parameters)
        else:
            raise ValueError(
                'Invalid framework name: only \'OpenVINO DLDT\', \'Caffe\' and \'TensorFlow\' are available')

    @abc.abstractmethod
    def get_report(self):
        pass


class OpenVINOTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        parameters = OrderedDict()
        parameters.update({'Device': self.indep_parameters.device})
        parameters.update({'Async request count': self.dep_parameters.async_request})
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Thread count': self.dep_parameters.nthreads})
        parameters.update({'Stream count': self.dep_parameters.nstreams})
        other_param = []
        for key in parameters:
            if parameters[key] is not None:
                other_param.append(f'{key}: {parameters[key]}')
        other_param = ', '.join(other_param)

        report_res = '{0};{1};{2};{3};{4};input_shape;{5};{6};{7};{8}'.format(
            self.model.task, self.model.name, self.dataset.name, self.model.source_framework,
            self.indep_parameters.inference_framework, self.model.precision,
            self.indep_parameters.batch_size, self.dep_parameters.mode, other_param)

        return report_res


class IntelCaffeTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        report_res = '{0};{1};{2};{3};{4};input_shape;{5};{6};Sync;Device: {7}, ' \
                     'Iteration count: {8}, Thread count: {9}, KMP_AFFINITY: {10}'.format(
            self.model.task, self.model.name, self.dataset.name, self.model.source_framework,
            self.indep_parameters.inference_framework, self.model.precision,
            self.indep_parameters.batch_size, self.indep_parameters.device,
            self.indep_parameters.iteration, self.dep_parameters.nthreads,
            self.dep_parameters.kmp_affinity)

        return report_res


class TensorFlowTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        report_res = '{0};{1};{2};{3};{4};input_shape;{5};{6};Sync;Device: {7}, Iteration count: {8}, ' \
                     'Thread count: {9}, Inter threads: {10}, Intra threads: {11}, KMP_AFFINITY: {12}'.format(
            self.model.task, self.model.name, self.dataset.name, self.model.source_framework,
            self.indep_parameters.inference_framework, self.model.precision,
            self.indep_parameters.batch_size, self.indep_parameters.device,
            self.indep_parameters.iteration, self.dep_parameters.nthreads,
            self.dep_parameters.num_inter_threads, self.dep_parameters.num_intra_threads,
            self.dep_parameters.kmp_affinity)

        return report_res


def process_config(config, log):
    test_parser = Parser()
    test_list = []

    tests = test_parser.get_tests_list(config)
    for idx, curr_test in enumerate(tests):
        try:
            model = test_parser.parse_model(curr_test)
            dataset = test_parser.parse_dataset(curr_test)
            indep_parameters = test_parser.parse_independent_parameters(curr_test)
            framework = indep_parameters.inference_framework
            dep_parameters = test_parser.parse_dependent_parameters(curr_test, framework)

            test_list.append(Test.get_test(framework, model, dataset, indep_parameters, dep_parameters))
        except ValueError as valerr:
            log.warning('Test {} not added to test list: {}'.format(idx + 1, valerr))
    return test_list
