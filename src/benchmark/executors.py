import abc
import docker
import os
from subprocess import Popen, PIPE


class executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log
        self.target_framework = None

    @staticmethod
    def get_executor(executor_type, log):
        if executor_type == 'host_machine':
            return host_executor(log)
        elif executor_type == 'docker_container':
            return docker_executor(log)

    def set_target_framework(self, target_framework):
        self.my_target_framework = target_framework.replace(' ', '_')

    @abc.abstractmethod
    def get_path_to_inference_folder(self):
        pass

    @abc.abstractmethod
    def get_infrastructure(self):
        pass

    @abc.abstractmethod
    def execute_process(self, command_line):
        pass


class host_executor(executor):
    def __init__(self, log):
        super().__init__(log)
        self.my_environment = os.environ.copy()

    def get_path_to_inference_folder(self):
        return '../inference'

    def get_infrastructure(self):
        import node_info as info
        hardware = info.get_system_characteristics()
        hardware_info = ''
        for key in hardware:
            hardware_info += '{}: {}, '.format(key, hardware[key])
        hardware_info = hardware_info[:-2]
        return hardware_info

    def execute_process(self, command_line):
        process = Popen(command_line, env=self.my_environment, shell=True, stdout=PIPE, universal_newlines=True)
        return_code = process.wait()
        out, _ = process.communicate()
        out = out.split('\n')[:-1]
        return return_code, out


class docker_executor(executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        self.my_container_dict = {cont.name: cont for cont in client.containers.list()}

    def get_path_to_inference_folder(self):
        return '/tmp/openvino-dl-benchmark/src/inference'

    def get_infrastructure(self):
        hardware_command = 'python3 /tmp/openvino-dl-benchmark/src/benchmark/node_info.py'
        command_line = 'bash -c "source /root/.bashrc && {}"'.format(hardware_command)
        output = self.my_container_dict[self.my_target_framework].exec_run(command_line, tty=True, privileged=True)
        if output[0] != 0:
            return 'None'
        hardware = [line.strip().split(': ') for line in output[-1].decode("utf-8").split('\n')[1:-1]]
        hardware_info = ''
        for line in hardware:
            hardware_info += '{}: {}, '.format(line[0], line[1])
        hardware_info = hardware_info[:-2]
        return hardware_info

    def execute_process(self, command_line):
        command_line = 'bash -c "source /root/.bashrc && {}"'.format(command_line)
        return self.my_container_dict[self.my_target_framework].exec_run(command_line, tty=True, privileged=True)
