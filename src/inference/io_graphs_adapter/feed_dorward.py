from .graph_adapter import IOGraphAdapter


class FeedForwardIO(IOGraphAdapter):
    def __init__(self, args, io_model_wrapper):
        super().__init__(args, io_model_wrapper)

    def process_output(self, result, log):
        return
