from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class OpenCVParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_BACKEND_TAG = 'Backend'
        CONFIG_FRAMEWORK_DEPENDENT_SCALEFACTOR_TAG = 'Scalefactor'
        CONFIG_FRAMEWORK_DEPENDENT_SIZE_TAG = 'Size'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_SWAP_RB_TAG = 'SwapRB'
        CONFIG_FRAMEWORK_DEPENDENT_CROP_TAG = 'Crop'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _backend = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_BACKEND_TAG)[0].firstChild
        _scalefactor = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_SCALEFACTOR_TAG)[0].firstChild
        _size = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_SIZE_TAG)[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        _swapRB = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_SWAP_RB_TAG)[0].firstChild
        _crop = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_CROP_TAG)[0].firstChild

        return OpenCVParameters(
            backend=_backend.data if _backend else None,
            scalefactor=_scalefactor.data if _scalefactor else None,
            size=_size.data if _size else None,
            mean=_mean.data if _mean else None,
            swapRB=_swapRB.data if _swapRB else None,
            crop=_crop.data if _crop else None,
        )


class OpenCVParameters(FrameworkParameters):
    def __init__(self, backend, scalefactor, size, mean, swapRB, crop):
        self.backend = None
        self.scalefactor = None
        self.size = None
        self.mean = None
        self.swapRB = None
        self.crop = None

        if self._parameter_not_is_none(backend):
            self.backend = backend
        if self._parameter_not_is_none(scalefactor):
            self.scalefactor = scalefactor
        if self._parameter_not_is_none(size):
            self.size = size
        if self._parameter_not_is_none(mean):
            self.mean = mean
        if self._parameter_not_is_none(swapRB):
            self.swapRB = swapRB
        if self._parameter_not_is_none(crop):
            self.crop = crop
