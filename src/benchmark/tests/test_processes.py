import logging as log
import sys

import pytest

from src.benchmark.frameworks.framework_wrapper_registry import FrameworkWrapperRegistry
from src.benchmark.frameworks.intel_caffe.intel_caffe_process import IntelCaffeProcess
from src.benchmark.frameworks.known_frameworks import KnownFrameworks
from src.benchmark.frameworks.openvino.openvino_benchmark_process import (OpenVINOBenchmarkPythonProcess,
                                                                          OpenVINOBenchmarkCppProcess,
                                                                          OpenVINOBenchmarkPythonOnnxProcess,
                                                                          OpenVINOBenchmarkCppOnnxProcess)
from src.benchmark.frameworks.openvino.openvino_process import OpenVINOProcess
from src.benchmark.frameworks.openvino.openvino_python_api_process import AsyncOpenVINOProcess, SyncOpenVINOProcess
from src.benchmark.frameworks.processes import ProcessHandler
from src.benchmark.frameworks.tensorflow.tensorflow_process import TensorFlowProcess
from src.benchmark.frameworks.opencv_dnn_cpp.opencv_dnn_cpp_process import OpenCVDNNCppProcess
from src.benchmark.frameworks.onnx_runtime.onnx_runtime_process import OnnxRuntimeProcess
from src.benchmark.frameworks.tensorflow_lite.tensorflow_lite_process import TensorFlowLiteProcess
from src.benchmark.tests.test_executor import get_host_executor

log.basicConfig(
    format='[ %(levelname)s ] %(message)s',
    level=log.INFO,
    stream=sys.stdout,
)


class DotDict(dict):
    """dot.notation access to dictionary attributes. For config mocking."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


OPENVINO_BENCHMARK_RESULT_RAW = """
[Step 11/11] Dumping statistics report
[ INFO ] Statistics report is stored to benchmark_report.csv
[ INFO ] Count:      1000 iterations
[ INFO ] Duration:   37201.83 ms
[ INFO ] Latency:
[ INFO ]        Median:     73.26 ms
[ INFO ]        Average:    74.38 ms
[ INFO ]        Min:        64.50 ms
[ INFO ]        Max:        151.40 ms
[ INFO ] Throughput: 26.88 FPS
[ INFO ] Returncode = 0
[ INFO ] End inference test on model : resnet-50-pytorch
[ INFO ] Saving test result in file
"""
TEST_BASIC_LINE = DotDict({'indep_parameters': DotDict({'inference_framework': 'inference_framework'}),
                           'dep_parameters': DotDict({'mode': 'mode'}),
                           'model': DotDict({'model': 'model'})})

WRAPPER_REGISTRY = FrameworkWrapperRegistry()


@pytest.mark.parametrize('os', [['Linux', 'python3'], ['Windows', 'python']])
def test_python_version(os, mocker):
    mocker.patch('platform.system', return_value=os[0])
    assert ProcessHandler.get_cmd_python_version() == os[1]


@pytest.mark.parametrize('inference_framework', [['OpenVINO DLDT', OpenVINOProcess], ['Caffe', IntelCaffeProcess],
                                                 ['TensorFlow', TensorFlowProcess],
                                                 ['OpenCV DNN Cpp', OpenCVDNNCppProcess],
                                                 ['ONNX Runtime', OnnxRuntimeProcess],
                                                 ['TensorFlowLite', TensorFlowLiteProcess]])
@pytest.mark.parametrize('mode', [['sync', SyncOpenVINOProcess], ['async', AsyncOpenVINOProcess],
                                  ['ovbenchmark_python_latency', OpenVINOBenchmarkPythonProcess],
                                  ['ovbenchmark_python_throughput', OpenVINOBenchmarkPythonProcess],
                                  ['ovbenchmark_cpp_latency', OpenVINOBenchmarkCppProcess],
                                  ['ovbenchmark_cpp_throughput', OpenVINOBenchmarkCppProcess],
                                  ['ovbenchmark_cpp_onnx', OpenVINOBenchmarkCppOnnxProcess],
                                  ['ovbenchmark_python_onnx', OpenVINOBenchmarkPythonOnnxProcess]])
def test_framework_wrapper(inference_framework, mode, mocker):
    test = TEST_BASIC_LINE
    test.indep_parameters.inference_framework = inference_framework[0]
    test.dep_parameters.mode = mode[0]
    wrapper = WRAPPER_REGISTRY[inference_framework[0]]
    mocker.patch('pathlib.Path.is_file', return_value=True)
    if inference_framework[0] == KnownFrameworks.openvino_dldt:
        assert isinstance(wrapper.create_process(test, get_host_executor(mocker), log, 'valid/benchmark/path'),
                          mode[1])
    else:
        assert isinstance(wrapper.create_process(test, get_host_executor(mocker), log, 'valid/benchmark/path'),
                          inference_framework[1])


def test_get_openvino_benchmark_app_metrics(mocker):
    mocker.patch(
        'src.benchmark.frameworks.openvino.openvino_benchmark_process.OpenVINOBenchmarkPythonProcess.'
        '_fill_command_line',
        return_value='ls')
    mocker.patch('src.benchmark.executors.HostExecutor.execute_process',
                 return_value=(0, OPENVINO_BENCHMARK_RESULT_RAW.encode('utf-8')))
    process = OpenVINOBenchmarkPythonProcess(TEST_BASIC_LINE, get_host_executor(mocker), log)
    process._output = OPENVINO_BENCHMARK_RESULT_RAW
    process.execute()
    assert process.get_performance_metrics() == (0.037, 26.88, 0.073)
