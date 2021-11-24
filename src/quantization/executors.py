import abc
import docker
import os
from subprocess import Popen, PIPE, STDOUT


class executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log


    @staticmethod
    def get_executor(executor_type, log):
        if executor_type == 'host_machine':
            return host_executor(log)
        elif executor_type == 'docker_container':
            return docker_executor(log)
        else:
            raise ValueError('Wrong executor type!')


    @abc.abstractmethod
    def execute_process(self, command_line):
        pass


class host_executor(executor):
    def __init__(self, log):
        super().__init__(log)
        self.my_environment = os.environ.copy()


    def execute_process(self, command_line):
        process = Popen(
            command_line,
            env=self.my_environment,
            shell=True,
            stdout=PIPE,
            stderr=STDOUT,
            universal_newlines=True
        )
        out, _ = process.communicate()
        return out



class docker_executor(executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        # self.my_containers = {cont for cont in client.containers.list()}
        self.my_container_dict = {cont.name: cont for cont in client.containers.list()}


    def execute_process(self, command_line):
        command_line = 'bash -c "source /root/.bashrc && {}"'.format(command_line)
        out = []

        # for cont in self.my_containers:
        #     out.append(cont.exec_run(command_line, tty=True, privileged=True))
        out.append(self.my_containers['OpenVINO_DLDT'].exec_run(
            command_line,
            tty=True,
            privileged=True
        ))
        return out
