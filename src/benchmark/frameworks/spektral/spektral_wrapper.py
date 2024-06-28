from .spektral_process import SpektralProcess
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper


class SpektralWrapper(FrameworkWrapper):
    framework_name = 'Spektral'

    @staticmethod
    def create_process(test, executor, log, **kwargs):
        return SpektralProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return Test(model, dataset, indep_parameters, dep_parameters)
