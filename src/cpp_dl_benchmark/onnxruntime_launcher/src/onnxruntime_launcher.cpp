#include "onnxruntime_launcher.hpp"

#include "inputs_preparation/inputs_preparation.hpp"
#include "utils/args_handler.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <onnxruntime_cxx_api.h>

#include <algorithm>
#include <chrono>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <vector>

namespace {
const std::map<ONNXTensorElementDataType, utils::DataPrecision> onnx_dtype_to_precision_map = {
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT, utils::DataPrecision::FP32},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT16, utils::DataPrecision::FP16},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_UINT8, utils::DataPrecision::U8},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT8, utils::DataPrecision::I8},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT32, utils::DataPrecision::I32},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_INT64, utils::DataPrecision::I64},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_BOOL, utils::DataPrecision::BOOL},
    {ONNX_TENSOR_ELEMENT_DATA_TYPE_UNDEFINED, utils::DataPrecision::UNKNOWN}};

utils::DataPrecision get_data_precision(ONNXTensorElementDataType type) {
    if (onnx_dtype_to_precision_map.count(type) > 0) {
        return onnx_dtype_to_precision_map.at(type);
    }
    else {
        throw std::invalid_argument("Does not support element data type " + std::to_string(type));
    }
}

ONNXTensorElementDataType get_onnx_data_type(utils::DataPrecision precision) {
    for (const auto [onnx_type, data_prectision] : onnx_dtype_to_precision_map) {
        if (precision == data_prectision) {
            return onnx_type;
        }
    }
    throw std::invalid_argument("Does not support element data type " + utils::get_precision_str(precision));
}
}  // namespace

void ONNXLauncher::log_framework_version() const {
    logger::info << "ONNX Runtime version: " << OrtGetApiBase()->GetVersionString() << logger::endl;
}

void ONNXLauncher::read(const std::string model_file, const std::string weights_file) {
    env = std::make_shared<Ort::Env>(ORT_LOGGING_LEVEL_ERROR, "ORT Benchmark");
    Ort::SessionOptions session_options;
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    session_options.SetExecutionMode(ExecutionMode::ORT_SEQUENTIAL);
    if (nthreads > 0) {
        session_options.SetIntraOpNumThreads(nthreads);
    }
    session = std::make_shared<Ort::Session>(*env, model_file.c_str(), session_options);
}

void ONNXLauncher::fill_inputs_outputs_info() {
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
        io.input_data_precisions.push_back(type);

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
        io.output_data_precisions.push_back(type);

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
    io.input_data_precisions = utils::reorder(io.input_data_precisions, idx);
    io.input_shapes = utils::reorder(io.input_shapes, idx);
}

IOTensorsInfo ONNXLauncher::get_io_tensors_info() const {
    std::vector<TensorDescription> input_tensors_info;
    for (size_t i = 0; i < io.input_names.size(); ++i) {
        std::vector<int> shape(io.input_shapes[i].size());
        std::transform(io.input_shapes[i].begin(), io.input_shapes[i].end(), shape.begin(), [](int64_t x) {
            return static_cast<int>(x);
        });
        input_tensors_info.push_back(
            {std::string(io.input_names[i]), shape, shape, "", get_data_precision(io.input_data_precisions[i]), false});
    }
    std::vector<TensorDescription> output_tensors_info;
    for (size_t i = 0; i < io.output_names.size(); ++i) {
        std::vector<int> shape(io.output_shapes[i].size());
        std::transform(io.output_shapes[i].begin(), io.output_shapes[i].end(), shape.begin(), [](int64_t x) {
            return static_cast<int>(x);
        });
        output_tensors_info.push_back(
            {std::string(io.output_names[i]), shape, {}, "", get_data_precision(io.output_data_precisions[i]), false});
    }
    return {input_tensors_info, output_tensors_info};
}

void ONNXLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>> tbuffers) {
    tensor_buffers = std::move(tbuffers);
    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);
    tensors.resize(tensor_buffers.size());
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            const auto& buffer = tensor_buffers[i][j];
            std::vector<int64_t> shape(buffer.shape().begin(), buffer.shape().end());
            tensors[i].push_back(Ort::Value::CreateTensor(memory_info,
                                                          buffer.get<void>(),
                                                          buffer.size(),
                                                          shape.data(),
                                                          shape.size(),
                                                          get_onnx_data_type(buffer.precision())));
        }
    }
}

void ONNXLauncher::warmup_inference() {
    run(tensors[0]);
}

void ONNXLauncher::run(const std::vector<Ort::Value>& input_tensors) {
    total_start_time = std::min(HighresClock::now(), total_start_time);

    infer_start_time = HighresClock::now();
    auto output = session->Run(Ort::RunOptions{nullptr},
                               io.input_names.data(),
                               input_tensors.data(),
                               io.input_names.size(),
                               io.output_names.data(),
                               io.output_names.size());
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));

    total_end_time = std::max(HighresClock::now(), total_end_time);
}

int ONNXLauncher::evaluate(int iterations_num, uint64_t time_limit_ns) {
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
