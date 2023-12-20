#include "tflite_launcher.hpp"

#include "common_launcher/launcher.hpp"
#include "custom_ops.hpp"
#include "inputs_preparation/inputs_preparation.hpp"
#include "utils/args_handler.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <tensorflow/lite/c/c_api.h>
#include <tensorflow/lite/delegates/gpu/delegate.h>
#include <tensorflow/lite/delegates/xnnpack/xnnpack_delegate.h>
#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>
#include <tensorflow/lite/model.h>
#include <tensorflow/lite/version.h>

#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <fstream>
#include <numeric>
#include <string>
#include <vector>

#include <nlohmann/json.hpp>

namespace {
const std::map<TfLiteType, utils::DataPrecision> tflite_dtype_to_precision_map{
    {kTfLiteFloat16, utils::DataPrecision::FP16},
    {kTfLiteFloat32, utils::DataPrecision::FP32},
    {kTfLiteFloat64, utils::DataPrecision::FP64},
    {kTfLiteInt8, utils::DataPrecision::I8},
    {kTfLiteInt16, utils::DataPrecision::I16},
    {kTfLiteInt32, utils::DataPrecision::I32},
    {kTfLiteInt64, utils::DataPrecision::I64},
    {kTfLiteUInt8, utils::DataPrecision::U8},
    {kTfLiteUInt16, utils::DataPrecision::U16},
    {kTfLiteUInt32, utils::DataPrecision::U32},
    {kTfLiteUInt64, utils::DataPrecision::U64},
    {kTfLiteBool, utils::DataPrecision::BOOL},
    {kTfLiteNoType, utils::DataPrecision::UNKNOWN}};

utils::DataPrecision get_data_precision(TfLiteType type) {
    if (tflite_dtype_to_precision_map.count(type) > 0) {
        return tflite_dtype_to_precision_map.at(type);
    }
    else {
        throw std::invalid_argument("Does not support element data type " + std::to_string(type));
    }
}

TfLiteType get_tflite_data_type(utils::DataPrecision precision) {
    for (const auto [tflite_type, data_prectision] : tflite_dtype_to_precision_map) {
        if (precision == data_prectision) {
            return tflite_type;
        }
    }
    throw std::invalid_argument("Does not support element data type " + utils::get_data_precision_str(precision));
}
}  // namespace

TFLiteLauncher::TFLiteLauncher(const int nthreads, const std::string& device) : Launcher(nthreads, device) {}

TFLiteLauncher::~TFLiteLauncher() {
    if (gpu_delegate != nullptr) {
        TfLiteGpuDelegateV2Delete(gpu_delegate);
    }
    if (xnnpack_delegate != nullptr) {
        TfLiteXNNPackDelegateDelete(xnnpack_delegate);
    }
}
std::string TFLiteLauncher::get_framework_name() const {
    return "TFLite";
}

std::string TFLiteLauncher::get_framework_version() const {
    return std::string(TFLITE_VERSION_STRING);
}

std::string TFLiteLauncher::get_backend_name() const {
#ifdef TFLITE_WITH_DEFAULT_BACKEND
    return "default";
#elif TFLITE_WITH_XNNPACK_BACKEND
    return "XNNPack";
#elif TFLITE_WITH_GPU_DELEGATE
    return "GPUDelegate";
#endif
}

void TFLiteLauncher::read(const std::string& model_file, const std::string& weights_file) {
    model = tflite::FlatBufferModel::BuildFromFile(model_file.c_str());
    if (!model) {
        throw std::runtime_error("Failed to read model " + model_file);
    }

#ifdef TFLITE_WITH_XNNPACK_BACKEND
    // XNNPACK engine used by TensorFlow Lite interpreter uses a single thread for inference by default.
    // https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/delegates/xnnpack/README.md#enable-xnnpack-via-bazel-build-flags-recommended-on-desktop
    resolver = std::make_unique<tflite::ops::builtin::BuiltinOpResolver>();
#else
    resolver = std::make_unique<tflite::ops::builtin::BuiltinOpResolverWithoutDefaultDelegates>();
#endif
    tflite_ops::RegisterSelectedOps(resolver.get());
    tflite::InterpreterBuilder builder(*model, *resolver);

    // Note that in this case Interpreter::SetNumThreads invocation does not take effect on number of threads used by
    // XNNPACK engine. In order to specify number of threads available for XNNPACK engine you should manually pass the
    // value when constructing the interpreter.
    if (nthreads != 0 && builder.SetNumThreads(nthreads) != kTfLiteOk) {
        throw std::runtime_error("Failed to set thread number");
    }
    builder(&interpreter);

#ifdef TFLITE_WITH_GPU_DELEGATE
    if (device == utils::Device::GPU) {
        auto gpu_options = TfLiteGpuDelegateOptionsV2Default();
        gpu_options.inference_preference = TFLITE_GPU_INFERENCE_PREFERENCE_SUSTAINED_SPEED;
        gpu_options.inference_priority1 = TFLITE_GPU_INFERENCE_PRIORITY_MIN_LATENCY;
        gpu_delegate = TfLiteGpuDelegateV2Create(&gpu_options);
        if (interpreter->ModifyGraphWithDelegate(gpu_delegate) != kTfLiteOk) {
            throw std::runtime_error("Failed to apply GPU delegate.");
        }
    }
    else {
        throw std::runtime_error(utils::get_device_str(device) + " device is not supported in GPU delegate!");
    }
#else
    if (device != utils::Device::CPU) {
        throw std::runtime_error(utils::get_device_str(device) + " device is not supported!");
    }
#endif
}

