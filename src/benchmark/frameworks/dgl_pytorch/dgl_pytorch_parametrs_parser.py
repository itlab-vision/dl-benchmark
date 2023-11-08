from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class DGLPyTorchParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_INFERENCE_MODE_TAG = 'InferenceMode'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _inference_mode = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INFERENCE_MODE_TAG)[0].firstChild

        return DGLPyTorchParameters(
            inference_mode=_inference_mode.data if _inference_mode else None,
        )


class DGLPyTorchParameters(FrameworkParameters):
    def __init__(self, inference_mode):
        self.inference_mode = None

        if self._parameter_is_not_none(inference_mode):
            self.inference_mode = inference_mode
