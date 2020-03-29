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

def prepare_ftp_connection(server_ip, server_login, server_psw, image_path):
    ftp_connection = ftplib.FTP(server_ip, server_login, server_psw)
    image_dir = os.path.split(image_path)[0]
    if ftp_connection.pwd() != image_dir:
        ftp_connection.cwd(image_dir)

    return ftp_connection

def download_image(server_ip, server_login, server_psw, image_path, download_dir, file_path):
    ftp_connection = prepare_ftp_connection(server_ip, server_login, server_psw, image_path)

    with open(file_path, 'wb') as container_image:
        ftp_connection.retrbinary('RETR {}'.format(os.path.split(image_path)[1]),
            container_image.write)

def main():
    args = build_parser()

    image_name = os.path.split(args.image_path)[1]
    joined_pass = os.path.join(args.download_dir, image_name)
    file_path = os.path.normpath(joined_pass)

    download_image(args.server_ip, args.server_login, args.server_psw,
        args.image_path, args.download_dir, file_path)

    os.system('docker load --input {}'.format(file_path))
    os.system('docker run --privileged -d -t {}'.format(image_name.split('.')[0]))

if __name__ == '__main__':
    sys.exit(main() or 0)
