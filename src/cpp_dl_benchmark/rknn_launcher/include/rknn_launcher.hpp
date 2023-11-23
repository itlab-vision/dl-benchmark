#pragma once

#include "common_launcher/launcher.hpp"
#include "inputs_preparation/tensor_utils.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <rknn_api.h>

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

class RKNNLauncher : public Launcher {
public:
    RKNNLauncher(const std::string& model_file = "", const int nthreads = -1); 
    virtual ~RKNNLauncher();

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
    mutable rknn_context rknnContext = 0;
    mutable int ret_code;

    int inputs_num = -1;
    std::vector<std::string> input_names;
    std::vector<std::vector<int>> input_shapes;
    std::vector<_rknn_tensor_type> input_data_precisions;
    std::vector<_rknn_tensor_format> input_layouts;
    rknn_input* inputs = nullptr;

    int outputs_num = -1;
    std::vector<std::string> output_names;
    std::vector<std::vector<int>> output_shapes;
    std::vector<_rknn_tensor_type> output_data_precisions;
    std::vector<_rknn_tensor_format> output_layouts;
    rknn_output* outputs = nullptr;

    void run(const int input_idx) override;
    void destroy_context();
};
