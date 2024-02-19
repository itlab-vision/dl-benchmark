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
            errmsg = 'Command line is empty, nothing to execute'
            self.__log.error(errmsg)
            raise AssertionError(errmsg)
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

    @staticmethod
    def get_reported_optional_value(report, param_name, value_type=float, to_round=True,
                                    round_precision=3, default_value='N/A'):
        reported_value = report['execution_results'].get(param_name, None)
        value = value_type(reported_value) if reported_value else default_value
        if to_round and value != default_value:
            return round(value, round_precision)
        return value

    def get_performance_metrics_from_json_report(self):
        if self._status != 0 or len(self._output) == 0:
            return {'average_time': None, 'fps': None, 'latency': None, 'batch_fps': None, 'latency_per_token': None,
                    'num_tokens': None, 'audio_len_avg': None, 'audio_sampling_rate': None,
                    'latency_per_second': None}

        report = self.get_json_report_content()

        MILLISECONDS_IN_SECOND = 1000
        fps = float(report['execution_results']['throughput'])
        latency = self.get_reported_optional_value(report, 'latency_median', default_value=0.0)
        average_time_of_single_pass = float(report['execution_results']['latency_avg'])
        batch_fps = self.get_reported_optional_value(report, 'batch_throughput', default_value=0.0)
        latency_per_token = self.get_reported_optional_value(report, 'latency_per_token')
        num_tokens = self.get_reported_optional_value(report, 'num_tokens')
        audio_len_avg = self.get_reported_optional_value(report, 'audio_len_avg')
        latency_per_second = self.get_reported_optional_value(report, 'latency_per_second')
        audio_sampling_rate = self.get_reported_optional_value(report, 'audio_sampling_rate')

        if self.launcher_latency_units == 'milliseconds':
            latency = round(latency / MILLISECONDS_IN_SECOND, 5)
            average_time_of_single_pass = round(average_time_of_single_pass / MILLISECONDS_IN_SECOND, 5)
        metrics = {}
        metrics['average_time'] = average_time_of_single_pass
        metrics['fps'] = fps
        metrics['latency'] = latency
        metrics['batch_fps'] = batch_fps
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
