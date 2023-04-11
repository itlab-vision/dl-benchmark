find_package(OpenCV REQUIRED dnn)

file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

if (BUILD_OPENCV_LAUNCHER)
    add_launcher(NAME opencv_dnn_benchmark
                 SOURCES ${SOURCES}
                 HEADERS ${HEADERS}
                 INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
                 DEPENDENCIES opencv_dnn
                 DEFINITIONS OCV_DNN)
endif()

if (BUILD_OPENCV_OV_LAUNCHER)
    add_launcher(NAME opencv_dnn_ov_benchmark
                 SOURCES ${SOURCES}
                 HEADERS ${HEADERS}
                 INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
                 DEPENDENCIES opencv_dnn
                 DEFINITIONS OCV_DNN_WITH_OV)
endif()
