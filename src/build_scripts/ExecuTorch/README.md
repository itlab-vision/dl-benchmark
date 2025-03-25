# Build ExecuTorch for Linux

1. Create conda environment:
```bash
conda create -y -n executorch_env python=3.10
```
```bash
conda activate executorch_env
```

2. Clone ExecuTorch repository:
```bash
git clone -b v0.5.0 https://github.com/pytorch/executorch
```
```bash
cd executorch && git submodule update --init
```

3. Install requirements for Python:
```bash
./install_requirements.sh
```

4. Configure it with cmake:
```bash
mkdir build1 && cd build1
```
```bash
cmake -DCMAKE_INSTALL_PREFIX=<install_prefix> \
      -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON \
      -DEXECUTORCH_BUILD_EXTENSION_RUNNER_UTIL=ON \
      -DEXECUTORCH_BUILD_EXTENSION_TENSOR=ON \
      -DEXECUTORCH_BUILD_DEVTOOLS=ON \
      -DBUILD_EXECUTORCH_PORTABLE_OPS=ON \
      -DEXECUTORCH_BUILD_XNNPACK=ON ../
```

5. Build and install:
```bash
make "-j$(nproc)" && make install
```