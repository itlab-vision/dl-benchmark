import wmi

from remote_helper import RemoteHelper


class WindowsRemoteHepler(RemoteHelper):
    def __init__(self, log):
        super().__init__(log)

    def connect(self, machine_ip, login, password):
        new_connection = wmi.WMI(
            machine_ip,
            user=login,
            password=password,
        )
        return new_connection

    def execute(self, con, command):
        process_startup = con.Win32_ProcessStartup.new()
        process_id, result = con.Win32_Process.Create(
            CommandLine=command,
            ProcessStartupInformation=process_startup,
        )
        watcher = None
        if result == 0:
            self.my_log.info(f'Process started successfully {process_id}')
            con.watch_for(
                notification_type='Deletion',
                wmi_class='Win32_Process',
                ProcessId=process_id,
            )
        else:
            self.my_log.info(f'Problem creating process {result}')
        return watcher

    def execute_python(self, con, command):
        return self.execute(con, f'python {command}')

    def wait(self, process):
        process_status = process()
        self.my_log.info(f'Ended process on Windows with name {process_status.CSName}')
