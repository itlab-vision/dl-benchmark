import abc
import os
import threading
import sys
import subprocess

import psutil
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
    def get_path_to_inference_folder(self):
        pass

    @abc.abstractmethod
    def get_infrastructure(self):
        pass

    @abc.abstractmethod
    def execute_process(self, command_line, timeout):
        pass


class HostExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)
        self.my_environment = os.environ.copy()
        self.process = None
        self.output = []

    def get_path_to_inference_folder(self):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'inference')

    def get_infrastructure(self):
        sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'node_info'))
        import node_info as info  # noqa: E402

        hardware = info.get_system_characteristics()
        hardware_info = ''
        for key in hardware:
            hardware_info += f'{key}: {hardware[key]}, '
        hardware_info = hardware_info[:-2]

        return hardware_info

    def execute_process(self, command_line, timeout):
        def target(cmd, stdout, stderr):
            self.process = subprocess.Popen(cmd, stdout=stdout, stderr=stderr,
                                            shell=isinstance(cmd, str))

            if stdout != subprocess.DEVNULL:
                self.output = []
                for line in self.process.stdout:
                    line = line.decode('utf-8')
                    self.output.append(line)

                    sys.stdout.write(line)

                sys.stdout.flush()
                self.process.stdout.close()

            self.process.wait()

        thread = threading.Thread(target=target, args=(command_line, subprocess.PIPE, subprocess.STDOUT))
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            try:
                self.my_log.error(f'Timeout {timeout} is reached, terminating')
                self.kill_process(self.process.pid)
                thread.join()
            except OSError as e:
                self.my_log.error(f'Cannot kill task by PID {e.strerror}')
                raise

        if self.process is None:
            return_code = 127
            self.my_log.error('Failed to create process')
        else:
            return_code = self.process.wait()
        self.my_log.info(f'Returncode = {return_code}')

        return return_code, self.output

    def kill_process(self, pid):
        try:
            process = psutil.Process(pid)
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()
        except OSError as err:
            print(err)


class DockerExecutor(Executor):
    def __init__(self, log):
        super().__init__(log)
        client = docker.from_env()
        self.my_container_dict = {cont.name: cont for cont in client.containers.list()}

    def get_path_to_inference_folder(self):
        return '/tmp/dl-benchmark/src/inference'

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

    def execute_process(self, command_line, _):
        command_line = f'bash -c "source /root/.bashrc && {command_line}"'

        return self.my_container_dict[self.my_target_framework].exec_run(command_line, tty=True, privileged=True)
