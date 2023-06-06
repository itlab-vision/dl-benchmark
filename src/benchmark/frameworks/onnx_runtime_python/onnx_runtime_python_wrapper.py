from .onnx_runtime_python_process import ONNXRuntimePythonProcess
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class ONNXRuntimePythonWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.onnx_runtime_python

    @staticmethod
    def create_process(test, executor, log, **kwargs):
        return ONNXRuntimePythonProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return Test(model, dataset, indep_parameters, dep_parameters)
