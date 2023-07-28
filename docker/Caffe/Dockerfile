FROM ubuntu_for_dli

WORKDIR /root/
RUN wget -q --no-check-certificate -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    ./miniconda3/bin/conda create -n caffe-env -y python=3.6.5 && \
    rm -rf /root/miniconda3/pkgs/* && \
    rm ~/Miniconda3-latest-Linux-x86_64.sh -f

ENV PATH /root/miniconda3/envs/caffe-env/bin:/root/miniconda3/bin:$PATH
RUN echo "source activate caffe-env" > ~/.bashrc
RUN export LD_LIBRARY_PATH=/root/miniconda3/envs/caffe-env/lib:${LD_LIBRARY_PATH}
RUN conda config --add channels intel
RUN /bin/bash -c "conda install -n caffe-env -y -c intel openvino-ie4py-ubuntu20=2022.1.0"
RUN /bin/bash -c "conda install -n caffe-env -y -c intel scikit-image=0.17.2"
RUN /bin/bash -c "conda install -n caffe-env -y -c intel caffe"
RUN /bin/bash -c "conda install -n caffe-env -y -c anaconda libgcc-ng=11.2.0"
RUN /bin/bash -c "conda install -n caffe-env -y -c defaults protobuf=3.17.2 libprotobuf=3.17.2 requests=2.27.1"

WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN /bin/bash -c "python3 setup.py install_core"
RUN /bin/bash -c "accuracy_check -c /tmp/dl-benchmark/docker/Caffe/config.yml -m data/test_models -s sample"

WORKDIR /tmp/
COPY models.lst models.lst
RUN /bin/bash -c "python3 ./open_model_zoo/tools/model_tools/downloader.py --list models.lst"
RUN rm models.lst
