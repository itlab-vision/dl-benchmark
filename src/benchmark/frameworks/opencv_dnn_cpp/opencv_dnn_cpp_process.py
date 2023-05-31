from pathlib import Path

from ..processes import ProcessHandler


class OpenCVDNNCppProcess(ProcessHandler):
    benchmark_app_name = 'opencv_cpp_benchmark'
    launcher_latency_units = 'milliseconds'

    def __init__(self, test, executor, log, cpp_benchmarks_dir):
        super().__init__(test, executor, log)

        invalid_path_exception = ValueError('Must provide valid path to the folder '
                                            'with OpenCV DNN Cpp benchmark (--cpp_benchmarks_dir)')
        if not cpp_benchmarks_dir:
            raise invalid_path_exception

        if self._test.dep_parameters.backend == 'IE':
            self._benchmark_path = Path(cpp_benchmarks_dir).joinpath('opencv_dnn_ov_benchmark')
        else:
            self._benchmark_path = Path(cpp_benchmarks_dir).joinpath('opencv_dnn_benchmark')

        if not self._benchmark_path.is_file():
            raise invalid_path_exception

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir):
        return OpenCVDNNCppProcess(test, executor, log, cpp_benchmarks_dir)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        return self._fill_command_line_cpp()
