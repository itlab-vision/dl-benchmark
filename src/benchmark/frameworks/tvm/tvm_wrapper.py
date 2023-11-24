from .tvm_process import TVMProcess
from .tvm_test import TVMTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class TVMWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.tvm

    @staticmethod
    def create_process(test, executor, log, **kwargs):
        return TVMProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return TVMTest(model, dataset, indep_parameters, dep_parameters)
