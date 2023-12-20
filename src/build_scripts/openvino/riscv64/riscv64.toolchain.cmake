set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR riscv64)

set(CMAKE_C_COMPILER riscv64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER riscv64-linux-gnu-g++)
set(CMAKE_STRIP riscv64-linux-gnu-strip)
set(PKG_CONFIG_EXECUTABLE riscv64-linux-gnu-pkg-config CACHE PATH "Path to RISC-V pkg-config")
