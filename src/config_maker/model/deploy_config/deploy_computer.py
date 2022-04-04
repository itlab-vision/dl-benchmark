# pylint: disable-next=E0401
from tags import CONFIG_COMPUTER_TAG, CONFIG_IP_TAG, CONFIG_LOGIN_TAG, CONFIG_PASSWORD_TAG, \
    CONFIG_OS_TAG, CONFIG_DOWNLOAD_FOLDER_TAG


class DeployComputer:
    def __init__(self, ip, login, password, os, download_folder):
        self.ip = ip
        self.login = login
        self.password = password
        self.os = os
        self.download_folder = download_folder

    def create_dom(self, file):
        DOM_COMPUTER_TAG = file.createElement(CONFIG_COMPUTER_TAG)
        DOM_IP_TAG = file.createElement(CONFIG_IP_TAG)
        DOM_LOGIN_TAG = file.createElement(CONFIG_LOGIN_TAG)
        DOM_PASSWORD_TAG = file.createElement(CONFIG_PASSWORD_TAG)
        DOM_OS_TAG = file.createElement(CONFIG_OS_TAG)
        DOM_DOWNLOAD_FOLDER_TAG = file.createElement(CONFIG_DOWNLOAD_FOLDER_TAG)

        DOM_IP_TAG.appendChild(file.createTextNode(self.ip))
        DOM_LOGIN_TAG.appendChild(file.createTextNode(self.login))
        DOM_PASSWORD_TAG.appendChild(file.createTextNode(self.password))
        DOM_OS_TAG.appendChild(file.createTextNode(self.os))
        DOM_DOWNLOAD_FOLDER_TAG.appendChild(file.createTextNode(self.download_folder))
        DOM_COMPUTER_TAG.appendChild(DOM_IP_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_LOGIN_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_PASSWORD_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_OS_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_DOWNLOAD_FOLDER_TAG)

        return DOM_COMPUTER_TAG

    @staticmethod
    def parse(dom):
        parsed_computers = dom.getElementsByTagName(CONFIG_COMPUTER_TAG)
        computers = []
        for parsed_computer in parsed_computers:
            ip = parsed_computer.getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data
            login = parsed_computer.getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data
            password = parsed_computer.getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data
            os = parsed_computer.getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data
            download_folder = parsed_computer.getElementsByTagName(CONFIG_DOWNLOAD_FOLDER_TAG)[0].firstChild.data
            computers.append(DeployComputer(ip, login, password, os, download_folder))
        return computers
