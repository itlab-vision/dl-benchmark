import logging as log

from .intel_caffe.intel_caffe_wrapper import IntelCaffeWrapper
from .openvino.openvino_wrapper import OpenVINOWrapper
from .singleton import Singleton
from .tensorflow.tensorflow_wrapper import TensorFlowWrapper
from .onnx_runtime.onnx_runtime_wrapper import OnnxRuntimeWrapper
from .tensorflow_lite.tensorflow_lite_wrapper import TensorFlowLiteWrapper
from .opencv_dnn_python.opencv_dnn_python_wrapper import OpenCVDNNPythonWrapper
from .mxnet.mxnet_wrapper import MXNetWrapper
from .opencv_dnn_cpp.opencv_dnn_cpp_wrapper import OpenCVDNNCppWrapper


class FrameworkWrapperRegistry(metaclass=Singleton):
    """Storage for all found framework wrappers.
    Framework wrapper is represented by a FrameworkWrapper subclass located in
    a separate package (openvino, tensorflow etc) inside frameworks package.
    """

    def __init__(self):
        self._framework_wrappers = {}
        self._get_wrappers()
        log.info(f'Available framework wrappers: {", ".join(self._framework_wrappers.keys())}')

    def __getitem__(self, framework_name):
        """Get framework wrapper by framework name"""
        if framework_name in self._framework_wrappers:
            return self._framework_wrappers[framework_name]
        raise ValueError(f'Unsupported framework name: {framework_name}. '
                         f'Available framework wrappers: {", ".join(self._framework_wrappers.keys())}')

    def _get_wrappers(self):
        self._framework_wrappers[IntelCaffeWrapper.framework_name] = IntelCaffeWrapper()
        self._framework_wrappers[TensorFlowWrapper.framework_name] = TensorFlowWrapper()
        self._framework_wrappers[OpenVINOWrapper.framework_name] = OpenVINOWrapper()
        self._framework_wrappers[OnnxRuntimeWrapper.framework_name] = OnnxRuntimeWrapper()
        self._framework_wrappers[TensorFlowLiteWrapper.framework_name] = TensorFlowLiteWrapper()
        self._framework_wrappers[OpenCVDNNPythonWrapper.framework_name] = OpenCVDNNPythonWrapper()
        self._framework_wrappers[MXNetWrapper.framework_name] = MXNetWrapper()
        self._framework_wrappers[OpenCVDNNCppWrapper.framework_name] = OpenCVDNNCppWrapper()

