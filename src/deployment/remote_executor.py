import time
from remote_helper import RemoteHelper


class RemoteExecutor:
    def __init__(self, os_type, python ,log):
        self.my_active_connection = None
        self.my_machine_ip = None
        self.my_process_list = []
        self.my_remote_helper = RemoteHelper.get_remote_helper(os_type.lower(), python, log)
        self.my_wait_counter = 10  # seconds
        self.my_attempts_counter = 3
        self.my_status = ''

    def create_connection(self, machine_ip, login, password):
        self.my_machine_ip = machine_ip

        for _ in range(self.my_attempts_counter):
            try:
                self.my_active_connection = self.my_remote_helper.connect(machine_ip, login, password)
                break
            except Exception:
                time.sleep(self.my_wait_counter)

    def execute_command(self, command, executor=None):
        if executor is None:
            executor = self.my_remote_helper.execute

        if self.my_active_connection is None:
            self.my_status = f'Error: can not connect to {self.my_machine_ip}!'
            return None

        new_process = None
        for _ in range(self.my_attempts_counter):
            try:
                new_process = executor(self.my_active_connection, command)
                break
            except Exception:
                time.sleep(self.my_wait_counter)

        if new_process is not None:
            self.my_process_list.append(new_process)
        else:
            self.my_status = f'Error: failed to creat process on {self.my_machine_ip}!'

    def execute_python(self, command):
        self.execute_command(command, executor=self.my_remote_helper.execute_python)

    def execute_command_and_wait(self, command, executor=None):
        if executor is None:
            executor = self.my_remote_helper.execute

        if self.my_active_connection is None:
            self.my_status = f'Error: can not connect to {self.my_machine_ip}!'
            return None

        new_process = None
        for _ in range(self.my_attempts_counter):
            try:
                new_process = self.my_remote_helper.execute(self.my_active_connection, command)
                break
            except Exception:
                time.sleep(self.my_wait_counter)

        if new_process is not None:
            self.my_remote_helper.wait(new_process)
        else:
            self.my_status = f'Error: failed to creat process on {self.my_machine_ip}!'

    def execute_python_and_wait(self, command):
        self.execute_command_and_wait(command, executor=self.my_remote_helper.execute_python)

    def wait_all(self):
        for process in self.my_process_list:
            self.my_remote_helper.wait(process)
        if len(self.my_process_list) > 0:
            self.my_status = f'Success: deploy done on {self.my_machine_ip}!'

    def get_status(self):
        return self.my_status
