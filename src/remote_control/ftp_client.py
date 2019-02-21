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
        help = 'Path to OpenVINO environment.', required = True)
    parser.add_argument('-os', '--os_type', type = str,
        help = 'Type of operating system.', required = True)
    return parser

def launch_benchmark(path_to_env, path_to_benchmark, path_to_ftp_client,
                     benchmark_config, os_type):
    if os_type == 'Windows':
        launch_benchmark_on_win(path_to_env, path_to_benchmark, 
            path_to_ftp_client, benchmark_config)
    elif os_type == 'Linux':
        launch_benchmark_on_linux(path_to_env, path_to_benchmark, 
            path_to_ftp_client, benchmark_config)


def launch_benchmark_on_win(path_to_env, path_to_benchmark, path_to_ftp_client,
                            benchmark_config):
    os.system(('{} & cd {} & python inference_benchmark.py -c {}' + 
            ' -f {}\\result_table.csv').format(path_to_env, path_to_benchmark, 
            benchmark_config, path_to_ftp_client))


def launch_benchmark_on_linux(path_to_env, path_to_benchmark,
                              path_to_ftp_client, benchmark_config):
    sp = subprocess.Popen(['/bin/bash', '-i', '-c', ('source {}; cd {};' +
        ' python3 inference_benchmark.py -c {} -f {}\\result_table.csv').format(
            path_to_env, path_to_benchmark, benchmark_config,
            path_to_ftp_client)])
    sp.communicate()



def main():
    param_list = build_parser().parse_args()
    path_to_ftp_client = os.path.split(os.path.abspath(__file__))[0]
    path_to_benchmark = os.path.normpath(path_to_ftp_client +
        '//..//benchmark')
    launch_benchmark(param_list.path_to_env, path_to_benchmark,
        path_to_ftp_client, param_list.benchmark_config,
        param_list.os_type)
        
    ftp_con = ftplib.FTP(param_list.server_ip,
        param_list.login, param_list.password)
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'result_table.csv'), 'rb')
    send = ftp_con.storbinary('STOR '+ platform.node() +
        '_result_table.csv', f)
    ftp_con.close()


if __name__ == '__main__':
    sys.exit(main() or 0)