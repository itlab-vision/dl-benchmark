import abc
# pylint: disable-next=E0401
from tags import CONFIG_COMPUTER_TAG, CONFIG_IP_TAG, CONFIG_LOGIN_TAG, CONFIG_PASSWORD_TAG, CONFIG_OS_TAG, \
    CONFIG_BENCHMARK_TAG, CONFIG_ACCURACY_CHECKER_TAG, CONFIG_FTP_CLIENT_PATH_TAG, CONFIG_CONFIG_TAG, \
    CONFIG_EXECUTOR_TAG, CONFIG_LOG_FILE_TAG, CONFIG_RESULT_FILE_TAG, CONFIG_AC_DATASET_PATH_TAG, CONFIG_DEFINITION_PATH


class RemoteComputer:
    def __init__(self, ip, login, password, os, path_to_ftp_client, *args):
        self.ip = ip
        self.login = login
        self.password = password
        self.os = os
        self.path_to_ftp_client = path_to_ftp_client
        self.benchmark = BenchmarkComponent(*args[0:4]) if len(args) > 2 else args[0]
        self.accuracy_checker = AccuracyCheckerComponent(*args[4:-1]) if len(args) > 2 else args[1]

    def create_dom(self, file):
        DOM_COMPUTER_TAG = file.createElement(CONFIG_COMPUTER_TAG)
        DOM_IP_TAG = file.createElement(CONFIG_IP_TAG)
        DOM_LOGIN_TAG = file.createElement(CONFIG_LOGIN_TAG)
        DOM_PASSWORD_TAG = file.createElement(CONFIG_PASSWORD_TAG)
        DOM_OS_TAG = file.createElement(CONFIG_OS_TAG)
        DOM_FTP_CLIENT_PATH_TAG = file.createElement(CONFIG_FTP_CLIENT_PATH_TAG)
        DOM_BENCHMARK_TAG = self.benchmark.create_dom(file)
        DOM_ACCURACY_CHECKER_TAG = self.accuracy_checker.create_dom(file)

        DOM_IP_TAG.appendChild(file.createTextNode(self.ip))
        DOM_LOGIN_TAG.appendChild(file.createTextNode(self.login))
        DOM_PASSWORD_TAG.appendChild(file.createTextNode(self.password))
        DOM_OS_TAG.appendChild(file.createTextNode(self.os))
        DOM_FTP_CLIENT_PATH_TAG.appendChild(file.createTextNode(self.path_to_ftp_client))
        DOM_COMPUTER_TAG.appendChild(DOM_IP_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_LOGIN_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_PASSWORD_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_OS_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_BENCHMARK_TAG)
        DOM_COMPUTER_TAG.appendChild(DOM_ACCURACY_CHECKER_TAG)

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
            ftp_client_path = parsed_computer.getElementsByTagName(CONFIG_FTP_CLIENT_PATH_TAG)[0].firstChild.data
            benchmark = BenchmarkComponent.parse(parsed_computer.getElementsByTagName(CONFIG_BENCHMARK_TAG)[0])
            accuracy_checker = AccuracyCheckerComponent.parse(
                parsed_computer.getElementsByTagName(CONFIG_ACCURACY_CHECKER_TAG)[0])
            computers.append(RemoteComputer(ip, login, password, os, ftp_client_path, benchmark, accuracy_checker))
        return computers


class Component(metaclass=abc.ABCMeta):
    def __init__(self, config, executor, log_file, res_file):
        self.parameters = {
            CONFIG_CONFIG_TAG: config,
            CONFIG_EXECUTOR_TAG: executor,
            CONFIG_LOG_FILE_TAG: log_file,
            CONFIG_RESULT_FILE_TAG: res_file
        }
        self.CONFIG_ROOT_TAG = None

    @staticmethod
    @abc.abstractmethod
    def parse(dom):
        pass

    def create_dom(self, file):
        DOM_ROOT_TAG = file.createElement(self.CONFIG_ROOT_TAG)

        for key in self.parameters:
            DOM_PARAMETER = file.createElement(key)
            DOM_PARAMETER.appendChild(file.createTextNode(self.parameters[key]))
            DOM_ROOT_TAG.appendChild(DOM_PARAMETER)

        return DOM_ROOT_TAG


class BenchmarkComponent(Component):
    def __init__(self, config, executor, log_file, res_file):
        super().__init__(config, executor, log_file, res_file)
        self.CONFIG_ROOT_TAG = CONFIG_BENCHMARK_TAG

    @staticmethod
    def parse(dom):
        config = ''
        executor = ''
        log_file = ''
        res_file = ''

        config_node = dom.getElementsByTagName(CONFIG_CONFIG_TAG)[0].firstChild
        if config_node:
            config = config_node.data
        executor_node = dom.getElementsByTagName(CONFIG_EXECUTOR_TAG)[0].firstChild
        if executor_node:
            executor = executor_node.data
        log_file_node = dom.getElementsByTagName(CONFIG_LOG_FILE_TAG)[0].firstChild
        if log_file_node:
            log_file = log_file_node.data
        res_file_node = dom.getElementsByTagName(CONFIG_RESULT_FILE_TAG)[0].firstChild
        if res_file_node:
            res_file = res_file_node.data
        return BenchmarkComponent(config, executor, log_file, res_file)


class AccuracyCheckerComponent(Component):
    def __init__(self, config, executor, dataset_path, definition_path, log_file, res_file):
        super().__init__(config, executor, log_file, res_file)
        self.parameters[CONFIG_AC_DATASET_PATH_TAG] = dataset_path
        self.parameters[CONFIG_DEFINITION_PATH] = definition_path
        self.CONFIG_ROOT_TAG = CONFIG_ACCURACY_CHECKER_TAG

    @staticmethod
    def parse(dom):
        config = ''
        executor = ''
        dataset_path = ''
        definition_path = ''
        log_file = ''
        res_file = ''

        config_node = dom.getElementsByTagName(CONFIG_CONFIG_TAG)[0].firstChild
        if config_node:
            config = config_node.data
        executor_node = dom.getElementsByTagName(CONFIG_EXECUTOR_TAG)[0].firstChild
        if executor_node:
            executor = executor_node.data
        dataset_path_node = dom.getElementsByTagName(CONFIG_AC_DATASET_PATH_TAG)[0].firstChild
        if dataset_path_node:
            dataset_path = dataset_path_node.data
        definition_path_node = dom.getElementsByTagName(CONFIG_DEFINITION_PATH)[0].firstChild
        if definition_path_node:
            definition_path = definition_path_node.data
        log_file_node = dom.getElementsByTagName(CONFIG_LOG_FILE_TAG)[0].firstChild
        if log_file_node:
            log_file = log_file_node.data
        res_file_node = dom.getElementsByTagName(CONFIG_RESULT_FILE_TAG)[0].firstChild
        if res_file_node:
            res_file = res_file_node.data

        return AccuracyCheckerComponent(config, executor, dataset_path, definition_path, log_file, res_file)
