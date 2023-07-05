from abc import ABC

from ..processes import ProcessHandler


class OpenVINOProcess(ProcessHandler, ABC):
    benchmark_app_name = None
    launcher_latency_units = None

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    def extract_inference_param(self, key):
        return None
