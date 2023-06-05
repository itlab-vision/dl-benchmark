from datetime import datetime
from pathlib import Path

from ..processes import ProcessHandler

ONNX_CPP_BENCHMARK_NAME = {'Default': 'onnxruntime_benchmark',
                           'CUDA': 'onnxruntime_cuda_benchmark',
                           'TensorRT': 'onnxruntime_tensorrt_benchmark',
                           }


class OnnxRuntimeProcess(ProcessHandler):
    def __init__(self, test, executor, log, cpp_benchmarks_dir='', provider='Default'):
        super().__init__(test, executor, log)

        invalid_path_exception = ValueError('Must provide valid path to the folder '
                                            'with ONNX Runtime benchmark (--cpp_benchmarks_dir),'
                                            f'benchmark app dir {cpp_benchmarks_dir} or benchmark app for '
                                            f'selected execution provider {provider} does not exist')
        if not cpp_benchmarks_dir:
            raise invalid_path_exception

        self._benchmark_path = Path(cpp_benchmarks_dir).joinpath(ONNX_CPP_BENCHMARK_NAME[provider])

        if not self._benchmark_path.is_file():
            raise invalid_path_exception

        self._report_path = executor.get_path_to_logs_folder().joinpath(
            f'ort_benchmark_{test.model.name}_{datetime.now().strftime("%d.%m.%y_%H:%M:%S")}.json')

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir='', **kwargs):
        device = test.indep_parameters.device
        provider = test.dep_parameters.provider
        if ((device == 'CPU' and provider not in ['Default'])
           or (device == 'NVIDIA_GPU' and provider not in ['CUDA', 'TensorRT'])):
            raise AssertionError('Unsupportend combination of: '
                                 f'device {device}, '
                                 f'execution provider {provider}')
        return OnnxRuntimeProcess(test, executor, log, cpp_benchmarks_dir, provider)

    def get_performance_metrics(self):
        return self.get_performance_metrics_cpp()

    def _fill_command_line(self):
        return self._fill_command_line_cpp()
