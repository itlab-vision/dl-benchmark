from .openvino_benchmark_process import (OpenVINOBenchmarkPythonProcess, OpenVINOBenchmarkCppProcess,
                                         OpenVINOBenchmarkPythonOnnxProcess, OpenVINOBenchmarkCppOnnxProcess)
from .openvino_python_api_process import AsyncOpenVINOProcess, SyncOpenVINOProcess


def create_process(test, executor, log, cpp_benchmarks_dir=None):
    mode = test.dep_parameters.mode.lower()
    if mode == 'sync':
        return SyncOpenVINOProcess(test, executor, log)
    if mode == 'async':
        return AsyncOpenVINOProcess(test, executor, log)
    if mode == 'ovbenchmark_python_latency':
        return OpenVINOBenchmarkPythonProcess(test, executor, log, 'latency')
    if mode == 'ovbenchmark_python_throughput':
        return OpenVINOBenchmarkPythonProcess(test, executor, log, 'throughput')
    if mode == 'ovbenchmark_python_onnx':
        return OpenVINOBenchmarkPythonOnnxProcess(test, executor, log)
    if mode == 'ovbenchmark_cpp_latency':
        return OpenVINOBenchmarkCppProcess(test, executor, log, cpp_benchmarks_dir, 'latency')
    if mode == 'ovbenchmark_cpp_throughput':
        return OpenVINOBenchmarkCppProcess(test, executor, log, cpp_benchmarks_dir, 'throughput')
    if mode == 'ovbenchmark_cpp_onnx':
        return OpenVINOBenchmarkCppOnnxProcess(test, executor, log, cpp_benchmarks_dir)
    raise AssertionError(f'Unknown openvino running mode {mode}')
