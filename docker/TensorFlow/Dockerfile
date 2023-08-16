FROM ubuntu_for_dli

WORKDIR /root/
ARG TF_VERSION=2.12.0
ARG FRAMEWORK
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python requests PyYAML docker
RUN export LD_LIBRARY_PATH=/root/miniconda3/lib:${LD_LIBRARY_PATH}

WORKDIR /tmp/
COPY models.lst models.lst
RUN python3 ./open_model_zoo/tools/model_tools/downloader.py --list models.lst
RUN rm models.lst

WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
COPY config_tf2.yml config_tf2.yml
COPY config_intel-tf.yml config_intel-tf.yml

RUN if [ "$FRAMEWORK" = "intel-tensorflow" ] || [ -z "$FRAMEWORK" ] ; then \
        pip3 install intel-tensorflow==${TF_VERSION}; \
        python3 setup.py install_core; \
        accuracy_check -c config_intel-tf.yml -m data/test_models -s sample; \
    elif [ "$FRAMEWORK" = "tensorflow" ] ; then \
        pip3 install tensorflow==${TF_VERSION}; \
        python3 setup.py install_core; \
        accuracy_check -c config_tf2.yml -m data/test_models -s sample; \
    fi
RUN rm config_tf2.yml && rm config_intel-tf.yml

WORKDIR /tmp/