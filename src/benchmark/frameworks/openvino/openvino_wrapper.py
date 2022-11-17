from .openvino_process_factory import create_process
from .openvino_test import OpenVINOTest
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class OpenVINOWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.openvino_dldt

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None):
        return create_process(test, executor, log, cpp_benchmarks_dir)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return OpenVINOTest(model, dataset, indep_parameters, dep_parameters)
