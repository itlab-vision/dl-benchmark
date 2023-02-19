#pragma once

#include "utils.hpp"

#include <memory>
#include <vector>

class Buffer {
  public:
    Buffer():
        data(nullptr),
        refcount(nullptr),
        total_size(-1)
    {}

    Buffer(size_t size, const utils::DataPrecision precision, void* data = nullptr) :
        size(size),
        data(data),
        precision(precision)
        {
        if (data) {
            refcount = nullptr;
            user_data = true;
            total_size = size * elem_size(precision);
            return;
        }
        allocate(size, precision);
    }

    void resize(size_t size) {
        if (user_data)
            throw std::runtime_error("Buffer: can't resize user data!");
        allocate(size, precision);
    }

    Buffer(const Buffer& buf) {
        data = buf.data;
        precision = buf.precision;
        user_data = buf.user_data;
        refcount = buf.refcount;
        total_size = buf.total_size;

        if (refcount)
            (*refcount)++;
    }

    Buffer& operator=(const Buffer& buf) {
        if (this == &buf)
            return *this;

        if (data)
            deallocate();

        data = buf.data;
        precision = buf.precision;
        user_data = buf.user_data;
        refcount = buf.refcount;
        total_size = buf.total_size;

        if (refcount)
            (*refcount)++;

        return *this;
    }

    std::shared_ptr<Buffer> clone() {
        auto buf = std::make_shared<Buffer>(this->getTotalSize()/elem_size(this->precision), this->precision);
        memcpy(buf->data, this->data, buf->getTotalSize());
        return buf;
    }

    void allocate(const size_t _size, const utils::DataPrecision _precision) {
        if (data)
            deallocate();
        size = _size;
        data = nullptr;
        precision = _precision;
        user_data = false;
        refcount = (int*)malloc(sizeof(int));
        total_size = _size * elem_size();

        if(total_size > 0) {
            data = malloc(total_size);
            if (!data)
                throw std::runtime_error("Failed to allocate " + std::to_string(total_size) + " bytes");
        }
        (*refcount) = 1;
    }

    void deallocate() {
        if (!data)
            return;

        if (!user_data) {
            if (!refcount)
                throw std::runtime_error("Buffer refcount is not initialized");

            if (--(*refcount) == 0) {
                free(data);
                free(refcount);

                data = nullptr;
                refcount = nullptr;
            }
        }
    }

    ~Buffer() {
        deallocate();
    }

    template <typename T>
    T* get() {
        return (T*)data;
    }

    template <typename T>
    T* get() const {
        return (T*)data;
    }

    size_t getTotalSize() const {
        return total_size;
    }

    bool isUserData() {
        return (data && user_data);
    }

    static size_t elem_size(utils::DataPrecision precision) {
        if (precision == utils::DataPrecision::FP32) {
            return sizeof(float);
        }
        else if (precision == utils::DataPrecision::FP16) {
            return sizeof(uint16_t);
        }
        else if (precision == utils::DataPrecision::I32) {
            return sizeof(int32_t);
        }
        else if (precision == utils::DataPrecision::I8) {
            return sizeof(int8_t);
        }
        else if ((precision == utils::DataPrecision::U8) ||
                 (precision == utils::DataPrecision::BOOL)) {
            return sizeof(uint8_t);
        }
        else if (precision == utils::DataPrecision::I64) {
            return sizeof(int64_t);
        }
        throw std::runtime_error("Unsupported precision!");
    }

    size_t elem_size() const {
        return elem_size(precision);
    }

    void* data;
    utils::DataPrecision precision;
    std::vector<int64_t> data_shape;
    size_t size;

  private:
    int* refcount;
    bool user_data;
    size_t total_size;
};
