#pragma once

#include <string>
#include <vector>

#include "inputs_preparation/tensor_utils.hpp"

class OutputDescription {
public:
    OutputDescription() {}
    
    OutputDescription(size_t count, const std::vector<int>& shape,
                      const std::string& name, const std::vector<float>& data)
        : output_name(name), tensor(count, shape, utils::DataPrecision::FP32, data) {}

    OutputDescription(const OutputDescription& output_descr)
        : output_name(output_descr.output_name), tensor(output_descr.tensor) {}

    OutputDescription(OutputDescription&& output_descr)
        : output_name(output_descr.output_name), tensor(output_descr.tensor) {}

    void swap(OutputDescription& other) noexcept {
        std::swap(output_name, other.output_name);
        tensor.swap(other.tensor);
    }

    OutputDescription& operator=(const OutputDescription& output_descr) {
        OutputDescription od_copy(output_descr);
        swap(od_copy);
        return *this;
    }

    OutputDescription& operator=(OutputDescription&& output_descr) {
        OutputDescription od_copy(output_descr);
        swap(od_copy);
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