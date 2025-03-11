find_package(executorch REQUIRED)

file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

list(REMOVE_ITEM EXECUTORCH_LIBRARIES extension_module)
list(REMOVE_ITEM EXECUTORCH_LIBRARIES optimized_kernels)
list(REMOVE_ITEM EXECUTORCH_LIBRARIES optimized_ops_lib)
list(REMOVE_ITEM EXECUTORCH_LIBRARIES optimized_native_cpu_ops_lib)

message(STATUS ${EXECUTORCH_})

add_launcher(NAME executorch_benchmark
    SOURCES ${SOURCES}
    HEADERS ${HEADERS}
    INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
                        "${EXECUTORCH_REPO_PATH}"
                        "${EXECUTORCH_INCLUDE_DIRS}"
                        "/home/ismukhin/projects/risc_build/executorch/build1/executorch_install/include"
    DEPENDENCIES
        -Wl,--whole-archive,--allow-multiple-definition
        ${EXECUTORCH_LIBRARIES}
        -Wl,--no-whole-archive
    DEFINITIONS EXECUTORCH)