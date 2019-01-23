import ftplib
import argparse
import sys
import platform


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--server_ip', type = str,
        help = 'Main ftp server address.', required = True)
    parser.add_argument('-l', '--login', type = str,
        help = 'Login to connect to ftp server.', required = True)
    parser.add_argument('-p', '--password', type = str,
        help = 'Password to connect to ftp server.', required = True)
    parser.add_argument('-f', '--file_name', type = str,
        help = 'CSV table name.', required = True)
    return parser

def main():
    param_list = build_parser().parse_args()
    ftp_con = ftplib.FTP(param_list.server_ip,
        param_list.login, param_list.password)
    f = open(param_list.file_name, 'rb')
    send = ftp_con.storbinary('STOR '+ platform.node() +
        '_' + param_list.file_name, f)
    ftp_con.close


if __name__ == '__main__':
    sys.exit(main() or 0)

