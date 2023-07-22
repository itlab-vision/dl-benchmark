from pathlib import Path

from ..processes import ProcessHandler


class TensorFlowLiteCppProcess(ProcessHandler):
    benchmark_app_name = 'tflite_cpp_benchmark'
    launcher_latency_units = 'milliseconds'

    def __init__(self, test, executor, log, cpp_benchmarks_dir):
        super().__init__(test, executor, log)

        invalid_path_exception = ValueError('Must provide valid path to the folder '
                                            'with TensorFlow Lite Cpp benchmark (--cpp_benchmarks_dir)')
        if not cpp_benchmarks_dir:
            raise invalid_path_exception

        backend = self._test.dep_parameters.backend.upper()
        supported_backends = ('DEFAULT', 'XNNPACK')
        if backend not in supported_backends:
            raise AssertionError(f'Unsupported backend: {backend}. Available backends: {supported_backends}')

        if backend == 'XNNPACK':
            self._benchmark_path = Path(cpp_benchmarks_dir).joinpath('tflite_xnnpack_benchmark')
        else:
            self._benchmark_path = Path(cpp_benchmarks_dir).joinpath('tflite_benchmark')

        if not self._benchmark_path.is_file():
            raise invalid_path_exception

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir):
        return TensorFlowLiteCppProcess(test, executor, log, cpp_benchmarks_dir)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        return self._fill_command_line_cpp()
