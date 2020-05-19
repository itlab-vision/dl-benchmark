from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal
from xml.dom import minidom


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

    def parse_config(self, path_to_config):
        CONFIG_ROOT_TAG = 'Computer'
        CONFIG_IP_TAG = 'IP'
        CONFIG_LOGIN_TAG = 'Login'
        CONFIG_PASSWORD_TAG = 'Password'
        CONFIG_OS_TAG = 'OS'
        CONFIG_DOWNLOAD_FOLDER_TAG = 'DownloadFolder'
        parsed_config = minidom.parse(path_to_config)
        computers = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
        self.__computers.clear()
        for idx, computer in enumerate(computers):
            self.__computers.append(DeployComputer())
            self.__computers[idx].ip = (computer.
                getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data)
            self.__computers[idx].login = (computer.
                getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data)
            self.__computers[idx].password = (computer.
                getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data)
            self.__computers[idx].os = (computer.
                getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data)
            self.__computers[idx].download_folder = (computer.
                getElementsByTagName(CONFIG_DOWNLOAD_FOLDER_TAG)[0].firstChild.data)

    def create_config(self):
        if len(self.__computers) == 0:
            return False
        file = minidom.Document()
        CONFIG_ROOT_TAG = file.createElement('Computers')
        file.appendChild(CONFIG_ROOT_TAG)
        for computer in self.__computers:
            CONFIG_COMPUTER_TAG = file.createElement('Computer')
            CONFIG_IP_TAG = file.createElement('IP')
            CONFIG_LOGIN_TAG = file.createElement('Login')
            CONFIG_PASSWORD_TAG = file.createElement('Password')
            CONFIG_OS_TAG = file.createElement('OS')
            CONFIG_DOWNLOAD_FOLDER_TAG = file.createElement('DownloadFolder')
            CONFIG_IP_TAG.appendChild(file.createTextNode(computer.ip))
            CONFIG_LOGIN_TAG.appendChild(file.createTextNode(computer.login))
            CONFIG_PASSWORD_TAG.appendChild(file.createTextNode(computer.password))
            CONFIG_OS_TAG.appendChild(file.createTextNode(computer.os))
            CONFIG_DOWNLOAD_FOLDER_TAG.appendChild(file.createTextNode(computer.download_folder))
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_IP_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_LOGIN_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_PASSWORD_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_OS_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_DOWNLOAD_FOLDER_TAG)
            CONFIG_ROOT_TAG.appendChild(CONFIG_COMPUTER_TAG)
        xml_str = file.toprettyxml(indent="\t", encoding="utf-8")
        with open("deploy_configuration.xml", 'wb') as f:
            f.write(xml_str)
        try:
            f = open("deploy_configuration.xml", 'r')
            f.close()
        except IOError:
            return False
        return True
