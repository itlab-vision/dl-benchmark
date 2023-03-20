#pragma once

#include "inputs_preparation/tensor_utils.hpp"
#include "utils/utils.hpp"

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

using HighresClock = std::chrono::high_resolution_clock;

using IOTensorsInfo = std::pair<std::vector<TensorDescr>, std::vector<TensorDescr>>;

class Launcher {
protected:
    int nthreads;

    std::vector<std::vector<TensorBuffer>> tensor_buffers;

    // time stamps for total time measurments;
    HighresClock::time_point total_start_time;
    HighresClock::time_point total_end_time;

    // time stamps for individual inference
    HighresClock::time_point infer_start_time;
    std::vector<double> latencies;

public:
    Launcher(int nthreads) : nthreads(nthreads){};
    virtual ~Launcher() {}

    virtual void log_framework_version() const = 0;

    virtual void read(const std::string model_file, const std::string weights_file = "") = 0;
    virtual void load() = 0;

    virtual void fill_inputs_outputs_info() = 0;
    virtual IOTensorsInfo get_io_tensors_info() const = 0;

    virtual void prepare_input_tensors(std::vector<std::vector<TensorBuffer>> tensor_buffers) = 0;

    virtual void warmup_inference() = 0;
    virtual int evaluate(int iterations_num, uint64_t time_limit_ns) = 0;

    std::vector<double> get_latencies() const;
    double get_total_time_ms() const;

    void reset_timers();
};
