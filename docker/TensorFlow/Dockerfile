FROM ubuntu:18.04
USER root
WORKDIR /

ARG DEPENDENCIES="autoconf \
                  ca-certificates \
                  libgtk2.0-dev \
                  sudo \
                  vim \
                  wget \
                  git"
RUN apt-get update && \
        apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
        rm -rf /var/lib/apt/lists/*

WORKDIR /root/
RUN python3 -m pip install —force-reinstall pip==19.0
RUN pip install opencv-python
RUN pip install intel-tensorflow==1.15.2

RUN pip install openvino-python
RUN export LD_LIBRARY_PATH=/root/miniconda3/lib:${LD_LIBRARY_PATH}

WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark
RUN git clone https://github.com/openvinotoolkit/open_model_zoo.git

#WORKDIR /tmp/open_model_zoo/
#ARG TAG_NAME=<Release tag in the open_model_zoo git repository>
#RUN git checkout tags/$TAG_NAME

WORKDIR /tmp/
COPY models.lst models.lst
RUN python3 ./open_model_zoo/tools/downloader/downloader.py --list models.lst
RUN rm models.lst

#ARG DATASET_DOWNLOAD_LINK=<Link to dataset project>
#RUN git clone $DATASET_DOWNLOAD_LINK
