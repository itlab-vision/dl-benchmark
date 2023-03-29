cmake_minimum_required(VERSION 3.13)

project(cpp_dl_benchmark CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

option(ENABLE_CLANG_FORMAT "Enable clang-format during the build" ON)
option(BUILD_ONNXRUNTIME_LAUNCHER "Build OpenCV launcher" ON)
option(BUILD_OPENCV_LAUNCHER "Build OpenCV launcher" ON)

include(CMakeParseArguments)

# check_code_style(NAME <target name>
#     CLANG_FORMAT <ON/OFF>)
macro(check_code_style)
    set(oneValueArgs NAME CLANG_FORMAT)
    cmake_parse_arguments(CHECK "${options}" "${oneValueArgs}"
        "${multiValueArgs}" ${ARGN})
    if(CHECK_CLANG_FORMAT)
        add_clang_format_target(${CHECK_NAME}_clang_format FOR_TARGETS ${CHECK_NAME})
    endif()
endmacro()

# add_launcher(NAME <target name>
#     SOURCES <source files>
#     [HEADERS <header files>]
#     [INCLUDE_DIRECTORIES <include dir>]
#     [DEPENDENCIES <dependencies>]
#     [DEFINITIONS <DEFINITIONS>])
macro(add_launcher)
    set(oneValueArgs NAME)
    set(multiValueArgs SOURCES HEADERS DEPENDENCIES INCLUDE_DIRECTORIES DEFINITIONS)
    cmake_parse_arguments(LAUNCHER "${options}" "${oneValueArgs}"
                          "${multiValueArgs}" ${ARGN})
    # Create executable file from sources
    add_executable(${LAUNCHER_NAME} "${LAUNCHER_SOURCES};${CMAKE_SOURCE_DIR}/main.cpp" ${LAUNCHER_HEADERS})

    check_code_style(NAME ${LAUNCHER_NAME}
        CLANG_FORMAT ${ENABLE_CLANG_FORMAT})

    if(LAUNCHER_INCLUDE_DIRECTORIES)
        target_include_directories(${LAUNCHER_NAME} PRIVATE ${LAUNCHER_INCLUDE_DIRECTORIES})
    endif()

    target_link_libraries(${LAUNCHER_NAME} PRIVATE
        opencv_core opencv_imgproc opencv_imgcodecs
        common_launcher inputs_preparation utils
        ${LAUNCHER_DEPENDENCIES}
        gflags
    )

    target_compile_definitions(${LAUNCHER_NAME} PRIVATE ${LAUNCHER_DEFINITIONS})
endmacro()

find_package(CMakeScripts REQUIRED
             PATHS "${CMAKE_CURRENT_SOURCE_DIR}/cmake"
             NO_CMAKE_FIND_ROOT_PATH
             NO_DEFAULT_PATH)
find_package(OpenCV REQUIRED core imgproc imgcodecs)

add_subdirectory(common)
add_subdirectory(thirdparty/gflags)

if (BUILD_OPENCV_LAUNCHER OR BUILD_OPENCV_IE_LAUNCHER)
    add_subdirectory(opencv_launcher)
endif()

if (BUILD_ONNXRUNTIME_LAUNCHER)
    add_subdirectory(onnxruntime_launcher)
endif()
