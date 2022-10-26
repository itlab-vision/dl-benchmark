from abc import ABC

from ..processes import ProcessHandler


class OpenVINOProcess(ProcessHandler, ABC):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def __add_nthreads_for_cmd_line(command_line, nthreads):
        return f'{command_line} -nthreads {nthreads}'
