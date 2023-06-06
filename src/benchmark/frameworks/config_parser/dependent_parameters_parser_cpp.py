from .dependent_parameters_parser import DependentParametersParser
from .framework_parameters_cpp import CppParameters


class CppParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        dep_parameters_tag = curr_test.getElementsByTagName('FrameworkDependent')[0]

        _backend = None
        if dep_parameters_tag.getElementsByTagName('Backend'):
            _backend = dep_parameters_tag.getElementsByTagName('Backend')[0].firstChild

        _provider = None
        if dep_parameters_tag.getElementsByTagName('Provider'):
            _provider = dep_parameters_tag.getElementsByTagName('Provider')[0].firstChild

        _input_type = None
        if dep_parameters_tag.getElementsByTagName('InputType'):
            _input_type = dep_parameters_tag.getElementsByTagName('InputType')[0].firstChild

        _input_shape = dep_parameters_tag.getElementsByTagName('InputShape')[0].firstChild
        _layout = dep_parameters_tag.getElementsByTagName('Layout')[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName('Mean')[0].firstChild
        _input_scale = dep_parameters_tag.getElementsByTagName('InputScale')[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName('ThreadCount')[0].firstChild
        _inference_requests_count = dep_parameters_tag.getElementsByTagName('InferenceRequestsCount')[0].firstChild

        return CppParameters(
            backend=_backend.data if _backend else None,
            provider=_provider.data if _provider else 'Default',
            input_shape=_input_shape.data if _input_shape else None,
            layout=_layout.data if _layout else None,
            mean=_mean.data if _mean else None,
            input_scale=_input_scale.data if _input_scale else None,
            thread_count=_thread_count.data if _thread_count else None,
            inference_requests_count=_inference_requests_count.data if _inference_requests_count else None,
            input_type=_input_type.data if _input_type else None,
        )
