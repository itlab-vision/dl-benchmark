import time
from remote_helper import remote_helper

class remote_executor:
    def __init__(self, os_type, log):
        self.my_process_list = []
        self.my_remote_helper = remote_helper.get_remote_helper(os_type.lower(), log)
        self.my_wait_counter = 10 # seconds
        self.my_attempts_counter = 3
        self.my_status = ''

    def create_connection(self, machine_ip, login, password):
        self.my_machine_ip = machine_ip

        for i in range(self.my_attempts_counter):
            try:
                self.my_active_connection = self.my_remote_helper.connect(machine_ip, login, password)
                break
            except:
                time.sleep(self.my_wait_counter)

    def execute_command(self, command):
        if self.my_active_connection is None:
            self.my_status = 'Error: can\'t connect to {}!'.format(self.my_machine_ip)
            return None

        new_process = None
        for i in range(self.my_attempts_counter):
            try:
                new_process = self.my_remote_helper.execute(self.my_active_connection, command)
                break
            except:
                time.sleep(self.my_wait_counter)

        if not new_process is None:
            self.my_process_list.append(new_process)
        else:
            self.my_status = 'Error: failed to creat process on {}!'.format(self.my_machine_ip)

    def execute_command_and_wait(self, command):
        if self.my_active_connection is None:
            self.my_status = 'Error: can\'t connect to {}!'.format(self.my_machine_ip)
            return None

        new_process = None
        for i in range(self.my_attempts_counter):
            try:
                new_process = self.my_remote_helper.execute(self.my_active_connection, command)
                break
            except:
                time.sleep(self.my_wait_counter)

        if new_process is not None:
            self.my_remote_helper.wait(new_process)
        else:
            self.my_status = 'Error: failed to creat process on {}!'.format(self.my_machine_ip)

    def wait_all(self):
        for process in self.my_process_list:
            self.my_remote_helper.wait(process)
        if len(self.my_process_list) > 0:
            self.my_status = 'Success: deploy done on {}!'.format(self.my_machine_ip)

    def get_status(self):
        return self.my_status
