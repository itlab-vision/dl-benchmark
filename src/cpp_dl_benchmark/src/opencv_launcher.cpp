// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#include "opencv_launcher.hpp"

#include "args_handler.hpp"
#include "inputs_preparation.hpp"
#include "logger.hpp"
#include "utils.hpp"

#include <opencv2/core/mat.hpp>
#include <opencv2/dnn.hpp>

#include <algorithm>
#include <chrono>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

void OCVLauncher::configure_framework(const std::vector<std::string> &args) {
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
}

void OCVLauncher::log_framework_version() const {
     logger::info << "OpenCV version: " << CV_VERSION << logger::endl;
}

void OCVLauncher::read(const std::string &model_path) {
    net = cv::dnn::readNet(model_path);
    int inputs_count = net.getLayersCount("__NetInputLayer__");
    if (inputs_count != 1) {
        throw std::runtime_error("Only models with 1 input supported.");
    }
}

void OCVLauncher::fill_inputs_outputs_info() {
    input_names.push_back(net.getLayer(0)->name);
    output_names = net.getUnconnectedOutLayersNames();
}

IOTensorsInfo OCVLauncher::get_io_tensors_info() const {
    std::vector<TensorDescr> input_tensors_info{{input_names[0], {-1,-1,-1,-1}, {}, "", utils::DataPrecision::FP32}};
    std::vector<TensorDescr> output_tensors_info;
    for (size_t i = 0; i < output_names.size(); ++i) {
        output_tensors_info.push_back(
            {std::string(output_names[i]), {}, {}, "", utils::DataPrecision::FP32});
    }
    return {input_tensors_info, output_tensors_info};
}

void OCVLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>> tbuffers) {
    tensor_buffers = std::move(tbuffers);
    // blobs.resize(tensor_buffers.size());
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            blobs.push_back(cv::Mat(tensor_buffers[i][j].shape(), CV_32F, tensor_buffers[i][j].get<void>()));
        }
    }
}

void OCVLauncher::warmup_inference() {
    run(blobs[0]);
}

void OCVLauncher::run(const cv::Mat &input_blob) {
    net.setInput(input_blob);
    total_start_time = std::min(HighresClock::now(), total_start_time);

    infer_start_time = HighresClock::now();
    net.forward(output_blobs, output_names);
    // std::vector<float> a((float*)output_blobs[0].data, (float*)output_blobs[0].data + 1000);
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));

    total_end_time = std::max(HighresClock::now(), total_end_time);
}

int OCVLauncher::evaluate(int iterations_num, uint64_t time_limit_ns) {
    int iteration = 0;
    auto start_time = HighresClock::now();
    auto uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    while ((iterations_num != 0 && iteration < iterations_num) ||
            (time_limit_ns != 0 && static_cast<uint64_t>(uptime) < time_limit_ns)) {
        run(blobs[iteration % blobs.size()]);
        ++iteration;
        uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    }

    return iteration;
}