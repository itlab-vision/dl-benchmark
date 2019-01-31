import wmi
import paramiko
import os
import sys
import argparse
import logging as log
import config_parser

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str, dest = 'config_path',
        help = 'Path to configuration file', required = True)
    config = parser.parse_args().config_path
    if not os.path.isfile(config):
        raise ValueError('Wrong path to configuration file!')
    return config

def run_benchmark(machine):
    if machine.os_type == 'Windows':
        run_on_windows(machine)
    elif machine.os_type == 'Linux':
        run_on_linux(machine)

def run_on_linux(machine): 
    paramiko_con = paramiko.SSHClient()
    paramiko_con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    paramiko_con.connect(hostname=machine.ip, username=machine.login,
        password=machine.psw)
    stdin, stdout, stderr = paramiko_con.exec_command('py3 ' + 
        machine.client_path + ' -ip ' + machine.ip + ' -l ' + 
        machine.login + ' -p ' + machine.psw + ' -os ' + machine.os_type)
    paramiko_con.close()

def run_on_windows(machine):
    wmi_con = wmi.WMI(machine.ip, user=machine.login, password=machine.psw)
    process_startup = wmi_con.Win32_ProcessStartup.new()
    process_id, result = wmi_con.Win32_Process.Create(CommandLine=('cmd.exe /c' 
        ' python ' + machine.client_path + ' -ip ' + machine.ip + ' -l ' + 
        machine.login + ' -p ' + machine.psw + ' -os ' + machine.os_type),
        ProcessStartupInformation=process_startup)
    if result == 0:
        log.info('Process started successfully {}'.format(process_id))
    else:
        log.info('Problem creating process {}'.format(result))

def main():
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)
    config = build_parser()
    log.info('Parsing config file')
    machine_list = config_parser.parse_config(config)
    for machine in machine_list:
        log.info('Run benchmark on {} machine'.format(machine.ip))
        run_benchmark(machine)
    log.info('Benchmark run on all machines')


if __name__ == '__main__':
    sys.exit(main() or 0)