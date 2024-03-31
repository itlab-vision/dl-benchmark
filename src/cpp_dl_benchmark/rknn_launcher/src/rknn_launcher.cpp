#include "rknn_launcher.hpp"

#include "common_launcher/launcher.hpp"
#include "inputs_preparation/inputs_preparation.hpp"
#include "utils/args_handler.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <rknn_api.h>

#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

namespace {
const std::map<_rknn_tensor_type, utils::DataPrecision> rknn_dtype_to_precision_map{
    {RKNN_TENSOR_FLOAT16, utils::DataPrecision::FP16},
    {RKNN_TENSOR_FLOAT32, utils::DataPrecision::FP32},
    {RKNN_TENSOR_INT8, utils::DataPrecision::I8},
    {RKNN_TENSOR_INT16, utils::DataPrecision::I16},
    {RKNN_TENSOR_INT32, utils::DataPrecision::I32},
    {RKNN_TENSOR_INT64, utils::DataPrecision::I64},
    {RKNN_TENSOR_UINT8, utils::DataPrecision::U8},
    {RKNN_TENSOR_UINT16, utils::DataPrecision::U16},
    {RKNN_TENSOR_UINT32, utils::DataPrecision::U32},
    {RKNN_TENSOR_BOOL, utils::DataPrecision::BOOL}};

const std::map<int, _rknn_core_mask> ncores_to_rknn_core_mask_map{
    {0, RKNN_NPU_CORE_AUTO}, /* default, run on NPU core randomly. */
    {1, RKNN_NPU_CORE_0}, /* run on NPU core 0. */
    {2, RKNN_NPU_CORE_0_1}, /* run on NPU core 1 and core 2. */
    {3, RKNN_NPU_CORE_0_1_2}}; /* run on NPU core 1 and core 2 and core 3. */

const std::map<int, std::string> ret_code_to_err_message{
    {RKNN_SUCC, "Execute succeed"},
    {RKNN_ERR_FAIL, "Execute failed"},
    {RKNN_ERR_TIMEOUT, "Execute timeout"},
    {RKNN_ERR_DEVICE_UNAVAILABLE, "Device is unavailable."},
    {RKNN_ERR_MALLOC_FAIL, "Memory malloc fail"},
    {RKNN_ERR_PARAM_INVALID, "Parameter is invalid"},
    {RKNN_ERR_MODEL_INVALID, "Model is invalid"},
    {RKNN_ERR_CTX_INVALID, "Context is invalid"},
    {RKNN_ERR_INPUT_INVALID, "Input is invalid"},
    {RKNN_ERR_OUTPUT_INVALID, "Output is invalid"},
    {RKNN_ERR_DEVICE_UNMATCH, "The device is unmatch, please update rknn sdk and npu driver/firmware"},
    {RKNN_ERR_INCOMPATILE_PRE_COMPILE_MODEL,
     "This RKNN model use pre_compile mode, but not compatible with current driver"},
    {RKNN_ERR_INCOMPATILE_OPTIMIZATION_LEVEL_VERSION,
     "This RKNN model set optimization level, but not compatible with current driver"},
    {RKNN_ERR_TARGET_PLATFORM_UNMATCH,
     "This RKNN model set target platform, but not compatible with current platform"}};

utils::DataPrecision get_data_precision(_rknn_tensor_type type) {
    if (rknn_dtype_to_precision_map.count(type) > 0) {
        return rknn_dtype_to_precision_map.at(type);
    }
    else {
        throw std::invalid_argument("Does not support element data type " + std::to_string(type));
    }
}

_rknn_tensor_type get_rknn_data_type(utils::DataPrecision precision) {
    for (const auto [rknn_type, data_prectision] : rknn_dtype_to_precision_map) {
        if (precision == data_prectision) {
            return rknn_type;
        }
    }
    throw std::invalid_argument("Does not support element data type " + utils::get_data_precision_str(precision));
}

inline void check_throw_error(int ret_code, const std::string& msg) {
    if (ret_code != RKNN_SUCC) {
        logger::err << msg << ": " << ret_code_to_err_message.at(ret_code) << logger::endl;
        throw std::runtime_error(msg);
    }
}
}  // namespace

RKNNLauncher::RKNNLauncher(const std::string& model_file, const int nthreads, const int fps) : Launcher(nthreads, fps, "NPU") {
    read(model_file);  // we need to create context to be able to query framework information
}

void RKNNLauncher::destroy_context() {
    if (rknnContext > 0) {
        if (outputs != nullptr) {
            rknn_outputs_release(rknnContext, outputs_num, outputs);
        }
        rknn_destroy(rknnContext);
    }
    delete[] inputs;
    delete[] outputs;
}

RKNNLauncher::~RKNNLauncher() {
    destroy_context();
}

std::string RKNNLauncher::get_framework_name() const {
    return "RKNN";
}

std::string RKNNLauncher::get_framework_version() const {
    rknn_sdk_version sdk_ver;
    ret_code = rknn_query(rknnContext, RKNN_QUERY_SDK_VERSION, &sdk_ver, sizeof(sdk_ver));
    if (ret_code != RKNN_SUCC) {
        logger::warn << "rknn_query fail: " << ret_code_to_err_message.at(ret_code) << logger::endl;
        return "Unknown";
    }
    return std::string(sdk_ver.api_version) + ", driver version: " + std::string(sdk_ver.drv_version);
}

std::string RKNNLauncher::get_backend_name() const {
    return "default";
}

