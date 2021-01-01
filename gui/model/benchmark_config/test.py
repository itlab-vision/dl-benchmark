class Test:
    def __init__(self, model=None, dataset=None, framework=None, batch_size=None, device=None, iter_count=None,
                 test_time_limit=None, mode=None, extension=None, async_req_count=None, thread_count=None,
                 stream_count=None, channel_swap=None, mean=None, input_scale=None):
        self.model = model
        self.dataset = dataset
        self.framework = framework
        self.batch_size = batch_size
        self.device = device
        self.iter_count = iter_count
        self.test_time_limit = test_time_limit
        self.mode = mode
        self.extension = extension
        self.async_req_count = async_req_count
        self.thread_count = thread_count
        self.stream_count = stream_count
        self.channel_swap = channel_swap
        self.mean = mean
        self.input_scale = input_scale

    def get_values_list(self):
        return [self.model, self.dataset, self.framework, self.batch_size, self.device, self.iter_count, self.test_time_limit,
                self.mode, self.extension, self.async_req_count, self.thread_count, self.stream_count, self.channel_swap,
                self.mean, self.input_scale]

    def grouping_dependent_values_check(self, other):
        self_values = self.get_values_list()
        other_values = other.get_values_list()
        independent_parameters_count = 7
        openvino_parameters_count = 5
        for i in range(independent_parameters_count):
            if self_values[i] != other_values[i]:
                return None
        if self.framework == 'OpenVINO DLDT':
            count = 0
            parameter = 0
            for i in range(independent_parameters_count, independent_parameters_count + openvino_parameters_count):
                if self_values[i] != other_values[i]:
                    parameter = i
                    count += 1
        if self.framework == 'Caffe':
            count = 0
            parameter = 0
            for i in range(independent_parameters_count + openvino_parameters_count, len(self_values)):
                if self_values[i] != other_values[i]:
                    parameter = i
                    count += 1
        if count != 1:
            return None
        else:
            return parameter

    def grouping_independent_values_check(self, other):
        if self.framework != other.framework:
            return None
        self_values = self.get_values_list()
        other_values = other.get_values_list()
        independent_parameters_count = 7
        openvino_parameters_count = 5
        if self.framework == 'OpenVINO DLDT':
            for i in range(independent_parameters_count, independent_parameters_count + openvino_parameters_count):
                if self_values[i] != other_values[i]:
                    return None
        if self.framework == 'Caffe':
            for i in range(independent_parameters_count + openvino_parameters_count, len(self_values)):
                if self_values[i] != other_values[i]:
                    return None
        count = 0
        parameter = 0
        for i in range(independent_parameters_count):
            if self_values[i] != other_values[i]:
                parameter = i
                count += 1
        if count != 1:
            return None
        else:
            return parameter
