FROM ubuntu_for_dli

# Install pycocotools, docker, PyYAML
RUN pip3 install pycocotools docker PyYAML

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

# Install GluonCV
RUN pip3 install gluoncv[full]

# Install MXNet
ARG MXNET_VERSION=1.9.1
RUN pip3 install mxnet==${MXNET_VERSION}
RUN pip uninstall -y numpy && pip install numpy==1.23.1

# Download Accuracy Checker
WORKDIR /tmp/
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN /bin/bash -c 'accuracy_check -c /tmp/dl-benchmark/docker/MXNet/config.yml -m data/test_models -s sample'
WORKDIR /tmp/
