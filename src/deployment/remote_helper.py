import abc


class RemoteHelper(metaclass=abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log

    @staticmethod
    def get_remote_helper(os_type, python ,log):
        if os_type == 'linux':
            from linux_remote_helper import LinuxRemoteHelper
            return LinuxRemoteHelper(python, log)
        elif os_type == 'windows':
            from windows_remote_helper import WindowsRemoteHepler
            return WindowsRemoteHepler(log)

    @abc.abstractmethod
    def connect(self, machine_ip, login, password):
        pass

    @abc.abstractmethod
    def execute(self, con, command):
        pass

    @abc.abstractmethod
    def execute_python(self, command):
        pass

    @abc.abstractmethod
    def wait(self, process):
        pass
