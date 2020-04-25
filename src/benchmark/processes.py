import abc
import os
import platform

class process(metaclass = abc.ABCMeta):
    def __init__(self, test, executor, log):
        self.my_test = test
        self.my_executor = executor
        self.my_log = log
        self.my_command_line = ''
        self.my_row_output = None

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

    def execute(self):
        self._fill_command_line()
        if self.my_command_line == '':
            self.my_log.error('Command line is empty')
        self.my_log.info('Start inference test on model : {}'.format(self.my_test.model.name))
        self.my_executor.set_target_framework(self.my_test.framework)
        self.my_row_output = self.my_executor.execute_process(self.my_command_line)

        if self.my_row_output[0] == 0:
            self.my_log.info('End inference test on model : {}'.format(self.my_test.model.name))
        else:
            self.my_log.warning('Inference test on model: {} was ended with error. Process logs:'.format(self.my_test.model.name))
            self.print_error()

    def get_status(self):
        return 'Success' if self.my_row_output[0] == 0 else 'Failed'

    @staticmethod
    def get_process(test, executor, log):
        if test.framework == 'OpenVINO':
            return OpenVINO_process.create_process(test, executor, log)

    @abc.abstractmethod
    def get_model_shape(self):
        pass

    @abc.abstractmethod
    def get_performance_metrics(self):
        pass

    @abc.abstractmethod
    def print_error(self):
        pass

class OpenVINO_process(process):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

        model_xml = self.my_test.model.model
        model_bin = self.my_test.model.weight
        dataset = self.my_test.dataset.path
        batch = self.my_test.parameter.batch_size
        device = self.my_test.parameter.device
        iteration = self.my_test.parameter.iteration
        self.my_common_params = '-m {0} -w {1} -i {2} -b {3} -d {4} -ni {5}'.format(model_xml, model_bin, dataset, batch, device, iteration)

        extension = self.my_test.parameter.extension
        if extension:
            self.add_extension_for_cmd_line(extension)

        nthreads = self.my_test.parameter.nthreads
        if nthreads:
            self.add_nthreads_for_cmd_line(nthreads)

    def get_model_shape(self):
        input_shape = 'Undefined'
        for line in self.my_row_output[1]:
            if 'Input shape: ' in line:
                input_shape = line.split(' ')[-1]
        return input_shape

    def add_extension_for_cmd_line(self, extension):
        self.my_common_params = '{0} -l {1}'.format(self.my_common_params, extension)

    def add_nthreads_for_cmd_line(self, nthreads):
        self.my_common_params = '{0} -nthreads {1}'.format(self.my_common_params, nthreads)

    def print_error(self):
        out = self.my_row_output[1]
        iserror = False
        for line in out:
            if line.rfind('ERROR! :') != -1:
                iserror = True
                print('    {0}'.format(line[8:]))
                continue
            if iserror:
                print('    {0}'.format(line))

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

    def add_min_inference_time_for_cmd_line(self, min_inference_time):
        self.my_command_line = '{0} -mi {1}'.format(self.my_command_line, min_inference_time)

    def add_raw_output_time_for_cmd_line(self, raw_output):
        self.my_command_line = '{0} {1}'.format(self.my_command_line, raw_output)

    def _fill_command_line(self):
        inference_folder = os.path.abspath('../inference')
        path_to_sync_scrypt = os.path.join(inference_folder, 'inference_sync_mode.py')

        python = process._get_cmd_python_version()
        self.my_command_line = '{0} {1} {2}'.format(python, path_to_sync_scrypt, self.my_common_params)

        min_inference_time = self.my_test.parameter.min_inference_time
        self.add_min_inference_time_for_cmd_line(min_inference_time)
        self.add_raw_output_time_for_cmd_line('--raw_output true')

    def get_performance_metrics(self):
        if self.my_row_output[0] != 0 or len(self.my_row_output[1]) == 0:
            return 0, 0, 0

        result = self.my_row_output[1][-1].split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])
        return average_time, fps, latency


class async_OpenVINO_process(OpenVINO_process):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    def add_nstreams_for_cmd_line(self, nstreams):
        self.my_command_line = '{0} -nstreams {1}'.format(self.my_command_line, nstreams)

    def add_requests_for_cmd_line(self, requests):
        self.my_command_line = '{0} -requests {1}'.format(self.my_command_line, requests)

    def _fill_command_line(self):
        inference_folder = os.path.abspath('../inference')
        path_to_async_scrypt = os.path.join(inference_folder, 'inference_async_mode.py')

        python = process._get_cmd_python_version()
        self.my_command_line = '{0} {1} {2}'.format(python, path_to_async_scrypt, self.my_common_params)

        nstreams = self.my_test.parameter.nstreams
        if nstreams:
            self.add_nstreams_for_cmd_line(nstreams)

        requests = self.my_test.parameter.requests
        if requests:
            self.add_requests_for_cmd_line(requests)

    def get_performance_metrics(self):
        if self.my_row_output[0] != 0 or len(self.my_row_output[1]) == 0:
            return 0, 0, 0

        result = self.my_row_output[1][-1].split(',')
        average_time = float(result[0])
        fps = float(result[1])
        return average_time, fps, 0
