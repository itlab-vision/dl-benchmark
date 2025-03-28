from .executorch_cpp_process import ExecuTorchCppProcess
from ..config_parser.test_reporter_cpp import CppTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class ExecuTorchCppWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.executorch_cpp

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir, **kwargs):
        return ExecuTorchCppProcess.create_process(test, executor, log, cpp_benchmarks_dir)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return CppTest(model, dataset, indep_parameters, dep_parameters)