void TFLiteLauncher::fill_inputs_outputs_info() {
    for (size_t i = 0; i < interpreter->inputs().size(); ++i) {
        input_names.push_back(interpreter->GetInputName(static_cast<int>(i)));
        const auto* input_tensor = interpreter->input_tensor(i);
        const auto* dims = input_tensor->dims;
        if (dims->size == 0) {
            input_shapes.emplace_back(4, -1);  // dummy input shape to enable providing shape from cmd
        }
        else {
            input_shapes.emplace_back(dims->data, dims->data + dims->size);
        }
        input_data_precisions.push_back(input_tensor->type);
    }

    for (size_t i = 0; i < interpreter->outputs().size(); ++i) {
        output_names.push_back(interpreter->GetOutputName(static_cast<int>(i)));
        const auto* output_tensor = interpreter->output_tensor(i);
        const auto* dims = output_tensor->dims;
        output_shapes.emplace_back(dims->data, dims->data + dims->size);
        output_data_precisions.push_back(output_tensor->type);
    }
}

IOTensorsInfo TFLiteLauncher::get_io_tensors_info() const {
    std::vector<TensorDescription> input_tensors_info;
    for (size_t i = 0; i < input_names.size(); ++i) {
        input_tensors_info.push_back(
            {input_names[i], input_shapes[i], input_shapes[i], "", get_data_precision(input_data_precisions[i]), true});
    }
    std::vector<TensorDescription> output_tensors_info;
    for (size_t i = 0; i < output_names.size(); ++i) {
        output_tensors_info.push_back(
            {output_names[i], output_shapes[i], {}, "", get_data_precision(output_data_precisions[i]), false});
    }
    return {input_tensors_info, output_tensors_info};
}

void TFLiteLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tbuffers) {
    tensor_buffers = std::move(tbuffers);
    const auto& inputs = tensor_buffers[0];
    for (int i = 0; i < inputs.size(); ++i) {
        if (inputs[i].shape() != input_shapes[i]) {
            if (interpreter->ResizeInputTensor(i, inputs[i].shape()) != kTfLiteOk) {
                throw std::runtime_error("Input tensor couldn't be resized. Use default model shape.");
            }
        }
    }

    if (interpreter->AllocateTensors() != kTfLiteOk) {
        throw std::runtime_error("Failed to allocate tensors");
    }
}

void TFLiteLauncher::run(const int input_idx) {
    auto& tbuffers = tensor_buffers[input_idx];
    for (size_t i = 0; i < interpreter->inputs().size(); ++i) {
        if (TfLiteTensorCopyFromBuffer(interpreter->input_tensor(i), tbuffers[i].get(), tbuffers[i].size()) !=
            kTfLiteOk) {
            throw std::runtime_error("Failed to copy tensor from buffer: Tensor expect " +
                                     std::to_string(interpreter->input_tensor(i)->bytes) + " bytes, Buffer contains " +
                                     std::to_string(tbuffers[i].size()) + " bytes");
        }
    }

    infer_start_time = HighresClock::now();
    auto status = interpreter->Invoke();
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));

    if (status != kTfLiteOk) {
        throw std::runtime_error("Failed invoke interpreter");
    }
}

std::vector<OutputTensors> TFLiteLauncher::get_output_tensors() {
    run(0);

    std::vector<OutputTensors> outputs;

    OutputTensors output;
    for (size_t i = 0; i < interpreter->outputs().size(); ++i) {
        const TfLiteTensor* result = interpreter->output_tensor(i);
        const float* raw_data = result->data.f;
        const auto* dims = result->dims;
        const std::vector<int> curr_output_shape(dims->data, dims->data + dims->size);

        size_t size = std::accumulate(curr_output_shape.begin(), curr_output_shape.end(), 1, std::multiplies<int>());

        const std::vector<float> data(raw_data, raw_data + size);

        output.emplace_back(size, curr_output_shape, output_names[i], data);
    }

    outputs.push_back(output);

    return outputs;
}