from xml.dom import minidom


class machine:
    def __init__(self, ip, login, password, os_type, path_to_ftp_client, benchmark_config, benchmark_executor, log_file, res_file):
        self.ip = ip
        self.login = login
        self.password = password
        self.os_type = os_type
        self.path_to_ftp_client = path_to_ftp_client
        self.benchmark_config = benchmark_config
        self.benchmark_executor = benchmark_executor
        self.log_file = log_file
        self.res_file = res_file


def parse_config(config):
    CONFIG_ROOT_TAG = 'Computers'
    CONFIG_IP_TAG = 'IP'
    CONFIG_LOGIN_TAG = 'Login'
    CONFIG_PASSWORD_TAG = 'Password'
    CONFIG_OS_TAG = 'OS'
    CONFIG_FTP_CLIENT_PATH_TAG = 'FTPClientPath'
    CONFIG_BENCHMARK_CONFIG_TAG = 'BenchmarkConfig'
    CONFIG_BENCHMARK_EXECUTOR_TAG = 'BenchmarkExecutor'
    CONFIG_LOG_FILE_TAG = 'LogFile'
    CONFIG_RESULT_FILE_TAG = 'ResultFile'

    available_mashines = minidom.parse(config).getElementsByTagName(CONFIG_ROOT_TAG)

    print(available_mashines)
    machine_list = []
    for available_mashine in available_mashines:
        machine_list.append(machine(
            ip=available_mashine.getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data,
            login=available_mashine.getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data,
            password=available_mashine.getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data,
            os_type=available_mashine.getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data,
            path_to_ftp_client=available_mashine.getElementsByTagName(CONFIG_FTP_CLIENT_PATH_TAG)[0].firstChild.data,
            benchmark_config=available_mashine.getElementsByTagName(CONFIG_BENCHMARK_CONFIG_TAG)[0].firstChild.data,
            benchmark_executor=available_mashine.getElementsByTagName(CONFIG_BENCHMARK_EXECUTOR_TAG)[0].firstChild.data,
            log_file=available_mashine.getElementsByTagName(CONFIG_LOG_FILE_TAG)[0].firstChild.data,
            res_file=available_mashine.getElementsByTagName(CONFIG_RESULT_FILE_TAG)[0].firstChild.data,
        ))
    return machine_list

parse_config('C:/Users/shave/Documents/ITlab/dl/dl-benchmark/src/configs/remote_configuration_file_template.xml')