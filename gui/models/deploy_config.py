class DeployComputer:
    def __init__(self, ip=None, login=None, password=None, os=None, download_folder=None):
        self.ip = ip
        self.login = login
        self.password = password
        self.os = os
        self.download_folder = download_folder


class DeployConfig:
    def __init__(self):
        self.computers = []

    def add_computer(self, computer):
        self.computers.append(computer)
