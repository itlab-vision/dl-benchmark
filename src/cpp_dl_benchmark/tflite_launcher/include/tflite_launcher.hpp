#pragma once
#include "common_launcher/launcher.hpp"
#include "inputs_preparation/tensor_utils.hpp"
#include "tflite_profiler.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>
#include <tensorflow/lite/model.h>

#include <chrono>
#include <cstdint>
#include <map>
#include <memory>
#include <string>
#include <vector>

class TFLiteLauncher final : public Launcher {
public:
    TFLiteLauncher(const int nthreads,
                   const int fps,
                   const std::string& device,
                   bool enableProfiling = false,
                   const std::string& profilingReportFilePath = "");
    virtual ~TFLiteLauncher();

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
    const bool enableProfiling;
    const std::string profilingReportFilePath;

    // Note that the model instance must outlive the
    // interpreter instance.
    std::unique_ptr<tflite::FlatBufferModel> model = nullptr;
    std::unique_ptr<tflite::Interpreter> interpreter = nullptr;
    std::unique_ptr<tflite::ops::builtin::BuiltinOpResolver> resolver;

    /// Use raw pointer as TfLiteDelegate is a C structure, so it has no
    /// virtual destructor. The default deleter of the unique_ptr does not know
    /// how to delete C++ objects deriving from TfLiteDelegate.
    TfLiteDelegate* gpu_delegate = nullptr;
    TfLiteDelegate* xnnpack_delegate = nullptr;

    std::unique_ptr<TFLiteProfiler> profiler;

    std::vector<std::string> input_names;
    std::vector<std::vector<int>> input_shapes;
    std::vector<TfLiteType> input_data_precisions;

    std::vector<std::string> output_names;
    std::vector<std::vector<int>> output_shapes;
    std::vector<TfLiteType> output_data_precisions;

    void onEvaluationStart() override;
    void onEvaluationEnd() override;

    void onSingleRunStart();
    void onSingleRunEnd();

    void run(const int input_idx) override;
};
