import os
import argparse
import ftplib
import sys

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server_ip', help = 'FTP server IP.',
        required = True, type = str)
    parser.add_argument('-l', '--server_login', type = str,
        help = 'Login to FTP server', required = True)
    parser.add_argument('-p', '--server_psw', type = str,
        help = 'Password to FTP server', required = True)
    parser.add_argument('-i', '--image_path', required = True, type = str,
        help = 'Path to container image on FTP server.')
    parser.add_argument('-d', '--download_dir', required = True, type = str,
        help = 'Path to directory on target machine where to download container image.')
    return parser.parse_args()

def prepare_ftp_connection(server_ip, server_login, server_psw, image_dir):
    log.info('Trying to connect to FTP server')
    ftp_connection = ftplib.FTP(server_ip, server_login, server_psw)
    log.info('Created FTP connection')

    if ftp_connection.pwd() != image_dir:
        log.info('Change current {} directory to target : {}'.format(ftp_connection.pwd(), image_dir))
        ftp_connection.cwd(image_dir)

    return ftp_connection

def download_image(server_ip, server_login, server_psw, image_dir, download_dir):
    ftp_connection = prepare_ftp_connection(server_ip, server_login, server_psw, image_dir)
    with open(download_dir, 'wb') as container_image:
        ftp_con.retrbinary('RETR {}'.format(os.path.split(args.image_path)[1]),
            container_image.write)


def main():
    args = build_parser()
    download_image(args.server_ip, args.server_login, args.server_psw,
        args.image_path, args.download_dir)

    os.system('docker load {}'.format())
    os.system('docker run --privileged {}'.os.path.split(args.image_path)[1])


if __name__ == '__main__':
    sys.exit(main() or 0)
