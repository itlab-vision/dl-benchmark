# TensorFlow Lite build for Linux RISC-V platform

1. Build and install prerequisites for TensorFlow Lite launcher (CPP API):
 
   ```bash
   cd dl-benchmark/src/build_scripts/tflite/riscv64
   sudo ./build_prerequisites_linux_riscv.sh
   ```

1. Build and install TensorFlow Lite launcher (CPP API):

   ```bash
   cd dl-benchmark/src/build_scripts/tflite/riscv64
   sudo ./build_cpp_tflite_launcher_linux_riscv.sh
   ```

1. Move resulting `dl-benchmark/build/riscv64_send_archive.tgz` to RISC-V board and unpack

   ```bash
   scp dl-benchmark/build/riscv64_send_archive.tgz {YOUR BOARD IP AND PATH}
   mkdir builded_launcher && tar -xvzf riscv64_send_archive.tgz -C builded_launcher
   ```

1. Set `LD_LIBRARY_PATH` to builded packages and `sysroot`:

   ```bash
   export LD_LIBRARY_PATH=builded_launcher/tflite_riscv_build:builded_launcher/opencv_riscv_build/lib:$LD_LIBRARY_PATH
   export LD_LIBRARY_PATH=builded_launcher/sysroot/lib/:$LD_LIBRARY_PATH
   ```

1. Download model to test:

   ```bash
   wget https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_08_02/mobilenet_v1_1.0_224.tgz
   mkdir mobilenet_v1_1.0_224 && tar -xvzf mobilenet_v1_1.0_224.tgz -C mobilenet_v1_1.0_224 && rm mobilenet_v1_1.0_224.tgz
   ```

1. Run TensorFlow Lite launcher (CPP API):

   ```bash
   ./builded_launcher/cpp_tflite_launcher_riscv_build/bin/tflite_benchmark -m mobilenet_v1_1.0_224/mobilenet_v1_1.0_224.tflite
   ```
