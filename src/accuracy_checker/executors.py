import abc
import os
import docker
from subprocess import Popen, PIPE, STDOUT


class executor(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log
        self.my_target_framework = None
        self.my_environment = os.environ.copy()

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

    @abc.abstractmethod
    def execute_process(self, command_line):
        pass

    @abc.abstractmethod
    def prepare_executor(self, tests):
        pass

    @abc.abstractmethod
    def prepare_command_line(self, test, command_line):
        pass


class host_executor(executor):
    def __init__(self, log):
        super().__init__(log)

    def execute_process(self, command_line):
        process = Popen(command_line, env=self.my_environment, shell=True, stdout=PIPE, stderr=STDOUT,
                        universal_newlines=True)
        out, _ = process.communicate()
        out = out.split('\n')
        return out

    def prepare_executor(self, tests):
        pass

    def prepare_command_line(self, test, command_line):
        return command_line


class docker_executor(executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        self.my_container_dict = {cont.name: cont for cont in client.containers.list()}

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
        return self.__copy_config(test.model.config, command_line)

    def __copy_config(self, path_to_config, command_line):
        docker_config = '/tmp/config.yml'
        cp_command = 'docker cp -L {0} {1}:{2}'.format(path_to_config, self.my_target_framework, docker_config)
        process = Popen(cp_command, env=self.my_environment, shell=True, stdout=PIPE, stderr=STDOUT,
                        universal_newlines=True)
        process.communicate()

        return command_line.replace(path_to_config, docker_config)

    def execute_process(self, command_line):
        command_line = 'bash -c "source /root/.bashrc && {}"'.format(command_line)
        _, out = self.my_container_dict[self.my_target_framework].exec_run(command_line, tty=True, privileged=True)
        return out
