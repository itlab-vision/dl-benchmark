FROM ubuntu:18.04
USER root
WORKDIR /

ARG DEPENDENCIES="autoconf \
                  ca-certificates \
                  libgtk2.0-dev \
                  sudo \
                  vim \
                  wget \
                  git \
                  libprotobuf-dev \
                  libgl1-mesa-glx"
RUN apt update && \
    apt install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root/
RUN wget --no-check-certificate -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    ./miniconda3/bin/conda config --add channels intel && \
    ./miniconda3/bin/conda install -c intel caffe=1.1.0 python=3.6.5 && \
    ./miniconda3/bin/conda install -c menpo opencv3=3.1.0 && \
    rm -rf /root/miniconda3/pkgs/* && \
    rm ~/Miniconda3-latest-Linux-x86_64.sh -f

ENV PATH /root/miniconda3/bin:$PATH
RUN echo "source activate base" > ~/.bashrc

RUN /bin/bash -c "conda upgrade -c anaconda pip && pip install openvino-python opencv-python docker"
RUN export LD_LIBRARY_PATH=/root/miniconda3/lib:${LD_LIBRARY_PATH}

WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark
RUN git clone https://github.com/openvinotoolkit/open_model_zoo.git

WORKDIR /tmp/open_model_zoo/
ARG TAG_NAME=<Release tag in the open_model_zoo git repository>
RUN git checkout tags/$TAG_NAME

WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN /bin/bash -c "python3 setup.py install_core"
RUN /bin/bash -c "conda install -c anaconda scikit-image=0.14.2"
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN /bin/bash -c "accuracy_check -c /tmp/dl-benchmark/docker/Caffe/config.yml -m data/test_models -s sample"

WORKDIR /tmp/
COPY models.lst models.lst
RUN python3 ./open_model_zoo/tools/downloader/downloader.py --list models.lst
RUN rm models.lst

ARG DATASET_DOWNLOAD_LINK=<Link to dataset project>
RUN git clone $DATASET_DOWNLOAD_LINK
