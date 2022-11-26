from .tensorflow_process import TensorFlowProcess
from .tensorflow_test import TensorFlowTest
from ..framework_wrapper import FrameworkWrapper


class TensorFlowWrapper(FrameworkWrapper):
    framework_name = 'TensorFlow'

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None):
        return TensorFlowProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return TensorFlowTest(model, dataset, indep_parameters, dep_parameters)
