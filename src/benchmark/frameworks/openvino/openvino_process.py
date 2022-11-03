from abc import ABC

from ..processes import ProcessHandler


class OpenVINOProcess(ProcessHandler, ABC):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)
