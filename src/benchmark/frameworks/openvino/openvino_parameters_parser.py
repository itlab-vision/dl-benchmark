from pathlib import Path

from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class OpenVINOParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_MODE_TAG = 'Mode'
        CONFIG_FRAMEWORK_DEPENDENT_EXTENSION_TAG = 'Extension'
        CONFIG_FRAMEWORK_DEPENDENT_INFER_REQUEST_COUNT_TAG = 'InferenceRequestsCount'
        CONFIG_FRAMEWORK_DEPENDENT_ASYNC_REQUEST_COUNT_TAG = 'AsyncRequestCount'
        CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG = 'ThreadCount'
        CONFIG_FRAMEWORK_DEPENDENT_STREAM_COUNT_TAG = 'StreamCount'
        CONFIG_FRAMEWORK_DEPENDENT_SHAPE_TAG = 'InputShape'
        CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG = 'Layout'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_SCALE_TAG = 'InputScale'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _mode = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MODE_TAG)[0].firstChild
        _extension = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_EXTENSION_TAG)[0].firstChild
        _async_request_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_ASYNC_REQUEST_COUNT_TAG)[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG)[0].firstChild
        _stream_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_STREAM_COUNT_TAG)[0].firstChild

        _infer_request_count = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_INFER_REQUEST_COUNT_TAG):
            _infer_request_count = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_INFER_REQUEST_COUNT_TAG)[0].firstChild

        _shape, _layout, _mean, _input_scale = None, None, None, None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_SHAPE_TAG):
            _shape = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_SHAPE_TAG)[0].firstChild
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG):
            _layout = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG)[0].firstChild
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG):
            _mean = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_SCALE_TAG):
            _input_scale = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_SCALE_TAG)[0].firstChild

        return OpenVINOParameters(
            mode=_mode.data if _mode else None,
            extension=_extension.data if _extension else None,
            infer_request_count=_infer_request_count.data if _infer_request_count else None,
            async_request_count=_async_request_count.data if _async_request_count else None,
            thread_count=_thread_count.data if _thread_count else None,
            stream_count=_stream_count.data if _stream_count else None,
            shape=_shape.data if _shape else None,
            layout=_layout.data if _layout else None,
            mean=_mean.data if _mean else None,
            input_scale=_input_scale.data if _input_scale else None,
        )


class OpenVINOParameters(FrameworkParameters):
    def __init__(self, mode, extension, infer_request_count, async_request_count, thread_count, stream_count,
                 shape, layout, mean, input_scale):
        self.mode = None
        self.extension = None
        self.infer_request = None
        self.async_request = None
        self.nthreads = None
        self.nstreams = None
        self.shape = None
        self.layout = None
        self.mean = None
        self.input_scale = None

        if self._mode_is_correct(mode):
            self.mode = mode.title()
        if self._extension_path_is_correct(extension):
            self.extension = extension
        else:
            raise ValueError('Wrong extension path for device. File not found.')
        if self._parameter_not_is_none(infer_request_count):
            if self._int_value_is_correct(infer_request_count):
                self.infer_request = infer_request_count
        if self.mode == 'Sync' or 'ovbenchmark' in self.mode.lower():
            if self._parameter_not_is_none(thread_count):
                if self._int_value_is_correct(thread_count):
                    self.nthreads = int(thread_count)
                else:
                    raise ValueError('Thread count can only take values: integer greater than zero.')
        if self.mode == 'Async':
            if self._parameter_not_is_none(async_request_count):
                if self._int_value_is_correct(async_request_count):
                    self.async_request = async_request_count
                else:
                    raise ValueError('Async requiest count can only take values: integer greater than zero.')
        if self.mode == 'Async' or 'ovbenchmark' in self.mode.lower():
            if self._parameter_not_is_none(stream_count):
                if self._int_value_is_correct(stream_count):
                    self.nstreams = stream_count
                else:
                    raise ValueError('Stream count can only take values: integer greater than zero.')

        if 'ovbenchmark' in self.mode.lower():
            if self._parameter_not_is_none(shape):
                self.shape = shape.strip()
            if self._parameter_not_is_none(layout):
                self.layout = layout.strip()

        if 'onnx' in self.mode.lower():
            if self._parameter_not_is_none(mean):
                if self._mean_is_correct(mean):
                    self.mean = mean.strip()
                else:
                    raise ValueError('Mean can only take values: list of 3 float elements.')
            if self._parameter_not_is_none(input_scale):
                self.input_scale = input_scale.strip()

    @staticmethod
    def _mode_is_correct(mode):
        const_correct_mode = ['sync', 'async',
                              'ovbenchmark_python_latency', 'ovbenchmark_python_throughput', 'ovbenchmark_python_onnx',
                              'ovbenchmark_cpp_latency', 'ovbenchmark_cpp_throughput', 'ovbenchmark_cpp_onnx']
        if mode.lower() in const_correct_mode:
            return True
        raise ValueError(f'Mode is a required parameter. Mode can only take values: {", ".join(const_correct_mode)}')

    def _extension_path_is_correct(self, extension):
        return not self._parameter_not_is_none(extension) or Path(extension).exists()
