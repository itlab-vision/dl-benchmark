import os
import sys
import argparse
import logging as log
import config_parser
import ftplib
import table_format

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'deployment'))
from remote_executor import remote_executor  # noqa: E402 pylint: disable=E0401


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, help='Path to configuration file', required=True)
    parser.add_argument('-s', '--server_ip', type=str, help='FTP server IP', required=True)
    parser.add_argument('-l', '--server_login', type=str, help='Login to FTP server', required=True)
    parser.add_argument('-p', '--server_psw', type=str, help='Password to FTP server', required=True)
    parser.add_argument('-br', '--benchmark_result_table', type=str,
                        help='Name of benchmark result table', required=False)
    parser.add_argument('-acr', '--accuracy_checker_result_table', type=str,
                        help='Name of accuracy checker result table', required=False)
    parser.add_argument('--ftp_dir', type=str, help='Path to the directory with results on the FTP.', required=True)
    args = parser.parse_args()
    if not os.path.isfile(args.config):
        raise ValueError('Wrong path to configuration file!')
    return args


def client_execution(machine, server_ip, server_login, server_psw, ftp_dir, log):
    executor = remote_executor(machine.os_type, log)
    executor.create_connection(machine.ip, machine.login, machine.password)
    command_line = '{} -ip {} -l {} -p {} -os {} --ftp_dir {}'.format(
        machine.path_to_ftp_client, server_ip, server_login, server_psw, machine.os_type, ftp_dir)
    command_line = add_benchmark_arguments(command_line, machine)
    command_line = add_accuracy_checker_arguments(command_line, machine)
    executor.execute_python(command_line)
    return executor


def add_benchmark_arguments(command_line, machine):
    if machine.benchmark.config:
        command_line = '{0} -b {1} --benchmark_executor {2} --benchmark_res_file {3} --benchmark_log_file {4}'.format(
            command_line, machine.benchmark.config, machine.benchmark.executor, machine.benchmark.res_file,
            machine.benchmark.log_file)
    return command_line


def add_accuracy_checker_arguments(command_line, machine):
    if machine.accuracy_checker.config:
        command_line = '{0} -ac {1} --accuracy_checker_executor {2} --accuracy_checker_res_file {3} \
        --accuracy_checker_log_file {4} --accuracy_checker_definitions {5} --accuracy_checker_source {6}'.format(
            command_line, machine.accuracy_checker.config, machine.accuracy_checker.executor,
            machine.accuracy_checker.res_file, machine.accuracy_checker.log_file, machine.accuracy_checker.definitions,
            machine.accuracy_checker.datasets)
    return command_line


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout
    )
    args = build_parser()
    log.info('Parsing configuration file')
    machine_list = config_parser.parse_config(args.config)

    client_list = []
    log.info('Clients start executing')
    for machine in machine_list:
        client_list.append(client_execution(
            machine,
            args.server_ip,
            args.server_login,
            args.server_psw,
            args.ftp_dir,
            log
        ))

    log.info('Executor script is waiting for all experiments')
    for client in client_list:
        client.wait_all()

    ftp_connection = ftplib.FTP(
        args.server_ip,
        args.server_login,
        args.server_psw
    )
    ftp_connection.cwd(args.ftp_dir)
    table_format.join_tables(ftp_connection, args.benchmark_result_table)
    table_format.join_tables(ftp_connection, args.accuracy_checker_result_table)
    ftp_connection.close()


if __name__ == '__main__':
    sys.exit(main() or 0)
