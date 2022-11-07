#include "onnxruntime_model.hpp"

#include "args_handler.hpp"
#include "logger.hpp"
#include "utils.hpp"

#include <opencv2/core/mat.hpp>

#include <onnxruntime_cxx_api.h>

#include <algorithm>
#include <chrono>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

bool ONNXTensorDescr::is_image() const {
    return (layout == "NCHW" || layout == "NHWC" || layout == "CHW" || layout == "HWC") && channels() == 3;
}

bool ONNXTensorDescr::is_image_info() const {
    return (layout.size() == 2 && layout.back() == 'C') && channels() >= 2;
}

bool ONNXTensorDescr::is_dynamic() const {
    return std::find(shape.begin(), shape.end(), -1) != shape.end();
}

bool ONNXTensorDescr::has_batch() const {
    return layout.find("N") != std::string::npos;
}

bool ONNXTensorDescr::is_dynamic_batch() const {
    if (has_batch()) {
        return shape[layout.find("N")] == -1;
    }
    return false;
}

void ONNXTensorDescr::set_batch(int batch_size) {
    std::size_t batch_index = layout.find("N");
    if (batch_index != std::string::npos) {
        data_shape[batch_index] = batch_size;
    }
}

int64_t ONNXTensorDescr::get_dimension_by_layout(char ch) const {
    size_t pos = layout.find(ch);
    if (pos == std::string::npos) {
        throw std::invalid_argument("Can't get " + std::string(ch, 1) + " from layout " + layout);
    }
    return data_shape.at(pos);
}

int64_t ONNXTensorDescr::channels() const {
    return get_dimension_by_layout('C');
}

int64_t ONNXTensorDescr::width() const {
    return get_dimension_by_layout('W');
}

int64_t ONNXTensorDescr::height() const {
    return get_dimension_by_layout('H');
}

ONNXModel::ONNXModel(int nthreads) : nthreads(nthreads) {}

void ONNXModel::read_model(const std::string &model_path) {
    env = std::make_shared<Ort::Env>(ORT_LOGGING_LEVEL_ERROR, "ORT Benchmark");
    Ort::SessionOptions session_options;
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    session_options.SetExecutionMode(ExecutionMode::ORT_SEQUENTIAL);
    if (nthreads > 0) {
        session_options.SetIntraOpNumThreads(nthreads);
    }
    session = std::make_shared<Ort::Session>(*env, model_path.c_str(), session_options);
}

void ONNXModel::fill_inputs_outputs_info() {
    auto allocator = Ort::AllocatorWithDefaultOptions();
    // Get input from model
    for (size_t i = 0; i < session->GetInputCount(); ++i) {
        // get input name
        auto input_name = session->GetInputNameAllocated(i, allocator);
        io.input_names.emplace_back(input_name.get());
        io.input_names_ptr.push_back(std::move(input_name));
        // get input type
        auto type_info = session->GetInputTypeInfo(i);
        auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
        ONNXTensorElementDataType type = tensor_info.GetElementType();
        io.input_data_types.push_back(type);

        // get input shapes/dims
        auto input_node_shape = tensor_info.GetShape();
        io.input_shapes.push_back(input_node_shape);
    }

    // Get outputs from model
    for (size_t i = 0; i < session->GetOutputCount(); ++i) {
        // get output name
        auto output_name = session->GetOutputNameAllocated(i, allocator);
        io.output_names.push_back(output_name.get());
        io.output_names_ptr.push_back(std::move(output_name));

        // get output type
        auto type_info = session->GetOutputTypeInfo(i);
        auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
        ONNXTensorElementDataType type = tensor_info.GetElementType();
        io.output_data_types.push_back(type);

        // get input shapes/dims
        auto output_node_shape = tensor_info.GetShape();
        io.output_shapes.push_back(output_node_shape);
    }

    // sort to keep inputs name order with input tensors
    std::vector<int> idx(io.input_names.size());
    std::iota(idx.begin(), idx.end(), 0);
    std::sort(idx.begin(), idx.end(), [&names = io.input_names](const int l, const int r) {
        return std::string(names[l]) < std::string(names[r]);
    });

    io.input_names = utils::reorder(io.input_names, idx);
    io.input_data_types = utils::reorder(io.input_data_types, idx);
    io.input_shapes = utils::reorder(io.input_shapes, idx);
}

IOTensorsInfo ONNXModel::get_io_tensors_info() const {
    std::vector<ONNXTensorDescr> input_tensors_info;
    for (size_t i = 0; i < io.input_names.size(); ++i) {
        input_tensors_info.push_back(
            {std::string(io.input_names[i]), io.input_shapes[i], io.input_shapes[i], "", io.input_data_types[i]});
    }
    std::vector<ONNXTensorDescr> output_tensors_info;
    for (size_t i = 0; i < io.output_names.size(); ++i) {
        output_tensors_info.push_back(
            {std::string(io.output_names[i]), io.output_shapes[i], {}, "", io.output_data_types[i]});
    }
    return {input_tensors_info, output_tensors_info};
}

void ONNXModel::reset_timers() {
    total_start_time = HighresClock::time_point::max();
    total_end_time = HighresClock::time_point::min();
    latencies.clear();
}

std::vector<double> ONNXModel::get_latencies() const {
    return latencies;
}

double ONNXModel::get_total_time_ms() const {
    return utils::ns_to_ms(total_end_time - total_start_time);
}

void ONNXModel::run(const std::vector<Ort::Value> &input_tensors) {
    total_start_time = std::min(HighresClock::now(), total_start_time);

    infer_start_time = HighresClock::now();
    session->Run(Ort::RunOptions{nullptr},
                 io.input_names.data(),
                 input_tensors.data(),
                 io.input_names.size(),
                 io.output_names.data(),
                 io.output_names.size());
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));

    total_end_time = std::max(HighresClock::now(), total_end_time);
}
