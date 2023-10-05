#include "output_processing/utils.hpp"

#include <fstream>
#include <filesystem>


std::vector<std::string> read_labels(const std::string& label_path) {
    std::vector<std::string> labels;

    std::filesystem::path path = label_path;
    std::ifstream in(path);
    if (in.is_open()) {
        std::string label;
        while (std::getline(in, label)) {
            labels.push_back(label);
        }
    }
    in.close();
    if (path.extension() == ".json") {
        // Remove parenthless
        labels.pop_back();
        labels.erase(labels.begin());
    }
    return labels;
}