import re
from pathlib import Path

from .openvino_process import OpenVINOProcess


class OpenVINOBenchmarkProcess(OpenVINOProcess):
    def __init__(self, test, executor, log, perf_hint=''):
        super().__init__(test, executor, log)
        self._perf_hint = perf_hint

    @staticmethod
    def _add_perf_hint_for_cmd_line(command_line, perf_hint):
        hint = perf_hint.lower()
        if hint in ('latency', 'throughput'):
            return f'{command_line} -hint {hint}'
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


class OpenVINOBenchmarkPythonProcess(OpenVINOBenchmarkProcess):
    def __init__(self, test, executor, log, perf_hint=''):
        super().__init__(test, executor, log, perf_hint)
        self._perf_hint = perf_hint

    @staticmethod
    def create_process(test, executor, log):
        return OpenVINOBenchmarkPythonProcess(test, executor, log)

    def _fill_command_line(self):
        model_xml = self._test.model.model
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        arguments = f'-m {model_xml} -i {dataset} -b {batch} -d {device} -niter {iteration}'

        extension = self._test.dep_parameters.extension
        if extension:
            arguments = self._add_extension_for_cmd_line(arguments, extension, device)

        nthreads = self._test.dep_parameters.nthreads
        if nthreads:
            arguments = self._add_argument_to_cmd_line(arguments, '-nthreads', nthreads)

        arguments = self._add_perf_hint_for_cmd_line(arguments, self._perf_hint)

        command_line = f'benchmark_app {arguments}'
        return command_line


class OpenVINOBenchmarkCppProcess(OpenVINOBenchmarkProcess):
    def __init__(self, test, executor, log, cpp_benchmarks_dir, perf_hint=''):
        super().__init__(test, executor, log, perf_hint)
        self._perf_hint = perf_hint

        invalid_path_exception = ValueError('Must provide valid path to the folder '
                                            'with OpenVINO C++ benchmark_app (--openvino_cpp_benchmark_path)')
        if not cpp_benchmarks_dir:
            raise invalid_path_exception

        self._benchmark_path = Path(cpp_benchmarks_dir).joinpath('benchmark_app')
        if not self._benchmark_path.is_file():
            raise invalid_path_exception

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None):
        return OpenVINOBenchmarkCppProcess(test, executor, log, cpp_benchmarks_dir)

    def _fill_command_line(self):
        model_xml = self._test.model.model
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        arguments = f'-m {model_xml} -i {dataset} -b {batch} -d {device} -niter {iteration} -report_type "no_counters"'

        extension = self._test.dep_parameters.extension
        if extension:
            arguments = self._add_extension_for_cmd_line(arguments, extension, device)

        nthreads = self._test.dep_parameters.nthreads
        if nthreads:
            arguments = self._add_argument_to_cmd_line(arguments, '-nthreads', nthreads)

        arguments = self._add_perf_hint_for_cmd_line(arguments, self._perf_hint)

        command_line = f'{self._benchmark_path} {arguments}'
        return command_line
