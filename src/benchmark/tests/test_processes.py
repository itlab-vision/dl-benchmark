import logging as log
import sys

import pytest

from src.benchmark.frameworks.framework_wrapper_registry import FrameworkWrapperRegistry
from src.benchmark.frameworks.intel_caffe.intel_caffe_process import IntelCaffeProcess
from src.benchmark.frameworks.known_frameworks import KnownFrameworks
from src.benchmark.frameworks.mxnet.mxnet_process import MXNetProcess
from src.benchmark.frameworks.tvm.tvm_process import TVMProcess
from src.benchmark.frameworks.onnx_runtime.onnx_runtime_process import OnnxRuntimeProcess
from src.benchmark.frameworks.onnx_runtime_python.onnx_runtime_python_process import ONNXRuntimePythonProcess
from src.benchmark.frameworks.opencv_dnn_cpp.opencv_dnn_cpp_process import OpenCVDNNCppProcess
from src.benchmark.frameworks.opencv_dnn_python.opencv_dnn_python_process import OpenCVDNNPythonProcess
from src.benchmark.frameworks.openvino.openvino_benchmark_process import (OpenVINOBenchmarkPythonProcess,
                                                                          OpenVINOBenchmarkCppProcess)
from src.benchmark.frameworks.openvino.openvino_process import OpenVINOProcess
from src.benchmark.frameworks.openvino.openvino_python_api_process import AsyncOpenVINOProcess, SyncOpenVINOProcess
from src.benchmark.frameworks.processes import ProcessHandler
from src.benchmark.frameworks.pytorch.pytorch_process import PyTorchProcess
from src.benchmark.frameworks.pytorch_cpp.pytorch_cpp_process import PyTorchCppProcess
from src.benchmark.frameworks.tensorflow.tensorflow_process import TensorFlowProcess
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


@pytest.mark.parametrize('inference_framework', [['OpenVINO DLDT', OpenVINOProcess],
                                                 ['Caffe', IntelCaffeProcess],
                                                 ['TensorFlow', TensorFlowProcess],
                                                 ['OpenCV DNN Cpp', OpenCVDNNCppProcess],
                                                 ['ONNX Runtime', OnnxRuntimeProcess],
                                                 ['TensorFlowLite', TensorFlowLiteProcess],
                                                 ['PyTorch', PyTorchProcess],
                                                 ['PyTorch Cpp', PyTorchCppProcess],
                                                 ['MXNet', MXNetProcess],
                                                 ['OpenCV DNN Python', OpenCVDNNPythonProcess],
                                                 ['ONNX Runtime Python', ONNXRuntimePythonProcess],
                                                 ['TVM', TVMProcess],
                                                 ])
@pytest.mark.parametrize('complex_test', [['sync', 'handwritten', None, SyncOpenVINOProcess],
                                          ['async', 'handwritten', None, AsyncOpenVINOProcess],
                                          ['sync', 'ovbenchmark', 'python', OpenVINOBenchmarkPythonProcess],
                                          ['sync', 'ovbenchmark', 'cpp', OpenVINOBenchmarkCppProcess],
                                          ['async', 'ovbenchmark', 'python', OpenVINOBenchmarkPythonProcess],
                                          ['async', 'ovbenchmark', 'cpp', OpenVINOBenchmarkCppProcess],
                                          ])
def test_framework_wrapper(inference_framework, complex_test, mocker):
    test = TEST_BASIC_LINE
    test.indep_parameters.inference_framework = inference_framework[0]
    test.dep_parameters.mode = complex_test[0]
    test.dep_parameters.code_source = complex_test[1]
    test.dep_parameters.runtime = complex_test[2]
    test.dep_parameters.provider = 'Default'
    wrapper = WRAPPER_REGISTRY[inference_framework[0]]
    mocker.patch('pathlib.Path.is_file', return_value=True)
    if inference_framework[0] == KnownFrameworks.openvino_dldt:
        assert isinstance(wrapper.create_process(test, get_host_executor(mocker), log,
                                                 cpp_benchmarks_dir='valid/benchmark/path'),
                          complex_test[-1])
    else:
        assert isinstance(wrapper.create_process(test, get_host_executor(mocker), log,
                                                 cpp_benchmarks_dir='valid/benchmark/path'),
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
    assert process.get_performance_metrics() == {'average_time': 0.0372,
                                                 'batch_fps': 0.0,
                                                 'latency_per_token': 'N/A',
                                                 'fps': 26.88,
                                                 'latency': 0.07326}
