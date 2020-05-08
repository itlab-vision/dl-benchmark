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


class DeployConfig(QObject):

    updateSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__computers = []

    def add_computer(self, ip, login, password, os, download_folder):
        self.__computers.append(DeployComputer(ip, login, password, os, download_folder))
        self.updateSignal.emit()

    def get_computers(self):
        return self.__computers

    def clear(self):
        self.__computers.clear()
        self.updateSignal.emit()
