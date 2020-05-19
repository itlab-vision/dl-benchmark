from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal


class DeployComputer:
    def __init__(self, ip=None, login=None, password=None, os=None, download_folder=None):
        self.ip = ip
        self.login = login
        self.password = password
        self.os = os
        self.download_folder = download_folder


class DeployConfig:
    def __init__(self):
        super().__init__()
        self.__computers = []

    def get_computers(self):
        return self.__computers

    def add_computer(self, ip, login, password, os, download_folder):
        self.__computers.append(DeployComputer(ip, login, password, os, download_folder))

    def change_computer(self, row, ip, login, password, os, download_folder):
        self.__computers[row] = DeployComputer(ip, login, password, os, download_folder)

    def delete_computer(self, index):
        self.__computers.pop(index)

    def delete_computers(self, indexes):
        for index in indexes:
            if index < len(self.__computers):
                self.delete_computer(index)

    def clear(self):
        self.__computers.clear()
