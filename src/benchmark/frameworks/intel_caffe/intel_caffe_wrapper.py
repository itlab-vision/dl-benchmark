from .intel_caffe_process import IntelCaffeProcess
from .intel_caffe_test import IntelCaffeTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class IntelCaffeWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.caffe

    @staticmethod
    def create_process(test, executor, log, cpp_benchmark_path=None):
        return IntelCaffeProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return IntelCaffeTest(model, dataset, indep_parameters, dep_parameters)
