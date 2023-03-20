#include "opencv_launcher.hpp"

#include "common_launcher/launcher.hpp"
#include "inputs_preparation/inputs_preparation.hpp"
#include "utils/args_handler.hpp"
#include "utils/logger.hpp"
#include "utils/utils.hpp"

#include <opencv2/core/mat.hpp>
#include <opencv2/dnn.hpp>

#include <algorithm>
#include <chrono>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

using MatShape = cv::dnn::CV__DNN_INLINE_NS::MatShape;

OCVLauncher::OCVLauncher(int nthreads) : Launcher(nthreads) {
    cv::setNumThreads(nthreads);
}

void OCVLauncher::log_framework_version() const {
    logger::info << "OpenCV version: " << CV_VERSION << logger::endl;
}

void OCVLauncher::read(const std::string model_file, const std::string weights_file) {
    net = cv::dnn::readNet(model_file, weights_file);
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);

    std::vector<MatShape> inputShapes, outputShapes;
    net.getLayerShapes(MatShape(), 0, inputShapes, outputShapes);
    if (inputShapes.size() > 1) {
        throw std::runtime_error("Only models with 1 input supported.");
    }
}

void OCVLauncher::fill_inputs_outputs_info() {
    input_names.push_back(net.getLayer(0)->name);
    try {
        std::vector<MatShape> input_layer_shapes, output_layer_shapes;
        net.getLayerShapes(MatShape(), 0, input_layer_shapes, output_layer_shapes);
        if (!input_layer_shapes.empty() && !input_layer_shapes[0].empty()) {
            input_shapes = input_layer_shapes;
        }
        else {
            input_shapes.push_back({-1, -1, -1, -1});  // dummy input shape to enable providing shape from cmd
        }
    } catch (const cv::Exception& ex) {
        input_shapes.push_back({-1, -1, -1, -1});
    }

    output_names = net.getUnconnectedOutLayersNames();
    for (const auto& name : output_names) {
        std::vector<MatShape> input_layer_shapes, output_layer_shapes;
        try {
            net.getLayerShapes(MatShape(), net.getLayerId(name), input_layer_shapes, output_layer_shapes);
        } catch (const cv::Exception& ex) {}
        if (!output_layer_shapes.empty()) {
            output_shapes.push_back(output_layer_shapes[0]);
        }
        else {
            output_shapes.push_back({});
        }
    }
}

IOTensorsInfo OCVLauncher::get_io_tensors_info() const {
    std::vector<TensorDescr> input_tensors_info{{input_names[0],
                                                 input_shapes[0],
                                                 input_shapes[0],
                                                 "",
                                                 utils::DataPrecision::FP32,
                                                 true}};  // only CV_32F type for IO supported
    std::vector<TensorDescr> output_tensors_info;
    for (size_t i = 0; i < output_names.size(); ++i) {
        output_tensors_info.push_back(
            {std::string(output_names[i]), output_shapes[i], {}, "", utils::DataPrecision::FP32, true});
    }
    return {input_tensors_info, output_tensors_info};
}

void OCVLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>> tbuffers) {
    tensor_buffers = std::move(tbuffers);
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            blobs.push_back(cv::Mat(tensor_buffers[i][j].shape(), CV_32F, tensor_buffers[i][j].get<void>()));
        }
    }
}

void OCVLauncher::warmup_inference() {
    run(blobs[0]);
}

void OCVLauncher::run(const cv::Mat& input_blob) {
    net.setInput(input_blob);
    total_start_time = std::min(HighresClock::now(), total_start_time);

    infer_start_time = HighresClock::now();
    net.forward(output_blobs, output_names);
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));

    total_end_time = std::max(HighresClock::now(), total_end_time);
}

int OCVLauncher::evaluate(int iterations_num, uint64_t time_limit_ns) {
    int iteration = 0;
    auto start_time = HighresClock::now();
    auto uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    while ((iterations_num != 0 && iteration < iterations_num) ||
           (time_limit_ns != 0 && static_cast<uint64_t>(uptime) < time_limit_ns)) {
        run(blobs[iteration % blobs.size()]);
        ++iteration;
        uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    }

    return iteration;
}
