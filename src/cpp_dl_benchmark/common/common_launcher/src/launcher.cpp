#include "common_launcher/launcher.hpp"

#include "utils/utils.hpp"

#include <nlohmann/json.hpp>

#include <algorithm>
#include <numeric>
#include <string>
#include <fstream>
#include <filesystem>

std::vector<double> Launcher::get_latencies() const {
    return latencies;
}

double Launcher::get_total_time_ms() const {
    return std::accumulate(latencies.begin(), latencies.end(), 0.0);
}

void Launcher::reset_timers() {
    latencies.clear();
}

void Launcher::warmup_inference() {
    run(0);
}

int Launcher::evaluate(int iterations_num, uint64_t time_limit_ns) {
    int iteration = 0;
    auto start_time = HighresClock::now();
    auto uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    while ((iterations_num != 0 && iteration < iterations_num) ||
           (time_limit_ns != 0 && static_cast<uint64_t>(uptime) < time_limit_ns)) {
        run(iteration % tensor_buffers.size());
        ++iteration;
        uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time).count();
    }

    return iteration;
}

void Launcher::dump_output(const std::vector<OutputDescription>& outputs,
                           const std::string& filename) {
    auto jsonObjects = nlohmann::json::array();

    for (auto& out : outputs) {
        nlohmann::json js;
        js["output_name"] = out.name();
        js["shape"] = out.shape();
        js["data"] = out.data();

        jsonObjects.push_back(js);
    }

    std::filesystem::path file_path(filename);
    if (!file_path.has_extension()) {
        file_path /= "output.json";
    }
    if (file_path.has_parent_path() && !std::filesystem::exists(file_path.parent_path())) {
        std::filesystem::create_directory(file_path.parent_path());
    }

    if (std::filesystem::exists(file_path)) {
        logger::warn << "File " + file_path.string() + " already exists, it will be overwritten." << logger::endl;
    }

    std::ofstream file(file_path);

    if (file.is_open()) {
        file << std::setw(4) << jsonObjects << std::endl;
        logger::info << "Saved output to " << file_path << logger::endl;
    }
    else {
        throw std::runtime_error("Something went wrong, can't open file: " + file_path.string());
    }

    reset_timers();
}