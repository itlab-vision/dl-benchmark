import abc
import os
import docker
from subprocess import Popen, PIPE, STDOUT


class executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log
        self.my_target_framework = None

    @staticmethod
    def get_executor(executor_type, log):
        if executor_type == 'host_machine':
            return host_executor(log)
        elif executor_type == 'docker_container':
            return docker_executor(log)
        else:
            raise ValueError('Wrong executor type!')

    def set_target_framework(self, target_framework):
        self.my_target_framework = target_framework.replace(' ', '_')
        self.my_target_framework = self.my_target_framework.replace('dlsdk', 'OpenVINO_DLDT')

    @abc.abstractmethod
    def execute_process(self, command_line):
        pass


class host_executor(executor):
    def __init__(self, log):
        super().__init__(log)
        self.my_environment = os.environ.copy()

    def execute_process(self, command_line):
        process = Popen(command_line, env=self.my_environment, shell=True, stdout=PIPE, stderr=STDOUT,
                        universal_newlines=True)
        out, _ = process.communicate()
        out = out.split('\n')
        return out


class docker_executor(executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        self.my_container_dict = {cont.name: cont for cont in client.containers.list()}

    def execute_process(self, command_line):
        command_line = 'bash -c "source /root/.bashrc && {}"'.format(command_line)
        return self.my_container_dict[self.my_target_framework].exec_run(command_line, tty=True, privileged=True)
