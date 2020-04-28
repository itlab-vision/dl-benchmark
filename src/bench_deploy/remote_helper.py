import abc

class remote_helper(metaclass = abc.ABCMeta):
    def __init__(self, log):
        self.my_log = log

    @staticmethod
    def get_remote_helper(os_type, log):
        if os_type == 'linux':
            from linux_remote_helper import linux_remote_helper
            return linux_remote_helper(log)
        elif os_type == 'windows':
            from windows_remote_hepler import windows_remote_hepler
            return windows_remote_hepler(log)

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
