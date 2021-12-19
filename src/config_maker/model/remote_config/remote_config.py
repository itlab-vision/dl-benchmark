import os
from xml.dom import minidom
from .remote_computer import RemoteComputer  # pylint: disable=E0402
from tags import CONFIG_COMPUTERS_TAG  # pylint: disable=E0401


class RemoteConfig:
    def __init__(self):
        self.__computers = []

    def get_computers(self):
        return self.__computers

    def add_computer(self, ip, login, password, os, path_to_ftp_client, *args):
        self.__computers.append(RemoteComputer(ip, login, password, os, path_to_ftp_client, *args))

    def change_computer(self, row, ip, login, password, os, path_to_ftp_client, *args):
        self.__computers[row] = RemoteComputer(ip, login, password, os, path_to_ftp_client, *args)

    def delete_computer(self, index):
        self.__computers.pop(index)

    def delete_computers(self, indexes):
        for index in indexes:
            if index < len(self.__computers):
                self.delete_computer(index)

    def copy_computers(self, indexes):
        for index in indexes:
            if index < len(self.__computers):
                self.__computers.append(self.__computers[index])

    def clear(self):
        self.__computers.clear()

    def parse_config(self, path_to_config):
        parsed_config = minidom.parse(path_to_config)
        self.__computers = RemoteComputer.parse(parsed_config)

    def create_config(self, path_to_config):
        if len(self.__computers) == 0:
            return False
        file = minidom.Document()
        DOM_ROOT_TAG = file.createElement(CONFIG_COMPUTERS_TAG)
        file.appendChild(DOM_ROOT_TAG)
        for model in self.__computers:
            DOM_ROOT_TAG.appendChild(model.create_dom(file))
        xml_str = file.toprettyxml(indent="\t", encoding="utf-8")
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        return os.path.exists(path_to_config)
