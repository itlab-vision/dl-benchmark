FROM ubuntu:18.04
USER root
WORKDIR /

ARG DEPENDENCIES="autoconf \
                  ca-certificates \
                  libgtk2.0-dev \
                  ffmpeg \
                  libsm6 \
                  libxext6 \
                  python3-pip \
                  python3-setuptools \
                  sudo \
                  vim \
                  wget \
                  git"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root/
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python requests PyYAML docker
RUN pip3 install openvino-python
RUN export LD_LIBRARY_PATH=/root/miniconda3/lib:${LD_LIBRARY_PATH}
RUN pip3 install --force-reinstall pip==19.0 && \
    pip3 install intel-tensorflow==1.15.2

WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark
RUN git clone https://github.com/openvinotoolkit/open_model_zoo.git

WORKDIR /tmp/open_model_zoo/
ARG TAG_NAME=<Release tag in the open_model_zoo git repository>
RUN git checkout tags/$TAG_NAME

WORKDIR /tmp/
COPY models.lst models.lst
RUN python3 ./open_model_zoo/tools/downloader/downloader.py --list models.lst
RUN rm models.lst

ARG DATASET_DOWNLOAD_LINK=<Link to dataset project>
RUN git clone $DATASET_DOWNLOAD_LINK

WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN python3 setup.py install_core
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN accuracy_check -c /tmp/dl-benchmark/docker/TensorFlow/config.yml -m data/test_models -s sample

WORKDIR /tmp/