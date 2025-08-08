from .executorch_process import ExecuTorchProcess
from .executorch_test import ExecuTorchTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class ExecuTorchWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.executorch

    @staticmethod
    def create_process(test, executor, log, **kwargs):
        return ExecuTorchProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return ExecuTorchTest(model, dataset, indep_parameters, dep_parameters)
