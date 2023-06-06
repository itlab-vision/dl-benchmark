find_package(Torch REQUIRED)

file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

if (BUILD_PYTORCH_LAUNCHER)
    add_launcher(NAME pytorch_benchmark
                 SOURCES ${SOURCES}
                 HEADERS ${HEADERS}
                 INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
                 DEPENDENCIES ${TORCH_LIBRARIES}
                 DEFINITIONS PYTORCH)
endif()