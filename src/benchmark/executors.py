import abc
import docker
import os
import platform
from subprocess import Popen, PIPE

PATH_TO_AUXILIARY = '../auxiliary'
sys.path.append(os.path.abspath(PATH_TO_AUXILIARY))
import node_info as info


class executor(metaclass = abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log
        self.my_target = None

    @staticmethod
    def get_executor(env_type, log):
        if env_type == 'host_machine':
            return linux_remote_helper(log)
        elif env_type == 'docker_container':
            return windows_remote_hepler(log)

    def set_target(self, target):
        self.my_target = target

    @abc.abstractmethod
    def get_infrastructure(self):
        pass

    @abc.abstractmethod
    def execute_process(self, command_line):
        pass

class host_executor(executor):
    def __init__(self, log):
        super().__init__(log)

    def get_infrastructure(self):
        hardware = info.get_system_characteristics()
        hardware_info = ''
        for key in hardware:
            hardware_info += '{}: {}, '.format(key, hardware[key])
        hardware_info = hardware_info[:-2]

        return hardware_info

    def execute_process(self, command_line):
        process = Popen(command_line, env = os.environ.copy(), shell = True,
        stdout = PIPE, universal_newlines = True)
        return_code = process.wait()
        out, _ = process.communicate()
        out = out.split('\n')[:-1]
        return return_code, out

class docker_executor(executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        self.my_container_dict = { container.name: container for container in client.containers.list() }

    def get_infrastructure(self):
        pass

    def execute_process(self, command_line):
        return self.my_container_dict[self.my_target].exec_run(command_line, privileged=True)
