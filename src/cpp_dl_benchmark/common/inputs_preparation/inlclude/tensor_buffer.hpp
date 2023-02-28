#pragma once

#include "utils.hpp"

#include <memory>
#include <vector>

class TensorBuffer {
  public:
    TensorBuffer() :
        data(nullptr),
        bytes_count(-1),
        elements_count(-1),
        data_shape{},
        data_precision(utils::DataPrecision::UNKNOWN)
    {}

    TensorBuffer(size_t elements_count, const std::vector<int> shape, const utils::DataPrecision dp) :
        data(new char[elements_count * elem_size(dp)]),
        bytes_count(elements_count * elem_size(dp)),
        elements_count(elements_count),
        data_shape(shape),
        data_precision(dp) {}

    void resize(size_t count) {
        allocate(count, data_precision);
    }

    TensorBuffer(const TensorBuffer& buf) = delete;
    TensorBuffer& operator=(const TensorBuffer& buf) = delete;

    TensorBuffer(TensorBuffer&& buf) :
    data(buf.data),
    bytes_count(buf.bytes_count),
    elements_count(buf.elements_count),
    data_shape(buf.data_shape),
    data_precision(buf.data_precision) {
        buf.data = nullptr;
        buf.bytes_count = -1;
        buf.data_shape = {};
        buf.elements_count = -1;
        buf.data_precision = utils::DataPrecision::UNKNOWN;
    }

    TensorBuffer& operator=(TensorBuffer&& buf) {
        if (this == &buf) {
            return *this;
        }

        if (data) {
            delete[] data;
        }

        data = buf.data;
        bytes_count = buf.bytes_count;
        elements_count = buf.elements_count;
        data_shape = buf.data_shape;
        data_precision = buf.data_precision;

        buf.data = nullptr;
        buf.data_precision = utils::DataPrecision::UNKNOWN;
        buf.bytes_count = -1;
        buf.data_shape = {};
        buf.elements_count = -1;

        return *this;
    }

    std::shared_ptr<TensorBuffer> clone() {
        auto buf = std::make_shared<TensorBuffer>(size() / elem_size(data_precision), data_shape, data_precision);
        memcpy(buf->data, data, buf->size());
        return buf;
    }

    void allocate(const size_t count, const utils::DataPrecision dp) {
        if (data) {
            delete[] data;
        }

        elements_count = count;
        data_precision = dp;
        bytes_count = elements_count * elem_size();
        data = nullptr;

        if(bytes_count > 0) {
            data = new char[bytes_count];
            if (!data) {
                throw std::runtime_error("Failed to allocate " + std::to_string(bytes_count) + " bytes");
            }
        }
    }

    ~TensorBuffer() {
        if (data) {
            delete[] data;
        }
    }

    template <typename T>
    T* get() {
        return reinterpret_cast<T*>(data);
    }

    template <typename T>
    T* get() const {
        return  reinterpret_cast<T*>(data);
    }

    int64_t size() const {
        return bytes_count;
    }

    int64_t count() const {
        return elements_count;
    }

    const std::vector<int>& shape() const {
        return data_shape;
    }

    utils::DataPrecision precision() const {
        return data_precision;
    }

    static int64_t elem_size(utils::DataPrecision data_precision) {
        if (data_precision == utils::DataPrecision::FP32) {
            return sizeof(float);
        }
        else if (data_precision == utils::DataPrecision::FP16) {
            return sizeof(int16_t);
        }
        else if (data_precision == utils::DataPrecision::I32) {
            return sizeof(int32_t);
        }
        else if (data_precision == utils::DataPrecision::I8) {
            return sizeof(int8_t);
        }
        else if ((data_precision == utils::DataPrecision::U8) ||
                 (data_precision == utils::DataPrecision::BOOL)) {
            return sizeof(uint8_t);
        }
        else if (data_precision == utils::DataPrecision::I64) {
            return sizeof(int64_t);
        }
        throw std::runtime_error("Unsupported precision!");
    }

    int64_t elem_size() const {
        return elem_size(data_precision);
    }

  private:
    char* data;
    int64_t bytes_count;
    int64_t elements_count;
    std::vector<int> data_shape;
    utils::DataPrecision data_precision;
};
