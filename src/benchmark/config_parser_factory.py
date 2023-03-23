from frameworks.intel_caffe.intel_caffe_parameters_parser import IntelCaffeParametersParser
from frameworks.known_frameworks import KnownFrameworks
from frameworks.onnx_runtime.onnx_runtime_parameters_parser import OnnxRuntimeParametersParser
from frameworks.openvino.openvino_parameters_parser import OpenVINOParametersParser
from frameworks.tensorflow.tensorflow_parameters_parser import TensorFlowParametersParser
from frameworks.tensorflow_lite.tensorflow_lite_parameters_parser import TensorFlowLiteParametersParser
from frameworks.mxnet.mxnet_parameters_parser import MXNetParametersParser
from frameworks.opencv.opencv_parameters_parser import OpenCVParametersParser


def get_parameters_parser(framework):
    if framework == KnownFrameworks.caffe:
        return IntelCaffeParametersParser()
    if framework == KnownFrameworks.tensorflow:
        return TensorFlowParametersParser()
    if framework == KnownFrameworks.openvino_dldt:
        return OpenVINOParametersParser()
    if framework == KnownFrameworks.onnx_runtime:
        return OnnxRuntimeParametersParser()
    if framework == KnownFrameworks.tensorflow_lite:
        return TensorFlowLiteParametersParser()
    if framework == KnownFrameworks.mxnet:
        return MXNetParametersParser()
    if framework == KnownFrameworks.opencv:
        return OpenCVParametersParser()
    raise NotImplementedError(f'Unknown framework {framework}')
