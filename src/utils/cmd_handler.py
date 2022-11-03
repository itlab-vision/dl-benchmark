import abc
import subprocess
import threading
import sys
import psutil


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
            try:
                self.log.error(f'Timeout {timeout} is reached, terminating')
                self.kill_process_by_pid(self.process.pid)
                thread.join()
            except OSError as e:
                self.log.error(f'Cannot kill task by PID {e.strerror}')
                raise

        if self.process is None:
            self.return_code = 127
            self.log.error(f'Failed to create process for {self.command_line}')
        else:
            self.return_code = self.process.wait()
        self.log.info(f'Returncode = {self.return_code}')

    def kill_process_by_pid(self, pid):
        try:
            process = psutil.Process(pid)
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()
        except OSError as err:
            print(err)
