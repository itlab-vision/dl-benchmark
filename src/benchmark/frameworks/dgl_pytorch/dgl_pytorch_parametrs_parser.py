from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class DGLPyTorchParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_num_inter_threads_TAG = 'InterOpThreads'
        CONFIG_FRAMEWORK_DEPENDENT_num_intra_threads_TAG = 'IntraOpThreads'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _num_inter_threads = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_num_inter_threads_TAG):
            _num_inter_threads = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_num_inter_threads_TAG)[0].firstChild

        _num_intra_threads = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_num_intra_threads_TAG):
            _num_intra_threads = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_num_intra_threads_TAG)[0].firstChild

        return DGLPyTorchParameters(
            num_inter_threads=_num_inter_threads.data if _num_inter_threads else None,
            num_intra_threads=_num_intra_threads.data if _num_intra_threads else None,
        )


class DGLPyTorchParameters(FrameworkParameters):
    def __init__(self, num_inter_threads, num_intra_threads):
        self.num_inter_threads = None
        self.num_intra_threads = None

        if self._parameter_is_not_none(num_inter_threads):
            self.num_inter_threads = num_inter_threads
        if self._parameter_is_not_none(num_intra_threads):
            self.num_intra_threads = num_intra_threads
