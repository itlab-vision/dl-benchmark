// Copyright (C) 2023 KNS Group LLC (YADRO
// SPDX-License-Identifier: Apache-2.0
//

#include "inputs_preparation.hpp"

#include "args_handler.hpp"
#include "buffer.hpp"
#include "logger.hpp"
#include "utils.hpp"

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <onnxruntime_cxx_api.h>

#include <fstream>
#include <limits>
#include <map>
#include <numeric>
#include <random>
#include <string>
#include <vector>

template <typename T>
using UniformDistribution = typename std::conditional<
    std::is_floating_point<T>::value,
    std::uniform_real_distribution<T>,
    typename std::conditional<std::is_integral<T>::value, std::uniform_int_distribution<T>, void>::type>::type;

cv::Mat read_image(const std::string &img_path, size_t height, size_t width) {
    auto img = cv::imread(img_path);
    cv::resize(img, img, cv::Size(width, height));
    return img;
}

template <typename T>
const T get_mat_value(const cv::Mat &mat, size_t h, size_t w, size_t c) {
    switch (mat.type()) {
        case CV_8UC1:
            return static_cast<T>(mat.at<uchar>(h, w));
        case CV_8UC3:
            return static_cast<T>(mat.at<cv::Vec3b>(h, w)[c]);
        case CV_32FC1:
            return static_cast<T>(mat.at<float>(h, w));
        case CV_32FC3:
            return static_cast<T>(mat.at<cv::Vec3f>(h, w)[c]);
    }
    throw std::runtime_error("cv::Mat type is not recognized");
};

template <class T, class T2>
Buffer create_random_tensor(const inputs::InputDescr &input_descr,
                                T rand_min = std::numeric_limits<uint8_t>::min(),
                                T rand_max = std::numeric_limits<uint8_t>::max()) {
    logger::info << "\t\tRandomly generated data" << logger::endl;
    auto tensor_descr = input_descr.tensor_descr;

    // auto allocator = Ort::AllocatorWithDefaultOptions();
    // auto tensor = Ort::Value::CreateTensor(allocator,
    //                                        tensor_descr.data_shape.data(),
    //                                        tensor_descr.data_shape.size(),
    //                                        tensor_descr.type);
    // auto *tensor_data = tensor.GetTensorMutableData<T>();
    // size_t tensor_size = tensor.GetTensorTypeAndShapeInfo().GetElementCount();

    int64_t tensor_size =
            std::accumulate(tensor_descr.data_shape.begin(), tensor_descr.data_shape.end(), 1, std::multiplies<int64_t>());
    Buffer buff;
    buff.data_shape = tensor_descr.data_shape;

    buff.allocate(tensor_size, tensor_descr.data_type);
    auto *tensor_data = buff.get<T>();

    std::mt19937 gen(0);
    UniformDistribution<T2> distribution(rand_min, rand_max);
    for (size_t i = 0; i < tensor_size; ++i) {
        tensor_data[i] = static_cast<T>(distribution(gen));
    }
    return buff;
}

template <class T>
Buffer create_tensor_from_image(const inputs::InputDescr &input_descr, int batch_size, int start_index) {
    auto tensor_descr = input_descr.tensor_descr;
    const auto &files = input_descr.files;

    // auto allocator = Ort::AllocatorWithDefaultOptions();
    // auto tensor = Ort::Value::CreateTensor(allocator,
    //                                        tensor_descr.data_shape.data(),
    //                                        tensor_descr.data_shape.size(),
    //                                        tensor_descr.type);
    // auto *tensor_data = tensor.GetTensorMutableData<T>();

    int64_t tensor_size =
            std::accumulate(tensor_descr.data_shape.begin(), tensor_descr.data_shape.end(), 1, std::multiplies<int64_t>());
    Buffer buff;
    buff.data_shape = tensor_descr.data_shape;

    buff.allocate(tensor_size, tensor_descr.data_type);
    auto *tensor_data = buff.get<T>();

    size_t channels = tensor_descr.channels();
    size_t width = tensor_descr.width();
    size_t height = tensor_descr.height();

    for (int b = 0; b < batch_size; ++b) {
        const auto &file_path = files[(start_index + b) % files.size()];
        logger::info << "\t\t" << file_path << logger::endl;
        cv::Mat img = read_image(file_path, height, width);
        for (size_t w = 0; w < width; ++w) {
            for (size_t h = 0; h < height; ++h) {
                for (size_t ch = 0; ch < channels; ++ch) {
                    size_t offset = b * channels * width * height + (ch * width * height + h * width + w);
                    tensor_data[offset] = (get_mat_value<T>(img, h, w, ch) - static_cast<T>(input_descr.mean[ch])) /
                                          static_cast<T>(input_descr.scale[ch]);
                }
            }
        }
    }
    return buff;
}

