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