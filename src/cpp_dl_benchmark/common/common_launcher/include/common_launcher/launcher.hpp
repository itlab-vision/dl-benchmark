#pragma once

#include "inputs_preparation/tensor_utils.hpp"
#include "output/output_description.hpp"
#include "utils/utils.hpp"

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

using HighresClock = std::chrono::high_resolution_clock;

using IOTensorsInfo = std::pair<std::vector<TensorDescription>, std::vector<TensorDescription>>;

class Launcher {
protected:
    int nthreads;
    utils::Device device;

    std::vector<std::vector<TensorBuffer>> tensor_buffers;

    // time stamps for individual inference
    HighresClock::time_point infer_start_time;
    std::vector<double> latencies;

    virtual void run(const int input_idx) = 0;

public:
    Launcher(const int nthreads, const std::string& device)
        : nthreads(nthreads), device(utils::get_device_from_str(device)){};
    virtual ~Launcher() {}

    virtual std::string get_framework_name() const = 0;
    virtual std::string get_framework_version() const = 0;
    virtual std::string get_backend_name() const = 0;
    virtual void read(const std::string& model_file, const std::string& weights_file = "") = 0;
    virtual void prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tensor_buffers) = 0;
    virtual void load() = 0;
    virtual void compile() = 0;

    virtual void fill_inputs_outputs_info() = 0;
    virtual IOTensorsInfo get_io_tensors_info() const = 0;

    void warmup_inference();
    int evaluate(int iterations_num, uint64_t time_limit_ns);

    virtual std::vector<OutputTensors> get_output_tensors() = 0;
    void dump_output(const std::vector<OutputTensors>& outputs, const std::string& filename = "output.json");

    std::vector<double> get_latencies() const;
    double get_total_time_ms() const;
    int get_threads_num() const {
        return nthreads;
    }
    void reset_timers();
};
