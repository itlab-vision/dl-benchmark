from .mxnet_process import MXNetProcess
from .mxnet_test import MXNetTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class MXNetWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.mxnet

    @staticmethod
    def create_process(test, executor, log, **kwargs):
        return MXNetProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return MXNetTest(model, dataset, indep_parameters, dep_parameters)
