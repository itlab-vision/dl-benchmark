import abc
import ftplib
import argparse
import sys
import platform
import os
import subprocess


class launcher(metaclass=abc.ABCMeta):
    def __init__(self, target, path_to_ftp_client, params_config, executor, os_type, result, logs):
        self.target = target
        self.path_to_target = os.path.normpath(path_to_ftp_client + "//..//" + self.target)
        self.executor = executor
        self.os_type = os_type
        self.result = os.path.join(path_to_ftp_client, result)
        self.logs = os.path.join(path_to_ftp_client, logs)
        self.source_config = params_config
        self.local_config = os.path.join(self.path_to_target, os.path.basename(self.source_config))

    @abc.abstractmethod
    def _get_command_line(self):
        pass

    def load_config(self, ftp_connection):
        with open(self.local_config, 'wb') as config_file:
            ftp_connection.retrbinary('RETR {}'.format(self.source_config), config_file.write)

    def download_result(self, ftp_connection):
        result_table = open(self.result, 'rb')
        ftp_connection.storbinary('STOR {0}_{1}_result_table.csv'.format(platform.node(), self.target), result_table)

    def launch(self):
        command_line = self._get_command_line()
        if self.os_type == 'Windows':
            self.launch_on_win(command_line)
        elif self.os_type == 'Linux':
            self.launch_linux(command_line)
        else:
            raise ValueError('Unsupported OS')

    def launch_on_win(self, command_line):
        os.system('cd {0} & python {1} > {2}'.format(self.path_to_target, command_line, self.logs))

    def launch_linux(self, command_line):
        sp = subprocess.Popen((
            'cd {0}; python3 {1} > {2}').format(self.path_to_target, command_line, self.logs),
            shell=True,
            executable='/bin/bash'
        )
        sp.communicate()

    @staticmethod
    def get_launcher(type, *args):
        if type == "benchmark":
            return benchmark_launcher(*args)
        elif type == "accuracy_checker":
            return accuracy_checker_launcher(*args)
        else:
            raise ValueError('Unsupported launcher type!')


class benchmark_launcher(launcher):
    def __init__(self, path_to_ftp_client, params_config, executor, os_type, result, logs):
        super().__init__("benchmark", path_to_ftp_client, params_config, executor, os_type, result, logs)

    def _get_command_line(self):
        return 'inference_benchmark.py -c {0} -r {1} --executor_type {2}'.format(self.local_config, self.result, self.executor)


class accuracy_checker_launcher(launcher):
    def __init__(self, path_to_ftp_client, params_config, executor, os_type, result, logs, datasets, definitions):
        super().__init__("accuracy_checker", path_to_ftp_client, params_config, executor, os_type, result, logs)
        self.datasets = datasets
        self.definitions = definitions

    def _get_command_line(self):
        return 'accuracy_checker.py -c {0} -s {1} -r {2} -d {3} --executor_type {4}'.format(self.local_config,
                                                                                            self.datasets, self.result,
                                                                                            self.definitions,
                                                                                            self.executor)


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--server_ip', type=str, help='Main ftp server address.', required=True)
    parser.add_argument('-l', '--login', type=str, help='Login to connect to ftp server.', required=True)
    parser.add_argument('-p', '--password', type=str, help='Password to connect to ftp server.', required=True)
    parser.add_argument('-b', '--benchmark_config', type=str,
                        help='Path to benchmark config file.', required=False)
    parser.add_argument('-ac', '--accuracy_checker_config', type=str,
                        help='Path to accuracy checker config file.', required=False)
    parser.add_argument('--benchmark_executor', type=str,
                        help='Type of benchmark executor.', required=False)
    parser.add_argument('--accuracy_checker_executor', type=str,
                        help='Type of accuracy checker executor.', required=False)
    parser.add_argument('-os', '--os_type', type=str, help='Type of operating system.', required=True)
    parser.add_argument('--ftp_dir', type=str, help='Path to the directory with results on the FTP.', required=True)
    parser.add_argument('--benchmark_res_file', type=str,
                        help='The name of the file to which benchmark results are written', required=False)
    parser.add_argument('--accuracy_checker_res_file', type=str,
                        help='The name of the file to which accuracy checker results are written', required=False)
    parser.add_argument('--benchmark_log_file', type=str,
                        help='The name of the file to which benchmark logs are written', required=False)
    parser.add_argument('--accuracy_checker_log_file', type=str,
                        help='The name of the file to which accuracy checker logs are written', required=False)
    parser.add_argument('--accuracy_checker_source', help='Path to directory in which input images will be searched',
                        type=str, required=False)
    parser.add_argument('--accuracy_checker_definitions', help='Path to the global datasets configuration file',
                        type=str, required=False)
    return parser


def main():
    param_list = build_parser().parse_args()
    path_to_ftp_client = os.path.split(os.path.abspath(__file__))[0]

    # benchmark
    if param_list.benchmark_config:
        benchmark = benchmark_launcher(path_to_ftp_client, param_list.benchmark_config, param_list.benchmark_executor,
                                       param_list.os_type, param_list.benchmark_res_file, param_list.benchmark_log_file)

        ftp_connection = ftplib.FTP(param_list.server_ip, param_list.login, param_list.password)
        benchmark.load_config(ftp_connection)
        ftp_connection.close()

        benchmark.launch()

        ftp_connection = ftplib.FTP(param_list.server_ip, param_list.login, param_list.password)
        ftp_connection.cwd(param_list.ftp_dir)
        benchmark.download_result(ftp_connection)
        ftp_connection.close()

    # accuracy checker
    if param_list.accuracy_checker_config:
        accuracy_checker = accuracy_checker_launcher(path_to_ftp_client, param_list.accuracy_checker_config,
                                                     param_list.accuracy_checker_executor, param_list.os_type,
                                                     param_list.accuracy_checker_res_file,
                                                     param_list.accuracy_checker_log_file,
                                                     param_list.accuracy_checker_source,
                                                     param_list.accuracy_checker_definitions)

        ftp_connection = ftplib.FTP(param_list.server_ip, param_list.login, param_list.password)
        accuracy_checker.load_config(ftp_connection)
        ftp_connection.close()

        accuracy_checker.launch()

        ftp_connection = ftplib.FTP(param_list.server_ip, param_list.login, param_list.password)
        ftp_connection.cwd(param_list.ftp_dir)
        accuracy_checker.download_result(ftp_connection)
        ftp_connection.close()


if __name__ == '__main__':
    sys.exit(main() or 0)
