from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class OnnxRuntimeParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        dep_parameters_tag = curr_test.getElementsByTagName('FrameworkDependent')[0]

        _shape = dep_parameters_tag.getElementsByTagName('Shape')[0].firstChild
        _layout = dep_parameters_tag.getElementsByTagName('Layout')[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName('Mean')[0].firstChild
        _scale = dep_parameters_tag.getElementsByTagName('Scale')[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName('ThreadCount')[0].firstChild
        _inference_requests_count = dep_parameters_tag.getElementsByTagName('InferenceRequestsCount')[0].firstChild

        return OnnxRuntimeParameters(
            shape=_shape.data if _shape else None,
            layout=_layout.data if _layout else None,
            mean=_mean.data if _mean else None,
            scale=_scale.data if _scale else None,
            thread_count=_thread_count.data if _thread_count else None,
            inference_requests_count=_inference_requests_count.data if _inference_requests_count else None,
        )


class OnnxRuntimeParameters(FrameworkParameters):
    def __init__(self, shape, layout, mean, scale, thread_count, inference_requests_count):
        self.shape = None
        self.layout = None
        self.mean = None
        self.scale = None
        self.thread_count = None
        self.inference_requests_count = None

        if shape is not None:
            self.shape = shape.strip()
        if layout is not None:
            self.layout = layout.strip()
        if mean is not None:
            self.mean = mean.strip()
        if scale is not None:
            self.scale = scale.strip()
        if thread_count is not None and self._int_value_is_correct(thread_count):
            self.thread_count = thread_count
        if inference_requests_count is not None and self._int_value_is_correct(inference_requests_count):
            self.inference_requests_count = inference_requests_count
