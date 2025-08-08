#pragma once

#include "common_launcher/launcher.hpp"
#include "inputs_preparation/tensor_utils.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"
#include "memory_manager.hpp"

#include <executorch/extension/module/module.h>
#include <executorch/extension/tensor/tensor.h>
#include <executorch/extension/memory_allocator/malloc_memory_allocator.h>
#include <executorch/extension/threadpool/cpuinfo_utils.h>
#include <executorch/extension/threadpool/threadpool.h>
#include <executorch/extension/data_loader/file_data_loader.h>

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>


class ExecuTorchLauncher : public Launcher {
public:
    ExecuTorchLauncher(const int nthreads, const int fps, const std::string& device);
    virtual ~ExecuTorchLauncher();

    std::string get_framework_name() const override;
    std::string get_framework_version() const override;
    std::string get_backend_name() const override;

    void read(const std::string& model_file, const std::string& weights_file = "") override;
    void load() override{};

    void fill_inputs_outputs_info() override;
    IOTensorsInfo get_io_tensors_info() const override;

    void prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tensor_buffers) override;
    void compile() override;

    std::vector<OutputTensors> get_output_tensors() override;

private:
    std::unique_ptr<InferenceAPI> inference_api;

    std::vector<std::string> input_names;
    std::vector<std::vector<int>> input_shapes;

    std::vector<std::string> output_names;
    std::vector<std::vector<int>> output_shapes;

    std::vector<std::vector<executorch::runtime::EValue>> tensors;

    void run(const int input_idx);
};