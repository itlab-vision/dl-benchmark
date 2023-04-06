from .dependent_parameters_parser import DependentParametersParser
from .framework_parameters_cpp import CppParameters


class CppParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        dep_parameters_tag = curr_test.getElementsByTagName('FrameworkDependent')[0]

        _backend = None
        if dep_parameters_tag.getElementsByTagName('Backend'):
            _backend = dep_parameters_tag.getElementsByTagName('Backend')[0].firstChild

        _shape = dep_parameters_tag.getElementsByTagName('InputShape')[0].firstChild
        _layout = dep_parameters_tag.getElementsByTagName('Layout')[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName('Mean')[0].firstChild
        _scale = dep_parameters_tag.getElementsByTagName('InputScale')[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName('ThreadCount')[0].firstChild
        _inference_requests_count = dep_parameters_tag.getElementsByTagName('InferenceRequestsCount')[0].firstChild

        return CppParameters(
            backend=_backend.data if _backend else None,
            shape=_shape.data if _shape else None,
            layout=_layout.data if _layout else None,
            mean=_mean.data if _mean else None,
            scale=_scale.data if _scale else None,
            thread_count=_thread_count.data if _thread_count else None,
            inference_requests_count=_inference_requests_count.data if _inference_requests_count else None,
        )
