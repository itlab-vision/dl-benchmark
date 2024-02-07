# Creating docker image of the computational node

## Install and configure Docker

1. Install Docker.

   ```bash
   sudo apt install docker.io
   ```

1. Add user to the docker group.

   ```bash
   sudo usermod -aG docker ${USER}
   ```

1. Relogin to activate changes.

   ```bash
   su ${USER}
   ```

## Build and archive the docker image

1. Build a base image.

   ```bash
   docker build -t ubuntu_for_dli [--build-arg DLI_BRANCH="<tag>"] \ 
       [--build-arg DATASET_DOWNLOAD_LINK="https://<github_user>:<user_gpg_key>@github.com/<repo>.git"] \
       <dockerfile_parent_dir>
   ```

1. Go to the directory with the framework of interest
   and build the image.

   ```bash
   docker build -t <image_name> <dockerfile_parent_dir>
   ```

1. Save the docker image to the archive.

   ```bash
   docker save <image_name> > <image_name>.tar
   ```

## Download and the archived docker image

1. Upload the image to the system.

   ```bash
   docker load < <image_name>.tar
   ```

1. Run the docker image.

   ```bash
   docker run -it <image_name>
   ```

## An example of a sequence of commands for building the OpenVINO image and executing benchmark

```bash
cd docker/
docker build -t ubuntu_for_dli .
cd OpenVINO_DLDT/
docker stop OpenVINO_DLDT
docker rm OpenVINO_DLDT
docker rmi dli_openvino:2022.2
docker build -t dli_openvino:2022.2 .
docker save dli_openvino:2022.2 > dli_openvino:2022.2.tar
docker load < dli_openvino:2022.2.tar
sudo docker run --privileged -it -d -v /dev:/dev \
    -v /tmp/models:/media/models \
    -v /tmp/datasets:/media/datasets \
    --name OpenVINO_DLDT \
      dli_openvino:2022.2
cd ../../src/benchmark
python3 inference_benchmark.py --executor_type docker_container \
    -c benchmark_config.xml -r results.csv
```

**Notes**:

1. `inference_benchmark.py` from the benchmark test configuration
   extracts the inference framework name (`OpenVINO_DLDT`) and connects
   to the running docker image by the given name, therefore, specifying
   the image name `--name OpenVINO_DLDT` when starting it is mandatory.
1. If there is a need to save a repository with datasets or models
   into the docker image, then when building the image you should specify
   the additional parameter:
   `--build-arg DATASET_DOWNLOAD_LINK="<YOUR_REPOSITORY>"`.
