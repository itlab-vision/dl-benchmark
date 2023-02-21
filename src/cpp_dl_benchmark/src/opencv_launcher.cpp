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
    // net.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
}

void OCVLauncher::log_framework_version() const {
     logger::info << "OpenCV version: " << CV_VERSION << logger::endl;
}

void OCVLauncher::read(const std::string &model_path) {
    net = cv::dnn::readNet(model_path);
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
    auto names = net.getLayerNames();
    for (auto n : names) {
        logger::info << n << logger::endl;
    }
    std::vector<std::string> types;
    net.getLayerTypes(types);
    logger::info << "types" << logger::endl;
    for (auto t : types) {
        logger::info << t << logger::endl;
    }

    logger::info << "input counts " << net.getLayersCount("__NetInputLayer__") << logger::endl;

    logger::info << net.getLayer(0)->name << logger::endl;

    // env = std::make_shared<Ort::Env>(ORT_LOGGING_LEVEL_ERROR, "ORT Benchmark");
    // Ort::SessionOptions session_options;
    // session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    // session_options.SetExecutionMode(ExecutionMode::ORT_SEQUENTIAL);
    // if (nthreads > 0) {
    //     session_options.SetIntraOpNumThreads(nthreads);
    // }
    // session = std::make_shared<Ort::Session>(*env, model_path.c_str(), session_options);
}

void OCVLauncher::fill_inputs_outputs_info() {
//     auto allocator = Ort::AllocatorWithDefaultOptions();
//     // Get input from model
//     for (size_t i = 0; i < session->GetInputCount(); ++i) {
//         // get input name
//         auto input_name = session->GetInputNameAllocated(i, allocator);
//         io.input_names.emplace_back(input_name.get());
//         io.input_names_ptr.push_back(std::move(input_name));
//         // get input type
//         auto type_info = session->GetInputTypeInfo(i);
//         auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
//         ONNXTensorElementDataType type = tensor_info.GetElementType();
//         io.input_data_precisions.push_back(type);

//         // get input shapes/dims
//         auto input_node_shape = tensor_info.GetShape();
//         io.input_shapes.push_back(input_node_shape);
//     }

//     // Get outputs from model
//     for (size_t i = 0; i < session->GetOutputCount(); ++i) {
//         // get output name
//         auto output_name = session->GetOutputNameAllocated(i, allocator);
//         io.output_names.push_back(output_name.get());
//         io.output_names_ptr.push_back(std::move(output_name));

//         // get output type
//         auto type_info = session->GetOutputTypeInfo(i);
//         auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
//         ONNXTensorElementDataType type = tensor_info.GetElementType();
//         io.output_data_precisions.push_back(type);

//         // get input shapes/dims
//         auto output_node_shape = tensor_info.GetShape();
//         io.output_shapes.push_back(output_node_shape);
//     }

//     // sort to keep inputs name order with input tensors
//     std::vector<int> idx(io.input_names.size());
//     std::iota(idx.begin(), idx.end(), 0);
//     std::sort(idx.begin(), idx.end(), [&names = io.input_names](const int l, const int r) {
//         return std::string(names[l]) < std::string(names[r]);
//     });

//     io.input_names = utils::reorder(io.input_names, idx);
//     io.input_data_precisions = utils::reorder(io.input_data_precisions, idx);
//     io.input_shapes = utils::reorder(io.input_shapes, idx);
}

IOTensorsInfo OCVLauncher::get_io_tensors_info() const {
    std::vector<TensorDescr> input_tensors_info;
    // for (size_t i = 0; i < io.input_names.size(); ++i) {
    //     input_tensors_info.push_back(
    //         {std::string(io.input_names[i]), io.input_shapes[i], io.input_shapes[i], "", get_data_precision(io.input_data_precisions[i])});
    // }
    // std::vector<TensorDescr> output_tensors_info;
    // for (size_t i = 0; i < io.output_names.size(); ++i) {
    //     output_tensors_info.push_back(
    //         {std::string(io.output_names[i]), io.output_shapes[i], {}, "", get_data_precision(io.output_data_precisions[i])});
    // }
    return {input_tensors_info, {}};
}


void OCVLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>> tbuffers) {
    tensor_buffers = std::move(tbuffers);
    blobs.resize(tensor_buffers.size());
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            std::vector<int> shape(tbuffers[i][j].shape().begin(), tbuffers[i][j].shape().end());
            blobs.push_back(cv::Mat(shape, CV_32F, tbuffers[i][j].get<void>()));
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
    net.forward();
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