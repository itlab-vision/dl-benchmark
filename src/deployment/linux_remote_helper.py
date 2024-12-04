import paramiko

from remote_helper import RemoteHelper


class LinuxRemoteHelper(RemoteHelper):
    def __init__(self, python, log):
        super().__init__(log)
        self.python = python

    def connect(self, machine_ip, login, password):
        new_connection = paramiko.SSHClient()
        new_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        new_connection.connect(
            hostname=machine_ip,
            username=login,
            password=password,
        )
        return new_connection

    def execute(self, con, command):
        transport = con.get_transport()
        channel = transport.open_session()
        try:
            channel.exec_command(command)
            self.my_log.info('Process started successfully')
        except paramiko.ssh_exception.SSHException:
            channel = None
            self.my_log.info('Problem creating process')
        return channel

    def execute_python(self, con, command):
        return self.execute(con, f'{self.python} {command}')

    def wait(self, process):
        channel_id = process.get_id()
        process.recv_exit_status()
        self.my_log.info(f'Ended process on Linux with id {channel_id}')
