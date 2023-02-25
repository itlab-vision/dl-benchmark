from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class TensorFlowLiteParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_CHANNEL_SWAP_TAG = 'ChannelSwap'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG = 'InputScale'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SHAPE_TAG = 'InputShape'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_NAME_TAG = 'InputName'
        CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG = 'Layout'
        CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG = 'ThreadCount'
        CONFIG_FRAMEWORK_DEPENDENT_DELEGATE = 'Delegate'
        CONFIG_FRAMEWORK_DEPENDENT_DELEGATE_OPTIONS = 'DelegateOptions'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _channel_swap = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_CHANNEL_SWAP_TAG)[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        _input_scale = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG)[0].firstChild
        _input_shape = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SHAPE_TAG)[0].firstChild
        _input_name = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_NAME_TAG)[0].firstChild
        _layout = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG)[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG)[0].firstChild
        _delegate = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_DELEGATE)[0].firstChild
        _delegate_options = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_DELEGATE_OPTIONS)[0].firstChild

        return TensorFlowLiteParameters(
            channel_swap=_channel_swap.data if _channel_swap else None,
            mean=_mean.data if _mean else None,
            input_scale=_input_scale.data if _input_scale else None,
            input_shape=_input_shape.data if _input_shape else None,
            input_name=_input_name.data if _input_name else None,
            layout=_layout.data if _layout else None,
            thread_count=_thread_count.data if _thread_count else None,
            delegate=_delegate.data if _delegate else None,
            delegate_options=_delegate_options.data if _delegate_options else None,
        )


class TensorFlowLiteParameters(FrameworkParameters):
    def __init__(self, channel_swap, mean, input_scale, input_shape, layout, input_name,
                 thread_count, delegate, delegate_options):
        self.channel_swap = None
        self.mean = None
        self.input_scale = None
        self.input_shape = None
        self.input_name = None
        self.layout = None
        self.nthreads = None
        self.delegate = None
        self.delegate_options = None

        if self._parameter_not_is_none(channel_swap):
            self.channel_swap = self._process_sequence_arg(channel_swap)
        if self._parameter_not_is_none(mean):
            self.mean = self._process_sequence_arg(mean)
        if self._parameter_not_is_none(input_scale):
            self.input_scale = self._process_sequence_arg(input_scale)
        if self._parameter_not_is_none(input_shape):
            self.input_shape = self._process_sequence_arg(input_shape)
        if self._parameter_not_is_none(input_name):
            self.input_name = input_name
        if self._parameter_not_is_none(layout):
            self.layout = layout
        if self._parameter_not_is_none(thread_count):
            if self._int_value_is_correct(thread_count):
                self.nthreads = thread_count
            else:
                raise ValueError('Threads count can only take integer value')
        if self._parameter_not_is_none(delegate):
            self.delegate = delegate
        if self._parameter_not_is_none(delegate_options):
            self.delegate_options = delegate_options

    @staticmethod
    def _process_sequence_arg(sequence):
        if '[' not in sequence:
            sequence = f'[{sequence}]'
        if ',' not in sequence:
            sequence = sequence.replace(' ', ',')
        return sequence
