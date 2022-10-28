import abc
import os
import sys
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT

import docker


class Executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log
        self.my_target_framework = None
        self.my_environment = os.environ.copy()
        self.path_to_csv_file = Path(__file__).resolve().parent.joinpath('result.csv')

    @staticmethod
    def get_executor(executor_type, log):
        if executor_type == 'host_machine':
            return HostExecutor(log)
        elif executor_type == 'docker_container':
            return DockerExecutor(log)
        else:
            raise ValueError('Wrong executor type!')

    def set_target_framework(self, target_framework):
        self.my_target_framework = target_framework.replace(' ', '_')

    def get_path_to_result_file(self):
        return self.path_to_csv_file

    @abc.abstractmethod
    def get_csv_file(self):
        pass

    @abc.abstractmethod
    def get_infrastructure(self):
        pass

    @abc.abstractmethod
    def execute_process(self, command_line):
        pass

    @abc.abstractmethod
    def prepare_executor(self, tests):
        pass

    @abc.abstractmethod
    def prepare_command_line(self, test, command_line):
        pass


class HostExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)

    def get_infrastructure(self):
        sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('node_info')))
        import node_info as info  # noqa: E402

        hardware = info.get_system_characteristics()
        hardware_info = ''
        for key in hardware:
            hardware_info += f'{key}: {hardware[key]}, '
        hardware_info = hardware_info[:-2]

        return hardware_info

    def execute_process(self, command_line):
        if self.path_to_csv_file.is_file():
            command_line = f'rm {self.path_to_csv_file} && {command_line}'
        process = Popen(command_line, env=self.my_environment, shell=True, stdout=PIPE, stderr=STDOUT,
                        universal_newlines=True)
        out, _ = process.communicate()
        out = out.split('\n')

        return out

    def get_csv_file(self):
        return str(self.path_to_csv_file)

    def prepare_executor(self, tests):
        pass

    def prepare_command_line(self, test, command_line):
        return command_line


class DockerExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        self.my_container_dict = {cont.name: cont for cont in client.containers.list()}
        self.path_to_docker_csv_file = '/tmp/result.csv'

    def prepare_executor(self, tests):
        old_path = tests[0].parameters.definitions
        dataset_definitions = '/tmp/dataset_definitions.yml'
        frameworks = set()
        for test in tests:
            test.parameters.definitions = dataset_definitions
            frameworks.add(test.framework.replace(' ', '_'))

        for framework in frameworks:
            cp_command = 'docker cp -L {0} {1}:{2}'.format(old_path, framework, dataset_definitions)
            process = Popen(cp_command, env=self.my_environment, shell=True, stdout=PIPE, stderr=STDOUT,
                            universal_newlines=True)
            process.communicate()

    def prepare_command_line(self, test, command_line):
        return self.__copy_config(test.config, command_line)

    def get_csv_file(self):
        return self.path_to_docker_csv_file

    def execute_process(self, command_line):
        self.my_container_dict[self.my_target_framework].exec_run(f'rm {self.get_csv_file()}', tty=True,
                                                                  privileged=True)
        command_line = f'bash -c "source /root/.bashrc && {command_line}"'
        _, out = self.my_container_dict[self.my_target_framework].exec_run(command_line, tty=True, privileged=True)
        self.move_csv_file_with_results()

        return out

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

    def move_csv_file_with_results(self):
        cp_command = 'docker cp -L {0}:{1} {2}'.format(self.my_target_framework,
                                                       self.path_to_docker_csv_file,
                                                       self.path_to_csv_file)
        process = Popen(cp_command, env=self.my_environment, shell=True, stdout=PIPE, stderr=STDOUT,
                        universal_newlines=True)
        process.communicate()

    def __copy_config(self, path_to_config, command_line):
        docker_config = '/tmp/config.yml'
        cp_command = 'docker cp -L {0} {1}:{2}'.format(path_to_config, self.my_target_framework, docker_config)
        process = Popen(cp_command, env=self.my_environment, shell=True, stdout=PIPE, stderr=STDOUT,
                        universal_newlines=True)
        process.communicate()

        return command_line.replace(path_to_config, docker_config)
