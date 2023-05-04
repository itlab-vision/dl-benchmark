from .intel_caffe_process import IntelCaffeProcess
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class IntelCaffeWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.caffe

    @staticmethod
    def create_process(test, executor, log, **kwargs):
        return IntelCaffeProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return Test(model, dataset, indep_parameters, dep_parameters)
