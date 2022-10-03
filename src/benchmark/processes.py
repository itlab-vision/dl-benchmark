import abc
import os
import platform
from abc import ABC


class ProcessHandler(metaclass=abc.ABCMeta):
    def __init__(self, test, executor, log):
        self.__my_log = log
        self._my_test = test
        self._my_executor = executor
        self._my_output = None
        self._my_row_output = None

    def __print_error(self):
        out = self._my_output
        is_error = False
        for line in out:
            if line.rfind('ERROR! :') != -1:
                is_error = True
                self.__my_log.error('    {0}'.format(line[8:]))
                continue
            if is_error:
                self.__my_log.error('    {0}'.format(line))

    @abc.abstractmethod
    def _fill_command_line(self):
        pass

    @staticmethod
    def _get_cmd_python_version():
        cmd_python_version = ''
        os_type = platform.system()
        if os_type == 'Linux':
            cmd_python_version = 'python3'
        else:
            cmd_python_version = 'python'

        return cmd_python_version

    def get_model_shape(self):
        input_shape = []
        for line in self._my_output:
            if 'Shape for input layer' in line:
                input_shape.append(line.split(':')[-1].strip())

        return ', '.join(input_shape) if len(input_shape) > 0 else 'Undefined'

    def execute(self):
        command_line = self._fill_command_line()
        if command_line == '':
            self.__my_log.error('Command line is empty')
        self.__my_log.info('Start inference test on model : {}'.format(self._my_test.model.name))
        self._my_executor.set_target_framework(self._my_test.indep_parameters.inference_framework)
        self._my_row_output = self._my_executor.execute_process(command_line)
        self._my_output = self._my_row_output[1]

        if type(self._my_output) is not list:
            self._my_output = self._my_output.decode("utf-8").split('\n')[:-1]

        if self._my_row_output[0] == 0:
            self.__my_log.info('End inference test on model : {}'.format(self._my_test.model.name))
        else:
            self.__my_log.warning('Inference test on model: {} was ended with error. '
                                  'Process logs:'.format(self._my_test.model.name))
            self.__print_error()

    def get_status(self):
        return self._my_row_output[0]

    @staticmethod
    def get_process(test, executor, log):
        if test.indep_parameters.inference_framework == 'OpenVINO DLDT':
            return OpenVINOProcess.create_process(test, executor, log)
        elif test.indep_parameters.inference_framework == 'Caffe':
            return IntelCaffeProcess.create_process(test, executor, log)
        elif test.indep_parameters.inference_framework == 'TensorFlow':
            return TensorFlowProcess.create_process(test, executor, log)
        else:
            raise ValueError(
                'Invalid framework name. Supported values: \'OpenVINO DLDT\', \'Caffe\', \'TensorFlow\'')

    @abc.abstractmethod
    def get_performance_metrics(self):
        pass


class OpenVINOProcess(ProcessHandler, ABC):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def __add_extension_for_cmd_line(command_line, extension):
        return '{0} -l {1}'.format(command_line, extension)

    @staticmethod
    def __add_nthreads_for_cmd_line(command_line, nthreads):
        return '{0} -nthreads {1}'.format(command_line, nthreads)

    @staticmethod
    def __add_raw_output_time_for_cmd_line(command_line, raw_output):
        return '{0} {1}'.format(command_line, raw_output)

    def _fill_command_line(self):
        model_xml = self._my_test.model.model
        model_bin = self._my_test.model.weight
        dataset = self._my_test.dataset.path
        batch = self._my_test.indep_parameters.batch_size
        device = self._my_test.indep_parameters.device
        iteration = self._my_test.indep_parameters.iteration

        command_line = '-m {0} -w {1} -i {2} -b {3} -d {4} -ni {5}'.format(
            model_xml, model_bin, dataset, batch, device, iteration)

        extension = self._my_test.dep_parameters.extension
        if extension:
            command_line = OpenVINOProcess.__add_extension_for_cmd_line(command_line, extension)
        nthreads = self._my_test.dep_parameters.nthreads
        if nthreads:
            command_line = OpenVINOProcess.__add_nthreads_for_cmd_line(command_line, nthreads)
        command_line = OpenVINOProcess.__add_raw_output_time_for_cmd_line(command_line, '--raw_output true')

        return command_line

    @staticmethod
    def create_process(test, executor, log):
        mode = test.dep_parameters.mode.lower()
        if mode == 'sync':
            return SyncOpenVINOProcess(test, executor, log)
        elif mode == 'async':
            return SyncOpenVINOProcess(test, executor, log)


