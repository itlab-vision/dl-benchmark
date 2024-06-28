from .paddlepaddle_process import PaddlePaddleProcess
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper


class PaddlePaddleWrapper(FrameworkWrapper):
    framework_name = 'PaddlePaddle'

    @staticmethod
    def create_process(test, executor, log, cpp_benchmark_path=None, **kwargs):
        return PaddlePaddleProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return Test(model, dataset, indep_parameters, dep_parameters)
