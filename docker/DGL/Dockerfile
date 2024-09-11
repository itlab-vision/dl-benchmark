FROM ubuntu_for_dli

WORKDIR /root/

ARG TORCH_VERSION=2.0.1
ARG TORCHAUDIO_VERSION=2.0.1
ARG TORCHVISION_VERSION=0.15.2

# Update pip
WORKDIR /tmp/
RUN pip3 install --upgrade pip

# Install PyTorch Python
RUN pip3 install torch==${TORCH_VERSION} \
                 torchvision==${TORCHVISION_VERSION} \
                 torchaudio==${TORCHAUDIO_VERSION}

# Install DGL(PyTorch)
RUN pip3 install dgl==2.0.0 -f https://data.dgl.ai/wheels/repo.html
RUN pip3 install dglgo==0.0.2 -f https://data.dgl.ai/wheels-test/repo.html

WORKDIR /tmp/
