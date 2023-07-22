#include "utils/utils.hpp"

#include <algorithm>
#include <exception>
#include <filesystem>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>

namespace utils {
std::string get_device_str(const Device d) {
    if (device_to_str_map.count(d) > 0) {
        return device_to_str_map.at(d);
    }
    return "UNKNOWN";
}

Device get_device_from_str(const std::string& dstr) {
    for (const auto& [device, device_str] : device_to_str_map) {
        if (device_str == dstr) {
            return device;
        }
    }
    return Device::UNKNOWN;
}

std::string get_data_precision_str(const DataPrecision p) {
    if (precision_to_str_map.count(p) > 0) {
        return precision_to_str_map.at(p);
    }
    return "UNKNOWN";
}
DataPrecision get_data_precision_from_str(const std::string& pstr) {
    for (const auto& [data_precision, precision_str] : precision_to_str_map) {
        if (pstr == precision_str) {
            return data_precision;
        }
    }
    return DataPrecision::UNKNOWN;
}

std::string guess_layout_from_shape(const std::vector<int>& shape) {
    if (shape.size() == 2) {
        return "NC";
    }
    if (shape.size() == 3) {
        return shape[0] > 4 && shape[2] <= 4 ? "HWC" : "CHW";
    }
    if (shape.size() == 4) {
        return shape[1] > 4 && shape[3] <= 4 ? "NHWC" : "NCHW";
    }
    throw std::invalid_argument("Unsupported shape with size " + std::to_string(shape.size()));
}

std::string format_double(const double number) {
    std::stringstream ss;
    ss << std::fixed << std::setprecision(2) << number;
    return ss.str();
};
}  // namespace utils