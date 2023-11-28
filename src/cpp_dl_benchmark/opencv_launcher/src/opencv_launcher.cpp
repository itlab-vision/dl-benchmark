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

OCVLauncher::OCVLauncher(const int nthreads, const std::string& device) : Launcher(nthreads, device) {
    if (nthreads > 0) {
        cv::setNumThreads(nthreads);
    }
    this->nthreads = cv::getNumThreads();
}

std::string OCVLauncher::get_framework_name() const {
    return "OpenCV";
}

std::string OCVLauncher::get_framework_version() const {
    return std::string(CV_VERSION);
}

std::string OCVLauncher::get_backend_name() const {
#ifdef OCV_DNN
    return "default";
#elif OCV_DNN_WITH_OV
    return "OpenVINO";
#endif
}

void OCVLauncher::set_backend(cv::dnn::Net& net) {
#ifdef OCV_DNN
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
#elif OCV_DNN_WITH_OV
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_INFERENCE_ENGINE);
#endif
}

void OCVLauncher::read(const std::string& model_file, const std::string& weights_file) {
    net = cv::dnn::readNet(model_file, weights_file);
    set_backend(net);

    if (device == utils::Device::GPU) {
        net.setPreferableTarget(cv::dnn::DNN_TARGET_OPENCL);
    }
    else if (device != utils::Device::CPU) {
        throw std::runtime_error(utils::get_device_str(device) + " device is not supported!");
    }

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
    std::vector<TensorDescription> input_tensors_info{{input_names[0],
                                                       input_shapes[0],
                                                       input_shapes[0],
                                                       "",
                                                       utils::DataPrecision::FP32,
                                                       true}};  // only CV_32F type for IO supported
    std::vector<TensorDescription> output_tensors_info;
    for (size_t i = 0; i < output_names.size(); ++i) {
        output_tensors_info.push_back(
            {std::string(output_names[i]), output_shapes[i], {}, "", utils::DataPrecision::FP32, true});
    }
    return {input_tensors_info, output_tensors_info};
}

void OCVLauncher::prepare_input_tensors(std::vector<std::vector<TensorBuffer>>&& tbuffers) {
    tensor_buffers = std::move(tbuffers);
    for (int i = 0; i < tensor_buffers.size(); ++i) {
        for (int j = 0; j < tensor_buffers[i].size(); ++j) {
            blobs.push_back(cv::Mat(tensor_buffers[i][j].shape(), CV_32F, tensor_buffers[i][j].get<void>()));
        }
    }
}

std::vector<OutputTensors> OCVLauncher::get_output_tensors() {
    throw std::logic_error("Method is not implemented");
}

void OCVLauncher::run(const int input_idx) {
    net.setInput(blobs[input_idx]);

    infer_start_time = HighresClock::now();
    net.forward(output_blobs, output_names);
    latencies.push_back(utils::ns_to_ms(HighresClock::now() - infer_start_time));
}
