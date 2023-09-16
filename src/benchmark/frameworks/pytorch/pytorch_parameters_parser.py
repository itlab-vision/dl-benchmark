from ..config_parser.dependent_parameters_parser import DependentParametersParser
from ..config_parser.framework_parameters_parser import FrameworkParameters


class PyTorchParametersParser(DependentParametersParser):
    def parse_parameters(self, curr_test):
        CONFIG_FRAMEWORK_DEPENDENT_TAG = 'FrameworkDependent'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_NAME_TAG = 'InputName'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SHAPE_TAG = 'InputShape'
        CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG = 'Mean'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG = 'InputScale'
        CONFIG_FRAMEWORK_DEPENDENT_OUTPUT_NAME_TAG = 'OutputName'
        CONFIG_FRAMEWORK_DEPENDENT_MODEL_TYPE_TAG = 'ModelType'
        CONFIG_FRAMEWORK_DEPENDENT_INFERENCE_MODE_TAG = 'InferenceMode'
        CONFIG_FRAMEWORK_DEPENDENT_TENSOR_RT_PRECISION = 'TensorRTPrecision'
        CONFIG_FRAMEWORK_DEPENDENT_LAYOUT = 'Layout'
        CONFIG_FRAMEWORK_DEPENDENT_INPUT_TYPE = 'InputType'
        CONFIG_FRAMEWORK_DEPENDENT_num_inter_threads_TAG = 'InterOpThreads'
        CONFIG_FRAMEWORK_DEPENDENT_num_intra_threads_TAG = 'IntraOpThreads'

        dep_parameters_tag = curr_test.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TAG)[0]

        _input_name = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_NAME_TAG)[0].firstChild
        _input_shape = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SHAPE_TAG)[0].firstChild
        _mean = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MEAN_TAG)[0].firstChild
        _input_scale = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INPUT_SCALE_TAG)[0].firstChild
        _output_name = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_OUTPUT_NAME_TAG)[0].firstChild
        _model_type = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_MODEL_TYPE_TAG)[0].firstChild
        _inference_mode = dep_parameters_tag.getElementsByTagName(
            CONFIG_FRAMEWORK_DEPENDENT_INFERENCE_MODE_TAG)[0].firstChild

        _tensor_rt_precision = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_TENSOR_RT_PRECISION):
            _tensor_rt_precision = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_TENSOR_RT_PRECISION)[0].firstChild

        _layout = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_LAYOUT):
            _layout = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_LAYOUT)[0].firstChild

        _input_type = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_INPUT_TYPE):
            _input_type = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_INPUT_TYPE)[0].firstChild

        _num_inter_threads = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_num_inter_threads_TAG):
            _num_inter_threads = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_num_inter_threads_TAG)[0].firstChild

        _num_intra_threads = None
        if dep_parameters_tag.getElementsByTagName(CONFIG_FRAMEWORK_DEPENDENT_num_intra_threads_TAG):
            _num_intra_threads = dep_parameters_tag.getElementsByTagName(
                CONFIG_FRAMEWORK_DEPENDENT_num_intra_threads_TAG)[0].firstChild

        return PyTorchParameters(
            input_name=_input_name.data if _input_name else None,
            input_shape=_input_shape.data if _input_shape else None,
            mean=_mean.data if _mean else None,
            input_scale=_input_scale.data if _input_scale else None,
            output_name=_output_name.data if _output_name else None,
            model_type=_model_type.data if _model_type else None,
            inference_mode=_inference_mode.data if _inference_mode else None,
            tensor_rt_precision=_tensor_rt_precision.data if _tensor_rt_precision else None,
            layout=_layout.data if _layout else None,
            input_type=_input_type.data if _input_type else None,
            num_inter_threads=_num_inter_threads.data if _num_inter_threads else None,
            num_intra_threads=_num_intra_threads.data if _num_intra_threads else None,
        )


class PyTorchParameters(FrameworkParameters):
    def __init__(self, input_name, input_shape, mean, input_scale, output_name, model_type, inference_mode,
                 tensor_rt_precision, layout, input_type, num_inter_threads, num_intra_threads):
        self.input_name = None
        self.input_shape = None
        self.mean = None
        self.input_scale = None
        self.output_name = None
        self.model_type = None
        self.inference_mode = None
        self.tensor_rt_precision = None
        self.layout = None
        self.input_type = None
        self.num_inter_threads = None
        self.num_intra_threads = None

        if self._parameter_is_not_none(input_name):
            self.input_name = input_name
        if self._parameter_is_not_none(input_shape):
            self.input_shape = input_shape
        if self._parameter_is_not_none(mean):
            self.mean = mean
        if self._parameter_is_not_none(input_scale):
            self.input_scale = input_scale
        if self._parameter_is_not_none(output_name):
            self.output_name = output_name
        if self._parameter_is_not_none(model_type):
            self.model_type = model_type
        if self._parameter_is_not_none(inference_mode):
            self.inference_mode = inference_mode
        if self._parameter_is_not_none(tensor_rt_precision):
            self.tensor_rt_precision = tensor_rt_precision
        if self._parameter_is_not_none(layout):
            self.layout = layout
        if self._parameter_is_not_none(input_type):
            self.input_type = input_type
        if self._parameter_is_not_none(num_inter_threads):
            self.num_inter_threads = num_inter_threads
        if self._parameter_is_not_none(num_intra_threads):
            self.num_intra_threads = num_intra_threads
