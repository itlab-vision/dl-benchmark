from .dgl_pytorch_process import DGLPyTorchProcess
from ..config_parser.test_reporter import Test
from ..framework_wrapper import FrameworkWrapper
from ..known_frameworks import KnownFrameworks


class DGLPyTorchWrapper(FrameworkWrapper):
    framework_name = KnownFrameworks.dgl_pytorch

    @staticmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None):
        return DGLPyTorchProcess.create_process(test, executor, log)

    @staticmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        return Test(model, dataset, indep_parameters, dep_parameters)
