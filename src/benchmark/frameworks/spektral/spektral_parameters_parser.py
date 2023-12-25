from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class SpektralParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        return SpektralParameters(
        )


class SpektralParameters(FrameworkParameters):
    def __init__(self):
        pass
