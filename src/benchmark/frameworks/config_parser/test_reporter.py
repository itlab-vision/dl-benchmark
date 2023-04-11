import abc
import logging as log


class Test(metaclass=abc.ABCMeta):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        self.model = model
        self.dataset = dataset
        self.indep_parameters = indep_parameters
        self.dep_parameters = dep_parameters
        self._log = log

    @abc.abstractmethod
    def get_report(self, process):
        pass

    @staticmethod
    def _get_optional_parameters_string(parameters_dict):
        parameter_strings = []
        for key in parameters_dict:
            if parameters_dict[key] is not None:
                parameter_strings.append(f'{key}: {parameters_dict[key]}')
        return ', '.join(parameter_strings)