template <class T>
Buffer create_image_info_tensor(const inputs::InputDescr &input_descr, const cv::Size &image_size, int batch_size) {
    auto tensor_descr = input_descr.tensor_descr;
    // auto allocator = Ort::AllocatorWithDefaultOptions();
    // auto tensor = Ort::Value::CreateTensor(allocator,
    //                                        tensor_descr.data_shape.data(),
    //                                        tensor_descr.data_shape.size(),
    //                                        tensor_descr.type);

    // size_t tensor_size = tensor.GetTensorTypeAndShapeInfo().GetElementCount();
    // auto *tensor_data = tensor.GetTensorMutableData<T>();
    int64_t tensor_size =
            std::accumulate(tensor_descr.data_shape.begin(), tensor_descr.data_shape.end(), 1, std::multiplies<int64_t>());
    Buffer buff;
    buff.allocate(tensor_size, tensor_descr.data_type);
    buff.data_shape = tensor_descr.data_shape;
    auto *tensor_data = buff.get<T>();

    logger::info << "\t\t" << image_size.width << "x" << image_size.height << logger::endl;
    for (int b = 0; b < batch_size; ++b) {
        int image_info_size = tensor_size / batch_size;
        for (int i = 0; i < image_info_size; ++i) {
            int id = b * image_info_size + i;
            if (0 == i) {
                tensor_data[id] = static_cast<T>(image_size.width);
            }
            else if (1 == i) {
                tensor_data[id] = static_cast<T>(image_size.height);
            }
            else {
                tensor_data[id] = 1;
            }
        }
    }
    return buff;
}

template <class T>
Buffer create_tensor_from_binary(const inputs::InputDescr &input_descr, int batch_size, int start_index) {
    auto tensor_descr = input_descr.tensor_descr;
    const auto &files = input_descr.files;

    int64_t tensor_size =
            std::accumulate(tensor_descr.data_shape.begin(), tensor_descr.data_shape.end(), 1, std::multiplies<int64_t>());
    Buffer buff;

    buff.allocate(tensor_size, tensor_descr.data_type);
    auto *tensor_data = buff.get<char>();

    // auto allocator = Ort::AllocatorWithDefaultOptions();
    // auto tensor = Ort::Value::CreateTensor(allocator,
    //                                        tensor_descr.data_shape.data(),
    //                                        tensor_descr.data_shape.size(),
    //                                        tensor_descr.type);

    // size_t tensor_size = tensor.GetTensorTypeAndShapeInfo().GetElementCount();
    // auto *tensor_data = tensor.GetTensorMutableData<char>();
    for (int b = 0; b < batch_size; ++b) {
        size_t input_id = (start_index + b) % files.size();
        const auto &file_path = files[input_id];
        logger::info << "\t\t" << file_path << logger::endl;

        std::ifstream binary_file(file_path, std::ios_base::binary | std::ios_base::ate);
        if (!binary_file) {
            throw std::runtime_error("Can't open " + file_path);
        }

        auto file_size = static_cast<std::size_t>(binary_file.tellg());
        auto input_size = tensor_size * sizeof(T) / batch_size;
        if (file_size != input_size) {
            throw std::invalid_argument("File " + file_path + " contains " + std::to_string(file_size) +
                                        " bytes but the model expects " + std::to_string(input_size));
        }

        binary_file.seekg(0, std::ios_base::beg);
        if (!binary_file.good()) {
            throw std::runtime_error("Can't read " + file_path);
        }

        if (tensor_descr.layout != "CN") {
            binary_file.read(&tensor_data[b * input_size], input_size);
        }
        else {
            for (int i = 0; i < tensor_descr.channels(); ++i) {
                binary_file.read(&tensor_data[(i * batch_size + b) * sizeof(T)], sizeof(T));
            }
        }
    }

    return buff;
}

