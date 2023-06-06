#include "pytorch_launcher.hpp"

#include <torch/script.h>
#include <torch/torch.h>

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
    for (const auto [type, data_prectision] : dtype_to_precision_map) {
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
    module = torch::jit::load(model_file, torch_device);
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
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            const auto& buffer = tensor_buffers[i][j];
            std::vector<int64_t> shape(buffer.shape().begin(), buffer.shape().end());
            tensors[i].push_back(
                torch::from_blob(buffer.get(), shape, get_data_type(buffer.precision())).to(torch_device));
        }
    }
}

void PytorchLauncher::warmup_inference() {
    run(tensors[0]);
}

void PytorchLauncher::run(const std::vector<torch::jit::IValue>& tensors) {
    torch::InferenceMode guard;

    total_start_time = std::min(HighresClock::now(), total_start_time);

    if (device == utils::Device::NVIDIA_GPU)
        torch::cuda::synchronize();
    infer_start_time = HighresClock::now();
    module.forward(tensors);
    if (device == utils::Device::NVIDIA_GPU)
        torch::cuda::synchronize();
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));

    total_end_time = std::max(HighresClock::now(), total_end_time);
}

int PytorchLauncher::evaluate(int iterations_num, uint64_t time_limit_ns) {
    int iteration = 0;
    auto start_time = HighresClock::now();
    auto uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    while ((iterations_num != 0 && iteration < iterations_num) ||
           (time_limit_ns != 0 && static_cast<uint64_t>(uptime) < time_limit_ns)) {
        run(tensors[iteration % tensor_buffers.size()]);
        ++iteration;
        uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    }

    return iteration;
}
