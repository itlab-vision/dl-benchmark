FROM ubuntu_for_dli

WORKDIR /root/
ARG SPEKTRAL_VERSION=1.3.0
ARG TF_VERSION=2.13.0
RUN pip3 install --upgrade pip

RUN pip3 install tensorflow==${TF_VERSION};
RUN pip3 install spektral==${SPEKTRAL_VERSION};