import os
import argparse
import ftplib
import sys

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server_ip', help = 'FTP server IP.',
        required = True, type = str)
    parser.add_argument('-l', '--server_login', type = str,
        help = 'Login to the FTP server.', required = True)
    parser.add_argument('-p', '--server_psw', type = str,
        help = 'Password to the FTP server.', required = True)
    parser.add_argument('-i', '--image_path', required = True, type = str,
        help = 'Path to container image on FTP server.')
    parser.add_argument('-d', '--upload_dir', required = True, type = str,
        help = 'Path to the directory on target machine where to upload container image.')
    return parser.parse_args()

def prepare_ftp_connection(server_ip, server_login, server_psw, image_path, log):
    log.info('Trying to connect to FTP server')
    ftp_connection = ftplib.FTP(server_ip, server_login, server_psw)
    log.info('Created FTP connection')

    image_dir = os.path.split(image_path)[0]
    if ftp_connection.pwd() != image_dir:
        log.info('Change current {} directory to target : {}'.format(ftp_connection.pwd(), image_dir))
        ftp_connection.cwd(image_dir)

    return ftp_connection

def upload_container_image(server_ip, server_login, server_psw, image_path, upload_dir, file_path, log):
    ftp_connection = prepare_ftp_connection(server_ip, server_login, server_psw, image_path, log)

    log.info('Download image from server')
    with open(file_path, 'wb') as container_image:
        ftp_connection.retrbinary('RETR {}'.format(os.path.split(image_path)[1]),
            container_image.write)
    log.info('Image download to client')

def main():
    # Enable log formatting
    log.basicConfig(format = '[ %(levelname)s ] %(message)s',
        level = log.INFO, stream = sys.stdout)

    args = build_parser()

    image_name = os.path.split(args.image_path)[1]
    joined_pass = os.path.join(args.upload_dir, image_name)
    file_path = os.path.normpath(joined_pass)

    upload_container_image(args.server_ip, args.server_login, args.server_psw,
        args.image_path, args.upload_dir, file_path, log)

    log.info('Load docker image from tar')
    os.system('docker load --input {}'.format(file_path))

    log.info('Run docker image')
    os.system('docker run --privileged -d -t {}'.format(image_name.split('.')[0]))

if __name__ == '__main__':
    sys.exit(main() or 0)
