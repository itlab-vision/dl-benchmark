from .framework_parameters_parser import FrameworkParameters


class CppParameters(FrameworkParameters):
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
