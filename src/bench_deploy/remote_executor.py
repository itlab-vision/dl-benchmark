from remote_helper import remote_helper

class remote_executor:
    def __init__(self, os_type, log):
        self.my_process_list = []
        self.my_remote_helper = remote_helper.get_remote_helper(os_type.lower(), log)

    def create_connection(self, machine_ip, login, password):
        self.my_active_connection = self.my_remote_helper.connect(machine_ip, login, password)

    def execute_command(self, command):
        if self.my_active_connection is None:
            raise ValueError('Connection is disabled!')
        new_process = self.my_remote_helper.execute(self.my_active_connection, command)

        if not new_process is None:
            self.my_process_list.append(new_process)

    def execute_command_and_wait(self, command):
        if self.my_active_connection is None:
            raise ValueError('Connection is disabled!')
        new_process = self.my_remote_helper.execute(self.my_active_connection, command)

        if new_process is not None:
            self.my_remote_helper.wait(new_process)

    def wait_all(self):
        for process in self.my_process_list:
            self.my_remote_helper.wait(process)
