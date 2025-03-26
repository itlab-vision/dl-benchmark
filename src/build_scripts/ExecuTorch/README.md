# Build ExecuTorch for Linux

1. Create conda environment and activate it.

   ```bash
   conda create -y -n executorch_env python=3.10
   conda activate executorch_env
   ```

1. Clone ExecuTorch repository and update submodules.

   ```bash
   git clone -b v0.5.0 https://github.com/pytorch/executorch
   cd executorch && git submodule update --init
   ```

1. Install requirements for Python.

   ```bash
   ./install_requirements.sh
   ```

1. Configure it with CMake.

   ```bash
   mkdir build && cd build
   cmake -DCMAKE_INSTALL_PREFIX=<install_prefix> \
         -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON \
         -DEXECUTORCH_BUILD_EXTENSION_RUNNER_UTIL=ON \
         -DEXECUTORCH_BUILD_EXTENSION_TENSOR=ON \
         -DEXECUTORCH_BUILD_DEVTOOLS=ON \
         -DBUILD_EXECUTORCH_PORTABLE_OPS=ON \
         -DEXECUTORCH_BUILD_XNNPACK=ON ../
   ```

1. Build and install.

   ```bash
   make "-j$(nproc)" && make install
   ```
