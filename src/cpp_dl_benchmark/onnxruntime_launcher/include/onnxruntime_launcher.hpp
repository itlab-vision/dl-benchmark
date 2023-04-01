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
    ONNXLauncher(int nthreads_) : Launcher(nthreads_){};
    virtual ~ONNXLauncher(){};

    void log_framework_version() const override;

    void read(const std::string model_file, const std::string weights_file = "") override;
    void load() override{};

    void fill_inputs_outputs_info() override;
    IOTensorsInfo get_io_tensors_info() const override;

    void prepare_input_tensors(std::vector<std::vector<TensorBuffer>> tensor_buffers) override;

    void warmup_inference() override;
    int evaluate(int iterations_num, uint64_t time_limit_ns) override;

    void topk(const Labels &lbls, uint64_t k) override;
    

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
    std::vector<std::vector<Ort::Value>> tensors;
    std::vector<std::vector<TensorBuffer>> tensor_buffers;

    void run(const std::vector<Ort::Value>& input_tensors);
    std::vector<Ort::Value> run_for_output(const std::vector<Ort::Value>& input_tensors);
    void topk_onnx(const std::vector<Ort::Value> &output, const Labels &lbls, uint64_t k = 5);
};
