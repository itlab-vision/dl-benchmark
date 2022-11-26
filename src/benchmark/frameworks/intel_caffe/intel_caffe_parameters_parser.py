from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class IntelCaffeParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_CHANNEL_SWAP_TAG = 'ChannelSwap'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG = 'InputScale'
        CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG = 'ThreadCount'
        CONFIG_FRAMEWORK_DEPENDENT_KMP_AFFINITY_TAG = 'KmpAffinity'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _channel_swap = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_CHANNEL_SWAP_TAG)[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        _input_scale = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG)[0].firstChild
        _thread_count = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_THREAD_COUNT_TAG)[0].firstChild
        _kmp_affinity = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_KMP_AFFINITY_TAG)[0].firstChild

        return IntelCaffeParameters(
            channel_swap=_channel_swap.data if _channel_swap else None,
            mean=_mean.data if _mean else None,
            input_scale=_input_scale.data if _input_scale else None,
            thread_count=_thread_count.data if _thread_count else None,
            kmp_affinity=_kmp_affinity.data if _kmp_affinity else None,
        )


class IntelCaffeParameters(FrameworkParameters):
    def __init__(self, channel_swap, mean, input_scale, thread_count, kmp_affinity):
        self.channel_swap = None
        self.mean = None
        self.input_scale = None
        self.nthreads = None
        self.kmp_affinity = None

        if self._parameter_not_is_none(channel_swap):
            if self._channel_swap_is_correct(channel_swap):
                self.channel_swap = channel_swap
            else:
                raise ValueError('Channel swap can only take values: list of unique values 0, 1, 2.')
        if self._parameter_not_is_none(mean):
            if self._mean_is_correct(mean):
                self.mean = mean
            else:
                raise ValueError('Mean can only take values: list of 3 float elements.')
        if self._parameter_not_is_none(input_scale):
            if self._float_value_is_correct(input_scale):
                self.input_scale = input_scale
            else:
                raise ValueError('Input scale can only take values: float greater than zero.')
        if self._parameter_not_is_none(thread_count):
            if self._int_value_is_correct(thread_count):
                self.nthreads = thread_count
            else:
                raise ValueError('Threads count can only take integer value')
        if self._parameter_not_is_none(kmp_affinity):
            self.kmp_affinity = kmp_affinity
