// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#pragma once
#include "common_launcher/launcher.hpp"
#include "inputs_preparation/tensor_utils.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <opencv2/core/mat.hpp>
#include <opencv2/dnn.hpp>

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

using HighresClock = std::chrono::high_resolution_clock;

class OCVLauncher : public Launcher {
public:
    OCVLauncher(int nthreads);
    virtual ~OCVLauncher(){};

    void log_framework_version() const override;

    void read(const std::string& model) override;
    void load() override{};

    void fill_inputs_outputs_info() override;
    IOTensorsInfo get_io_tensors_info() const override;

    void prepare_input_tensors(std::vector<std::vector<TensorBuffer>> tensor_buffers) override;

    void warmup_inference() override;
    int evaluate(int iterations_num, uint64_t time_limit_ns) override;

private:
    cv::dnn::Net net;
    std::vector<std::string> input_names;
    std::vector<std::vector<int>> input_shapes;

    std::vector<std::string> output_names;
    std::vector<std::vector<int>> output_shapes;

    std::vector<cv::Mat> blobs;
    std::vector<std::vector<TensorBuffer>> tensor_buffers;

    std::vector<cv::Mat> output_blobs;

    void run(const cv::Mat& input_blob);
};
