import abc


class DependentParametersParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_parameters(self, curr_test):
        pass
