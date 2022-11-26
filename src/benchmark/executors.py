import abc
import os
import sys
from pathlib import Path

import docker

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from cmd_handler import CMDHandler  # noqa: E402, PLC0411


class Executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.log = log
        self.target_framework = None

    @staticmethod
    def get_executor(executor_type, log):
        if executor_type == 'host_machine':
            return HostExecutor(log)
        if executor_type == 'docker_container':
            return DockerExecutor(log)
        raise ValueError('Executor type must be from list: host_machine, docker_container')

    def set_target_framework(self, target_framework):
        self.target_framework = target_framework.replace(' ', '_')

    @abc.abstractmethod
    def get_path_to_inference_folder(self):
        pass

    @abc.abstractmethod
    def get_infrastructure(self):
        pass

    @abc.abstractmethod
    def execute_process(self, command_line, timeout):
        pass

    @abc.abstractmethod
    def get_path_to_logs_folder(self):
        pass

    @abc.abstractmethod
    def get_file_content(self, path):
        pass


class HostExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)
        self.environment = os.environ.copy()

    def get_path_to_inference_folder(self):
        return str(Path(__file__).resolve().parents[1].joinpath('inference'))

    def get_infrastructure(self):
        sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('node_info')))
        import node_info as info  # noqa: E402

        hardware = info.get_system_characteristics()
        hardware_info = ''
        for key in hardware:
            hardware_info += f'{key}: {hardware[key]}, '
        hardware_info = hardware_info[:-2]

        return hardware_info

    def execute_process(self, command_line, timeout):
        cmd_handler = CMDHandler(command_line, self.log, self.environment)
        cmd_handler.run(timeout)
        return cmd_handler.return_code, cmd_handler.output

    def get_path_to_logs_folder(self):
        logs_folder = Path().resolve().joinpath('logs')
        logs_folder.mkdir(exist_ok=True)
        return logs_folder

    def get_file_content(self, path):
        with open(path) as file:
            return file.read()


class DockerExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        self.container_dict = {cont.name: cont for cont in client.containers.list()}

    def get_path_to_inference_folder(self):
        return '/tmp/dl-benchmark/src/inference'

    def get_infrastructure(self):
        hardware_command = 'python3 /tmp/dl-benchmark/src/node_info/node_info.py'
        command_line = f'bash -c "source /root/.bashrc && {hardware_command}"'
        output = self.container_dict[self.target_framework].exec_run(command_line, tty=True, privileged=True)
        if output[0] != 0:
            return 'None'
        hardware = [line.strip().split(': ') for line in output[-1].decode('utf-8').split('\n')[1:-1]]
        hardware_info = ''
        for line in hardware:
            hardware_info += f'{line[0]}: {line[1]}, '
        hardware_info = hardware_info[:-2]

        return hardware_info

    def execute_process(self, command_line, _):
        command_line = f'bash -c "source /root/.bashrc && {command_line}"'
        return self.container_dict[self.target_framework].exec_run(command_line, tty=True, privileged=True)

    def get_path_to_logs_folder(self):
        raise NotImplementedError()

    def get_file_content(self, path):
        raise NotImplementedError()
