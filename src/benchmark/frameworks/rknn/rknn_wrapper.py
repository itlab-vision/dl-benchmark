from .rknn_process import RknnProcess
from ..config_parser.test_reporter_cpp import CppTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class RknnWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.rknn

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir, **kwargs):
        return RknnProcess.create_process(test, executor, log, cpp_benchmarks_dir)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return CppTest(model, dataset, indep_parameters, dep_parameters)
