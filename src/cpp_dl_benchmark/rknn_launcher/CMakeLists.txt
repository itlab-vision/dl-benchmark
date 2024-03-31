file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

set(RKNN_LIB_SUBFOLDER ${CMAKE_SYSTEM_PROCESSOR})
if (CMAKE_SYSTEM_NAME STREQUAL "Android")
    set(RKNN_LIB_SUBFOLDER ${ANDROID_ABI})
endif()

if (RKNN_DIR)
    find_library(RKNN_LIB_PATH librknnrt.so
                ${RKNN_DIR}/runtime/RK3588/${CMAKE_SYSTEM_NAME}/librknn_api/${RKNN_LIB_SUBFOLDER}
                CMAKE_FIND_ROOT_PATH_BOTH)

    set(RKNN_INCLUDE_DIR "${RKNN_DIR}/runtime/RK3588/${CMAKE_SYSTEM_NAME}/librknn_api/include")
    get_filename_component(RKNN_INCLUDE_DIR ${RKNN_INCLUDE_DIR} ABSOLUTE)

    set(RKNN_LIBRARY "rknn")
    add_library(${RKNN_LIBRARY} SHARED IMPORTED)
    set_target_properties(${RKNN_LIBRARY} PROPERTIES
                        INTERFACE_INCLUDE_DIRECTORIES ${RKNN_INCLUDE_DIR}
                        IMPORTED_LOCATION ${RKNN_LIB_PATH}
                        IMPORTED_IMPLIB ${RKNN_LIB_PATH})

    add_launcher(NAME rknn_benchmark
                SOURCES ${SOURCES}
                HEADERS ${HEADERS}
                INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
                DEPENDENCIES ${RKNN_LIBRARY}
                DEFINITIONS RKNN)
else()
    message(WARNING "RKNN_DIR wasn't provided, skipping RKNN launcher")
endif()
