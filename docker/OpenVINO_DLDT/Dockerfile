FROM ubuntu_for_dli

# Install OpenVINO
ARG OV_SHORT_VERSION=2023.3
ARG OV_LONG_VERSION="${OV_SHORT_VERSION}.0.13775.ceeafaf64f3_x86_64"
RUN sudo mkdir /opt/intel && \
    wget -q https://storage.openvinotoolkit.org/repositories/openvino/packages/${OV_SHORT_VERSION}/linux/l_openvino_toolkit_ubuntu22_${OV_LONG_VERSION}.tgz \
        -O /tmp/openvino.tgz --no-check-certificate --quiet && \
    tar -zxvf /tmp/openvino.tgz -C /opt/intel/ && \
    sudo ln -s /opt/intel/l_openvino_toolkit_ubuntu22_${OV_LONG_VERSION} /opt/intel/openvino_2023 && \
    rm /tmp/openvino.tgz

# Install OpenVINO dependencies
ENV INSTALL_DIR /opt/intel/openvino_2023/
WORKDIR $INSTALL_DIR/install_dependencies
RUN echo y | ./install_openvino_dependencies.sh
RUN cat /root/.bashrc > tmp && echo 'source $INSTALL_DIR/setupvars.sh' > /root/.bashrc

# Configure for GPU
RUN sudo apt install -y gpg-agent
RUN wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \ 
    sudo gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] \
    https://repositories.intel.com/gpu/ubuntu jammy unified" | \
    sudo tee /etc/apt/sources.list.d/intel-gpu-jammy.list
RUN sudo apt-get update -y
RUN sudo apt-get install -y -qq ocl-icd-libopencl1 intel-opencl-icd intel-level-zero-gpu level-zero
RUN usermod -a -G video,users root

# Test Accuracy Checker
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN pip3 uninstall opencv-python -y && pip3 install "opencv-python-headless"
RUN /bin/bash -c "accuracy_check -c sample/sample_config.yml -m data/test_models -s sample"

WORKDIR /tmp/

