#include "tflite_profiler.hpp"

#include <tensorflow/lite/interpreter.h>
#include <tensorflow/lite/profiling/buffered_profiler.h>
#include <tensorflow/lite/profiling/profile_summarizer.h>
#include <tensorflow/lite/profiling/profile_summary_formatter.h>
#include <tensorflow/lite/tools/benchmark/benchmark_model.h>
#include <tensorflow/lite/tools/logging.h>

#include <fstream>
#include <memory>
#include <string>

std::shared_ptr<tflite::profiling::ProfileSummaryFormatter> createProfileSummaryFormatter(bool format_as_csv) {
    return format_as_csv ? std::make_shared<tflite::profiling::ProfileSummaryCSVFormatter>()
                         : std::make_shared<tflite::profiling::ProfileSummaryDefaultFormatter>();
}

TFLiteProfiler::TFLiteProfiler(tflite::Interpreter* interpreter, const std::string& csv_file_path)
    : interpreter(interpreter), run_summarizer(createProfileSummaryFormatter(!csv_file_path.empty())),
      init_summarizer(createProfileSummaryFormatter(!csv_file_path.empty())),
      profiler(max_num_initial_entries, allow_dynamic_profiling_buffer_increase), csv_file_path(csv_file_path) {
    interpreter->SetProfiler(&profiler);
    // Start profile to catch events on preparation stage:
    // TFLite interpreter initialization and model graph preparation.
    profiler.Reset();
    profiler.StartProfiling();
}

void TFLiteProfiler::reset() {
    // Gather preparation stage statistics
    profiler.StopProfiling();
    auto profile_events = profiler.GetProfileEvents();
    init_summarizer.ProcessProfiles(profile_events, *interpreter);
    profiler.Reset();
}

void TFLiteProfiler::start() {
    profiler.Reset();
    profiler.StartProfiling();
}

void TFLiteProfiler::stop() {
    profiler.StopProfiling();
    auto profile_events = profiler.GetProfileEvents();
    run_summarizer.ProcessProfiles(profile_events, *interpreter);
}

void TFLiteProfiler::dump_output() {
    std::ofstream output_file(csv_file_path);
    std::ostream* output_stream = nullptr;
    if (output_file.good()) {
        output_stream = &output_file;
    }
    if (init_summarizer.HasProfiles()) {
        write_output("Profiling Info for Benchmark Initialization:",
                     init_summarizer.GetOutputString(),
                     output_stream == nullptr ? &TFLITE_LOG(INFO) : output_stream);
    }
    if (run_summarizer.HasProfiles()) {
        write_output("Operator-wise Profiling Info for Regular Benchmark Runs:",
                     run_summarizer.GetOutputString(),
                     output_stream == nullptr ? &TFLITE_LOG(INFO) : output_stream);
    }
}

void TFLiteProfiler::write_output(const std::string& header, const std::string& data, std::ostream* stream) {
    (*stream) << header << std::endl;
    (*stream) << data << std::endl;
}
