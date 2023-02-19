// Copyright (C) 2023 KNS Group LLC (YADRO)
// SPDX-License-Identifier: Apache-2.0
//

#pragma once
#include "buffer.hpp"
#include "model.hpp"
#include "utils.hpp"

#include <onnxruntime_cxx_api.h>

#include <cstdint>
#include <map>
#include <string>
#include <vector>

namespace inputs {
struct InputDescr {
    TensorDescr tensor_descr;
    std::vector<std::string> files;
    std::vector<float> mean = {0.f, 0.f, 0.f};
    std::vector<float> scale = {1.f, 1.f, 1.f};
};

using InputsInfo = std::map<std::string, InputDescr>;

int get_batch_size(const InputsInfo &inputs_info);

void set_batch_size(InputsInfo &inputs_info, int batch_size);

InputsInfo get_inputs_info(const std::map<std::string, std::vector<std::string>> &input_files,
                           const std::vector<TensorDescr> &model_inputs,
                           const std::string &layout_string,
                           const std::string &shape_string,
                           const std::string &mean_string,
                           const std::string &scale_string);

std::vector<std::vector<Buffer>> get_input_tensors(const InputsInfo &inputs_info,
                                                       int batch_size,
                                                       int tensors_num = 1);
} // namespace inputs
