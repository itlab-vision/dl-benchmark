#pragma once

#include <map>
#include <string>
#include <vector>


bool ClassificationTask(const std::map<std::string, std::vector<std::vector<float>>>& output_tensors,
                        const size_t number_top, const std::string& labels);