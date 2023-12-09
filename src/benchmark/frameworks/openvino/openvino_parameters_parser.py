from pathlib import Path

from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class OpenVINOParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_MODE_TAG = 'Mode'
        CONFIG_FRAMEWORK_DEPENDENT_CODE_SOURCE_TAG = 'CodeSource'
        CONFIG_FRAMEWORK_DEPENDENT_RUNTIME_TAG = 'Runtime'
        CONFIG_FRAMEWORK_DEPENDENT_HINT_TAG = 'Hint'
        CONFIG_FRAMEWORK_DEPENDENT_FRONTEND_TAG = 'Frontend'
        CONFIG_FRAMEWORK_DEPENDENT_EXTENSION_TAG = 'Extension'
        CONFIG_FRAMEWORK_DEPENDENT_INFER_REQUEST_COUNT_TAG = 'InferenceRequestsCount'
        CONFIG_FRAMEWORK_DEPENDENT_ASYNC_REQUEST_COUNT_TAG = 'AsyncRequestCount'
        CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG = 'ThreadCount'
        CONFIG_FRAMEWORK_DEPENDENT_STREAM_COUNT_TAG = 'StreamCount'
        CONFIG_FRAMEWORK_DEPENDENT_SHAPE_TAG = 'InputShape'
        CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG = 'Layout'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_SCALE_TAG = 'InputScale'
        CONFIG_FRAMEWORK_DEPENDENT_CHANGE_PREPROC_OPTIONS_TAG = 'ChangePreprocessOptions'
        CONFIG_FRAMEWORK_DEPENDENT_NUM_OUTPUT_TOKENS_LLM_TAG = 'NumOutputTokensLLM'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _mode = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MODE_TAG)[0].firstChild

        _code_source, _runtime, _hint = None, None, None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_CODE_SOURCE_TAG):
            _code_source = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_CODE_SOURCE_TAG)[0].firstChild
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_RUNTIME_TAG):
            _runtime = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_RUNTIME_TAG)[0].firstChild
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_HINT_TAG):
            _hint = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_HINT_TAG)[0].firstChild

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

        _frontend = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_FRONTEND_TAG):
            _frontend = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_FRONTEND_TAG)[0].firstChild

        _shape, _layout, _mean, _input_scale = None, None, None, None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_SHAPE_TAG):
            _shape = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_SHAPE_TAG)[0].firstChild
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG):
            _layout = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG)[0].firstChild
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG):
            _mean = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_SCALE_TAG):
            _input_scale = dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_SCALE_TAG)[0].firstChild

        _num_output_tokens = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_NUM_OUTPUT_TOKENS_LLM_TAG):
            _num_output_tokens = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_NUM_OUTPUT_TOKENS_LLM_TAG)[0].firstChild

        _change_preproc_options = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_CHANGE_PREPROC_OPTIONS_TAG):
            _change_preproc_options = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_CHANGE_PREPROC_OPTIONS_TAG)[0].firstChild

        return OpenVINOParameters(
            mode=_mode.data if _mode else None,
            code_source=_code_source.data if _code_source else 'handwritten',
            runtime=_runtime.data if _runtime else None,
            hint=_hint.data if _hint else None,
            frontend=_frontend.data if _frontend else 'IR',
            extension=_extension.data if _extension else None,
            infer_request_count=_infer_request_count.data if _infer_request_count else None,
            async_request_count=_async_request_count.data if _async_request_count else None,
            thread_count=_thread_count.data if _thread_count else None,
            stream_count=_stream_count.data if _stream_count else None,
            shape=_shape.data if _shape else None,
            layout=_layout.data if _layout else None,
            mean=_mean.data if _mean else None,
            input_scale=_input_scale.data if _input_scale else None,
            change_preproc_options=_change_preproc_options.data if _change_preproc_options else None,
            num_output_tokens=_num_output_tokens.data if _num_output_tokens else None,
        )


