from .tensorflow_lite_process import TensorFlowLiteProcess
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper


class TensorFlowLiteWrapper(FrameworkWrapper):
    framework_name = 'TensorFlowLite'

    @staticmethod
    def create_process(test, executor, log, cpp_benchmark_path=None, **kwargs):
        return TensorFlowLiteProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return Test(model, dataset, indep_parameters, dep_parameters)
