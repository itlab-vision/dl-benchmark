import json
from pathlib import Path
from datetime import datetime

from ..processes import ProcessHandler


class OnnxRuntimeProcess(ProcessHandler):
    def __init__(self, test, executor, log, cpp_benchmarks_dir):
        super().__init__(test, executor, log)

        invalid_path_exception = ValueError('Must provide valid path to the folder '
                                            'with ONNX Runtime benchmark (--cpp_benchmarks_dir)')
        if not cpp_benchmarks_dir:
            raise invalid_path_exception

        self._benchmark_path = Path(cpp_benchmarks_dir).joinpath('onnxruntime_benchmark')
        if not self._benchmark_path.is_file():
            raise invalid_path_exception

        self._report_path = executor.get_path_to_logs_folder().joinpath(
            f'ort_benchmark_{test.model.name}_{datetime.now().strftime("%d.%m.%y_%H:%M:%S")}.json')

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir):
        return OnnxRuntimeProcess(test, executor, log, cpp_benchmarks_dir)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        report = json.loads(self._executor.get_file_content(self._report_path))

        # calculate average time of single pass metric to align output with custom launchers
        MILLISECONDS_IN_SECOND = 1000
        duration = float(report['execution_results']['execution_time'])
        iter_count = float(report['execution_results']['iterations_num'])
        average_time_of_single_pass = (round(duration / MILLISECONDS_IN_SECOND / iter_count, 3)
                                       if None not in (duration, iter_count) else None)

        fps = float(report['execution_results']['throughput'])
        latency = round(float(report['execution_results']['latency_median']) / MILLISECONDS_IN_SECOND, 3)

        return average_time_of_single_pass, fps, latency

    def _fill_command_line(self):
        model = self._test.model.model
        dataset = self._test.dataset.path
        iteration_count = self._test.indep_parameters.iteration

        arguments = f'-m {model} -i {dataset} -niter {iteration_count} -save_report -report_path {self._report_path}'
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-b', self._test.indep_parameters.batch_size)

        arguments = self._add_optional_argument_to_cmd_line(arguments, '-shape', self._test.dep_parameters.shape)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-layout', self._test.dep_parameters.layout)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-mean', self._test.dep_parameters.mean)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-scale', self._test.dep_parameters.scale)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-nthreads',
                                                            self._test.dep_parameters.thread_count)
        arguments = self._add_optional_argument_to_cmd_line(arguments, '-nireq',
                                                            self._test.dep_parameters.inference_requests_count)

        command_line = f'{self._benchmark_path} {arguments}'
        return command_line
