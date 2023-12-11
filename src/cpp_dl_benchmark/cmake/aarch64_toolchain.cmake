set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

find_program(GCC_AARCH64 NAMES aarch64-linux-gnu-gcc aarch64-linux-gnu-gcc-10 PATHS ENV PATH)
find_program(G++_AARCH64 NAMES aarch64-linux-gnu-g++ aarch64-linux-gnu-g++-10 PATHS ENV PATH)
set(CMAKE_C_COMPILER ${GCC_AARCH64})
set(CMAKE_CXX_COMPILER ${G++_AARCH64})
