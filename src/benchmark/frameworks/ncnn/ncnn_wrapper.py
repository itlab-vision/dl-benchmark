from .ncnn_process import NcnnProcess
from .ncnn_test import NcnnTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class NcnnWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.ncnn

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None):
        return NcnnProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return NcnnTest(model, dataset, indep_parameters, dep_parameters)
