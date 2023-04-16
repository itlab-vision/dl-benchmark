from frameworks.intel_caffe.intel_caffe_parameters_parser import IntelCaffeParametersParser
from frameworks.known_frameworks import KnownFrameworks
from frameworks.openvino.openvino_parameters_parser import OpenVINOParametersParser
from frameworks.tensorflow.tensorflow_parameters_parser import TensorFlowParametersParser
from frameworks.tensorflow_lite.tensorflow_lite_parameters_parser import TensorFlowLiteParametersParser
from frameworks.mxnet.mxnet_parameters_parser import MXNetParametersParser
from frameworks.opencv_dnn_python.opencv_dnn_python_parameters_parser import OpenCVDNNPythonParametersParser
from frameworks.pytorch.pytorch_parameters_parser import PyTorchParametersParser
from frameworks.config_parser.dependent_parameters_parser_cpp import CppParametersParser


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
    if framework == KnownFrameworks.mxnet:
        return MXNetParametersParser()
    if framework == KnownFrameworks.opencv_dnn_python:
        return OpenCVDNNPythonParametersParser()
    if framework == KnownFrameworks.opencv_dnn_cpp:
        return CppParametersParser()
    if framework == KnownFrameworks.pytorch:
        return PyTorchParametersParser()
    raise NotImplementedError(f'Unknown framework {framework}')
