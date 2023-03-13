from .opencv_process import OpenCVProcess
from .opencv_test import OpenCVTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class OpenCVWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.opencv

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir):
        return OpenCVProcess.create_process(test, executor, log, cpp_benchmarks_dir)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return OpenCVTest(model, dataset, indep_parameters, dep_parameters)
