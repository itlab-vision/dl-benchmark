#import wmi
import paramiko
import os
import sys
import logging as log

class remote_executor:
    def __init__(self, os_type):
        self.my_process_list = []
        self.my_os_type = os_type.lower()

    def create_connection(self, machine_ip, login, password):
        new_connection = None
        if self.my_os_type == 'linux':
            new_connection = self.__create_linux_connection(machine_ip, login, password)
        elif self.my_os_type == 'windows':
            new_connection = self.__create_windows_connection(machine_ip, login, password)

        self.my_active_connection = new_connection

    def execute_command(self, command):
        if self.my_active_connection is None:
            raise ValueError('Connection is disabled!')
        new_process = None
        if self.my_os_type == 'linux':
            new_process = self.__execute_command_on_linux(command)
        elif self.my_os_type == 'windows':
            new_process = self.__execute_command_on_windows(command)

        if not new_process is None:
            self.my_process_list.append(new_process)

    def execute_command_and_wait(self, command):
        if self.my_active_connection is None:
            raise ValueError('Connection is disabled!')
        new_process = None
        if self.my_os_type == 'linux':
            new_process = self.__execute_command_on_linux(command)
        elif self.my_os_type == 'windows':
            new_process = self.__execute_command_on_windows(command)

        if not new_process is None:
            self.__wait_process(new_process)

    def wait_all(self):
        for process in self.my_process_list:
            self.__wait_process(process)

    def __create_linux_connection(self, machine_ip, login, password):
        new_connection = paramiko.SSHClient()
        new_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        new_connection.connect(hostname = machine_ip, username = login,
            password = password)

        return new_connection

    def __create_windows_connection(self, machine_ip, login, password):
        new_connection = wmi.WMI(machine_ip, user = login,
            password = password)

        return new_connection

    def __execute_command_on_linux(self, command):
        transport = self.my_active_connection.get_transport()
        channel = transport.open_session()

        try:
            channel.exec_command(command)
            log.info('Process started successfully')
        except paramiko.ssh_exception.SSHException:
            channel = None
            log.info('Problem creating process')

        return channel

    def __execute_command_on_windows(self, command):
        process_startup = self.my_active_connection.Win32_ProcessStartup.new()
        process_id, result = self.my_active_connection.Win32_Process.Create(CommandLine = command,
            ProcessStartupInformation = process_startup)

        watcher = None
        if result == 0:
            log.info('Process started successfully {}'.format(process_id))
            self.my_active_connection.watch_for(notification_type = 'Deletion',
                wmi_class = 'Win32_Process', ProcessId = process_id)
        else:
            log.info('Problem creating process {}'.format(result))

        return watcher

    def __wait_process(self, process):
        if self.my_os_type == 'linux':
            self.__wait_linux_process(process)
        elif self.my_os_type == 'windows':
            self.__wait_windows_process(process)

    def __wait_windows_process(self, watcher):
        process_status = watcher()
        log.info('Ended process on Windows with name {}'.format(
            process_status.CSName))

    def __wait_linux_process(self, channel):
        channel_id = channel.get_id()
        process_status = channel.recv_exit_status()
        log.info('Ended process on Linux with id {}'.format(channel_id))
