// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#pragma once
#include "logger.hpp"

#include <onnxruntime_cxx_api.h>

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
enum class DataPrecision : unsigned int {
    FP32 = 0,
    FP16,
    U8,
    I8,
    I32,
    I64,
    BOOL,
    UNKNOWN
};

static const std::map<DataPrecision, std::string> precision_to_str_map = {
    {DataPrecision::FP32, "FP32"},
    {DataPrecision::FP16, "FP16"},
    {DataPrecision::U8, "U8"},
    {DataPrecision::I8, "INT8"},
    {DataPrecision::I32, "INT32"},
    {DataPrecision::I64, "INT64"},
    {DataPrecision::BOOL, "BOOL"}
};

std::string get_precision_str(DataPrecision p);

std::string guess_layout_from_shape(const std::vector<int64_t> &shape);

std::string format_double(const double number);

template <typename T>
std::vector<T> reorder(const std::vector<T> &vec, const std::vector<int> &indexes) {
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

static inline uint64_t sec_to_ns(uint32_t duration) {
    return duration * 1000000000LL;
}
} // namespace utils
