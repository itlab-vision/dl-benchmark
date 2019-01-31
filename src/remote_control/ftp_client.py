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
    parser.add_argument('-os', '--os_type', type = str,
        help = 'Type of operating system.', required = True)
    return parser

def main():
    param_list = build_parser().parse_args()
    if (param_list.os_type == 'Windows')
        os.system(os.path.dirname(os.path.abspath(__file__))
            + '\\launch_benchmark.bat')
    elif (param_list.os_type == 'Linux')
        pass
    ftp_con = ftplib.FTP(param_list.server_ip,
        param_list.login, param_list.password)
    f = open(os.path.dirname(os.path.abspath(__file__)) +
        '\\result_table.csv', 'rb')
    send = ftp_con.storbinary('STOR '+ platform.node() +
        '_result_table.csv', f)
    ftp_con.close()



if __name__ == '__main__':
    sys.exit(main() or 0)

