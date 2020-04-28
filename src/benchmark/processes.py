import abc
import os
import platform

class process(metaclass = abc.ABCMeta):
    def __init__(self, test, executor, log):
        self._my_test = test
        self.__my_executor = executor
        self.__my_log = log
        self._my_row_output = None

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
        input_shape = 'Undefined'
        for line in self.my_output:
            if 'Input shape: ' in line:
                input_shape = line.split(' ')[-1]
        return input_shape

    def print_error(self):
        out = self._my_row_output[1]
        iserror = False
        for line in out:
            if line.rfind('ERROR! :') != -1:
                iserror = True
                print('    {0}'.format(line[8:]))
                continue
            if iserror:
                print('    {0}'.format(line))

    def execute(self):
        command_line = self._fill_command_line()
        if command_line == '':
            self.__my_log.error('Command line is empty')
        self.__my_log.info('Start inference test on model : {}'.format(self._my_test.model.name))
        self.__my_executor.set_target_framework(self._my_test.framework)
        self._my_row_output = self.__my_executor.execute_process(command_line)
        self.my_output = self._my_row_output[1]

        if type(self.my_output) is not list:
            self.my_output = self.my_output.decode("utf-8").split('\n')[:-1]

        if self._my_row_output[0] == 0:
            self.__my_log.info('End inference test on model : {}'.format(self._my_test.model.name))
        else:
            self.__my_log.warning('Inference test on model: {} was ended with error. Process logs:'.format(self._my_test.model.name))
            self.print_error()

    def get_status(self):
        return self._my_row_output[0]

    @staticmethod
    def get_process(test, executor, log):
        if test.framework == 'OpenVINO':
            return OpenVINO_process.create_process(test, executor, log)

    @abc.abstractmethod
    def get_performance_metrics(self):
        pass

class OpenVINO_process(process):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

        model_xml = self._my_test.model.model
        model_bin = self._my_test.model.weight
        dataset = self._my_test.dataset.path
        batch = self._my_test.parameter.batch_size
        device = self._my_test.parameter.device
        iteration = self._my_test.parameter.iteration
        self.my_common_params = '-m {0} -w {1} -i {2} -b {3} -d {4} -ni {5}'.format(model_xml, model_bin, dataset, batch, device, iteration)

        extension = self._my_test.parameter.extension
        if extension:
            self.__add_extension_for_cmd_line(extension)

        nthreads = self._my_test.parameter.nthreads
        if nthreads:
            self.__add_nthreads_for_cmd_line(nthreads)

    def __add_extension_for_cmd_line(self, extension):
        self.my_common_params = '{0} -l {1}'.format(self.my_common_params, extension)

    def __add_nthreads_for_cmd_line(self, nthreads):
        self.my_common_params = '{0} -nthreads {1}'.format(self.my_common_params, nthreads)

    @staticmethod
    def create_process(test, executor, log):
        mode = (test.parameter.mode).lower()
        if mode == 'sync':
            return sync_OpenVINO_process(test, executor, log)
        elif mode == 'async':
            return async_OpenVINO_process(test, executor, log)

class sync_OpenVINO_process(OpenVINO_process):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def __add_min_inference_time_for_cmd_line(command_line, min_inference_time):
        return '{0} -mi {1}'.format(command_line, min_inference_time)

    @staticmethod
    def __add_raw_output_time_for_cmd_line(command_line, raw_output):
        return '{0} {1}'.format(command_line, raw_output)

    def _fill_command_line(self):
        path_to_sync_scrypt = os.path.join(self._my_test.parameter.inference_folder, 'inference_sync_mode.py')

        python = process._get_cmd_python_version()
        command_line = '{0} {1} {2}'.format(python, path_to_sync_scrypt, self.my_common_params)

        min_inference_time = self._my_test.parameter.min_inference_time
        command_line = sync_OpenVINO_process.__add_min_inference_time_for_cmd_line(command_line, min_inference_time)
        command_line = sync_OpenVINO_process.__add_raw_output_time_for_cmd_line(command_line, '--raw_output true')

        return command_line

    def get_performance_metrics(self):
        if self._my_row_output[0] != 0 or len(self.my_output) == 0:
            return 0, 0, 0

        result = self.my_output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])
        return average_time, fps, latency

class async_OpenVINO_process(OpenVINO_process):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def __add_nstreams_for_cmd_line(command_line, nstreams):
        return '{0} -nstreams {1}'.format(command_line, nstreams)

    @staticmethod
    def __add_requests_for_cmd_line(command_line, requests):
        return '{0} -requests {1}'.format(command_line, requests)

    def _fill_command_line(self):
        path_to_async_scrypt = os.path.join(self._my_test.parameter.inference_folder, 'inference_async_mode.py')

        python = process._get_cmd_python_version()
        command_line = '{0} {1} {2}'.format(python, path_to_async_scrypt, self.my_common_params)

        nstreams = self._my_test.parameter.nstreams
        if nstreams:
            command_line = async_OpenVINO_process.__add_nstreams_for_cmd_line(command_line, nstreams)

        requests = self._my_test.parameter.requests
        if requests:
            command_line = async_OpenVINO_process.__add_requests_for_cmd_line(command_line, requests)

        return command_line

    def get_performance_metrics(self):
        if self._my_row_output[0] != 0 or len(self.my_output) == 0:
            return 0, 0, 0

        result = self.my_output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        return average_time, fps, 0