Buffer get_tensor_from_image(const inputs::InputDescr &input_descr, int batch_size, int start_index) {
    auto precision = input_descr.tensor_descr.data_type;
    if (precision == utils::DataPrecision::FP32) {
        return create_tensor_from_image<float>(input_descr, batch_size, start_index);
    }
    else if (precision == utils::DataPrecision::I32) {
        return create_tensor_from_image<int32_t>(input_descr, batch_size, start_index);
    }
    else if (precision == utils::DataPrecision::I64) {
        return create_tensor_from_image<int64_t>(input_descr, batch_size, start_index);
    }

    throw std::invalid_argument("Unsupported tensor precision: " + utils::get_precision_str(precision));
}

Buffer get_image_info_tensor(const inputs::InputDescr &input_descr, const cv::Size &image_size, int batch_size) {
    auto precision = input_descr.tensor_descr.data_type;
    if (precision == utils::DataPrecision::FP16) {
        return create_image_info_tensor<short>(input_descr, image_size, batch_size);
    }
    if (precision == utils::DataPrecision::FP32) {
        return create_image_info_tensor<float>(input_descr, image_size, batch_size);
    }
    else if (precision == utils::DataPrecision::I32) {
        return create_image_info_tensor<int32_t>(input_descr, image_size, batch_size);
    }
    else if (precision == utils::DataPrecision::I64) {
        return create_image_info_tensor<int64_t>(input_descr, image_size, batch_size);
    }

    throw std::invalid_argument("Unsupported tensor precision: " + utils::get_precision_str(precision));
}

Buffer get_tensor_from_binary(const inputs::InputDescr &input_descr, int batch_size, int start_index) {
    auto precision = input_descr.tensor_descr.data_type;
    if (precision == utils::DataPrecision::FP16) {
        return create_tensor_from_binary<short>(input_descr, batch_size, start_index);
    }
    if (precision == utils::DataPrecision::FP32) {
        return create_tensor_from_binary<float>(input_descr, batch_size, start_index);
    }
    else if (precision == utils::DataPrecision::I32) {
        return create_tensor_from_binary<int32_t>(input_descr, batch_size, start_index);
    }
    else if (precision == utils::DataPrecision::I64) {
        return create_tensor_from_binary<int64_t>(input_descr, batch_size, start_index);
    }
    else if (precision == utils::DataPrecision::U8 || precision == utils::DataPrecision::BOOL) {
        return create_tensor_from_binary<uint8_t>(input_descr, batch_size, start_index);
    }

    throw std::invalid_argument("Unsupported tensor precision: " + utils::get_precision_str(precision));
}

Buffer get_random_tensor(const inputs::InputDescr &input_descr) {
    auto precision = input_descr.tensor_descr.data_type;
    if (precision == utils::DataPrecision::FP16) {
        return create_random_tensor<short, short>(input_descr);
    }
    if (precision == utils::DataPrecision::FP32) {
        return create_random_tensor<float, float>(input_descr);
    }
    else if (precision == utils::DataPrecision::I32) {
        return create_random_tensor<int32_t, int32_t>(input_descr);
    }
    else if (precision == utils::DataPrecision::I64) {
        return create_random_tensor<int64_t, int64_t>(input_descr);
    }
    else if (precision == utils::DataPrecision::I8) {
        return create_random_tensor<int8_t, int32_t>(input_descr);
    }
    else if (precision == utils::DataPrecision::U8) {
        return create_random_tensor<uint8_t, uint32_t>(input_descr);
    }
    else if (precision == utils::DataPrecision::BOOL) {
        return create_random_tensor<uint8_t, uint32_t>(input_descr, 0, 1);
    }
    throw std::invalid_argument("Unsupported tensor precision: " + utils::get_precision_str(precision));
}

