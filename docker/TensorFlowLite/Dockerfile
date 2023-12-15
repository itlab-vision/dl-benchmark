FROM ubuntu_for_dli

WORKDIR /root/
ARG TFLITE_VERSION=2.10.0
ARG TF_VERSION=2.10.0
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python requests PyYAML docker
RUN export LD_LIBRARY_PATH=/root/miniconda3/lib:${LD_LIBRARY_PATH}

WORKDIR /tmp/
COPY downloadmodels.sh downloadmodels.sh
COPY models.lst models.lst
RUN python3 ./open_model_zoo/tools/model_tools/downloader.py --name mobilenet-v1-1.0-224-tf

RUN pip3 install -r ./dl-benchmark/src/model_converters/requirements.txt
RUN pip3 install tensorflow==${TF_VERSION}
RUN pip3 install tflite==${TFLITE_VERSION}
RUN pip3 install --upgrade numpy==1.23.5
RUN pip3 install --upgrade Tensorflow.probability==0.18.0
RUN pip3 install --upgrade onnx==1.10.2
RUN python3 ./open_model_zoo/tools/model_tools/converter.py --name mobilenet-v1-1.0-224-tf

WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
COPY config_tf2.yml config_tf2.yml


RUN python3 setup.py install_core
RUN accuracy_check -c config_tf2.yml -m ../../../public -s sample

RUN rm config_tf2.yml

WORKDIR /tmp/
