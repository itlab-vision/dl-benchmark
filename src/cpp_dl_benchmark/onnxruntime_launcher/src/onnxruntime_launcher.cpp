#include "onnxruntime_launcher.hpp"

#include "inputs_preparation/inputs_preparation.hpp"
#include "utils/args_handler.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <onnxruntime_c_api.h>
#include <onnxruntime_cxx_api.h>

#include <algorithm>
#include <chrono>
#include <fstream>
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
    throw std::invalid_argument("Does not support element data type " + utils::get_data_precision_str(precision));
}

void check_status(OrtStatusPtr status) {
    if (status != nullptr) {
        std::string error_message = Ort::GetApi().GetErrorMessage(status);
        OrtErrorCode error_code = Ort::GetApi().GetErrorCode(status);
        Ort::GetApi().ReleaseStatus(status);
        throw Ort::Exception(std::move(error_message), error_code);
    }
}
}  // namespace

ONNXLauncher::~ONNXLauncher() {
#ifdef ORT_CUDA
    Ort::GetApi().ReleaseCUDAProviderOptions(cuda_options);
#endif
}

std::string ONNXLauncher::get_framework_name() const {
    return "ONNXRuntime";
}

std::string ONNXLauncher::get_framework_version() const {
    return std::string(OrtGetApiBase()->GetVersionString());
}

std::string ONNXLauncher::get_backend_name() const {
#ifdef ORT_DEFAULT
    return "default";
#elif ORT_CUDA
    return "CUDA";
#elif ORT_TENSORRT
    return "TensorRT";
#endif
}

void ONNXLauncher::read(const std::string& model_file, const std::string& weights_file) {
    env = std::make_shared<Ort::Env>(ORT_LOGGING_LEVEL_ERROR, "ORT Benchmark");
    Ort::SessionOptions session_options;
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    if (device == utils::Device::CPU) {
        session_options.SetExecutionMode(ExecutionMode::ORT_SEQUENTIAL);
        if (nthreads > 0) {
            session_options.SetIntraOpNumThreads(nthreads);
        }
    }
#ifdef ORT_CUDA
    else if (device == utils::Device::NVIDIA_GPU) {
        check_status(Ort::GetApi().CreateCUDAProviderOptions(&cuda_options));
        std::vector<const char*> keys{"device_id",
                                      "arena_extend_strategy",
                                      "cudnn_conv_algo_search",
                                      "do_copy_in_default_stream",
                                      "cudnn_conv_use_max_workspace",
                                      "cudnn_conv1d_pad_to_nc1d"};
        std::vector<const char*> values{"0", "kSameAsRequested", "DEFAULT", "1", "1", "1"};
        check_status(Ort::GetApi().UpdateCUDAProviderOptions(cuda_options, keys.data(), values.data(), keys.size()));
        check_status(Ort::GetApi().SessionOptionsAppendExecutionProvider_CUDA_V2(session_options, cuda_options));
    }
#elif ORT_TENSORRT
    else if (device == utils::Device::NVIDIA_GPU) {
        check_status(Ort::GetApi().CreateTensorRTProviderOptions(&tensorrt_options));
        std::vector<const char*> keys{"device_id", "trt_fp16_enable", "trt_max_workspace_size"};
        std::vector<const char*> values{"0", "1", "4294967296"};
        check_status(
            Ort::GetApi().UpdateTensorRTProviderOptions(tensorrt_options, keys.data(), values.data(), keys.size()));
        check_status(
            Ort::GetApi().SessionOptionsAppendExecutionProvider_TensorRT_V2(session_options, tensorrt_options));
    }
#endif
    else {
        throw std::runtime_error(utils::get_device_str(device) + " device is not supported!");
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

void ONNXLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tbuffers) {
    tensor_buffers = std::move(tbuffers);
    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);
    tensors.resize(tensor_buffers.size());
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            auto& buffer = tensor_buffers[i][j];
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

void ONNXLauncher::run(const int input_idx) {
    infer_start_time = HighresClock::now();
    auto output = session->Run(Ort::RunOptions{nullptr},
                               io.input_names.data(),
                               tensors[input_idx].data(),
                               io.input_names.size(),
                               io.output_names.data(),
                               io.output_names.size());
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));
}

std::vector<Ort::Value> ONNXLauncher::run_for_output(const int input_idx) {
    return session->Run(Ort::RunOptions{nullptr},
                        io.input_names.data(),
                        tensors[input_idx].data(),
                        io.input_names.size(),
                        io.output_names.data(),
                        io.output_names.size());
}

std::vector<OutputTensors> ONNXLauncher::get_output_tensors() {
    std::vector<OutputTensors> outputs;

    for (size_t idx = 0; idx < tensors.size(); ++idx) {
        auto result = run_for_output(idx);
        auto* raw_data = result[0].GetTensorData<float>();
        auto size = result[0].GetTensorTypeAndShapeInfo().GetElementCount();

        std::vector<int64_t> shape = result[0].GetTensorTypeAndShapeInfo().GetShape();
        std::string name = std::string(io.output_names[0]);
        std::vector<float> data(raw_data, raw_data + size);

        std::vector<int> int_shape(shape.begin(), shape.end());
        OutputTensors output({{size, int_shape, name, data}});

        outputs.push_back(output);
    }

    return outputs;
}
