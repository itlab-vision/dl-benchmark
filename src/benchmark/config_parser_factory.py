from frameworks.intel_caffe.intel_caffe_parameters_parser import IntelCaffeParametersParser
from frameworks.known_frameworks import KnownFrameworks
from frameworks.openvino.openvino_parameters_parser import OpenVINOParametersParser
from frameworks.tensorflow.tensorflow_parameters_parser import TensorFlowParametersParser
from frameworks.tensorflow_lite.tensorflow_lite_parameters_parser import TensorFlowLiteParametersParser
from frameworks.mxnet.mxnet_parameters_parser import MXNetParametersParser
from frameworks.opencv_dnn_python.opencv_dnn_python_parameters_parser import OpenCVDNNPythonParametersParser
from frameworks.pytorch.pytorch_parameters_parser import PyTorchParametersParser
from frameworks.onnx_runtime_python.onnx_runtime_python_parameters_parser import ONNXRuntimePythonParametersParser
from frameworks.config_parser.dependent_parameters_parser_cpp import CppParametersParser
from frameworks.dgl_pytorch.dgl_pytorch_parametrs_parser import DGLPyTorchParametersParser
from frameworks.tvm.tvm_parameters_parser import TVMParametersParser
from frameworks.ncnn.ncnn_parameters_parser import NcnnParametersParser
from frameworks.spektral.spektral_parameters_parser import SpektralParametersParser


def get_parameters_parser(framework):
    if framework == KnownFrameworks.caffe:
        return IntelCaffeParametersParser()
    if framework == KnownFrameworks.tensorflow:
        return TensorFlowParametersParser()
    if framework == KnownFrameworks.openvino_dldt:
        return OpenVINOParametersParser()
    if framework == KnownFrameworks.onnx_runtime:
        return CppParametersParser()
    if framework == KnownFrameworks.tensorflow_lite:
        return TensorFlowLiteParametersParser()
    if framework == KnownFrameworks.tensorflow_lite_cpp:
        return CppParametersParser()
    if framework == KnownFrameworks.mxnet:
        return MXNetParametersParser()
    if framework == KnownFrameworks.opencv_dnn_python:
        return OpenCVDNNPythonParametersParser()
    if framework == KnownFrameworks.onnx_runtime_python:
        return ONNXRuntimePythonParametersParser()
    if framework == KnownFrameworks.opencv_dnn_cpp:
        return CppParametersParser()
    if framework == KnownFrameworks.pytorch:
        return PyTorchParametersParser()
    if framework == KnownFrameworks.pytorch_cpp:
        return CppParametersParser()
    if framework == KnownFrameworks.dgl_pytorch:
        return DGLPyTorchParametersParser()
    if framework == KnownFrameworks.tvm:
        return TVMParametersParser()
    if framework == KnownFrameworks.ncnn:
        return NcnnParametersParser()
    if framework == KnownFrameworks.spektral:
        return SpektralParametersParser()
    if framework == KnownFrameworks.rknn:
        return CppParametersParser()
    raise NotImplementedError(f'Unknown framework {framework}')
