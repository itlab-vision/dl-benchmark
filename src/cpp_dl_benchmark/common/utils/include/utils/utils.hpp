#pragma once
#include "logger.hpp"

#include <chrono>
#include <cstdint>
#include <exception>
#include <iomanip>
#include <iterator>
#include <map>
#include <sstream>
#include <string>
#include <vector>

using HighresClock = std::chrono::high_resolution_clock;
using ns = std::chrono::nanoseconds;

namespace utils {

enum class Device : unsigned int {
    CPU = 0,
    GPU,
    NVIDIA_GPU,
    ARM,
    UNKNOWN
};

static const std::map<Device, std::string> device_to_str_map = {{Device::CPU, "CPU"},
                                                                {Device::GPU, "GPU"},
                                                                {Device::NVIDIA_GPU, "NVIDIA_GPU"},
                                                                {Device::ARM, "ARM"}};

std::string get_device_str(const Device d);

Device get_device_from_str(const std::string& dstr);

enum class DataPrecision : unsigned int {
    FP16 = 0,
    FP32,
    FP64,
    U8,
    U16,
    U32,
    U64,
    I8,
    I16,
    I32,
    I64,
    BOOL,
    UNKNOWN
};

static const std::map<DataPrecision, std::string> precision_to_str_map = {{DataPrecision::FP32, "FP32"},
                                                                          {DataPrecision::FP16, "FP16"},
                                                                          {DataPrecision::U8, "U8"},
                                                                          {DataPrecision::I8, "INT8"},
                                                                          {DataPrecision::I32, "INT32"},
                                                                          {DataPrecision::I64, "INT64"},
                                                                          {DataPrecision::BOOL, "BOOL"}};

std::string get_data_precision_str(const DataPrecision p);

DataPrecision get_data_precision_from_str(const std::string& precision_str);

std::string guess_layout_from_shape(const std::vector<int>& shape);

std::string format_double(const double number);

template<typename T>
std::vector<T> reorder(const std::vector<T>& vec, const std::vector<int>& indexes) {
    if (vec.size() != indexes.size()) {
        throw std::invalid_argument("Sizes of two vectors must be equal.");
    }

    std::vector<T> res(vec.size());
    for (size_t i = 0; i < vec.size(); ++i) {
        res[i] = vec[indexes[i]];
    }

    return res;
}

static inline double ns_to_ms(std::chrono::nanoseconds duration) {
    return static_cast<double>(duration.count()) * 0.000001;
}

static inline uint64_t sec_to_ms(uint32_t duration) {
    return duration * 1000LL;
}

static inline float sec_to_ms(float duration) {
    return duration * 1000;
}

static inline uint64_t sec_to_ns(uint32_t duration) {
    return duration * 1000000000LL;
}
}  // namespace utils
