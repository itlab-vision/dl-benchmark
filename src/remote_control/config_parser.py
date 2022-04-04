from xml.dom import minidom


class benchmark:
    def __init__(self, config, executor, log_file, res_file):
        self.config = config
        self.executor = executor
        self.log_file = log_file
        self.res_file = res_file

    @staticmethod
    def parse(dom):
        CONFIG_BENCHMARK_TAG = 'Benchmark'
        CONFIG_CONFIG_TAG = 'Config'
        CONFIG_EXECUTOR_TAG = 'Executor'
        CONFIG_LOG_FILE_TAG = 'LogFile'
        CONFIG_RESULT_FILE_TAG = 'ResultFile'

        parsed_benchmark = dom.getElementsByTagName(CONFIG_BENCHMARK_TAG)[0]
        return benchmark(
            config=parsed_benchmark.getElementsByTagName(CONFIG_CONFIG_TAG)[0].firstChild.data,
            executor=parsed_benchmark.getElementsByTagName(CONFIG_EXECUTOR_TAG)[0].firstChild.data,
            log_file=parsed_benchmark.getElementsByTagName(CONFIG_LOG_FILE_TAG)[0].firstChild.data,
            res_file=parsed_benchmark.getElementsByTagName(CONFIG_RESULT_FILE_TAG)[0].firstChild.data,
        )


class accuracy_checker:
    def __init__(self, config, executor, datasets, definitions, log_file, res_file):
        self.config = config
        self.executor = executor
        self.datasets = datasets
        self.definitions = definitions
        self.log_file = log_file
        self.res_file = res_file

    @staticmethod
    def parse(dom):
        CONFIG_ACCURACY_CHECKER_TAG = 'AccuracyChecker'
        CONFIG_CONFIG_TAG = 'Config'
        CONFIG_EXECUTOR_TAG = 'Executor'
        CONFIG_DATASET_PATH_TAG = 'DatasetPath'
        CONFIG_DEFINITION_PATH_TAG = 'DefinitionPath'
        CONFIG_LOG_FILE_TAG = 'LogFile'
        CONFIG_RESULT_FILE_TAG = 'ResultFile'

        parsed_accuracy_checker = dom.getElementsByTagName(CONFIG_ACCURACY_CHECKER_TAG)[0]
        return accuracy_checker(
            config=parsed_accuracy_checker.getElementsByTagName(CONFIG_CONFIG_TAG)[0].firstChild.data,
            executor=parsed_accuracy_checker.getElementsByTagName(CONFIG_EXECUTOR_TAG)[0].firstChild.data,
            datasets=parsed_accuracy_checker.getElementsByTagName(CONFIG_DATASET_PATH_TAG)[0].firstChild.data,
            definitions=parsed_accuracy_checker.getElementsByTagName(CONFIG_DEFINITION_PATH_TAG)[0].firstChild.data,
            log_file=parsed_accuracy_checker.getElementsByTagName(CONFIG_LOG_FILE_TAG)[0].firstChild.data,
            res_file=parsed_accuracy_checker.getElementsByTagName(CONFIG_RESULT_FILE_TAG)[0].firstChild.data,
        )


class machine:
    def __init__(self, ip, login, password, os_type, path_to_ftp_client, benchmark_info, accuracy_checker_info):
        self.ip = ip
        self.login = login
        self.password = password
        self.os_type = os_type
        self.path_to_ftp_client = path_to_ftp_client
        self.benchmark = benchmark_info
        self.accuracy_checker = accuracy_checker_info


def parse_config(config):
    CONFIG_COMPUTER_TAG = 'Computer'
    CONFIG_IP_TAG = 'IP'
    CONFIG_LOGIN_TAG = 'Login'
    CONFIG_PASSWORD_TAG = 'Password'
    CONFIG_OS_TAG = 'OS'
    CONFIG_FTP_CLIENT_PATH_TAG = 'FTPClientPath'

    available_maсhines = minidom.parse(config).getElementsByTagName(CONFIG_COMPUTER_TAG)

    machine_list = []
    for available_machine in available_maсhines:
        machine_list.append(machine(
            ip=available_machine.getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data,
            login=available_machine.getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data,
            password=available_machine.getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data,
            os_type=available_machine.getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data,
            path_to_ftp_client=available_machine.getElementsByTagName(CONFIG_FTP_CLIENT_PATH_TAG)[0].firstChild.data,
            benchmark_info=benchmark.parse(available_machine),
            accuracy_checker_info=accuracy_checker.parse(available_machine)
        ))
    return machine_list
