FROM ubuntu_for_dli

WORKDIR /root/
ARG PADDLE_VERSION=2.6.0
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python requests PyYAML docker
RUN export LD_LIBRARY_PATH=/root/miniconda3/lib:${LD_LIBRARY_PATH}

WORKDIR /tmp/
COPY downloadmodels.sh downloadmodels.sh
COPY models.lst models.lst
RUN mkdir resnet50_paddle
RUN curl -o .\resnet50_paddle\resnet50.pdmodel https://github.com/itlab-vision/itlab-vision-dl-benchmark-models/main/paddlepaddle_models/resnet50/resnet50/resnet50.pdmodel
RUN curl -o .\resnet50_paddle\resnet50.pdiparams https://github.com/itlab-vision/itlab-vision-dl-benchmark-models/main/paddlepaddle_models/resnet50/resnet50/resnet50.pdiparams

RUN pip3 install paddlepaddle==${PADDLE_VERSION} -i https://mirror.baidu.com/pypi/simple

WORKDIR /tmp/
