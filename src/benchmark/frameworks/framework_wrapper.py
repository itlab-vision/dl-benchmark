from abc import ABCMeta, abstractmethod


class FrameworkWrapper(metaclass=ABCMeta):
    """Base abstract class for framework wrapper.
    The framework_name attribute should be initialized in a derived class
    with framework name string used in configuration file."""

    framework_name = ''

    def __init_subclass__(cls):
        if not isinstance(cls.framework_name, str) or len(cls.framework_name) == 0:
            raise NotImplementedError(f'Static attribute framework_name is not initialized in class {cls.__name__}')

    @staticmethod
    @abstractmethod
    def create_process(test, executor, log, cpp_benchmarks_dir=None, **kwargs):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_test(model, dataset, indep_parameters, dep_parameters):
        raise NotImplementedError()
