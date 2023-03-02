# #!/bin/bash

# Copyright (C) 2023 KNS Group LLC (YADRO)
# All Rights Reserved.

# This software contains the intellectual property of YADRO
# or is licensed to YADRO from third parties. Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by YADRO.
#

echo "deb http://apt.llvm.org/$(lsb_release -cs)/ llvm-toolchain-$(lsb_release -cs)-16 main" | sudo tee -a /etc/apt/sources.list
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
rm llvm-snapshot.gpg.key
sudo apt install -y clang-format-16