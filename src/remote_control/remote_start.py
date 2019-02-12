import wmi
import paramiko
import os
import sys
import argparse
import logging as log
import config_parser


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str,
        help = 'Path to configuration file', required = True)
    parser.add_argument('-s', '--server_ip', type = str,
        help = 'Ip FTP server', required = True)
    parser.add_argument('-l', '--server_login', type = str,
        help = 'Login to FTP server', required = True)
    parser.add_argument('-p', '--server_psw', type = str,
        help = 'Password to FTP server', required = True)
    parser = parser.parse_args()
    if not os.path.isfile(parser.config):
        raise ValueError('Wrong path to configuration file!')
    return parser


def run_benchmark(machine, server_ip, server_login, server_psw):
    if machine.os_type == 'Windows':
        run_on_windows(machine, server_ip, server_login, server_psw)
    elif machine.os_type == 'Linux':
        run_on_linux(machine, server_ip, server_login, server_psw)


def run_on_linux(machine, server_ip, server_login, server_psw): 
    paramiko_con = paramiko.SSHClient()
    paramiko_con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko_con.connect(hostname=machine.ip, username=machine.login,
        password=machine.psw)
    paramiko_con.exec_command('python {} -ip {} -l {} -p {} -os {}'.format(
        machine.client_path, server_ip, server_login,
        server_psw, machine.os_type))
    paramiko_con.close()


def run_on_windows(machine, server_ip, server_login, server_psw):
    wmi_con = wmi.WMI(machine.ip, user=machine.login, password=machine.psw)
    process_startup = wmi_con.Win32_ProcessStartup.new()
    process_id, result = wmi_con.Win32_Process.Create(CommandLine=(
        'cmd.exe /c python {} -ip {} -l {} -p {} -os {}'.format(
        machine.client_path, server_ip, server_login,
        server_psw, machine.os_type)),
        ProcessStartupInformation=process_startup)
    if result == 0:
        log.info('Process started successfully {}'.format(process_id))
    else:
        log.info('Problem creating process {}'.format(result))


def main():
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    parser = build_parser()
    log.info('Parsing config file')
    machine_list = config_parser.parse_config(parser.config)
    for machine in machine_list:
        log.info('Run benchmark on {} machine'.format(machine.ip))
        run_benchmark(machine, parser.server_ip, parser.server_login,
            parser.server_psw)
    log.info('Benchmark run on all machines')


if __name__ == '__main__':
    sys.exit(main() or 0)