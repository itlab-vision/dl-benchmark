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
        return self.get_performance_metrics_cpp()

    def _fill_command_line(self):
        return self._fill_command_line_cpp()
