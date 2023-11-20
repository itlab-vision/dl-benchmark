#include "utils/report.hpp"

#include "utils/logger.hpp"

#include <nlohmann/json.hpp>

#include <filesystem>
#include <fstream>
#include <iomanip>
#include <map>
#include <string>
#include <utility>
#include <vector>

void Report::save() {
    nlohmann::json js;
    std::filesystem::path file_path(path);
    if (!file_path.has_extension()) {
        file_path /= "benchmark_report.json";
    }
    if (file_path.has_parent_path() && !std::filesystem::exists(file_path.parent_path())) {
        std::filesystem::create_directories(file_path.parent_path());
    }

    if (std::filesystem::exists(file_path)) {
        logger::warn << "File " + file_path.string() + " already exists, it will be overwritten." << logger::endl;
    }

    for (const auto& [cat, records] : records_per_category) {
        auto category = record_categories_str.at(cat);
        for (const auto& r : records) {
            js[category][r.name] = r.val;
        }
    }
    std::ofstream out_stream(file_path);
    if (out_stream.is_open()) {
        out_stream << std::setw(4) << js << std::endl;
        logger::info << "Saved report to " << file_path << logger::endl;
    }
    else {
        throw std::runtime_error("Something went wrong, can't open file: " + file_path.string());
    }
}

void Report::add_record(Category type, const std::vector<Record>& records) {
    if (record_categories_str.count(type) == 0) {
        throw std::invalid_argument("Unsupported record type: " + std::to_string((uint)type));
    }
    for (const auto& r : records) {
        records_per_category[type].push_back(r);
    }
}
