from .mxnet_process import MXNetProcess
from .mxnet_test import MXNetTest
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class MXNetWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.mxnet

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None):
        return MXNetProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return MXNetTest(model, dataset, indep_parameters, dep_parameters)