void RKNNLauncher::read(const std::string& model_file, const std::string& weights_file) {
    destroy_context();  // destroy previous context to make clean model load to measure loading time
    std::ifstream f(model_file, std::ios::binary | std::ios::ate);
    if (!f.is_open()) {
        std::string err_msg = "Can't open " + model_file;
        logger::err << err_msg << logger::endl;
        throw std::runtime_error(err_msg);
    }

    int modelSize = f.tellg();
    f.seekg(0, std::ios::beg);

    auto model = std::unique_ptr<unsigned char[]>(new unsigned char[modelSize]);
    if (!model) {
        std::string err_msg = "Failed to read model " + model_file;
        logger::err << err_msg << logger::endl;
        throw std::runtime_error(err_msg);
    }
    f.read((char*)model.get(), modelSize);
    if (modelSize != f.gcount()) {
        std::string err_msg = std::to_string(f.gcount()) + " bytes was read, but " + std::to_string(modelSize) +
                              " was expected in " + model_file;
        logger::err << err_msg << logger::endl;
        throw std::runtime_error(err_msg);
    }

    ret_code = rknn_init(&rknnContext, model.get(), modelSize, 0, NULL);
    check_throw_error(ret_code, "rknn_init failed");

    if (nthreads < 0 || nthreads > 3) {
        std::string err_msg = "Up to three cores are available to specify, prvided: " + std::to_string(nthreads);
        logger::err << err_msg << logger::endl;
        throw std::runtime_error(err_msg);
    }

    auto core_mask = ncores_to_rknn_core_mask_map.at(nthreads);
    ret_code = rknn_set_core_mask(rknnContext, core_mask);
    check_throw_error(ret_code, "rknn_set_core_mask failed");
}

void RKNNLauncher::fill_inputs_outputs_info() {
    // Get Model Input Output Info
    rknn_input_output_num io_num;
    ret_code = rknn_query(rknnContext, RKNN_QUERY_IN_OUT_NUM, &io_num, sizeof(io_num));
    check_throw_error(ret_code, "rknn_query failed");

    inputs_num = io_num.n_input;
    rknn_tensor_attr input_attrs[io_num.n_input];
    memset(input_attrs, 0, io_num.n_input * sizeof(rknn_tensor_attr));
    for (size_t i = 0; i < io_num.n_input; ++i) {
        input_attrs[i].index = i;
        // query info
        ret_code = rknn_query(rknnContext, RKNN_QUERY_INPUT_ATTR, &(input_attrs[i]), sizeof(rknn_tensor_attr));
        check_throw_error(ret_code, "rknn_query failed");

        input_names.push_back(input_attrs[i].name);
        input_shapes.emplace_back(input_attrs[i].dims, input_attrs[i].dims + input_attrs[i].n_dims);
        input_data_precisions.push_back(input_attrs[i].type);
        input_layouts.push_back(input_attrs[i].fmt);
    }

    outputs_num = io_num.n_output;
    rknn_tensor_attr output_attrs[io_num.n_output];
    memset(output_attrs, 0, io_num.n_output * sizeof(rknn_tensor_attr));
    for (size_t i = 0; i < io_num.n_output; ++i) {
        output_attrs[i].index = i;
        // query info
        ret_code = rknn_query(rknnContext, RKNN_QUERY_OUTPUT_ATTR, &(output_attrs[i]), sizeof(rknn_tensor_attr));
        check_throw_error(ret_code, "rknn_query failed");

        output_names.push_back(output_attrs[i].name);
        output_shapes.emplace_back(output_attrs[i].dims, output_attrs[i].dims + output_attrs[i].n_dims);
        output_data_precisions.push_back(output_attrs[i].type);
        output_layouts.push_back(output_attrs[i].fmt);
    }

    inputs = new rknn_input[io_num.n_input];
    outputs = new rknn_output[io_num.n_output];
    memset(outputs, 0, outputs_num * sizeof(rknn_output));
}

IOTensorsInfo RKNNLauncher::get_io_tensors_info() const {
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

void RKNNLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tbuffers) {
    tensor_buffers = std::move(tbuffers);
    memset(inputs, 0, inputs_num * sizeof(rknn_input));
}

void RKNNLauncher::run(const int input_idx) {
    auto& tbuffers = tensor_buffers[input_idx];
    for (size_t i = 0; i < inputs_num; ++i) {
        inputs[i].index = i;
        inputs[i].type = get_rknn_data_type(tbuffers[i].precision());
        inputs[i].size = tbuffers[i].size();
        inputs[i].fmt = input_layouts[i];
        inputs[i].buf = tbuffers[i].get();
        ret_code = rknn_inputs_set(rknnContext, inputs_num, inputs);
        check_throw_error(ret_code, "rknn_input_set failed");
    }

    infer_start_time = HighresClock::now();
    ret_code = rknn_run(rknnContext, nullptr);
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));

    check_throw_error(ret_code, "rknn_run failed");
}

std::vector<OutputTensors> RKNNLauncher::get_output_tensors() {
    run(0);

    for (size_t i = 0; i < outputs_num; ++i) {
        outputs[i].want_float = 1;
    }
    ret_code = rknn_outputs_get(rknnContext, outputs_num, outputs, NULL);
    check_throw_error(ret_code, "rknn_outputs_get failed");

    OutputTensors out_tensors;
    for (size_t i = 0; i < outputs_num; ++i) {
        size_t size = std::accumulate(output_shapes[i].begin(), output_shapes[i].end(), 1, std::multiplies<int>());
        auto* buf = static_cast<float*>(outputs[i].buf);
        const std::vector<float> data(buf, buf + size);
        out_tensors.emplace_back(size, output_shapes[i], output_names[i], data);
    }

    return {out_tensors};
}
