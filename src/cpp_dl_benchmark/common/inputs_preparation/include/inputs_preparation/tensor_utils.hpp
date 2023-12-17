#pragma once

#include "utils/utils.hpp"

#include <cstring>
#include <memory>
#include <string>
#include <vector>

struct TensorDescription {
    std::string name;
    std::vector<int> shape;
    std::vector<int> data_shape;
    std::string layout;
    utils::DataPrecision data_precision;
    bool is_reshapable;

    bool is_image() const;
    bool is_image_info() const;
    bool is_dynamic() const;
    bool has_batch() const;
    bool is_dynamic_batch() const;
    int get_dimension_by_layout(char ch) const;
    int channels() const;
    int width() const;
    int height() const;
    void set_batch(int batch_size);
};

class TensorBuffer {
public:
    TensorBuffer()
        : data(nullptr), bytes_count(-1), elements_count(-1), data_shape{},
          data_precision(utils::DataPrecision::UNKNOWN) {}

    TensorBuffer(size_t elements_count, const std::vector<int> shape, const utils::DataPrecision dp)
        : data(new char[elements_count * elem_size(dp)]), bytes_count(elements_count * elem_size(dp)),
          elements_count(elements_count), data_shape(shape), data_precision(dp) {}

    void resize(size_t count) {
        allocate(count, data_precision);
    }

    template<typename T = void>
    TensorBuffer(size_t elements_count,
                 const std::vector<int> shape,
                 const utils::DataPrecision dp,
                 const std::vector<T>& data_vec)
        : data(new char[elements_count * elem_size(dp)]), bytes_count(elements_count * elem_size(dp)),
          elements_count(elements_count), data_shape(shape), data_precision(dp) {
        memcpy(data, data_vec.data(), bytes_count);
    }

    void swap(TensorBuffer& other) noexcept {
        std::swap(data, other.data);
        std::swap(bytes_count, other.bytes_count);
        std::swap(elements_count, other.elements_count);
        std::swap(data_shape, other.data_shape);
        std::swap(data_precision, other.data_precision);
    }

    TensorBuffer(const TensorBuffer& buf)
        : data(new char[buf.bytes_count]), bytes_count(buf.bytes_count), elements_count(buf.elements_count),
          data_shape(buf.data_shape), data_precision(buf.data_precision) {
        memcpy(data, buf.get(), bytes_count);
    }

    TensorBuffer(TensorBuffer&& buf) noexcept : TensorBuffer() {
        swap(buf);
    }

    TensorBuffer& operator=(const TensorBuffer& buf) {
        TensorBuffer tb_copy(buf);
        swap(tb_copy);
        return *this;
    }

    TensorBuffer& operator=(TensorBuffer&& buf) {
        swap(buf);
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

        if (bytes_count > 0) {
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

    template<typename T = void>
    T* get() {
        return reinterpret_cast<T*>(data);
    }

    template<typename T = void>
    const T* get() const {
        return reinterpret_cast<T*>(data);
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
        else if ((data_precision == utils::DataPrecision::U8) || (data_precision == utils::DataPrecision::BOOL)) {
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
