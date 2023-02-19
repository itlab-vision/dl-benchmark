// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#pragma once
#include "buffer.hpp"
#include "model.hpp"
#include "logger.hpp"
#include "utils.hpp"

#include <opencv2/core/mat.hpp>

#include <onnxruntime_cxx_api.h>

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

using HighresClock = std::chrono::high_resolution_clock;

static const std::map<ONNXTensorElementDataType, utils::DataPrecision> onnx_dtype_to_precision_map = {
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT, utils::DataPrecision::FP32},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT16, utils::DataPrecision::FP16},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_UINT8, utils::DataPrecision::U8},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT8, utils::DataPrecision::I8},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT32, utils::DataPrecision::I32},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT64, utils::DataPrecision::I64},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_BOOL, utils::DataPrecision::BOOL},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_UNDEFINED, utils::DataPrecision::UNKNOWN}
};

static utils::DataPrecision get_data_precision(ONNXTensorElementDataType type) {
    if (onnx_dtype_to_precision_map.count(type) > 0) {
        return onnx_dtype_to_precision_map.at(type);
    }
    else {
        throw std::invalid_argument("Does not support element data type " + std::to_string(type));
    }
}

class ONNXModel : public Model {
private:
    struct IOInfo {
        std::vector<const char *> input_names;
        std::vector<Ort::AllocatedStringPtr> input_names_ptr;
        std::vector<ONNXTensorElementDataType> input_data_types;
        std::vector<std::vector<int64_t>> input_shapes;

        std::vector<const char *> output_names;
        std::vector<Ort::AllocatedStringPtr> output_names_ptr;
        std::vector<ONNXTensorElementDataType> output_data_types;
        std::vector<std::vector<int64_t>> output_shapes;
    } io;

    std::shared_ptr<Ort::Env> env;
    std::shared_ptr<Ort::Session> session;

    std::vector<std::vector<Ort::Value>> tensors;
    std::vector<std::vector<Buffer>> tensor_buffers;

    // time stamps for total time measurments;
    HighresClock::time_point total_start_time;
    HighresClock::time_point total_end_time;

    // time stamps for individual inference
    HighresClock::time_point infer_start_time;
    std::vector<double> latencies;

public:
    ONNXModel(int nthreads_) : Model(nthreads_) {};
    virtual ~ONNXModel() {};

    void configure_framework(const std::vector<std::string> &args) override;
    void log_framework_version() const override;

    void read(const std::string &model) override;
    void load() override {};

    void fill_inputs_outputs_info() override;
    IOTensorsInfo get_io_tensors_info() const override;

    // void set_batch_size(int batch_size) override {}; // TODO
    void prepare_input_tensors(std::vector<std::vector<Buffer>> tensor_buffers) override;

    void warmup_inference() override;
    void run(const std::vector<Ort::Value> &input_tensors);
    int evaluate(int iterations_num, uint64_t time_limit_ns) override;
};
