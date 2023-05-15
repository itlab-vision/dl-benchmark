import re
from pathlib import Path

from .openvino_process import OpenVINOProcess


class OpenVINOBenchmarkProcess(OpenVINOProcess):
    def __init__(self, test, executor, log, perf_hint='', api_mode=''):
        super().__init__(test, executor, log)
        self._perf_hint = perf_hint
        self._api_mode = api_mode

    @staticmethod
    def _add_perf_hint_for_cmd_line(command_line, perf_hint):
        hint = perf_hint.lower()
        if hint in ('latency', 'throughput', 'none'):
            return f'{command_line} -hint {hint}'

        return command_line

    @staticmethod
    def _add_api_mode_for_cmd_line(command_line, api_mode):
        api = api_mode.lower()
        if api in ('sync', 'async'):
            return f'{command_line} -api {api}'

        return command_line

    @staticmethod
    def _add_extension_for_cmd_line(command_line, extension, device):
        if 'GPU' in device:
            return f'{command_line} -c {extension}'
        if 'CPU' in device or 'MYRIAD' in device:
            return f'{command_line} -l {extension}'

        return command_line

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        # calculate average time of single pass metric to align output with custom launchers
        duration = self._get_benchmark_app_metric('Duration')
        iter_count = self._get_benchmark_app_metric('Count')
        average_time_of_single_pass = (round(duration / 1000 / iter_count, 3)
                                       if None not in (duration, iter_count) else None)

        fps = self._get_benchmark_app_metric('Throughput')
        latency = round(self._get_benchmark_app_metric('Median') / 1000, 3)

        return average_time_of_single_pass, fps, latency

    def _get_benchmark_app_metric(self, metric_name):
        """
        gets metric value from benchmark app full output
        :param metric_name: metric name, ex 'Throughput'
        :return: float value or None if pattern not found
        """
        for line in self._output:
            regex = re.compile(f'.*{metric_name}:\\s+(?P<metric>\\d*\\.\\d+|\\d+).*')
            res = regex.match(line)
            if res:
                try:
                    return float(res.group('metric'))
                except ValueError:
                    return None

    def _add_common_arguments(self, arguments, device):
        extension = self._test.dep_parameters.extension
        if extension:
            arguments = self._add_extension_for_cmd_line(arguments, extension, device)

        arguments = self._add_optional_argument_to_cmd_line(arguments, '-shape', self._test.dep_parameters.shape)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-layout', self._test.dep_parameters.layout)

        nireq = self._test.dep_parameters.infer_request
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-nireq', nireq)

        nstreams = self._test.dep_parameters.nstreams
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-nstreams', nstreams)
        nthreads = self._test.dep_parameters.nthreads
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-nthreads', nthreads)

        return arguments

    def extract_inference_param(self, key):
        regex = re.compile(rf'\s*{key}\s*[:,]\s*(?P<value>.+)$')
        for line in self._output:
            res = regex.search(line)
            if res:
                return res.group('value')
        return None


class OpenVINOBenchmarkPythonProcess(OpenVINOBenchmarkProcess):
    def __init__(self, test, executor, log, perf_hint='', api_mode=''):
        super().__init__(test, executor, log, perf_hint, api_mode)

    @staticmethod
    def create_process(test, executor, log):
        return OpenVINOBenchmarkPythonProcess(test, executor, log)

    def _fill_command_line(self):
        model_xml = self._test.model.model
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration
        frontend = self._test.dep_parameters.frontend
        time = int(self._test.indep_parameters.test_time_limit)

        arguments = f'-m {model_xml} -i {dataset} -b {batch} -d {device} -niter {iteration} -t {time}'

        arguments = self._add_api_mode_for_cmd_line(arguments, self._api_mode)
        arguments = self._add_perf_hint_for_cmd_line(arguments, self._perf_hint)
        arguments = self._add_common_arguments(arguments, device)
        if frontend != 'IR':
            arguments = self._add_optional_argument_to_cmd_line(arguments, '-imean', self._test.dep_parameters.mean)
            arguments = self._add_optional_argument_to_cmd_line(arguments, '-iscale',
                                                                self._test.dep_parameters.input_scale)
        command_line = f'benchmark_app {arguments}'

        return command_line

    def extract_inference_param(self, key):
        if key == 'nireq':
            regex = re.compile(r'\s*(\d+)\s*inference\s+requests')
            for line in self._output:
                if 'Measuring performance' in line:
                    res = regex.search(line)
                    if res:
                        return res.group(1)
            return None
        return super().extract_inference_param(key)


class OpenVINOBenchmarkCppProcess(OpenVINOBenchmarkProcess):
    def __init__(self, test, executor, log, cpp_benchmarks_dir, perf_hint='', api_mode=''):
        super().__init__(test, executor, log, perf_hint, api_mode)

        invalid_path_exception = ValueError('Must provide valid path to the folder '
                                            'with OpenVINO C++ benchmark_app (--openvino_cpp_benchmark_dir)')
        if not cpp_benchmarks_dir:
            raise invalid_path_exception

        self._benchmark_path = Path(cpp_benchmarks_dir).joinpath('benchmark_app')
        if not self._benchmark_path.is_file():
            raise invalid_path_exception

        self._report_path = executor.get_path_to_logs_folder().joinpath('benchmark_report.json')

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None):
        return OpenVINOBenchmarkCppProcess(test, executor, log, cpp_benchmarks_dir)

    def _fill_command_line(self):
        model_xml = self._test.model.model
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration
        frontend = self._test.dep_parameters.frontend
        time = int(self._test.indep_parameters.test_time_limit)

        arguments = (f'-m {model_xml} -i {dataset} -b {batch} -d {device} -niter {iteration} -t {time} '
                     f'-report_type "no_counters" -json_stats -report_folder {self._report_path.parent.absolute()}')

        arguments = self._add_api_mode_for_cmd_line(arguments, self._api_mode)
        arguments = self._add_perf_hint_for_cmd_line(arguments, self._perf_hint)
        arguments = self._add_common_arguments(arguments, device)
        if frontend != 'IR':
            arguments = self._add_optional_argument_to_cmd_line(arguments, '-imean', self._test.dep_parameters.mean)
            arguments = self._add_optional_argument_to_cmd_line(arguments, '-iscale',
                                                                self._test.dep_parameters.input_scale)

        command_line = f'{self._benchmark_path} {arguments}'

        return command_line

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        report = self.get_json_report_content()

        # calculate average time of single pass metric to align output with custom launchers
        MILLISECONDS_IN_SECOND = 1000
        duration = float(report['execution_results']['execution_time'])
        iter_count = float(report['execution_results']['iterations_num'])
        average_time_of_single_pass = (round(duration / MILLISECONDS_IN_SECOND / iter_count, 3)
                                       if None not in (duration, iter_count) else None)

        fps = round(float(report['execution_results']['throughput']), 3)
        latency = round(float(report['execution_results']['latency_median']) / MILLISECONDS_IN_SECOND, 3)

        return average_time_of_single_pass, fps, latency

    def extract_inference_param(self, key):
        if key == 'nireq':
            return self.get_json_report_content()['configuration_setup']['nireq']
        return super().extract_inference_param(key)
