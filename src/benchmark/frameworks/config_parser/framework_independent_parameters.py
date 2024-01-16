from .framework_parameters_parser import FrameworkParameters


class FrameworkIndependentParameters(FrameworkParameters):
    def __init__(self, inference_framework, batch_size, device, num_devices, iterarion_count, test_time_limit,
                 timeout_overhead, custom_models_links=None, raw_output=True):
        self.inference_framework = None
        self.batch_size = None
        self.device = None
        self.num_devices = num_devices
        self.iteration = None
        self.test_time_limit = None
        self.custom_models_links = custom_models_links
        self.raw_output = raw_output
        if self._parameter_is_not_none(inference_framework):
            self.inference_framework = inference_framework
        else:
            raise ValueError('Inference framework is required parameter.')
        if batch_size is not None:
            if self._int_value_is_correct(batch_size):
                self.batch_size = int(batch_size)
            else:
                raise ValueError('Batch size can only take values: integer greater than zero.'
                                 'Set "None" as batch value to ignore this argument in inference app')
        if self._parameter_is_not_none(device):
            self.device = device.upper()
        else:
            raise ValueError('Device is required parameter.')
        if self._parameter_is_not_none(iterarion_count) and self._int_value_is_correct(iterarion_count):
            self.iteration = int(iterarion_count)
        else:
            raise ValueError('Iteration count is required parameter. '
                             'Iteration count can only take values: integer greater than zero.')

        if self._parameter_is_not_none(test_time_limit):
            self.test_time_limit = int(test_time_limit)
        else:
            raise ValueError('Test time limit is required parameter. '
                             'Test time limit can only `take values: float greater than zero.')

        if self._parameter_is_not_none(timeout_overhead):
            self.timeout_overhead = int(timeout_overhead)
        else:
            default_timeout_overhead = 300
            self.timeout_overhead = default_timeout_overhead
