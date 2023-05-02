from .openvino_benchmark_process import OpenVINOBenchmarkPythonProcess, OpenVINOBenchmarkCppProcess
from .openvino_python_api_process import AsyncOpenVINOProcess, SyncOpenVINOProcess


def create_process(test, executor, log, cpp_benchmarks_dir=None, **kwargs):
    mode = test.dep_parameters.mode.lower()
    code_source = test.dep_parameters.code_source
    runtime = test.dep_parameters.runtime
    hint = test.dep_parameters.hint
    if mode == 'sync' and code_source == 'handwritten':
        return SyncOpenVINOProcess(test, executor, log)
    if mode == 'async' and code_source == 'handwritten':
        return AsyncOpenVINOProcess(test, executor, log)
    if code_source == 'ovbenchmark' and runtime == 'python':
        return OpenVINOBenchmarkPythonProcess(test, executor, log, hint, mode)
    if code_source == 'ovbenchmark' and runtime == 'cpp':
        return OpenVINOBenchmarkCppProcess(test, executor, log, cpp_benchmarks_dir, hint, mode)
    raise AssertionError('Unsupportend combination of: '
                         f'openvino running mode {mode}, '
                         f'code_source {code_source}, '
                         f'runtime {runtime}, '
                         f'hint {hint}')
