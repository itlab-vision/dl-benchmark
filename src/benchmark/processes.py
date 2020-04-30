import abc
import os
import platform

class process(metaclass = abc.ABCMeta):
    def __init__(self, test, executor, inference_folder, log):
        self._my_test = test
        self._my_inference_folder = inference_folder
        self.__my_executor = executor
        self.__my_log = log
        self._my_output = None
        self._my_row_output = None

    def __print_error(self):
        out = self._my_row_output[1]
        iserror = False
        for line in out:
            if line.rfind('ERROR! :') != -1:
                iserror = True
                self.__my_log.error('    {0}'.format(line[8:]))
                continue
            if iserror:
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
        input_shape = 'Undefined'
        for line in self._my_output:
            if 'Input shape: ' in line:
                input_shape = line.split(' ')[-1]
        return input_shape

    def execute(self):
        command_line = self._fill_command_line()
        if command_line == '':
            self.__my_log.error('Command line is empty')
        self.__my_log.info('Start inference test on model : {}'.format(self._my_test.model.name))
        self.__my_executor.set_target_framework(self._my_test.indep_parameters.inference_framework)
        self._my_row_output = self.__my_executor.execute_process(command_line)
        self._my_output = self._my_row_output[1]

        if type(self._my_output) is not list:
            self._my_output = self._my_output.decode("utf-8").split('\n')[:-1]

        if self._my_row_output[0] == 0:
            self.__my_log.info('End inference test on model : {}'.format(self._my_test.model.name))
        else:
            self.__my_log.warning('Inference test on model: {} was ended with error. Process logs:'.format(self._my_test.model.name))
            self.__print_error()

    def get_status(self):
        return self._my_row_output[0]

    @staticmethod
    def get_process(test, executor, inference_folder, log):
        if test.indep_parameters.inference_framework == 'OpenVINO DLDT':
            return OpenVINO_process.create_process(test, executor, inference_folder, log)

    @abc.abstractmethod
    def get_performance_metrics(self):
        pass

class OpenVINO_process(process):
    def __init__(self, test, executor, inference_folder, log):
        super().__init__(test, executor, inference_folder, log)

    @staticmethod
    def __add_extension_for_cmd_line(command_line, extension):
        return '{0} -l {1}'.format(command_line, extension)

    @staticmethod
    def __add_nthreads_for_cmd_line(command_line, nthreads):
        return '{0} -nthreads {1}'.format(command_line, nthreads)

    def _fill_command_line(self):
        model_xml = self._my_test.model.model
        model_bin = self._my_test.model.weight
        dataset = self._my_test.dataset.path
        batch = self._my_test.indep_parameters.batch_size
        device = self._my_test.indep_parameters.device
        iteration = self._my_test.indep_parameters.iteration

        command_line = '-m {0} -w {1} -i {2} -b {3} -d {4} -ni {5}'.format(model_xml, model_bin, dataset, batch, device, iteration)

        extension = self._my_test.dep_parameters.extension
        if extension:
            command_line = OpenVINO_process.__add_extension_for_cmd_line(command_line, extension)

        nthreads = self._my_test.dep_parameters.nthreads
        if nthreads:
            command_line = OpenVINO_process.__add_nthreads_for_cmd_line(command_line, nthreads)

        return command_line

    @staticmethod
    def create_process(test, executor, inference_folder, log):
        mode = (test.dep_parameters.mode).lower()
        if mode == 'sync':
            return sync_OpenVINO_process(test, executor, inference_folder, log)
        elif mode == 'async':
            return async_OpenVINO_process(test, executor, inference_folder, log)

class sync_OpenVINO_process(OpenVINO_process):
    def __init__(self, test, executor, inference_folder, log):
        super().__init__(test, executor, inference_folder, log)

    @staticmethod
    def __add_raw_output_time_for_cmd_line(command_line, raw_output):
        return '{0} {1}'.format(command_line, raw_output)

    def _fill_command_line(self):
        path_to_sync_scrypt = os.path.join(self._my_inference_folder, 'inference_sync_mode.py')

        python = process._get_cmd_python_version()
        common_params = super()._fill_command_line()
        command_line = '{0} {1} {2}'.format(python, path_to_sync_scrypt, common_params)

        command_line = sync_OpenVINO_process.__add_raw_output_time_for_cmd_line(command_line, '--raw_output true')

        return command_line

    def get_performance_metrics(self):
        if self._my_row_output[0] != 0 or len(self._my_output) == 0:
            return None, None, None

        result = self._my_output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])
        return average_time, fps, latency

class async_OpenVINO_process(OpenVINO_process):
    def __init__(self, test, executor, inference_folder, log):
        super().__init__(test, executor, inference_folder, log)

    @staticmethod
    def __add_nstreams_for_cmd_line(command_line, nstreams):
        return '{0} -nstreams {1}'.format(command_line, nstreams)

    @staticmethod
    def __add_requests_for_cmd_line(command_line, requests):
        return '{0} -requests {1}'.format(command_line, requests)

    def _fill_command_line(self):
        path_to_async_scrypt = os.path.join(self._my_inference_folder, 'inference_async_mode.py')

        python = process._get_cmd_python_version()
        common_params = super()._fill_command_line()
        command_line = '{0} {1} {2}'.format(python, path_to_async_scrypt, common_params)

        nstreams = self._my_test.dep_parameters.nstreams
        if nstreams:
            command_line = async_OpenVINO_process.__add_nstreams_for_cmd_line(command_line, nstreams)

        requests = self._my_test.dep_parameters.requests
        if requests:
            command_line = async_OpenVINO_process.__add_requests_for_cmd_line(command_line, requests)

        return command_line

    def get_performance_metrics(self):
        if self._my_row_output[0] != 0 or len(self._my_output) == 0:
            return None, None, None

        result = self._my_output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        return average_time, fps, 0
