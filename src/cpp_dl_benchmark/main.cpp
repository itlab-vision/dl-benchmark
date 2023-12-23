#include "common_launcher/launcher.hpp"
#include "inputs_preparation/inputs_preparation.hpp"
#include "utils/args_handler.hpp"

#if defined(OCV_DNN) || defined(OCV_DNN_WITH_OV)
#include "opencv_launcher.hpp"
#elif defined(ORT_DEFAULT) || defined(ORT_CUDA) || defined(ORT_TENSORRT)
#include "onnxruntime_launcher.hpp"
#elif defined(TFLITE_WITH_DEFAULT_BACKEND) || defined(TFLITE_WITH_XNNPACK_BACKEND) || defined(TFLITE_WITH_GPU_DELEGATE)
#include "tflite_launcher.hpp"
#elif defined(PYTORCH) || defined(PYTORCH_TENSORRT)
#include "pytorch_launcher.hpp"
#endif

#include "utils/report.hpp"
#include "utils/statistics.hpp"
#include "utils/utils.hpp"

#include <gflags/gflags.h>

#include <chrono>
#include <iostream>
#include <string>
#include <vector>

namespace {
constexpr char help_msg[] = "show the help message and exit";
DEFINE_bool(h, false, help_msg);

constexpr char model_msg[] =
    "path to a file with a trained model or a config file.\n"
    "                                                      available formats\n"
    "                                                          ONNX Runtime - .onnx\n"
    "                                                          OpenCV - .xml, .onnx, .pb, .protoxt.";
DEFINE_string(m, "", model_msg);

constexpr char weights_msg[] = "path to a model weights file.\n"
                               "                          available formats:\n"
                               "                          OpenCV - .caffemodel, .bin";
DEFINE_string(w, "", weights_msg);

constexpr char input_msg[] =
    "path to an input to process. The input must be an image and/or binaries, a folder of images and/or binaries.\n"
    "                                                      ex.: \"input1:file1 input2:file2 input3:file3\" or just "
    "path "
    "to the file or folder if model has one input";
DEFINE_string(i, "", input_msg);

constexpr char device_msg[] =
    "target device to infer on. Avalaibale devices depends on the framework:\n"
    "                                                          ONNX Runtime: CPU, CUDA (CUDA EP)\n"
    "                                                          OpenCV: CPU, GPU";
DEFINE_string(d, "CPU", device_msg);

constexpr char batch_size_msg[] = "batch size value. If not provided, batch size value is determined from the model";
DEFINE_uint32(b, 0, batch_size_msg);

constexpr char shape_msg[] = "shape for network input.\n"
                             "                                                      ex., "
                             "\"input1[1,128],input2[1,128],input3[1,128]\" or just \"[1,3,224,224]\"";
DEFINE_string(shape, "", shape_msg);

constexpr char layout_msg[] =
    "layout for network input.\n"
    "                                                      ex.: \"input1[NCHW],input2[NC]\" or just \"[NCHW]\"";
DEFINE_string(layout, "", layout_msg);

constexpr char dtype_msg[] =
    "data type of network input.\n"
    "                                                      ex.: \"input1[FP32],input2[FP32]\" or just \"[FP32]\"";
DEFINE_string(dtype, "", dtype_msg);

constexpr char input_mean_msg[] =
    "mean values per channel for input image.\n"
    "                                                      applicable only for models with image input.\n"
    "                                                      ex.: [123.675,116.28,103.53] or with specifying inputs "
    "src[255,255,255]";
DEFINE_string(mean, "", input_mean_msg);

constexpr char input_scale_msg[] =
    "scale values per channel for input image.\n"
    "                                                      applicable only for models with image inputs.\n"
    "                                                      ex.: [58.395,57.12,57.375] or with specifying inputs "
    "src[255,255,255]";
DEFINE_string(scale, "", input_scale_msg);

constexpr char channel_swap_msg[] =
    "switch the input channels order from BGR to RGB.\n"
    "                                                      applicable only for models with image inputs.\n"
    "                                                      image are uploaded in BGR format by default";
DEFINE_bool(channel_swap, false, channel_swap_msg);

constexpr char threads_num_msg[] = "number of threads to utilize.";
DEFINE_uint32(nthreads, 0, threads_num_msg);

constexpr char requests_num_msg[] = "number of inference requests. If not provided, default value is set.";
DEFINE_uint32(nireq, 0, requests_num_msg);

constexpr char iterations_num_msg[] = "number of iterations. If not provided, default time limit is set.";
DEFINE_uint32(niter, 0, iterations_num_msg);

constexpr char time_msg[] = "time limit for inference in seconds";
DEFINE_uint32(t, 0, time_msg);

constexpr char save_report_msg[] = "save report in JSON format.";
DEFINE_bool(save_report, false, save_report_msg);

constexpr char report_path_msg[] = "destination path for report.";
DEFINE_string(report_path, "", report_path_msg);

constexpr char dump_output_msg[] = "save final tensor value.";
DEFINE_bool(dump_output, false, dump_output_msg);

constexpr char output_path_msg[] = "destination path for output.";
DEFINE_string(output_path, "", output_path_msg);

void parse(int argc, char* argv[]) {
    gflags::ParseCommandLineFlags(&argc, &argv, false);
    if (FLAGS_h || 1 == argc) {
        std::cout <<
#ifdef OCV_DNN
            "opencv_dnn"
#elif OCV_DNN_WITH_OV
            "opencv_dnn_ov"
#elif ORT_DEFAULT
            "onnxruntime"
#elif ORT_CUDA
            "onnxruntime_cuda"
#elif ORT_TENSORRT
            "onnxruntime_tensorrt"
#elif TFLITE_WITH_DEFAULT_BACKEND
            "tflite"
#elif TFLITE_WITH_XNNPACK_BACKEND
            "tflite_xnnpack"
#elif TFLITE_WITH_GPU_DELEGATE
            "tflite_gpu_delegate"
#elif PYTORCH
            "pytorch"
#elif PYTORCH_TENSORRT
            "pytorch_tensorrt"
#endif
                  << "_benchmark"
                  << "\nOptions:"
                  << "\n\t[-h]                                          " << help_msg
                  << "\n\t[-help]                                       print help on all arguments"
                  << "\n\t -m <MODEL FILE>                              " << model_msg
                  << "\n\t[-w <WEIGHTS FILE>]                           " << weights_msg
                  << "\n\t[-i <INPUT>]                                  " << input_msg
                  << "\n\t[-d <DEVICE>]                                 " << device_msg
                  << "\n\t[-b <NUMBER>]                                 " << batch_size_msg
                  << "\n\t[--shape <[N,C,H,W]>]                         " << shape_msg
                  << "\n\t[--layout <[NCHW]>]                           " << layout_msg
                  << "\n\t[--dtype <[FP32]>]                            " << dtype_msg
                  << "\n\t[--mean <R G B>]                              " << input_mean_msg
                  << "\n\t[--scale <R G B>]                             " << input_scale_msg
                  << "\n\t[--channel_swap]                              " << channel_swap_msg
                  << "\n\t[--nthreads <NUMBER>]                         " << threads_num_msg
                  << "\n\t[--nireq <NUMBER>]                            " << requests_num_msg
                  << "\n\t[--niter <NUMBER>]                            " << iterations_num_msg
                  << "\n\t[-t <NUMBER>]                                 " << time_msg
                  << "\n\t[--save_report]                               " << save_report_msg
                  << "\n\t[--report_path <PATH>]                        " << report_path_msg
                  << "\n\t[--dump_output]                               " << dump_output_msg
                  << "\n\t[--output_path <PATH>]                        " << output_path_msg << "\n";
        exit(0);
    }
    if (FLAGS_m.empty()) {
        throw std::invalid_argument{"-m <MODEL FILE> can't be empty"};
    }
}

void log_model_inputs_outputs(const IOTensorsInfo& tensors_info) {
    const auto& [model_inputs, model_outputs] = tensors_info;

    logger::info << "\tModel inputs:" << logger::endl;
    for (const auto& input : model_inputs) {
        logger::info << "\t\t" << input.name << ": " << utils::get_data_precision_str(input.data_precision) << " "
                     << args::shape_string(input.shape) << logger::endl;
    }
    logger::info << "\tModel outputs:" << logger::endl;
    for (const auto& output : model_outputs) {
        logger::info << "\t\t" << output.name << ": " << utils::get_data_precision_str(output.data_precision) << " "
                     << args::shape_string(output.shape) << logger::endl;
    }
}

void log_step(const std::string optional_info = "") {
    static size_t step_id = 0;
    static const std::map<size_t, std::string> steps = {{1, "Parsing and validating input arguments"},
                                                        {2, "Loading"},
                                                        {3, "Reading model files"},
                                                        {4, "Configuring input of the model"},
                                                        {5, "Setting execution parameters"},
                                                        {6, "Creating input tensors"},
                                                        {7, "Measuring model performance"},
                                                        {8, "Saving statistics report"}};

    step_id++;
    if (steps.count(step_id) == 0) {
        throw std::invalid_argument("Invalid number of step " + std::to_string(step_id) +
                                    " was provided, number of the step should be less than " +
                                    std::to_string(steps.size()));
    }

    std::cout << "[Step " << step_id << "/" << steps.size() << "] " << steps.at(step_id)
              << (optional_info.empty() ? "" : " (" + optional_info + ")") << std::endl;
}
}  // namespace

