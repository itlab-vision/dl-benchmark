#pragma once

#include <string>
#include <vector>
#include <algorithm>
#include <numeric>


std::vector<std::string> read_labels(const std::string& label_path);

template<typename T>
std::vector<size_t> argsort(const std::vector<T> &array) {
    std::vector<size_t> indices(array.size());
    std::iota(indices.begin(), indices.end(), 0);
    std::sort(indices.begin(), indices.end(),
              [&array](int left, int right) -> bool {
                  return array[left] < array[right];
              });

    return indices;
}