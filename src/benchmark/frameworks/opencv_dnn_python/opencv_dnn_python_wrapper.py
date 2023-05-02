from .opencv_dnn_python_process import OpenCVDNNPythonProcess
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class OpenCVDNNPythonWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.opencv_dnn_python

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None, **kwargs):
        return OpenCVDNNPythonProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return Test(model, dataset, indep_parameters, dep_parameters)
