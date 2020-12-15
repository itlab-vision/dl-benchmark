import abc
import os
from subprocess import Popen, PIPE, STDOUT


class Executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log

    @staticmethod
    def get_executor(executor_type, log):
        if executor_type == 'host_machine':
            return Host_executor(log)
        else:
            raise ValueError('Wrong executor type!')

    @abc.abstractmethod
    def execute_process(self, command_line):
        pass


class Host_executor(Executor):
    def __init__(self, log):
        super().__init__(log)
        self.my_environment = os.environ.copy()

    def execute_process(self, command_line):
        process = Popen(command_line, env=self.my_environment, shell=True, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
        out, _ = process.communicate()
        with open('log.txt', 'w+') as file:
            file.write(out)
        out = out.split('\n')
        return out
