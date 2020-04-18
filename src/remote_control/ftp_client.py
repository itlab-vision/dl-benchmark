import ftplib
import argparse
import sys
import platform
import os
import subprocess


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--server_ip', type = str,
        help = 'Main ftp server address.', required = True)
    parser.add_argument('-l', '--login', type = str,
        help = 'Login to connect to ftp server.', required = True)
    parser.add_argument('-p', '--password', type = str,
        help = 'Password to connect to ftp server.', required = True)
    parser.add_argument('-env', '--path_to_env', type = str,
        help = 'Path to OpenVINO environment.', required = True)
    parser.add_argument('-b', '--benchmark_config', type = str,
        help = 'Path to config file.', required = True)
    parser.add_argument('-os', '--os_type', type = str,
        help = 'Type of operating system.', required = True)
    parser.add_argument('--res_file', type = str,
        help = 'The name of the file to which the results'
        'are written', required = True)
    parser.add_argument('--log_file', type = str,
        help = 'The name of the file to which the logs'
        'are written', required = True)
    return parser

def launch_benchmark(path_to_env, path_to_benchmark, benchmark_config,
                     os_type, path_to_res_table, log_file):
    if os_type == 'Windows':
        launch_benchmark_on_win(path_to_env, path_to_benchmark, 
            benchmark_config, path_to_res_table, log_file)
    elif os_type == 'Linux':
        launch_benchmark_on_linux(path_to_env, path_to_benchmark, 
            benchmark_config, path_to_res_table, log_file)
    else:
        raise ValueError('Unsupported OS')


def launch_benchmark_on_win(path_to_env, path_to_benchmark, benchmark_config,
                            path_to_res_table, log_file):
    os.system(('{} > {} & cd {} & python inference_benchmark.py -c {}' + 
        ' -f {} >> {}').format(path_to_env, log_file, path_to_benchmark, 
        benchmark_config, path_to_res_table, log_file))


def launch_benchmark_on_linux(path_to_env, path_to_benchmark,
                              benchmark_config, path_to_res_table, log_file):
    sp = subprocess.Popen(('source {} > {}; cd {};' +
        'python3 inference_benchmark.py -c {} -f {} >> {}').format(path_to_env,
        log_file, path_to_benchmark, benchmark_config, path_to_res_table,
        log_file), shell=True, executable='/bin/bash')
    sp.communicate()



def main():
    param_list = build_parser().parse_args()
    path_to_ftp_client = os.path.split(os.path.abspath(__file__))[0]
    path_to_benchmark = os.path.normpath(path_to_ftp_client +
        '//..//benchmark')
    log_file = os.path.join(path_to_ftp_client, param_list.log_file)
    path_to_res_table = os.path.join(path_to_ftp_client, param_list.res_file)

    #Connect to FTP and take benchmark config file
    ftp_connection = ftplib.FTP(param_list.server_ip,
        param_list.login, param_list.password)

    with open(param_list.benchmark_config, 'wb') as config_file:
        ftp_connection.retrbinary('RETR {}'.format(param_list.benchmark_config),
            config_file.write)

    launch_benchmark(param_list.path_to_env, path_to_benchmark,
        param_list.benchmark_config, param_list.os_type,
        path_to_res_table, log_file)

    result_table = open(path_to_res_table, 'rb')
    ftp_connection.storbinary('STOR {}_result_table.csv'.format(platform.node()),
        result_table)
    ftp_connection.close()


if __name__ == '__main__':
    sys.exit(main() or 0)