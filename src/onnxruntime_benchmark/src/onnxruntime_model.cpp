// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#include "onnxruntime_model.hpp"

#include "args_handler.hpp"
#include "inputs_preparation.hpp"
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

// bool ONNXTensorDescr::is_image() const {
//     return (layout == "NCHW" || layout == "NHWC" || layout == "CHW" || layout == "HWC") && channels() == 3;
// }

// bool ONNXTensorDescr::is_image_info() const {
//     return (layout.size() == 2 && layout.back() == 'C') && channels() >= 2;
// }

// bool ONNXTensorDescr::is_dynamic() const {
//     return std::find(shape.begin(), shape.end(), -1) != shape.end();
// }

// bool ONNXTensorDescr::has_batch() const {
//     return layout.find("N") != std::string::npos;
// }

// bool ONNXTensorDescr::is_dynamic_batch() const {
//     if (has_batch()) {
//         return shape[layout.find("N")] == -1;
//     }
//     return false;
// }

// void ONNXTensorDescr::set_batch(int batch_size) {
//     std::size_t batch_index = layout.find("N");
//     if (batch_index != std::string::npos) {
//         data_shape[batch_index] = batch_size;
//     }
// }

// int64_t ONNXTensorDescr::get_dimension_by_layout(char ch) const {
//     size_t pos = layout.find(ch);
//     if (pos == std::string::npos) {
//         throw std::invalid_argument("Can't get " + std::string(ch, 1) + " from layout " + layout);
//     }
//     return data_shape.at(pos);
// }

// int64_t ONNXTensorDescr::channels() const {
//     return get_dimension_by_layout('C');
// }

// int64_t ONNXTensorDescr::width() const {
//     return get_dimension_by_layout('W');
// }

// int64_t ONNXTensorDescr::height() const {
//     return get_dimension_by_layout('H');
// }

void ONNXModel::configure_framework(const std::vector<std::string> &args) {

}

void ONNXModel::log_framework_version() const {
     logger::info << "ONNX Runtime version: " << OrtGetApiBase()->GetVersionString() << logger::endl;
}

void ONNXModel::read(const std::string &model_path) {
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
    std::vector<TensorDescr> input_tensors_info;
    for (size_t i = 0; i < io.input_names.size(); ++i) {
        input_tensors_info.push_back(
            {std::string(io.input_names[i]), io.input_shapes[i], io.input_shapes[i], "", get_data_precision(io.input_data_types[i])});
    }
    std::vector<TensorDescr> output_tensors_info;
    for (size_t i = 0; i < io.output_names.size(); ++i) {
        output_tensors_info.push_back(
            {std::string(io.output_names[i]), io.output_shapes[i], {}, "", get_data_precision(io.output_data_types[i])});
    }
    return {input_tensors_info, output_tensors_info};
}


void ONNXModel::prepare_input_tensors(std::vector<std::vector<Buffer>> tbuffers) {
    tensor_buffers = std::move(tbuffers);
    auto allocator = Ort::AllocatorWithDefaultOptions();
    // auto tensor = Ort::Value::CreateTensor(allocator,
    //                                        tensor_descr.data_shape.data(),
    //                                        tensor_descr.data_shape.size(),
    //                                        tensor_descr.type);
    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);
    // size_t tensor_size = tensor.GetTensorTypeAndShapeInfo().GetElementCount();
    // auto *tensor_data = tensor.GetTensorMutableData<char>();

    tensors.reserve(tensor_buffers.size());
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        for (int j = 0; j < tensor_buffers[j].size(); ++j) {
            auto& buffer = tensor_buffers[i][j];
            if (buffer.precision == utils::DataPrecision::FP32) {
                tensors[i].push_back(Ort::Value::CreateTensor<float>(memory_info,
                                                                     buffer.get<float>(),
                                                                     buffer.size,
                                                                     buffer.data_shape.data(),
                                                                     buffer.data_shape.size()));
            }
            else if (buffer.precision == utils::DataPrecision::FP16) {
                tensors[i].push_back(Ort::Value::CreateTensor(memory_info,
                                    buffer.data,
                                    buffer.size,
                                    buffer.data_shape.data(),
                                    buffer.data_shape.size(),
                                    ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT16));
            }
            else if (buffer.precision == utils::DataPrecision::I32) {
                tensors[i].push_back(Ort::Value::CreateTensor<int32_t>(memory_info,
                                    buffer.get<int32_t>(),
                                    buffer.size,
                                    buffer.data_shape.data(),
                                    buffer.data_shape.size()));
            }
            else if (buffer.precision == utils::DataPrecision::I8) {
                tensors[i].push_back(Ort::Value::CreateTensor<int8_t>(memory_info,
                                    buffer.get<int8_t>(),
                                    buffer.size,
                                    buffer.data_shape.data(),
                                    buffer.data_shape.size()));
            }
            else if (buffer.precision == utils::DataPrecision::U8) {
                tensors[i].push_back(Ort::Value::CreateTensor<uint8_t>(memory_info,
                    buffer.get<uint8_t>(),
                    buffer.size,
                    buffer.data_shape.data(),
                    buffer.data_shape.size()));
            }
            else if (buffer.precision == utils::DataPrecision::BOOL) {
                tensors[i].push_back(Ort::Value::CreateTensor(memory_info,
                    buffer.data,
                    buffer.size,
                    buffer.data_shape.data(),
                    buffer.data_shape.size(),
                    ONNX_TENSOR_ELEMENT_DATA_TYPE_BOOL));
            }
            else if (buffer.precision == utils::DataPrecision::I64) {
                tensors[i].push_back(Ort::Value::CreateTensor<int64_t>(memory_info,
                    buffer.get<int64_t>(),
                    buffer.size,
                    buffer.data_shape.data(),
                    buffer.data_shape.size()));
            }
            throw std::runtime_error("Unsupported precision!");
        }
    }
}

void ONNXModel::warmup_inference() {
    run(tensors[0]);
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

int ONNXModel::evaluate(int iterations_num, uint64_t time_limit_ns) {
    int iteration = 0;
    auto start_time = HighresClock::now();
    auto uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    while ((iterations_num != 0 && iteration < iterations_num) ||
            (time_limit_ns != 0 && static_cast<uint64_t>(uptime) < time_limit_ns)) {
        run(tensors[iteration % tensors.size()]);
        ++iteration;
        uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    }

    return iteration;
}