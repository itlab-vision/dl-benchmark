from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal
from xml.dom import minidom


class Model:
    def __init__(self, task=None, name=None, precision=None, framework=None, model_path=None, weights_path=None):
        self.task = task
        self.name = name
        self.precision = precision
        self.framework = framework
        self.model_path = model_path
        self.weights_path = weights_path


class Dataset:
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path


class RemoteComputer:
    def __init__(self, ip=None, login=None, password=None, os=None, path_to_ftp_client=None, benchmark_config=None,
                 log_file=None, res_file=None):
        self.ip = ip
        self.login = login
        self.password = password
        self.os = os
        self.path_to_ftp_client = path_to_ftp_client
        self.benchmark_config = benchmark_config
        self.log_file = log_file
        self.res_file = res_file


class DeployComputer:
    def __init__(self, ip=None, login=None, password=None, os=None, download_folder=None):
        self.ip = ip
        self.login = login
        self.password = password
        self.os = os
        self.download_folder = download_folder


class Models:
    def __init__(self):
        self.__models = []

    def get_models(self):
        return self.__models

    def add_model(self, task, name, precision, framework, model_path, weights_path):
        self.__models.append(Model(task, name, precision, framework, model_path, weights_path))

    def change_model(self, row, task, name, precision, framework, model_path, weights_path):
        self.__models[row] = Model(task, name, precision, framework, model_path, weights_path)

    def delete_model(self, index):
        self.__models.pop(index)

    def delete_models(self, indexes):
        for index in indexes:
            if index < len(self.__models):
                self.delete_model(index)

    def clear(self):
        self.__models.clear()

    def parse_config(self, path_to_config):
        CONFIG_ROOT_TAG = 'Model'
        CONFIG_TASK_TAG = 'Task'
        CONFIG_NAME_TAG = 'Name'
        CONFIG_PRECISION_TAG = 'Precision'
        CONFIG_SOURCE_FRAMEWORK_TAG = 'SourceFramework'
        CONFIG_MODEL_PATH_TAG = 'ModelPath'
        CONFIG_WEIGHTS_PATH_TAG = 'WeightsPath'
        parsed_config = minidom.parse(path_to_config)
        models = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
        self.__models.clear()
        for idx, model in enumerate(models):
            self.__models.append(Model())
            self.__models[idx].task = model.getElementsByTagName(CONFIG_TASK_TAG)[0].firstChild.data
            self.__models[idx].name = model.getElementsByTagName(CONFIG_NAME_TAG)[0].firstChild.data
            self.__models[idx].precision = model.getElementsByTagName(CONFIG_PRECISION_TAG)[0].firstChild.data
            self.__models[idx].framework = model.getElementsByTagName(CONFIG_SOURCE_FRAMEWORK_TAG)[0].firstChild.data
            self.__models[idx].model_path = model.getElementsByTagName(CONFIG_MODEL_PATH_TAG)[0].firstChild.data
            self.__models[idx].weights_path = model.getElementsByTagName(CONFIG_WEIGHTS_PATH_TAG)[0].firstChild.data


class RemoteConfig:
    def __init__(self):
        self.__computers = []

    def get_computers(self):
        return self.__computers

    def add_computer(self, ip, login, password, os, path_to_ftp_client, benchmark_config, log_file, res_file):
        self.__computers.append(RemoteComputer(ip, login, password, os, path_to_ftp_client, benchmark_config,
                                               log_file, res_file))

    def change_computer(self, row, ip, login, password, os, path_to_ftp_client, benchmark_config, log_file, res_file):
        self.__computers[row] = RemoteComputer(ip, login, password, os, path_to_ftp_client, benchmark_config,
                                               log_file, res_file)

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
        CONFIG_FTP_CLIENT_PATH_TAG = 'FTPClientPath'
        CONFIG_BENCHMARK_CONFIG_TAG = 'BenchmarkConfig'
        CONFIG_LOG_FILE_TAG = 'LogFile'
        CONFIG_RESULT_FILE_TAG = 'ResultFile'
        parsed_config = minidom.parse(path_to_config)
        computers = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
        self.__computers.clear()
        for idx, computer in enumerate(computers):
            self.__computers.append(RemoteComputer())
            self.__computers[idx].ip = (computer.
                                        getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data)
            self.__computers[idx].login = (computer.
                                           getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data)
            self.__computers[idx].password = (computer.
                                              getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data)
            self.__computers[idx].os = (computer.
                                        getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data)
            self.__computers[idx].path_to_ftp_client = (computer.
                                                        getElementsByTagName(CONFIG_FTP_CLIENT_PATH_TAG)[
                                                            0].firstChild.data)
            self.__computers[idx].benchmark_config = (computer.
                                                      getElementsByTagName(CONFIG_BENCHMARK_CONFIG_TAG)[
                                                          0].firstChild.data)
            self.__computers[idx].log_file = (computer.
                                              getElementsByTagName(CONFIG_LOG_FILE_TAG)[0].firstChild.data)
            self.__computers[idx].res_file = (computer.
                                              getElementsByTagName(CONFIG_RESULT_FILE_TAG)[0].firstChild.data)

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
            CONFIG_FTP_CLIENT_PATH_TAG = file.createElement('FTPClientPath')
            CONFIG_BENCHMARK_CONFIG_TAG = file.createElement('BenchmarkConfig')
            CONFIG_LOG_FILE_TAG = file.createElement('LogFile')
            CONFIG_RESULT_FILE_TAG = file.createElement('ResultFile')
            CONFIG_IP_TAG.appendChild(file.createTextNode(computer.ip))
            CONFIG_LOGIN_TAG.appendChild(file.createTextNode(computer.login))
            CONFIG_PASSWORD_TAG.appendChild(file.createTextNode(computer.password))
            CONFIG_OS_TAG.appendChild(file.createTextNode(computer.os))
            CONFIG_FTP_CLIENT_PATH_TAG.appendChild(file.createTextNode(computer.path_to_ftp_client))
            CONFIG_BENCHMARK_CONFIG_TAG.appendChild(file.createTextNode(computer.benchmark_config))
            CONFIG_LOG_FILE_TAG.appendChild(file.createTextNode(computer.log_file))
            CONFIG_RESULT_FILE_TAG.appendChild(file.createTextNode(computer.res_file))
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_IP_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_LOGIN_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_PASSWORD_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_OS_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_FTP_CLIENT_PATH_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_BENCHMARK_CONFIG_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_LOG_FILE_TAG)
            CONFIG_COMPUTER_TAG.appendChild(CONFIG_RESULT_FILE_TAG)
            CONFIG_ROOT_TAG.appendChild(CONFIG_COMPUTER_TAG)
        xml_str = file.toprettyxml(indent="\t", encoding="utf-8")
        with open("remote_configuration.xml", 'wb') as f:
            f.write(xml_str)
        try:
            f = open("remote_configuration.xml", 'r')
            f.close()
        except IOError:
            return False
        return True


class DeployConfig:
    def __init__(self):
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
                                                     getElementsByTagName(CONFIG_DOWNLOAD_FOLDER_TAG)[
                                                         0].firstChild.data)

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
