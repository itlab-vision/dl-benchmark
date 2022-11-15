import abc
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from cmd_handler import CMDHandler  # noqa: E402, PLC0411


class Executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.log = log
        self.environment = os.environ.copy()

    @staticmethod
    def get_executor(executor_type, log):
        if executor_type == 'host_machine':
            return HostExecutor(log)
        else:
            raise ValueError('Wrong executor type!')

    @abc.abstractmethod
    def execute_process(self, command_line):
        pass


class HostExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)

    def execute_process(self, command_line):
        cmd_handler = CMDHandler(command_line, self.log, self.environment)
        cmd_handler.run(None)

        return cmd_handler.return_code, cmd_handler.output