std::vector<std::vector<Buffer>> inputs::get_input_tensors(const inputs::InputsInfo &inputs_info,
                                                               int batch_size,
                                                               int tensors_num) {
    std::vector<cv::Size> img_input_sizes;
    for (const auto &[name, input_descr] : inputs_info) {
        const auto &tensor_descr = input_descr.tensor_descr;
        if (tensor_descr.is_image()) {
            img_input_sizes.emplace_back(static_cast<int>(tensor_descr.width()),
                                         static_cast<int>(tensor_descr.height()));
        }
    }

    std::vector<std::vector<Buffer>> tensors(tensors_num);
    int start_file_index = 0;
    for (int i = 0; i < tensors_num; ++i) {
        logger::info << "Input config " << i << logger::endl;
        for (const auto &[name, input_descr] : inputs_info) {
            const auto &tensor_descr = input_descr.tensor_descr;
            logger::info << " \t" << name << " (" << tensor_descr.layout << " "
                         << utils::get_precision_str(tensor_descr.data_type) << " "
                         << args::shape_string(tensor_descr.data_shape) << ")" << logger::endl;

            if (!input_descr.files.empty() && static_cast<int>(input_descr.files.size()) < batch_size) {
                logger::warn << "\tNumber of input files is less than batch size. Some files will be duplicated."
                             << logger::endl;
            }

            if (tensor_descr.is_image_info() && img_input_sizes.size() == 1) {
                if (!input_descr.files.empty()) {
                    logger::warn << "\tFiles for image info type will be ignored." << logger::endl;
                }
                tensors[i].push_back(get_image_info_tensor(input_descr, img_input_sizes[0], batch_size));
            }
            else if (input_descr.files.empty()) {
                tensors[i].push_back(get_random_tensor(input_descr));
            }
            else if (tensor_descr.is_image()) {
                tensors[i].push_back(get_tensor_from_image(input_descr, batch_size, start_file_index));
            }
            else {
                tensors[i].push_back(get_tensor_from_binary(input_descr, batch_size, start_file_index));
            }
        }
        start_file_index += batch_size;
    }
    return tensors;
}

