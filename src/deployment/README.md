# Deployment of infrastructure to run benchmarking

## How to use

Command line:

```bash
python3 deploy.py \
    -s <server_ip> -l <user_login> -p <user_psw> \
    -i <path_to_image> -d <folder_on_FTP> -n <container_name> \
    --machine_list <path_to_config> --project_folder <path_to_project_folder>
```

Command line arguments:

- `-s / --server_ip <server_ip>` is an IP address of the FTP server where
  the container images are stored.
- `-l / --server_login <user_login>` is a login to connect to the FTP server.
- `-p / --server_psw <user_psw>` is a password to connect to the FTP server.
- `-i / --image_path <path_to_image>` is a path to the docker image.
- `-d / --upload_dir <folder_on_FTP>` is a directory on the FTP server
  where the docker image will be uploaded.
- `-n / --container_name <container_name>` is the name with which the docker
  container will be launched.
- `--machine_list <path_to_config>` is a path to the configuration file
  with the list of computing nodes.
- `--project_folder <path_to_project_folder>` is a path to the directory
  containing the project source codes.


**Note**: if arguments are not passed or passed incorrectly, the script
will crash.

## How it works

1. The `deploy.py` script copies the provided docker image to the FTP server.
1. It goes through the list of computing nodes, the parameters of which
   are given in the configuration file `machine_list`, and the client
   `client.py` is launched.
1. `client.py` downloads the docker image from the FTP server, then performs
   a local deployment of the docker image.

## Deployment script results

The result of the script will be a running Docker container on each
machine specified in the `machine_list` configuration file.
