#pragma once

#include "inputs_preparation/tensor_utils.hpp"

#include <string>
#include <vector>

class OutputTensor {
public:
    OutputTensor() {}

    OutputTensor(size_t count, const std::vector<int>& shape, const std::string& name, const std::vector<float>& data)
        : output_name(name), tensor(count, shape, utils::DataPrecision::FP32, data) {}

    OutputTensor(const OutputTensor& output) : output_name(output.output_name), tensor(output.tensor) {}

    OutputTensor(OutputTensor&& output)
        : output_name(std::move(output.output_name)), tensor(std::move(output.tensor)) {}

    void swap(OutputTensor& other) noexcept {
        std::swap(output_name, other.output_name);
        tensor.swap(other.tensor);
    }

    OutputTensor& operator=(const OutputTensor& output) {
        OutputTensor od_copy(output);
        swap(od_copy);
        return *this;
    }

    OutputTensor& operator=(OutputTensor&& output) {
        swap(output);
        return *this;
    }

    const std::vector<int>& shape() const {
        return tensor.shape();
    }

    const std::string& name() const {
        return output_name;
    }

    const std::vector<float> data() const {
        return {tensor.get<float>(), tensor.get<float>() + tensor.count()};
    }

    float& operator[](size_t idx) {
        return tensor.get<float>()[idx];
    }

    const float& operator[](size_t idx) const {
        return tensor.get<float>()[idx];
    }

private:
    std::string output_name;
    TensorBuffer tensor;
};

using OutputTensors = std::vector<OutputTensor>;