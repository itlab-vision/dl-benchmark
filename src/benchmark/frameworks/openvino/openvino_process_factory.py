from .openvino_benchmark_process import OpenVINOBenchmarkPythonProcess, OpenVINOBenchmarkCppProcess
from .openvino_python_api_process import AsyncOpenVINOProcess, SyncOpenVINOProcess


def create_process(test, executor, log, cpp_benchmark_path=None):
    mode = test.dep_parameters.mode.lower()
    if mode == 'sync':
        return SyncOpenVINOProcess(test, executor, log)
    if mode == 'async':
        return AsyncOpenVINOProcess(test, executor, log)
    if mode == 'ovbenchmark_python_latency':
        return OpenVINOBenchmarkPythonProcess(test, executor, log, 'latency')
    if mode == 'ovbenchmark_python_throughput':
        return OpenVINOBenchmarkPythonProcess(test, executor, log, 'throughput')
    if mode == 'ovbenchmark_cpp_latency':
        return OpenVINOBenchmarkCppProcess(test, executor, log, cpp_benchmark_path, 'latency')
    if mode == 'ovbenchmark_cpp_throughput':
        return OpenVINOBenchmarkCppProcess(test, executor, log, cpp_benchmark_path, 'throughput')
    raise AssertionError(f'Unknown openvino running mode {mode}')
