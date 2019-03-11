import os
import sys
import argparse
import logging as log
import config_parser
from process_watcher import process_watcher as pw

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str,
        help = 'Path to configuration file', required = True)
    parser.add_argument('-s', '--server_ip', type = str,
        help = 'FTP server IP', required = True)
    parser.add_argument('-l', '--server_login', type = str,
        help = 'Login to FTP server', required = True)
    parser.add_argument('-p', '--server_psw', type = str,
        help = 'Password to FTP server', required = True)
    parser = parser.parse_args()
    if not os.path.isfile(parser.config):
        raise ValueError('Wrong path to configuration file!')
    return parser


def main():
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    parser = build_parser()
    log.info('Parsing config file')
    machine_list = config_parser.parse_config(parser.config)
    proc_watcher = pw()
    proc_watcher.run_benchmark_on_all_machines(machine_list, parser.server_ip,
        parser.server_login, parser.server_psw)


if __name__ == '__main__':
    sys.exit(main() or 0)