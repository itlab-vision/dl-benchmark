FROM ubuntu_for_dli

WORKDIR /root/
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python requests PyYAML docker
RUN export LD_LIBRARY_PATH=/root/miniconda3/lib:${LD_LIBRARY_PATH}
RUN pip3 install intel-tensorflow==2.12.0

WORKDIR /tmp/
COPY models.lst models.lst
RUN python3 ./open_model_zoo/tools/model_tools/downloader.py --list models.lst
RUN rm models.lst

#ARG DATASET_DOWNLOAD_LINK=<Link to dataset project>
#RUN git clone $DATASET_DOWNLOAD_LINK

WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN python3 setup.py install_core
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN accuracy_check -c /tmp/dl-benchmark/docker/TensorFlow/config.yml -m data/test_models -s sample

WORKDIR /tmp/