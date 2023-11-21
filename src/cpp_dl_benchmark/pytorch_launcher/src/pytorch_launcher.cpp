#include "pytorch_launcher.hpp"

#include <torch/script.h>
#include <torch/torch.h>
#ifdef PYTORCH_TENSORRT
#include "torch_tensorrt/torch_tensorrt.h"
#endif

#include <algorithm>
#include <chrono>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

namespace {
const std::map<torch::Dtype, utils::DataPrecision> dtype_to_precision_map{{torch::kFloat16, utils::DataPrecision::FP16},
                                                                          {torch::kFloat32, utils::DataPrecision::FP32},
                                                                          {torch::kFloat64, utils::DataPrecision::FP64},
                                                                          {torch::kInt8, utils::DataPrecision::I8},
                                                                          {torch::kInt16, utils::DataPrecision::I16},
                                                                          {torch::kInt32, utils::DataPrecision::I32},
                                                                          {torch::kInt64, utils::DataPrecision::I64},
                                                                          {torch::kUInt8, utils::DataPrecision::U8}};

utils::DataPrecision get_data_precision(torch::Dtype type) {
    if (dtype_to_precision_map.count(type) > 0) {
        return dtype_to_precision_map.at(type);
    }
    else {
        std::ostringstream s;
        s << type;
        throw std::invalid_argument("Does not support element data type " + s.str());
    }
}

torch::Dtype get_data_type(utils::DataPrecision precision) {
    for (const auto& [type, data_prectision] : dtype_to_precision_map) {
        if (precision == data_prectision) {
            return type;
        }
    }
    throw std::invalid_argument("Does not support element data type " + utils::get_data_precision_str(precision));
}
}  // namespace

PytorchLauncher::PytorchLauncher(int nthreads, const std::string& device) : Launcher(nthreads, device) {
    if (nthreads > 0) {
        torch::set_num_threads(nthreads);
    }
    nthreads = torch::get_num_threads();
}

PytorchLauncher::~PytorchLauncher() {}
std::string PytorchLauncher::get_framework_name() const {
    return "PyTorch";
}

std::string PytorchLauncher::get_framework_version() const {
    return std::string(TORCH_VERSION);
}

std::string PytorchLauncher::get_backend_name() const {
    return "default";
}

void PytorchLauncher::read(const std::string& model_file, const std::string& weights_file) {
    if (device == utils::Device::CPU) {
        device_type = torch::kCPU;
    }
    else if (device == utils::Device::NVIDIA_GPU && torch::cuda::is_available()) {
        device_type = torch::kCUDA;
    }
    else {
        throw std::runtime_error(utils::get_device_str(device) + " device is not supported!");
    }

    torch::Device torch_device(device_type, 0);
    try {
        module = torch::jit::load(model_file, torch_device);
    } catch (const c10::Error& e) {
        throw std::runtime_error("Failed to read model " + model_file);
    }
    module.eval();
}

void PytorchLauncher::fill_inputs_outputs_info() {}

IOTensorsInfo PytorchLauncher::get_io_tensors_info() const {
    return {{}, {}};
}

void PytorchLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tbuffers) {
    torch::Device torch_device(device_type, 0);
    tensor_buffers = std::move(tbuffers);
    tensors.resize(tensor_buffers.size());
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        if (i == 0) {
            input_shapes.resize(tensor_buffers[0].size());
        }
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            auto& buffer = tensor_buffers[i][j];
            std::vector<int64_t> shape(buffer.shape().begin(), buffer.shape().end());
            tensors[i].push_back(
                torch::from_blob(buffer.get(), shape, get_data_type(buffer.precision())).to(torch_device));
            if (i == 0) {
                input_shapes[j] = shape;
            }
        }
    }
}

void PytorchLauncher::compile() {
#ifdef PYTORCH_TENSORRT
    logger::info << "Compile model for TensorRT" << logger::endl;
    auto compile_settings = torch_tensorrt::ts::CompileSpec(input_shapes);
    compile_settings.enabled_precisions = {torch::kFloat};
    compile_settings.truncate_long_and_double = true;
    module = torch_tensorrt::ts::compile(module, compile_settings);
#endif
}

void PytorchLauncher::run(const int input_idx) {
    torch::InferenceMode guard;

    if (device == utils::Device::NVIDIA_GPU)
        torch::cuda::synchronize();
    infer_start_time = HighresClock::now();
    module.forward(tensors[input_idx]);
    if (device == utils::Device::NVIDIA_GPU)
        torch::cuda::synchronize();
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));
}

std::vector<OutputTensors> PytorchLauncher::get_output_tensors() {
    const auto out = module.forward(tensors[0]);
    if (out.isTuple()) {
        throw std::runtime_error("Output dumping is supported only for models with one output!");
    }

    OutputTensors output;
    const auto result = out.toTensor();
    auto* raw_data = result.data_ptr<float>();
    auto size = result.numel();

    auto shape = result.sizes();
    std::string name = "output";
    std::vector<float> data(raw_data, raw_data + size);

    std::vector<int> int_shape(shape.begin(), shape.end());
    output.emplace_back(static_cast<size_t>(size), int_shape, name, data);

    return {output};
}