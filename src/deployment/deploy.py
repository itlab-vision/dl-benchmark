import argparse
import ftplib
import logging as log
import os
import sys
from xml.dom import minidom

from remote_executor import RemoteExecutor


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--server_ip',
                        help='FTP server IP.',
                        required=True,
                        type=str)
    parser.add_argument('-l', '--server_login',
                        type=str,
                        help='Login to the FTP server.',
                        required=True)
    parser.add_argument('-p', '--server_psw',
                        type=str,
                        help='Password to the FTP server.',
                        required=True)
    parser.add_argument('-i', '--image_path',
                        required=True,
                        type=str,
                        help='Path to the container image on the host machine.')
    parser.add_argument('-d', '--upload_dir',
                        required=True,
                        type=str,
                        help='Path to the directory on the FTP server to copy the container image.')
    parser.add_argument('-n', '--container_name',
                        required=True,
                        type=str,
                        help='Name of the docker container.')
    parser.add_argument('--machine_list',
                        required=True,
                        type=str,
                        help='Path to the config file in .xml format.')
    parser.add_argument('--project_folder',
                        required=True,
                        type=str,
                        help='Link to github project.')

    args = parser.parse_args()

    if not os.path.isfile(args.image_path):
        raise ValueError('Wrong path to container image!')

    return args


def prepare_ftp_connection(server_ip, server_login, server_psw, upload_dir, log):
    log.info('Deploy script is connecting to the FTP server')
    ftp_connection = ftplib.FTP(server_ip, server_login, server_psw)
    log.info('FTP connection was created')

    if ftp_connection.pwd() != upload_dir:
        log.info(f'Current directory {ftp_connection.pwd()} changed to target : {upload_dir}')
        ftp_connection.cwd(upload_dir)
    return ftp_connection


def copy_image_to_server(server_ip, server_login, server_psw, upload_dir, image_path, log):
    ftp_connection = prepare_ftp_connection(
        server_ip,
        server_login,
        server_psw,
        upload_dir,
        log,
    )

    target_image = open(image_path, 'rb')
    image_name = os.path.split(image_path)[1]

    log.info('Image copying to server')
    ftp_connection.storbinary(f'STOR {image_name}', target_image)
    log.info('Image copied to server')

    ftp_connection.close()


def parse_machine_list(path_to_config):
    CONFIG_ROOT_TAG = 'Computer'
    CONFIG_IP_TAG = 'IP'
    CONFIG_LOGIN_TAG = 'Login'
    CONFIG_PASSWORD_TAG = 'Password'
    CONFIG_OS_TAG = 'OS'
    CONFIG_DOWNLOAD_FOLDER_TAG = 'DownloadFolder'
    CONFIG_DATASET_FOLDER_TAG = 'DatasetFolder'
    CONFIG_MODEL_FOLDER_TAG = 'ModelFolder'

    parsed_config = minidom.parse(path_to_config)
    machine_list = []

    computers = parsed_config.getElementsByTagName(CONFIG_ROOT_TAG)
    for idx, computer in enumerate(computers):
        machine_list.append({})
        machine_list[idx]['ip'] = computer.getElementsByTagName(CONFIG_IP_TAG)[0].firstChild.data
        machine_list[idx]['login'] = computer.getElementsByTagName(CONFIG_LOGIN_TAG)[0].firstChild.data
        machine_list[idx]['password'] = computer.getElementsByTagName(CONFIG_PASSWORD_TAG)[0].firstChild.data
        machine_list[idx]['os_type'] = computer.getElementsByTagName(CONFIG_OS_TAG)[0].firstChild.data
        machine_list[idx]['download_folder'] = computer.getElementsByTagName(
            CONFIG_DOWNLOAD_FOLDER_TAG)[0].firstChild.data
        machine_list[idx]['dataset_folder'] = computer.getElementsByTagName(
            CONFIG_DATASET_FOLDER_TAG)[0].firstChild.data
        machine_list[idx]['model_folder'] = computer.getElementsByTagName(
            CONFIG_MODEL_FOLDER_TAG)[0].firstChild.data
    return machine_list


def client_execution(machine, server_ip, server_login, server_psw, image_path, download_dir,
                     project_folder, container_name, model_path, dataset_path, log):
    executor = RemoteExecutor(machine['os_type'], log)
    executor.create_connection(machine['ip'], machine['login'], machine['password'])
    joined_pass = os.path.join(project_folder, 'src/bench_deploy')
    project_folder = os.path.normpath(joined_pass)
    command = (f'python3 {project_folder}/client.py '
               f'-s {server_ip} '
               f'-l {server_login} '
               f'-p {server_psw} '
               f'-i {image_path} '
               f'-d {download_dir} '
               f'-n {container_name} '
               f'-mp {model_path} '
               f'-dp {dataset_path} > log.txt')
    executor.execute_command(command)
    return executor


def main():
    # Enable log formatting
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )

    args = cli_argument_parser()

    # First stage send container to the FTP server
    copy_image_to_server(
        args.server_ip,
        args.server_login,
        args.server_psw,
        args.upload_dir,
        args.image_path,
        log,
    )

    # Second stage config file and prepare machine list
    machine_list = parse_machine_list(args.machine_list)

    # Third stage connect to each machine start client script
    client_list = []
    log.info('Clients start executing')
    image_ftp_path = os.path.join(args.upload_dir, os.path.split(args.image_path)[1])
    for machine in machine_list:
        client_list.append(client_execution(
            machine,
            args.server_ip,
            args.server_login,
            args.server_psw,
            image_ftp_path,
            machine['download_folder'],
            args.project_folder,
            args.container_name,
            machine['model_folder'],
            machine['dataset_folder'],
            log,
        ))

    # Fourth stage wait all clients
    log.info('Deploy script is waiting clients')
    for client in client_list:
        client.wait_all()

    log.info('Deploy status:')
    for client in client_list:
        log.info(client.get_status())


if __name__ == '__main__':
    sys.exit(main() or 0)
