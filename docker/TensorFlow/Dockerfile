FROM ubuntu_for_dli

WORKDIR /root/
ARG TF_VERSION=2.12.0
ARG FRAMEWORK
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python requests PyYAML docker
RUN export LD_LIBRARY_PATH=/root/miniconda3/lib:${LD_LIBRARY_PATH}

RUN if [ "$FRAMEWORK" = "intel-tensorflow" ] ; then \
        pip3 install intel-tensorflow==${TF_VERSION} ; \
    elif [ "$FRAMEWORK" = "tensorflow" ] ; then \
        pip3 install tensorflow==${TF_VERSION}; \
    fi

WORKDIR /tmp/
COPY models.lst models.lst
RUN python3 ./open_model_zoo/tools/model_tools/downloader.py --list models.lst
RUN rm models.lst

WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN python3 setup.py install_core
RUN accuracy_check -c /tmp/dl-benchmark/docker/TensorFlow/config.yml -m data/test_models -s sample

WORKDIR /tmp/