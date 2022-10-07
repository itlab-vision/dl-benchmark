import abc
import os
import sys
from subprocess import Popen, PIPE

import docker


class Executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log
        self.target_framework = None
        self.my_target_framework = None

    @staticmethod
    def get_executor(executor_type, log):
        if executor_type == 'host_machine':
            return HostExecutor(log)
        elif executor_type == 'docker_container':
            return DockerExecutor(log)

    def set_target_framework(self, target_framework):
        self.my_target_framework = target_framework.replace(' ', '_')

    @abc.abstractmethod
    def get_infrastructure(self):
        pass

    @abc.abstractmethod
    def execute_process(self, command_line):
        pass


class HostExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)
        self.my_environment = os.environ.copy()

    def get_infrastructure(self):
        sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'node_info'))
        import node_info as info  # noqa: E402

        hardware = info.get_system_characteristics()
        hardware_info = ''
        for key in hardware:
            hardware_info += f'{key}: {hardware[key]}, '
        hardware_info = hardware_info[:-2]

        return hardware_info

    def execute_process(self, command_line):
        process = Popen(command_line, env=self.my_environment, shell=True, stdout=PIPE, universal_newlines=True)
        return_code = process.wait()
        out, _ = process.communicate()
        out = out.split('\n')[:-1]

        return return_code, out


class DockerExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        self.my_container_dict = {cont.name: cont for cont in client.containers.list()}

    def get_infrastructure(self):
        hardware_command = 'python3 /tmp/dl-benchmark/src/node_info/node_info.py'
        command_line = f'bash -c "source /root/.bashrc && {hardware_command}"'
        output = self.my_container_dict[self.my_target_framework].exec_run(command_line, tty=True, privileged=True)
        if output[0] != 0:
            return 'None'
        hardware = [line.strip().split(': ') for line in output[-1].decode('utf-8').split('\n')[1:-1]]
        hardware_info = ''
        for line in hardware:
            hardware_info += f'{line[0]}: {line[1]}, '
        hardware_info = hardware_info[:-2]

        return hardware_info

    def execute_process(self, command_line):
        command_line = f'bash -c "source /root/.bashrc && {command_line}"'

        return self.my_container_dict[self.my_target_framework].exec_run(command_line, tty=True, privileged=True)
