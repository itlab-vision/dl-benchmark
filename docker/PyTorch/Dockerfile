FROM ubuntu_for_dli

WORKDIR /root/
ARG TORCH_VERSION=2.0.1
ARG TORCHVISION_VERSION=0.15.2
RUN pip3 install --upgrade pip && \
    pip3 install opencv-python requests

RUN pip3 install torch==${TORCH_VERSION} \
                 torchvision==${TORCHVISION_VERSION}

ENV ACCURACY_CHECKER_PATH=/tmp/open_model_zoo/tools/accuracy_checker
WORKDIR $ACCURACY_CHECKER_PATH
COPY config.yml config.yml
# make module path relative
ARG MODELS_DIR=$ACCURACY_CHECKER_PATH/data/test_models
RUN sed -i 's|MODELS_DIR|'${MODELS_DIR}'|g' config.yml

# please uncomment out when OMZ version will be >=2023.0 (see commit: a89aade)
# RUN python3 setup.py install_core; \
#    accuracy_check -c config.yml -m data/test_models -s sample

WORKDIR /tmp/
