import abc
import sys

from constants import Status


class DockerHandler(metaclass=abc.ABCMeta):
    def __init__(self, command_line, log, client, container_id, print_output=True):
        self.command_line = command_line
        self.log = log
        self.docker_client = client
        self.output = []
        self.container_id = container_id
        self.return_code = Status.EXIT_SUCCESS.value
        self.print_output = print_output

    def run(self):
        exec_instance = self.docker_client.api.exec_create(self.container_id, self.command_line,
                                                           privileged=True, tty=False)
        exec_output = self.docker_client.api.exec_start(exec_instance['Id'], tty=False, stream=True)
        self.output = []
        try:
            for stdout_out in exec_output:
                if stdout_out is not None:
                    line = stdout_out.decode('utf-8')
                    if self.print_output:
                        sys.stdout.write(line)
                        sys.stdout.flush()
                    self.output.extend(line.splitlines())
        except Exception as err:
            self.log.error(err)

        exit_metadata = self.docker_client.api.exec_inspect(exec_instance['Id'])
        exit_code = exit_metadata['ExitCode']
        self.exit_code = exit_code if Status.has_value(exit_code) else Status.PROCESS_CMD_ERROR.value
        self.return_code = self.exit_code
        self.log.info(f'Docker returncode = {self.exit_code}')
