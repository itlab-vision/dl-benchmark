from xml.dom import minidom
from model.remote_config.remote_computer import RemoteComputer


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
            self.__computers[idx].ip = computer.getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data
            self.__computers[idx].login = computer.getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data
            self.__computers[idx].password = computer.getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data
            self.__computers[idx].os = computer.getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data
            self.__computers[idx].path_to_ftp_client = computer.getElementsByTagName(CONFIG_FTP_CLIENT_PATH_TAG)[0].firstChild.data
            self.__computers[idx].benchmark_config = computer.getElementsByTagName(CONFIG_BENCHMARK_CONFIG_TAG)[0].firstChild.data
            self.__computers[idx].log_file = computer.getElementsByTagName(CONFIG_LOG_FILE_TAG)[0].firstChild.data
            self.__computers[idx].res_file = computer.getElementsByTagName(CONFIG_RESULT_FILE_TAG)[0].firstChild.data

    def create_config(self, path_to_config):
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
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        try:
            f = open(path_to_config, 'r')
            f.close()
        except IOError:
            return False
        return True
