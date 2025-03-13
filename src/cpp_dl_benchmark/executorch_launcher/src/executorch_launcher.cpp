#include "executorch_launcher.hpp"
#include <executorch/extension/tensor/tensor.h>
#include <executorch/runtime/core/exec_aten/exec_aten.h>

using namespace executorch::aten;

namespace {
    const std::map<ScalarType, utils::DataPrecision> dtype_to_precision_map{{ScalarType::Half, utils::DataPrecision::FP16},
                                                                            {ScalarType::Float, utils::DataPrecision::FP32},
                                                                            {ScalarType::Double, utils::DataPrecision::FP64},
                                                                            {ScalarType::Char, utils::DataPrecision::I8},
                                                                            {ScalarType::Short, utils::DataPrecision::I16},
                                                                            {ScalarType::Int, utils::DataPrecision::I32},
                                                                            {ScalarType::Long, utils::DataPrecision::I64},
                                                                            {ScalarType::Byte, utils::DataPrecision::U8}};
    
    utils::DataPrecision get_data_precision(ScalarType type) {
        if (dtype_to_precision_map.count(type) > 0) {
            return dtype_to_precision_map.at(type);
        }
        else {
            throw std::invalid_argument("Does not support element data type ");
        }
    }
    
    ScalarType get_data_type(utils::DataPrecision precision) {
        for (const auto& [type, data_prectision] : dtype_to_precision_map) {
            if (precision == data_prectision) {
                return type;
            }
        }
        throw std::invalid_argument("Does not support element data type " + utils::get_data_precision_str(precision));
    }
}  // namespace




ExecuTorchLauncher::ExecuTorchLauncher(const int nthreads, const int fps, const std::string& device) : Launcher(nthreads, fps, device) {
    if (nthreads > 0) {
        executorch::extension::threadpool::get_threadpool()->_unsafe_reset_threadpool(nthreads);
    }
    else {
        auto threads = executorch::extension::cpuinfo::get_num_performant_cores();
        executorch::extension::threadpool::get_threadpool()->_unsafe_reset_threadpool(threads); 
    }
}

ExecuTorchLauncher::~ExecuTorchLauncher() {}

std::string ExecuTorchLauncher::get_framework_name() const {
    return "ExecuTorch";
}

std::string ExecuTorchLauncher::get_framework_version() const {
    return "unknown";
}

std::string ExecuTorchLauncher::get_backend_name() const {
#ifdef EXECUTORCH_DEFAULT
    return "default";
#elif EXECUTORCH_XNNPACK
    return "XNNPACK";
#endif
}

void ExecuTorchLauncher::read(const std::string& model_file, const std::string& weights_file) {
    module = std::make_shared<executorch::extension::Module>(model_file);
}

void ExecuTorchLauncher::fill_inputs_outputs_info() {}

IOTensorsInfo ExecuTorchLauncher::get_io_tensors_info() const {
    return {{}, {}};
}

void ExecuTorchLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tbuffers) {
    tensor_buffers = std::move(tbuffers);
    tensors.resize(tensor_buffers.size());
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        if (i == 0) {
            input_shapes.resize(tensor_buffers[0].size());
        }
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            auto& buffer = tensor_buffers[i][j];
            std::vector<int> shape(buffer.shape().begin(), buffer.shape().end());
            tensors[i].push_back(
                executorch::extension::from_blob(buffer.get(), shape, get_data_type(buffer.precision())));
            if (i == 0) {
                input_shapes[j] = shape;
            }
        }
    }
}

void ExecuTorchLauncher::compile() {}

std::vector<OutputTensors> ExecuTorchLauncher::get_output_tensors() {
    const auto out = module->execute("forward", tensors[0]);
    if (!out.ok()) {
        throw std::runtime_error("Output dumping is supported only for models with one output!");
    }

    OutputTensors output;
    const auto result = out->at(0).toTensor();
    auto* raw_data = result.const_data_ptr<float>();
    auto size = result.numel();

    auto shape = result.sizes();
    std::string name = "output";
    std::vector<float> data(raw_data, raw_data + size);

    std::vector<int> int_shape(shape.begin(), shape.end());
    output.emplace_back(static_cast<size_t>(size), int_shape, name, data);

    return {output};
}

void ExecuTorchLauncher::run(const int input_idx) {
    infer_start_time = HighresClock::now();
    module->execute("forward", tensors[input_idx]);
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));
}
