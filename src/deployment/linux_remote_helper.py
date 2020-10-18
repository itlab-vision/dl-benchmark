import paramiko # pylint: disable=E0401
from remote_helper import remote_helper


class linux_remote_helper(remote_helper):
    def __init__(self, log):
        super().__init__(log)


    def connect(self, machine_ip, login, password):
        new_connection = paramiko.SSHClient()
        new_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        new_connection.connect(hostname = machine_ip, username = login,
            password = password)

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
        return self.execute(con, 'python3 {}'.format(command))


    def wait(self, process):
        channel_id = process.get_id()
        process_status = process.recv_exit_status()
        self.my_log.info('Ended process on Linux with id {}'.format(channel_id))
