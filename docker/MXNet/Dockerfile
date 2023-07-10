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

# Download Accuracy Checker
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN /bin/bash -c 'accuracy_check -c sample/sample_config.yml -m data/test_models -s sample'
WORKDIR /tmp/