inputs::InputsInfo inputs::get_inputs_info(const std::map<std::string, std::vector<std::string>> &input_files,
                                           const std::vector<TensorDescr> &model_inputs,
                                           const std::string &layout_string,
                                           const std::string &shape_string,
                                           const std::string &mean_string,
                                           const std::string &scale_string) {
    // parse input layouts and input shapes
    std::map<std::string, std::string> input_layouts = args::parse_shape_layout_string(layout_string);
    std::map<std::string, std::vector<int64_t>> input_shapes;
    for (const auto &[input_name, shape] : args::parse_shape_layout_string(shape_string)) {
        input_shapes.emplace(input_name, args::string_to_vec<long>(shape, ','));
    }

    // parse mean and check
    std::map<std::string, std::vector<float>> means = args::parse_mean_scale_string(mean_string);
    for (const auto &[input_name, input_mean] : means) {
        if (input_mean.size() > 4) {
            throw std::logic_error("Mean must have one value per channel (up to 4 channels supposed), but given: " +
                                   mean_string);
        }
    }

    // parse scale and check
    std::map<std::string, std::vector<float>> scales = args::parse_mean_scale_string(scale_string);
    for (const auto &[input_name, input_scale] : scales) {
        if (input_scale.size() > 4) {
            throw std::logic_error("Scale must have one value per channel (up to 4 channels supposed), but given: " +
                                   mean_string);
        }
    }

    // Check dynamic inputs
    bool is_dynamic_input = std::any_of(model_inputs.begin(), model_inputs.end(), [](const auto &tensor_descr) {
        return tensor_descr.is_dynamic();
    });

    if (is_dynamic_input && input_shapes.empty()) {
        throw std::logic_error("Shapes must be specified explicitly for models with dynamic input shapes.");
    }

    inputs::InputsInfo inputs_info;
    for (const auto &input : model_inputs) {
        inputs::InputDescr input_descr;
        input_descr.tensor_descr = input;
        auto &tensor_descr = input_descr.tensor_descr;

        std::string name = input.name;
        if (input_files.count(name) > 0) {
            input_descr.files = input_files.at(name);
        }
        else if (input_files.count("") > 0 && input_files.size() == 1) { // case with 1 input without specifying name
            input_descr.files = input_files.at("");
        }
        else if (input_files.size() > 1) {
            throw std::invalid_argument("Input name " + name + " not found in the names provided with -i argument.");
        }

        auto &data_shape = tensor_descr.data_shape;
        if (!input_shapes.empty() && is_dynamic_input) {
            if (input_shapes.count(name) > 0) {
                data_shape = input_shapes.at(name);
            }
            else if (input_shapes.count("") > 0 && input_shapes.size() == 1) { // handle case without specifying name
                data_shape = input_shapes.at("");
            }
            else if (input_shapes.size() > 1) {
                throw std::invalid_argument("Input name " + name +
                                            " not found in the names provided with -shape argument.");
            }
        }
        else if (!input_shapes.empty()) {
            logger::warn << "Model inputs are static, -shape option will be ignored!" << logger::endl;
        }

        auto &layout = tensor_descr.layout;
        if (!input_layouts.empty()) {
            if (input_layouts.count(name) > 0) {
                layout = input_layouts.at(name);
            }
            else if (input_layouts.count("") > 0 && input_layouts.size() == 1) {
                layout = input_layouts.at("");
            }
            else if (input_layouts.size() > 1) {
                throw std::invalid_argument("Input name " + name +
                                            " not found in the names provided with -layout argument.");
            }
        }
        else {
            logger::warn << "Layout for input \"" << name
                         << "\" will be detected automatically, as it wasn't provided explicitly." << logger::endl;
            input_descr.tensor_descr.layout = utils::guess_layout_from_shape(input_descr.tensor_descr.data_shape);
        }

        if (!means.empty()) {
            std::vector<float> mean;
            if (means.count(name) > 0) {
                mean = means.at(name);
            }
            else if (means.count("") > 0 && means.size() == 1) {
                mean = means.at("");
            }
            else if (means.size() > 1) {
                throw std::invalid_argument("Input name " + name +
                                            " not found in the names provided with -mean argument.");
            }
            if (!mean.empty()) {
                if (mean.size() != static_cast<size_t>(tensor_descr.channels())) {
                    throw std::logic_error("Number of mean values (" + std::to_string(mean.size()) +
                                           ") must be equal to the number of model's input channels (" +
                                           std::to_string(tensor_descr.channels()) + ")");
                }
                input_descr.mean = mean;
            }
        }

        if (!scales.empty()) {
            std::vector<float> scale;
            if (scales.count(name) > 0) {
                scale = scales.at(name);
            }
            else if (scales.count("") > 0 && scales.size() == 1) {
                scale = scales.at("");
            }
            else if (scales.size() > 1) {
                throw std::invalid_argument("Input name " + name +
                                            " not found in the names provided with -scales argument.");
            }

            if (!scale.empty()) {
                if (scale.size() != static_cast<size_t>(tensor_descr.channels())) {
                    throw std::logic_error("Number of scale values (" + std::to_string(scale.size()) +
                                           ") must be equal to the number of model's input channels (" +
                                           std::to_string(tensor_descr.channels()) + ")");
                }
                input_descr.scale = scale;
            }
        }

        inputs_info.emplace(name, input_descr);
    }

    return inputs_info;
}

void inputs::set_batch_size(inputs::InputsInfo &inputs_info, int batch_size) {
    for (auto &[_, input_descr] : inputs_info) {
        input_descr.tensor_descr.set_batch(batch_size);
    }
}

int inputs::get_batch_size(const inputs::InputsInfo &inputs_info) {
    int batch_size = 0;
    for (auto &[name, info] : inputs_info) {
        auto &tensor_descr = info.tensor_descr;
        std::size_t batch_index = tensor_descr.layout.find("N");
        if (batch_index != std::string::npos) {
            if (batch_size == 0) {
                batch_size = tensor_descr.data_shape[batch_index];
            }
            else if (batch_size != tensor_descr.data_shape[batch_index]) {
                throw std::logic_error("Batch size is different for different inputs!");
            }
        }
    }
    if (batch_size == 0) {
        logger::warn << "Batch dimension not found, batch is set to 1" << logger::endl;
        batch_size = 1;
    }
    return batch_size;
}
