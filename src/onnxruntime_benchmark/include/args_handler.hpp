// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#pragma once

#include <algorithm>
#include <exception>
#include <filesystem>
#include <iterator>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>

namespace args {
std::map<std::string, std::vector<std::string>> parse_input_files_arguments(const std::vector<std::string> &args,
                                                                            size_t max_files = 20);

std::map<std::string, std::string> parse_shape_layout_string(const std::string &parameter_string);

std::map<std::string, std::vector<float>> parse_mean_scale_string(const std::string &parameter_string);

std::vector<std::string> split(const std::string &s, char delim);

template <typename T>
std::string shape_string(std::vector<T> shape) {
    std::ostringstream s;
    s << "[";
    std::copy(shape.begin(), shape.end() - 1, std::ostream_iterator<T>(s, ","));
    s << shape.back() << "]";
    return s.str();
}

template <class T>
std::vector<T> string_to_vec(const std::string &str, const char delim) {
    std::vector<T> res;
    const auto string_values = split(str, delim);
    try {
        for (auto &v : string_values) {
            if constexpr (std::is_same<float, T>::value) {
                res.push_back(std::stof(v));
            }
            else if constexpr (std::is_same<double, T>::value) {
                res.push_back(std::stod(v));
            }
            else if constexpr (std::is_same<int, T>::value) {
                res.push_back(std::stoi(v));
            }
            else if constexpr (std::is_same<long, T>::value) {
                res.push_back(std::stol(v));
            }
            else if constexpr (std::is_same<std::string, T>::value) {
                res.push_back(v);
            }
            else {
                static_assert(!sizeof(T), "No match template argument for this function."
                                          "Available types for argument are float, double, int, long and string");
            }
        }
    } catch (const std::invalid_argument &) {
        throw std::invalid_argument("Can't parse mean or scale argument");
    }

    return res;
}
} // namespace args
