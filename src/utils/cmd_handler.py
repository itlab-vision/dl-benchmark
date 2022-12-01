import abc
import os
import subprocess
import threading
import sys

from constants import Status


class CMDHandler(metaclass=abc.ABCMeta):
    def __init__(self, command_line, log, env=None):
        self.command_line = command_line
        self.log = log
        self.env = env
        self.output = []
        self.process = None
        self.return_code = 0

    def run(self, timeout):

        def target(stdout, stderr):
            self.process = subprocess.Popen(self.command_line, stdout=stdout, stderr=stderr, env=self.env,
                                            shell=isinstance(self.command_line, str))

            if stdout != subprocess.DEVNULL:
                self.output = []
                for line in self.process.stdout:
                    line = line.decode('utf-8')
                    self.output.append(line)

                    sys.stdout.write(line)

                sys.stdout.flush()
                self.process.stdout.close()

            self.process.wait()

        thread = threading.Thread(target=target, args=(subprocess.PIPE, subprocess.STDOUT))
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.return_code = Status.PROCESS_TIMEOUT.value
            try:
                self.log.error(f'Timeout {timeout} is reached, terminating')
                self.kill_process_by_pid(self.process.pid)
                thread.join()
            except OSError as e:
                self.log.error(f'Cannot kill task by PID {e.strerror}')

        if self.process is None:
            self.return_code = Status.PROCESS_CREATE_ERROR.value
            self.log.error(f'Failed to create process for {self.command_line}')
        else:
            self.return_code = self.process.wait()
        self.log.info(f'Returncode = {self.return_code}')

    def kill_process_by_pid(self, pid):
        try:
            if sys.platform == 'win32':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)])
            else:
                os.system(f'pkill -TERM -P {pid}')
        except OSError as err:
            print(err)
