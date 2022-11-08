from frameworks.intel_caffe.intel_caffe_parameters_parser import IntelCaffeParametersParser
from frameworks.known_frameworks import KnownFrameworks
from frameworks.onnx_runtime.onnx_runtime_parameters_parser import OnnxRuntimeParametersParser
from frameworks.openvino.openvino_parameters_parser import OpenVINOParametersParser
from frameworks.tensorflow.tensorflow_parameters_parser import TensorFlowParametersParser


def get_parameters_parser(framework):
    if framework == KnownFrameworks.caffe:
        return IntelCaffeParametersParser()
    if framework == KnownFrameworks.tensorflow:
        return TensorFlowParametersParser()
    if framework == KnownFrameworks.openvino_dldt:
        return OpenVINOParametersParser()
    if framework == KnownFrameworks.onnx_runtime:
        return OnnxRuntimeParametersParser()
    raise NotImplementedError(f'Unknown framework {framework}')
