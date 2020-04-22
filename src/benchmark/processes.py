import abc

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
    def get_cmd_python_version():
        cmd_python_version = ''
        os_type = platform.system()
        if os_type == 'Linux':
            cmd_python_version = 'python3'
        else:
            cmd_python_version = 'python'
        return cmd_python_version

    def execute(self):
        self.my_row_output = self.my_executor.execute_process(self.my_command_line)

    def get_status(self):
        return self.my_row_output[0]

    @staticmethod
    def get_executor(test, executor, log):
        if test == 'OpenVINO':
            return OpenVINO_process.create_process(test, executor, log)

    @abc.abstractmethod
    def get_model_shape(self):
        pass

    @abc.abstractmethod
    def get_performance_metrics(self):
        pass

class OpenVINO_process(process):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

        model_xml = my_test.model.model
        model_bin = my_test.model.weight
        dataset = my_test.dataset.path
        batch = my_test.parameter.batch_size
        device = my_test.parameter.device
        iteration = my_test.parameter.iteration
        self.my_common_params = '-m {2} -w {3} -i {4} -b {5} -d {6} -ni {7}'.format(model_xml, model_bin, dataset, batch, device, iteration)

        extension = my_test.parameter.extension
        if extension:
            self.add_extension_for_cmd_line(extension)

        nthreads = my_test.parameter.nthreads
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

        python = process.get_cmd_python_version()
        self.my_command_line = '{} {} {}'.(python, path_to_sync_scrypt, self.self.my_common_params)

        min_inference_time = my_test.parameter.min_inference_time
        self.add_min_inference_time_for_cmd_line(min_inference_time)
        self.add_raw_output_time_for_cmd_line('--raw_output true')

    def get_performance_metrics(self):
        result = my_row_output[1][-1].split(',')
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

        python = process.get_cmd_python_version()
        self.my_command_line = '{} {} {}'.(python, path_to_async_scrypt, self.self.my_common_params)

        nstreams = my_test.parameter.nstreams
        if nstreams:
            self.add_nstreams_for_cmd_line(nstreams)

        requests = my_test.parameter.requests
        if requests:
            self.add_requests_for_cmd_line(requests)

    def get_performance_metrics(self):
        result = my_row_output[1][-1].split(',')
        average_time = float(result[0])
        fps = float(result[1])
        return average_time, fps
