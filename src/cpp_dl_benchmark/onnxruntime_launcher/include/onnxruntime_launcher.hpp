#pragma once
#include "common_launcher/launcher.hpp"
#include "inputs_preparation/tensor_utils.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <onnxruntime_cxx_api.h>

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

using HighresClock = std::chrono::high_resolution_clock;

class ONNXLauncher : public Launcher {
public:
    ONNXLauncher(const int nthreads, const std::string& device) : Launcher(nthreads, device){};
    virtual ~ONNXLauncher();

    std::string get_framework_name() const override;
    std::string get_framework_version() const override;
    std::string get_backend_name() const override;

    void read(const std::string& model_file, const std::string& weights_file = "") override;
    void load() override{};

    void fill_inputs_outputs_info() override;
    IOTensorsInfo get_io_tensors_info() const override;

    void prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tensor_buffers) override;
    void compile() override{};

    std::vector<OutputTensors> get_output_tensors() override;

private:
    struct IOInfo {
        std::vector<const char*> input_names;
        std::vector<Ort::AllocatedStringPtr> input_names_ptr;
        std::vector<ONNXTensorElementDataType> input_data_precisions;
        std::vector<std::vector<int64_t>> input_shapes;

        std::vector<const char*> output_names;
        std::vector<Ort::AllocatedStringPtr> output_names_ptr;
        std::vector<ONNXTensorElementDataType> output_data_precisions;
        std::vector<std::vector<int64_t>> output_shapes;
    } io;

    std::shared_ptr<Ort::Env> env;
    std::shared_ptr<Ort::Session> session;
    Ort::SessionOptions session_options;
#ifdef ORT_CUDA
    OrtCUDAProviderOptionsV2* cuda_options = nullptr;
#elif ORT_TENSORRT
    OrtTensorRTProviderOptionsV2* tensorrt_options = nullptr;
#endif
    std::vector<std::vector<Ort::Value>> tensors;

    void run(const int input_idx) override;
    std::vector<Ort::Value> run_for_output(const int input_idx);
};
