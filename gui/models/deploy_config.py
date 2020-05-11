from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal


class DeployComputer:
    def __init__(self, ip=None, login=None, password=None, os=None, download_folder=None):
        self.__ip = ip
        self.__login = login
        self.__password = password
        self.__os = os
        self.__download_folder = download_folder

    def get_ip(self):
        return self.__ip

    def get_login(self):
        return self.__login

    def get_password(self):
        return self.__password

    def get_os(self):
        return self.__os

    def get_download_folder(self):
        return self.__download_folder

    def set_ip(self, ip):
        self.__ip = ip

    def set_login(self, login):
        self.__login = login

    def set_password(self, password):
        self.__password = password

    def set_os(self, os):
        self.__os = os

    def set_download_folder(self, download_folder):
        self.__download_folder = download_folder


class DeployConfig(QObject):

    updateSignal = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.__computers = []

    def get_computers(self):
        return self.__computers

    def add_computer(self, ip, login, password, os, download_folder):
        self.__computers.append(DeployComputer(ip, login, password, os, download_folder))
        self.updateSignal.emit(self.__computers)

    def delete_computer(self, index):
        self.__computers.pop(index)

    def delete_computers(self, indexes):
        for index in indexes:
            if index < len(self.__computers):
                self.delete_computer(index)
        self.updateSignal.emit(self.__computers)

    def clear(self):
        self.__computers.clear()
        self.updateSignal.emit(self.__computers)
