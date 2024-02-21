// Implementation is inspired by:
// https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/tools/benchmark/profiling_listener.h

#pragma once

#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/profiling/buffered_profiler.h>
#include <tensorflow/lite/profiling/profile_summarizer.h>
#include <tensorflow/lite/profiling/profile_summary_formatter.h>
#include <tensorflow/lite/tools/benchmark/benchmark_model.h>

#include <memory>
#include <string>

// Dumps profiling events if profiling is enabled.
class TFLiteProfiler final {
public:
    constexpr static uint32_t max_num_initial_entries = 1024;
    constexpr static bool allow_dynamic_profiling_buffer_increase = true;

    TFLiteProfiler(tflite::Interpreter* interpreter, const std::string& out_csv_path = "");

    void reset();

    void start();
    void stop();

    void dump_output();

private:
    tflite::Interpreter* interpreter;
    tflite::profiling::ProfileSummarizer run_summarizer;
    tflite::profiling::ProfileSummarizer init_summarizer;
    tflite::profiling::BufferedProfiler profiler;

    std::string csv_file_path;

    void write_output(const std::string& header, const std::string& data, std::ostream* stream);
};
