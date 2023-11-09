from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class OpenCVDNNPythonParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_BACKEND_TAG = 'Backend'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG = 'InputScale'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SHAPE_TAG = 'InputShape'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_NAME_TAG = 'InputName'
        CONFIG_FRAMEWORK_DEPENDENT_OUTPUT_NAMES_TAG = 'OutputNames'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_STD_TAG = 'Std'
        CONFIG_FRAMEWORK_DEPENDENT_SWAP_RB_TAG = 'SwapRB'
        CONFIG_FRAMEWORK_DEPENDENT_CROP_TAG = 'Crop'
        CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG = 'Layout'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _backend = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_BACKEND_TAG)[0].firstChild
        _input_scale = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG)[0].firstChild
        _input_shape = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SHAPE_TAG)[0].firstChild
        _input_name = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_NAME_TAG)[0].firstChild
        _output_names = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_OUTPUT_NAMES_TAG)[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        _std = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_STD_TAG)[0].firstChild
        _swapRB = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_SWAP_RB_TAG)[0].firstChild
        _crop = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_CROP_TAG)[0].firstChild
        _layout = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_LAYOUT_TAG)[0].firstChild

        return OpenCVParameters(
            backend=_backend.data if _backend else None,
            input_scale=_input_scale.data if _input_scale else None,
            input_shape=_input_shape.data if _input_shape else None,
            input_name=_input_name.data if _input_name else None,
            output_names=_output_names.data if _output_names else None,
            mean=_mean.data if _mean else None,
            std=_std.data if _std else None,
            swapRB=_swapRB.data if _swapRB else None,
            crop=_crop.data if _crop else None,
            layout=_layout.data if _layout else None,
        )


class OpenCVParameters(FrameworkParameters):
    def __init__(self, backend, input_scale, input_name, output_names,
                 input_shape, mean, std, swapRB, crop, layout):
        self.backend = None
        self.input_scale = None
        self.input_shape = None
        self.input_name = None
        self.output_names = None
        self.mean = None
        self.std = None
        self.swapRB = None
        self.crop = None
        self.layout = None

        if self._parameter_is_not_none(backend):
            self.backend = backend
        if self._parameter_is_not_none(input_scale):
            self.input_scale = input_scale
        if self._parameter_is_not_none(input_name):
            self.input_name = input_name
        if self._parameter_is_not_none(output_names):
            self.output_names = output_names
        if self._parameter_is_not_none(input_shape):
            self.input_shape = input_shape
        if self._parameter_is_not_none(mean):
            self.mean = mean
        if self._parameter_is_not_none(std):
            self.std = std
        if self._parameter_is_not_none(swapRB):
            self.swapRB = swapRB
        if self._parameter_is_not_none(crop):
            self.crop = crop
        if self._parameter_is_not_none(layout):
            self.layout = layout
