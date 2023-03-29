from .opencv_dnn_python_process import OpenCVDNNPythonProcess
from .opencv_dnn_python_test import OpenCVDNNPythonTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class OpenCVDNNPythonWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.opencv

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None):
        return OpenCVDNNPythonProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return OpenCVDNNPythonTest(model, dataset, indep_parameters, dep_parameters)
