from .tensorflow_lite_process import TensorFlowLiteProcess
from .tensorflow_lite_test import TensorFlowLiteTest
from ..framework_wrapper import FrameworkWrapper


class TensorFlowLiteWrapper(FrameworkWrapper):
    framework_name = 'TensorFlowLite'

    @staticmethod
    def create_process(test, executor, log, cpp_benchmark_path=None):
        return TensorFlowLiteProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return TensorFlowLiteTest(model, dataset, indep_parameters, dep_parameters)
