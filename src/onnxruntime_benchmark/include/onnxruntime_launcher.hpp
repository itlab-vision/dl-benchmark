// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#pragma once
#include "tensor_buffer.hpp"
#include "launcher.hpp"
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

class ONNXLauncher : public Launcher {
public:
    ONNXLauncher(int nthreads_) : Launcher(nthreads_) {};
    virtual ~ONNXLauncher() {};

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
    struct IOInfo {
        std::vector<const char *> input_names;
        std::vector<Ort::AllocatedStringPtr> input_names_ptr;
        std::vector<ONNXTensorElementDataType> input_data_precisions;
        std::vector<std::vector<int64_t>> input_shapes;

        std::vector<const char *> output_names;
        std::vector<Ort::AllocatedStringPtr> output_names_ptr;
        std::vector<ONNXTensorElementDataType> output_data_precisions;
        std::vector<std::vector<int64_t>> output_shapes;
    } io;

    std::shared_ptr<Ort::Env> env;
    std::shared_ptr<Ort::Session> session;

    std::vector<std::vector<Ort::Value>> tensors;
    std::vector<std::vector<TensorBuffer>> tensor_buffers;

    void run(const std::vector<Ort::Value> &input_tensors);
};
