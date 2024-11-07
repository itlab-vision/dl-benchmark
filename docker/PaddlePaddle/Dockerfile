FROM ubuntu_for_dli

WORKDIR /root/
ARG PADDLE_VERSION=2.5.2
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python requests PyYAML docker

WORKDIR /tmp/
RUN mkdir resnet50_paddle
WORKDIR /tmp/resnet50_paddle/
RUN wget -q https://github.com/itlab-vision/itlab-vision-dl-benchmark-models/tree/main/paddlepaddle_models/resnet50/resnet50/inference.pdmodel
RUN wget -q https://github.com/itlab-vision/itlab-vision-dl-benchmark-models/tree/main/paddlepaddle_models/resnet50/resnet50/inference.pdiparams
WORKDIR /tmp/
RUN wget https://paddle-inference-dist.bj.bcebos.com/Paddle-Inference-Demo/resnet50.tgz
RUN tar xzf resnet50.tgz
RUN python3 -m pip install paddlepaddle==${PADDLE_VERSION} -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
COPY config_paddle.yml config_paddle.yml

RUN python3 setup.py install_core

RUN accuracy_check -c config_paddle.yml -m ../../../resnet50 -s sample

WORKDIR /tmp/

