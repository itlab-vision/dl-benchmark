from .tensorflow_process import TensorFlowProcess
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper


class TensorFlowWrapper(FrameworkWrapper):
    framework_name = 'TensorFlow'

    @staticmethod
    def create_process(test, executor, log, **kwargs):
        return TensorFlowProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return Test(model, dataset, indep_parameters, dep_parameters)
