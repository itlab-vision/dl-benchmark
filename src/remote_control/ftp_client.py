import ftplib
import argparse
import sys
import platform
import os


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


def main():
    param_list = build_parser().parse_args()
    path_to_ftp_client = os.path.split(os.path.abspath(__file__))[0]
    path_to_benchmark = os.path.normpath(path_to_ftp_client +
        '//..//benchmark')
    if param_list.os_type == 'Windows':
        os.system(('{} & cd {} & python inference_benchmark.py -c {}' + 
            ' -f {}\\result_table.csv').format(param_list.path_to_env,
            path_to_benchmark, param_list.benchmark_config,
            path_to_ftp_client))
    
    elif param_list.os_type == 'Linux':
        os.system(('source {}; cd {}; python inference_benchmark.py -c {}' + 
            ' -f {}\\result_table.csv').format(param_list.path_to_env,
            path_to_benchmark, param_list.benchmark_config,
            path_to_ftp_client))
    ftp_con = ftplib.FTP(param_list.server_ip,
        param_list.login, param_list.password)
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'result_table.csv'), 'rb')
    send = ftp_con.storbinary('STOR '+ platform.node() +
        '_result_table.csv', f)
    ftp_con.close()


if __name__ == '__main__':
    sys.exit(main() or 0)