class SyncOpenVINOProcess(OpenVINOProcess):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    def _fill_command_line(self):
        path_to_sync_scrypt = os.path.normpath(os.path.join(
            self._my_executor.get_path_to_inference_folder(),
            'inference_sync_mode.py')
        )
        python = ProcessHandler._get_cmd_python_version()
        common_params = super()._fill_command_line()
        command_line = '{0} {1} {2}'.format(python, path_to_sync_scrypt, common_params)

        return command_line

    def get_performance_metrics(self):
        if self._my_row_output[0] != 0 or len(self._my_output) == 0:
            return None, None, None

        result = self._my_output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency


class AsyncOpenVINOProcess(OpenVINOProcess):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def __add_nstreams_for_cmd_line(command_line, nstreams):
        return '{0} -nstreams {1}'.format(command_line, nstreams)

    @staticmethod
    def __add_requests_for_cmd_line(command_line, requests):
        return '{0} --requests {1}'.format(command_line, requests)

    def _fill_command_line(self):
        path_to_async_scrypt = os.path.normpath(os.path.join(
            self._my_executor.get_path_to_inference_folder(),
            'inference_async_mode.py')
        )
        python = ProcessHandler._get_cmd_python_version()
        common_params = super()._fill_command_line()
        command_line = '{0} {1} {2}'.format(python, path_to_async_scrypt, common_params)
        nstreams = self._my_test.dep_parameters.nstreams
        if nstreams:
            command_line = AsyncOpenVINOProcess.__add_nstreams_for_cmd_line(command_line, nstreams)
        requests = self._my_test.dep_parameters.async_request
        if requests:
            command_line = AsyncOpenVINOProcess.__add_requests_for_cmd_line(command_line, requests)

        return command_line

    def get_performance_metrics(self):
        if self._my_row_output[0] != 0 or len(self._my_output) == 0:
            return None, None, None

        result = self._my_output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])

        return average_time, fps, 0


class IntelCaffeProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def __add_channel_swap_for_cmd_line(command_line, channel_swap):
        return '{0} --channel_swap {1}'.format(command_line, channel_swap)

    @staticmethod
    def __add_mean_for_cmd_line(command_line, mean):
        return '{0} --mean {1}'.format(command_line, mean)

    @staticmethod
    def __add_input_scale_for_cmd_line(command_line, input_scale):
        return '{0} --input_scale {1}'.format(command_line, input_scale)

    @staticmethod
    def __add_nthreads_for_cmd_line(command_line, nthreads):
        return 'OMP_NUM_THREADS={1} {0}'.format(command_line, nthreads)

    @staticmethod
    def __add_kmp_affinity_for_cmd_line(command_line, kmp_affinity):
        return 'KMP_AFFINITY={1} {0}'.format(command_line, kmp_affinity)

    @staticmethod
    def __add_raw_output_time_for_cmd_line(command_line, raw_output):
        return '{0} {1}'.format(command_line, raw_output)

    def _fill_command_line(self):
        path_to_intelcaffe_scrypt = os.path.normpath(os.path.join(
            self._my_executor.get_path_to_inference_folder(),
            'inference_caffe.py')
        )
        python = ProcessHandler._get_cmd_python_version()

        model_prototxt = self._my_test.model.model
        model_caffemodel = self._my_test.model.weight
        dataset = self._my_test.dataset.path
        batch = self._my_test.indep_parameters.batch_size
        device = self._my_test.indep_parameters.device
        iteration = self._my_test.indep_parameters.iteration

        common_params = '-m {0} -w {1} -i {2} -b {3} -d {4} -ni {5}'.format(
            model_prototxt, model_caffemodel, dataset, batch, device, iteration)
        channel_swap = self._my_test.dep_parameters.channel_swap
        if channel_swap:
            common_params = IntelCaffeProcess.__add_channel_swap_for_cmd_line(common_params, channel_swap)
        mean = self._my_test.dep_parameters.mean
        if mean:
            common_params = IntelCaffeProcess.__add_mean_for_cmd_line(common_params, mean)
        input_scale = self._my_test.dep_parameters.input_scale
        if input_scale:
            common_params = IntelCaffeProcess.__add_input_scale_for_cmd_line(common_params, input_scale)

        common_params = IntelCaffeProcess.__add_raw_output_time_for_cmd_line(common_params, '--raw_output true')
        command_line = '{0} {1} {2}'.format(python, path_to_intelcaffe_scrypt, common_params)

        nthreads = self._my_test.dep_parameters.nthreads
        if nthreads:
            command_line = IntelCaffeProcess.__add_nthreads_for_cmd_line(command_line, nthreads)
        kmp_affinity = self._my_test.dep_parameters.kmp_affinity
        if kmp_affinity:
            command_line = IntelCaffeProcess.__add_kmp_affinity_for_cmd_line(command_line, kmp_affinity)

        return command_line

    def get_performance_metrics(self):
        if self._my_row_output[0] != 0 or len(self._my_output) == 0:
            return None, None, None

        result = self._my_output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    @staticmethod
    def create_process(test, executor, log):
        return IntelCaffeProcess(test, executor, log)


class TensorFlowProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def __add_channel_swap_for_cmd_line(command_line, channel_swap):
        return '{0} --channel_swap {1}'.format(command_line, channel_swap)

    @staticmethod
    def __add_mean_for_cmd_line(command_line, mean):
        return '{0} --mean {1}'.format(command_line, mean)

    @staticmethod
    def __add_input_scale_for_cmd_line(command_line, input_scale):
        return '{0} --input_scale {1}'.format(command_line, input_scale)

    @staticmethod
    def __add_input_shape_for_cmd_line(command_line, input_shape):
        return '{0} --input_shape {1}'.format(command_line, input_shape)

    @staticmethod
    def __add_input_name_for_cmd_line(command_line, input_name):
        return '{0} --input_name {1}'.format(command_line, input_name)

    @staticmethod
    def __add_output_names_for_cmd_line(command_line, output_names):
        return '{0} --output_names {1}'.format(command_line, output_names)

    @staticmethod
    def __add_nthreads_for_cmd_line(command_line, nthreads):
        return 'OMP_NUM_THREADS={1} {0}'.format(command_line, nthreads)

    @staticmethod
    def __add_num_inter_threads_for_cmd_line(command_line, num_inter_threads):
        return '{0} --num_inter_threads {1}'.format(command_line, num_inter_threads)

    @staticmethod
    def __add_num_intra_threads_for_cmd_line(command_line, num_intra_threads):
        return '{0} --num_intra_threads {1}'.format(command_line, num_intra_threads)

    @staticmethod
    def __add_kmp_affinity_for_cmd_line(command_line, kmp_affinity):
        return 'KMP_AFFINITY={1} {0}'.format(command_line, kmp_affinity)

    @staticmethod
    def __add_raw_output_time_for_cmd_line(command_line, raw_output):
        return '{0} {1}'.format(command_line, raw_output)

    def _fill_command_line(self):
        path_to_tensorflow_scrypt = os.path.normpath(os.path.join(
            self._my_executor.get_path_to_inference_folder(),
            'inference_tensorflow.py')
        )
        python = ProcessHandler._get_cmd_python_version()

        model = self._my_test.model.model
        dataset = self._my_test.dataset.path
        batch = self._my_test.indep_parameters.batch_size
        device = self._my_test.indep_parameters.device
        iteration = self._my_test.indep_parameters.iteration

        common_params = '-m {0} -i {1} -b {2} -d {3} -ni {4}'.format(model, dataset, batch, device, iteration)

        channel_swap = self._my_test.dep_parameters.channel_swap
        if channel_swap:
            common_params = TensorFlowProcess.__add_channel_swap_for_cmd_line(common_params, channel_swap)
        mean = self._my_test.dep_parameters.mean
        if mean:
            common_params = TensorFlowProcess.__add_mean_for_cmd_line(common_params, mean)
        input_scale = self._my_test.dep_parameters.input_scale
        if input_scale:
            common_params = TensorFlowProcess.__add_input_scale_for_cmd_line(common_params, input_scale)
        input_shape = self._my_test.dep_parameters.input_shape
        if input_shape:
            common_params = TensorFlowProcess.__add_input_shape_for_cmd_line(common_params, input_shape)
        input_name = self._my_test.dep_parameters.input_name
        if input_name:
            common_params = TensorFlowProcess.__add_input_name_for_cmd_line(common_params, input_name)
        output_names = self._my_test.dep_parameters.output_names
        if output_names:
            common_params = TensorFlowProcess.__add_output_names_for_cmd_line(common_params, output_names)
        num_inter_threads = self._my_test.dep_parameters.num_inter_threads
        if num_inter_threads:
            common_params = TensorFlowProcess.__add_num_inter_threads_for_cmd_line(common_params, num_inter_threads)
        num_intra_threads = self._my_test.dep_parameters.num_intra_threads
        if num_intra_threads:
            common_params = TensorFlowProcess.__add_num_intra_threads_for_cmd_line(common_params, num_intra_threads)

        common_params = TensorFlowProcess.__add_raw_output_time_for_cmd_line(common_params, '--raw_output true')

        command_line = '{0} {1} {2}'.format(python, path_to_tensorflow_scrypt, common_params)

        nthreads = self._my_test.dep_parameters.nthreads
        if nthreads:
            command_line = TensorFlowProcess.__add_nthreads_for_cmd_line(command_line, nthreads)
        kmp_affinity = self._my_test.dep_parameters.kmp_affinity
        if kmp_affinity:
            command_line = TensorFlowProcess.__add_kmp_affinity_for_cmd_line(command_line, kmp_affinity)

        return command_line

    def get_performance_metrics(self):
        if self._my_row_output[0] != 0 or len(self._my_output) == 0:
            return None, None, None

        result = self._my_output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    @staticmethod
    def create_process(test, executor, log):
        return TensorFlowProcess(test, executor, log)
