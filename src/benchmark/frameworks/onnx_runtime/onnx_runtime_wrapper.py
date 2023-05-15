from .onnx_runtime_process import OnnxRuntimeProcess
from ..config_parser.test_reporter_cpp import CppTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class OnnxRuntimeWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.onnx_runtime

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir):
        return OnnxRuntimeProcess.create_process(test, executor, log, cpp_benchmarks_dir)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return CppTest(model, dataset, indep_parameters, dep_parameters)
