import abc
import json
import os
import platform
from datetime import datetime
from pathlib import Path


class ProcessHandler(metaclass=abc.ABCMeta):
    def __init__(self, test, executor, log):
        self.__log = log
        self._test = test
        self._executor = executor
        self._output = None
        self._status = None
        self.timestamp = datetime.now().strftime('%d.%m.%y_%H-%M-%S')
        self.inference_script_root = Path(self._executor.get_path_to_inference_folder())

    @property
    @abc.abstractmethod
    def benchmark_app_name(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def launcher_latency_units(self):
        # use seconds or milliseconds as latency measuring units
        raise NotImplementedError

    @property
    def report_path(self):
        report_name = f'{self.benchmark_app_name}_{self._test.model.name}_{self.timestamp}.json'
        report_path = Path(self._executor.get_path_to_logs_folder()) / report_name
        return report_path

    @staticmethod
    def get_cmd_python_version():
        cmd_python_version = ''
        os_type = platform.system()
        if os_type == 'Linux':
            cmd_python_version = 'python3'
        else:
            cmd_python_version = 'python'

        return cmd_python_version

    def get_model_shape(self):
        input_shape = []
        for line in self._output:
            if 'Shape for input layer' in line:
                input_shape.append(line.split(':')[-1].strip())

        return ', '.join(input_shape) if len(input_shape) > 0 else 'Undefined'

    def execute(self):
        command_line = self._fill_command_line()
        if command_line == '':
            self.__log.error('Command line is empty')
        self.__log.info(f'Start inference test on model: {self._test.model.name}')
        self.__log.info(f'Command line is: {command_line}')
        self._executor.set_target_framework(self._test.indep_parameters.inference_framework)

        # add timeout overhead because time_limit in bechmark app applies for inference stage only
        # set None n case of test_time_limit is unset for backward compatibility
        configured_time_limit = self._test.indep_parameters.test_time_limit
        configured_timeout_overhead = self._test.indep_parameters.timeout_overhead
        timeout = configured_time_limit + configured_timeout_overhead if configured_time_limit else None
        self._status, self._output = self._executor.execute_process(command_line, timeout)

        if type(self._output) is not list:
            self._output = self._output.decode('utf-8').split('\n')[:-1]

        if self._status == 0:
            self.__log.info(f'End inference test on model : {self._test.model.name}')
        else:
            self.__log.warning(f'Inference test on model: {self._test.model.name} was ended with error. '
                               f'Process logs: {self._output}')
            self.__print_error()
            self.__save_failed_test_log()

    def get_status(self):
        return self._status

    @abc.abstractmethod
    def get_performance_metrics(self):
        pass

    def get_json_report_content(self):
        if self.report_path:
            return json.loads(self._executor.get_file_content(self.report_path))

    def get_output_lines(self):
        return self._output

    def get_performance_metrics_from_json_report(self):
        if self._status != 0 or len(self._output) == 0:
            return {'average_time': None, 'fps': None, 'latency': None, 'batch_fps': None, 'latency_per_token': None}

        report = self.get_json_report_content()

        MILLISECONDS_IN_SECOND = 1000
        fps = float(report['execution_results']['throughput'])
        reported_latency = report['execution_results'].get('latency_median', None)
        latency = float(reported_latency) if reported_latency else 0.0
        average_time_of_single_pass = float(report['execution_results']['latency_avg'])
        reported_batch_fps = report['execution_results'].get('batch_throughput', None)
        batch_fps = round(float(reported_batch_fps), 3) if reported_batch_fps else 0.0
        reported_latency_per_token = report['execution_results'].get('latency_per_token', None)
        latency_per_token = round(float(reported_latency_per_token), 3) if reported_latency_per_token else 'N/A'
        if self.launcher_latency_units == 'milliseconds':
            latency = round(latency / MILLISECONDS_IN_SECOND, 5)
            average_time_of_single_pass = round(average_time_of_single_pass / MILLISECONDS_IN_SECOND, 5)
        metrics = {'average_time': average_time_of_single_pass, 'fps': fps, 'latency': latency, 'batch_fps': batch_fps,
                   'latency_per_token': latency_per_token}

        return metrics

    @abc.abstractmethod
    def _fill_command_line(self):
        pass

    def _fill_command_line_cpp(self):
        model = self._test.model.model
        weights = self._test.model.weight
        iteration_count = self._test.indep_parameters.iteration
        time = int(self._test.indep_parameters.test_time_limit)
        dataset_path = self._test.dataset.path if self._test.dataset else None

        arguments = f'-m {model}'
        if weights.lower() != 'none':
            arguments += f' -w {weights}'
        arguments += f' -niter {iteration_count} -save_report -report_path {self.report_path} -t {time}'

        arguments = self._add_optional_argument_to_cmd_line(arguments, '-i', dataset_path)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-b', self._test.indep_parameters.batch_size)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-d', self._test.indep_parameters.device)

        arguments = self._add_optional_argument_to_cmd_line(arguments, '-shape', self._test.dep_parameters.input_shape)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-layout', self._test.dep_parameters.layout)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-mean', self._test.dep_parameters.mean)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-scale', self._test.dep_parameters.input_scale)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-nthreads',
                                                            self._test.dep_parameters.thread_count)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-nireq',
                                                            self._test.dep_parameters.inference_requests_count)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-dtype',
                                                            self._test.dep_parameters.input_type)

        command_line = f'{self._benchmark_path} {arguments}'
        return command_line

    @staticmethod
    def _add_argument_to_cmd_line(command_line, argument, value):
        return f'{command_line} {argument} {value}'

    @staticmethod
    def _add_flag_to_cmd_line(command_line, flag):
        return f'{command_line} {flag}'

    @staticmethod
    def _add_env_to_cmd_line(command_line, name, value):
        return f'{name}={value} {command_line}'

    @staticmethod
    def _add_optional_argument_to_cmd_line(command_line, argument, value):
        if value:
            return ProcessHandler._add_argument_to_cmd_line(command_line, argument, value)
        return command_line

    def __print_error(self):
        out = self._output
        is_error = False
        for line in out:
            if line.rfind('ERROR! :') != -1:
                is_error = True
                self.__log.error(f'    {line[8:]}')
                continue
            if is_error:
                self.__log.error(f'    {line}')

    def __save_failed_test_log(self):
        log_filename = self.__make_log_filename()
        out = self._output
        self.__log.info(f'Save failed test log to {log_filename}')

        with open(log_filename, 'w', encoding='utf-8') as file:
            for line in out:
                file.write(line)

    def __make_log_filename(self):
        test_settings = [self._test.model.name,
                         self._test.indep_parameters.inference_framework.replace(' ', '_'),
                         self._test.indep_parameters.device,
                         self._test.model.precision,
                         str(self._test.indep_parameters.batch_size),
                         ]
        if hasattr(self._test.dep_parameters, 'mode') and self._test.dep_parameters.mode:
            test_settings.append(self._test.dep_parameters.mode)
        if hasattr(self._test.dep_parameters, 'code_source') and self._test.dep_parameters.code_source:
            test_settings.append(self._test.dep_parameters.code_source)
        if hasattr(self._test.dep_parameters, 'runtime') and self._test.dep_parameters.runtime:
            test_settings.append(self._test.dep_parameters.runtime)
        if hasattr(self._test.dep_parameters, 'hint') and self._test.dep_parameters.hint:
            test_settings.append(self._test.dep_parameters.hint)
        filename = '_'.join(test_settings) + '_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename += '.log'
        file_root = Path(os.getcwd())
        if not os.access(file_root, os.W_OK):
            self.__log.warning(f'Current folder {file_root} not writable, save failed test log to /tmp')
            file_root = Path('/tmp/failed_test_log')
            file_root.mkdir(exist_ok=True)

        return file_root / filename