int main(int argc, char* argv[]) {
    std::shared_ptr<Report> report;
    try {
        log_step();  // Parsing and validating input arguments
        logger::info << "Parsing input arguments" << logger::endl;
        parse(argc, argv);

        std::unique_ptr<Launcher> launcher;

        std::string device = FLAGS_d;
        if (device.empty()) {
#if defined(OCV_DNN) || defined(OCV_DNN_WITH_OV) || defined(ORT_DEFAULT)
            device = "CPU";
#elif defined(ORT_CUDA) || defined(ORT_TENSORRT)
            device = "NVIDIA_GPU";
#endif
            logger::info << "Device wasn't specified. Default will be used: " << device << logger::endl;
        }

#if defined(OCV_DNN) || defined(OCV_DNN_WITH_OV)
        launcher = std::make_unique<OCVLauncher>(FLAGS_nthreads, device);
#elif defined(ORT_DEFAULT) || defined(ORT_CUDA) || defined(ORT_TENSORRT)
        launcher = std::make_unique<ONNXLauncher>(FLAGS_nthreads, device);
#elif defined(TFLITE_WITH_DEFAULT_BACKEND) || defined(TFLITE_WITH_XNNPACK_BACKEND) || defined(TFLITE_WITH_GPU_DELEGATE)
        launcher = std::make_unique<TFLiteLauncher>(FLAGS_nthreads, device);
#elif defined(PYTORCH) || defined(PYTORCH_TENSORRT)
        launcher = std::make_unique<PytorchLauncher>(FLAGS_nthreads, device);
#endif

        if (FLAGS_save_report) {
            report = std::make_shared<Report>(FLAGS_report_path);
            report->add_record(Report::Category::FRAMEWORK_INFO, {{"name", launcher->get_framework_name()}});
            report->add_record(Report::Category::FRAMEWORK_INFO, {{"version", launcher->get_framework_version()}});
            report->add_record(Report::Category::FRAMEWORK_INFO, {{"device", device}});
            report->add_record(Report::Category::FRAMEWORK_INFO, {{"backend", launcher->get_backend_name()}});
        }

        logger::info << "Checking input files" << logger::endl;
        std::vector<gflags::CommandLineFlagInfo> flags;
        gflags::GetAllFlags(&flags);
        if (FLAGS_save_report) {
            for (auto& flag : flags) {
                if (!flag.is_default) {
                    report->add_record(Report::Category::CMD_OPTIONS, {{flag.name, flag.current_value}});
                }
            }
        }
        auto input_files = args::parse_input_files_arguments(gflags::GetArgvs());

        log_step();  // Loading framework
        logger::info << launcher->get_framework_name() << " " << launcher->get_framework_version() << logger::endl;
        logger::info << "\tEnabled backend: " << launcher->get_backend_name() << logger::endl;

        log_step();  // Reading model files
        logger::info << "Reading model " << FLAGS_m << logger::endl;
        auto start_time = HighresClock::now();
        launcher->read(FLAGS_m, FLAGS_w);
        auto read_model_time = utils::ns_to_ms(HighresClock::now() - start_time);
        logger::info << "Read model took " << utils::format_double(read_model_time) << " ms" << logger::endl;

        logger::info << "Model inputs/outputs info:" << logger::endl;
        launcher->fill_inputs_outputs_info();
        auto io_tensors_info = launcher->get_io_tensors_info();
        log_model_inputs_outputs(io_tensors_info);

        logger::info << "Device: " << device << logger::endl;
        logger::info << "\tThreads number: "
                     << (launcher->get_threads_num() ? std::to_string(launcher->get_threads_num()) : "DEFAULT")
                     << logger::endl;

        log_step();  // Configuring input of the model
        auto inputs_info = inputs::get_inputs_info(io_tensors_info.first,
                                                   input_files,
                                                   FLAGS_layout,
                                                   FLAGS_shape,
                                                   FLAGS_mean,
                                                   FLAGS_scale,
                                                   FLAGS_dtype,
                                                   FLAGS_channel_swap);

        // determine batch size
        int batch_size = inputs::get_batch_size(inputs_info);
        bool is_dynamic_batch = std::any_of(inputs_info.begin(), inputs_info.end(), [](const auto& pair) {
            const auto& [name, input_descr] = pair;
            return input_descr.tensor_descr.is_dynamic_batch();
        });
        if (FLAGS_b > 0 && is_dynamic_batch) {
            if (!FLAGS_shape.empty() && batch_size != -1) {
                logger::warn << "Batch size provided with -b option will be used." << logger::endl;
            }
            batch_size = FLAGS_b;
        }
        else if (is_dynamic_batch && batch_size == -1) {
            throw std::logic_error("Model has dynamic batch size, but -b option wasn't provided.");
        }
        else if (FLAGS_b > 0) {
            throw std::logic_error("Can't set batch for model with static batch dimension.");
        }

        // setting batch
        inputs::set_batch_size(inputs_info, batch_size);
        logger::info << "Set batch to " << batch_size << logger::endl;

        log_step();  // Setting execution parameters
        // number of inference requests
        int num_requests = FLAGS_nireq;
        if (FLAGS_nireq == 0) {
            num_requests = 1;
        }

        // set and align iterations limit
        int64_t num_iterations = FLAGS_niter;
        if (num_iterations > 0) {
            num_iterations = ((num_iterations + num_requests - 1) / num_requests) * num_requests;
            if (FLAGS_niter != num_iterations) {
                logger::warn << "Provided number of iterations " << FLAGS_niter << " was changed to " << num_iterations
                             << " to be aligned with number of inference requests " << num_requests << logger::endl;
            }
        }
        // set time limit
        uint32_t time_limit_sec = 0;
        if (FLAGS_t != 0) {
            time_limit_sec = FLAGS_t;
        }
        else if (FLAGS_niter == 0) {
            time_limit_sec = 60;
            logger::info << "Default time limit is set: " << time_limit_sec << " seconds " << logger::endl;
        }
        uint64_t time_limit_ns = utils::sec_to_ns(time_limit_sec);
        if (report) {
            report->add_record(
                Report::Category::CONFIGURATION_SETUP,
                {{"batch_size", std::to_string(batch_size)},
                 {"duration", std::to_string(utils::sec_to_ms(time_limit_sec))},
                 {"iterations_num", std::to_string(num_iterations)},
                 {"tensors_num", std::to_string(num_requests)},
                 {"target_device", device},
                 {"threads_num", std::to_string(launcher->get_threads_num())},
                 {"precision",
                  io_tensors_info.first.empty() ? "UNKNOWN"
                                                : get_data_precision_str(io_tensors_info.first[0].data_precision)}});
        }

        log_step();  // Creating input tensors
        auto tensors_buffers = inputs::get_input_tensors(inputs_info, batch_size, num_requests);
        launcher->prepare_input_tensors(std::move(tensors_buffers));
        launcher->compile();

        log_step(std::to_string(num_requests) + " inference requests, limits: " +
                 (num_iterations > 0
                      ? std::to_string(num_iterations) + " iterations"
                      : std::to_string(utils::sec_to_ms(time_limit_sec)) + " ms"));  // Measuring model performance

        if (FLAGS_dump_output) {
            std::vector<OutputTensors> output = launcher->get_output_tensors();
            FLAGS_output_path.empty() ? launcher->dump_output(output)
                                      : launcher->dump_output(output, FLAGS_output_path);
        }

        // warm up before benhcmarking
        launcher->warmup_inference();
        auto first_inference_time = launcher->get_latencies()[0];
        logger::info << "Warming up inference took " << utils::format_double(first_inference_time) << " ms"
                     << logger::endl;
        launcher->reset_timers();

        int iterations_num = launcher->evaluate(num_iterations, time_limit_ns);

        log_step();  // Saving statistics report
        double total_time = launcher->get_total_time_ms();
        Metrics metrics(launcher->get_latencies(), batch_size);
        // Performance metrics report
        logger::info << "Count: " << iterations_num << " iterations" << logger::endl;
        logger::info << "Duration: " << utils::format_double(total_time) << " ms" << logger::endl;
        logger::info << "Latency:" << logger::endl;
        logger::info << "\tMedian   " << utils::format_double(metrics.latency.median) << " ms" << logger::endl;
        logger::info << "\tAverage: " << utils::format_double(metrics.latency.avg) << " ms" << logger::endl;
        logger::info << "\tStd:     " << utils::format_double(metrics.latency.std) << " ms" << logger::endl;
        logger::info << "\tMin:     " << utils::format_double(metrics.latency.min) << " ms" << logger::endl;
        logger::info << "\tMax:     " << utils::format_double(metrics.latency.max) << " ms" << logger::endl;
        logger::info << "Throughput: " << utils::format_double(metrics.fps) << " FPS" << logger::endl;

        if (report) {
            report->add_record(Report::Category::EXECUTION_RESULTS,
                               {{"execution_time", utils::format_double(total_time)},
                                {"first_inference_time", utils::format_double(first_inference_time)},
                                {"iterations_num", std::to_string(iterations_num)},
                                {"latency_avg", utils::format_double(metrics.latency.avg)},
                                {"latency_std", utils::format_double(metrics.latency.std)},
                                {"latency_max", utils::format_double(metrics.latency.max)},
                                {"latency_median", utils::format_double(metrics.latency.median)},
                                {"latency_min", utils::format_double(metrics.latency.min)},
                                {"read_network_time", utils::format_double(read_model_time)},
                                {"throughput", utils::format_double(metrics.fps)}});
            report->save();
        }
    } catch (const std::exception& ex) {
        logger::err << ex.what() << logger::endl;
        if (report) {
            report->add_record(Report::Category::EXECUTION_RESULTS, {{"error", ex.what()}});
            report->save();
        }
        return 3;
    }
    return 0;
}
