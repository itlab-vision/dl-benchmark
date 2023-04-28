# #!/bin/bash

echo "deb http://apt.llvm.org/$(lsb_release -cs)/ llvm-toolchain-$(lsb_release -cs)-16 main" | sudo tee -a /etc/apt/sources.list
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
rm llvm-snapshot.gpg.key
sudo apt install -y clang-format-16