class OpenVINOParameters(FrameworkParameters):
    def __init__(self, mode, code_source, runtime, hint, frontend, extension,
                 infer_request_count, async_request_count, thread_count, stream_count,
                 shape, layout, mean, input_scale, change_preproc_options, num_output_tokens):
        self.mode = None
        self.code_source = None
        self.runtime = None
        self.hint = None
        self.frontend = None
        self.extension = None
        self.infer_request = None
        self.async_request = None
        self.nthreads = None
        self.nstreams = None
        self.shape = None
        self.layout = None
        self.mean = None
        self.input_scale = None
        self.change_preproc_options = None
        self.num_output_tokens = None

        if self._mode_is_correct(mode):
            self.mode = mode.title()

        if self._code_source_is_correct(code_source):
            self.code_source = code_source

        if self._parameter_is_not_none(runtime):
            if self._runtime_is_correct(runtime):
                self.runtime = runtime
        else:
            if self.code_source == 'ovbenchmark':
                self.runtime = 'python'

        if self._parameter_is_not_none(hint):
            if self._hint_is_correct(hint):
                self.hint = hint
        else:
            if self.code_source == 'ovbenchmark':
                self.hint = 'latency'

        if self._extension_path_is_correct(extension):
            self.extension = extension
        else:
            raise ValueError('Wrong extension path for device. File not found.')

        if self._parameter_is_not_none(infer_request_count):
            if self._int_value_is_correct(infer_request_count):
                self.infer_request = infer_request_count
            if self.code_source == 'ovbenchmark' and self.hint != 'none':
                raise ValueError(f'Cannot set nireq for ovbenchmark and hint {self.hint}')

        if self.mode == 'Sync' or self.code_source == 'ovbenchmark':
            if self._parameter_is_not_none(thread_count):
                if self._int_value_is_correct(thread_count):
                    self.nthreads = int(thread_count)
                else:
                    raise ValueError('Thread count can only take values: integer greater than zero.')

        if self.mode == 'Async' and self.code_source == 'handwritten':
            if self._parameter_is_not_none(async_request_count):
                if self._int_value_is_correct(async_request_count):
                    self.async_request = async_request_count
                else:
                    raise ValueError('Async request count can only take values: integer greater than zero.')

        if self.mode == 'Async' or self.code_source == 'ovbenchmark':
            if self._parameter_is_not_none(stream_count):
                if self._int_value_is_correct(stream_count):
                    self.nstreams = stream_count
                else:
                    raise ValueError('Stream count can only take values: integer greater than zero.')

        if self.code_source == 'ovbenchmark':
            if self._parameter_is_not_none(shape):
                self.shape = shape.strip()
            if self._parameter_is_not_none(layout):
                self.layout = layout.strip()

        if self._frontend_is_correct(frontend):
            self.frontend = frontend if frontend else 'IR'
        if self.frontend != 'IR':
            if self._parameter_is_not_none(mean):
                if self._mean_is_correct(mean):
                    self.mean = mean.strip()
                else:
                    raise ValueError('Mean can only take values: list of 3 float elements.')
            if self._parameter_is_not_none(input_scale):
                self.input_scale = input_scale.strip()
            if self._parameter_is_not_none(change_preproc_options):
                if change_preproc_options != 'Rename':
                    raise ValueError('Only "Rename" option is available')
                else:
                    self.change_preproc_options = change_preproc_options

        if num_output_tokens is not None:
            if self._int_value_is_correct(num_output_tokens):
                self.num_output_tokens = int(num_output_tokens)
            else:
                raise ValueError('NumOutputTokensLLM can only take values: integer greater than zero.')

    @staticmethod
    def _mode_is_correct(mode):
        const_correct_mode = ['sync', 'async']
        if mode.lower() in const_correct_mode:
            return True
        raise ValueError(f'Mode is a required parameter. Mode can only take values: {", ".join(const_correct_mode)}')

    @staticmethod
    def _code_source_is_correct(code_source):
        const_correct_code_source = ['ovbenchmark', 'handwritten']
        if code_source.lower() in const_correct_code_source:
            return True
        raise ValueError(f'SourceCode can only take values: {", ".join(const_correct_code_source)}')

    @staticmethod
    def _runtime_is_correct(runtime):
        const_correct_runtime = ['cpp', 'python']
        if runtime.lower() in const_correct_runtime:
            return True
        raise ValueError(f'Runtime is an optional parameter (by default it is empty), '
                         f'but if not empty Runtime can only take values: {", ".join(const_correct_runtime)}')

    @staticmethod
    def _hint_is_correct(hint):
        const_correct_hint = ['latency', 'throughput', 'none']
        if hint.lower() in const_correct_hint:
            return True
        raise ValueError(f'Hint is an optional parameter (by default it is empty), '
                         f'but if not empty Hint can only take values: {", ".join(const_correct_hint)}')

    @staticmethod
    def _frontend_is_correct(frontend):
        const_correct_frontend = ['ir', 'tensorflow', 'tensorflow_lite', 'onnx']
        if not frontend:
            return True
        if frontend.lower() in const_correct_frontend:
            return True
        raise ValueError('Frontend is an optional parameter (by default it is ir), '
                         f'but Frontend can only take values: {", ".join(const_correct_frontend)}')

    def _extension_path_is_correct(self, extension):
        return not self._parameter_is_not_none(extension) or Path(extension).exists()
