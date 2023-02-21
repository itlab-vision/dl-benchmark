// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#pragma once
#include "tensor_buffer.hpp"
#include "launcher.hpp"
#include "logger.hpp"
#include "utils.hpp"

#include <opencv2/core/mat.hpp>
#include <opencv2/dnn.hpp>

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

using HighresClock = std::chrono::high_resolution_clock;

// static const std::map<ONNXTensorElementDataType, utils::DataPrecision> onnx_dtype_to_precision_map = {
//     {ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT, utils::DataPrecision::FP32},
//     {ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT16, utils::DataPrecision::FP16},
//     {ONNX_TENSOR_ELEMENT_DATA_TYPE_UINT8, utils::DataPrecision::U8},
//     {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT8, utils::DataPrecision::I8},
//     {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT32, utils::DataPrecision::I32},
//     {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT64, utils::DataPrecision::I64},
//     {ONNX_TENSOR_ELEMENT_DATA_TYPE_BOOL, utils::DataPrecision::BOOL},
//     {ONNX_TENSOR_ELEMENT_DATA_TYPE_UNDEFINED, utils::DataPrecision::UNKNOWN}
// };

// static utils::DataPrecision get_data_precision(ONNXTensorElementDataType type) {
//     if (onnx_dtype_to_precision_map.count(type) > 0) {
//         return onnx_dtype_to_precision_map.at(type);
//     }
//     else {
//         throw std::invalid_argument("Does not support element data type " + std::to_string(type));
//     }
// }

class OCVLauncher : public Launcher {
public:
    OCVLauncher(int nthreads_) : Launcher(nthreads_) {};
    virtual ~OCVLauncher() {};

    void configure_framework(const std::vector<std::string> &args) override;
    void log_framework_version() const override;

    void read(const std::string &model) override;
    void load() override {};

    void fill_inputs_outputs_info() override;
    IOTensorsInfo get_io_tensors_info() const override;

    // void set_batch_size(int batch_size) override {}; // TODO
    void prepare_input_tensors(std::vector<std::vector<TensorBuffer>> tensor_buffers) override;

    void warmup_inference() override;
    int evaluate(int iterations_num, uint64_t time_limit_ns) override;
private:

    cv::dnn::Net net;
    std::vector<std::string> input_names;
    std::vector<std::vector<int64_t>> input_shapes;
    std::vector<cv::Mat> blobs;
    std::vector<std::vector<TensorBuffer>> tensor_buffers;

    void run(const cv::Mat &input_blob);
};
