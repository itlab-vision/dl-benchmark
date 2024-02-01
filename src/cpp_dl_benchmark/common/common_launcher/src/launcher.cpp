#include "common_launcher/launcher.hpp"

#include "utils/utils.hpp"

#include <nlohmann/json.hpp>

#include <algorithm>
#include <chrono>
#include <condition_variable>
#include <filesystem>
#include <fstream>
#include <mutex>
#include <numeric>
#include <string>
#include <thread>

std::vector<double> Launcher::get_latencies() const {
    return latencies;
}

double Launcher::get_total_time_ms() const {
    return total_time;
}

void Launcher::reset_timers() {
    latencies.clear();
}

void Launcher::warmup_inference() {
    run(0);
}

int Launcher::evaluate(int iterations_num, uint64_t time_limit_ns) {
    std::condition_variable cv;
    std::mutex mtx;
    int iteration = 0;
    auto start_time = HighresClock::now();
    auto uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time);
    while ((iterations_num != 0 && iteration < iterations_num) ||
           (time_limit_ns != 0 && static_cast<uint64_t>(uptime.count()) < time_limit_ns)) {
        run(iteration % tensor_buffers.size());
        ++iteration;
        std::unique_lock<std::mutex> lk(mtx);
        if (latencies.back() < target_frame_latency) {
            cv.wait_for(lk, std::chrono::duration<double, std::milli>(target_frame_latency - latencies.back()));
        }
        uptime = std::chrono::duration_cast<ns>(HighresClock::now() - start_time);
    }
    total_time = utils::ns_to_ms(uptime);

    return iteration;
}

void Launcher::dump_output(const std::vector<OutputTensors>& outputs, const std::string& filename) {
    auto json_outputs = nlohmann::json::array();

    std::filesystem::path file_path(filename);
    if (!file_path.has_extension()) {
        file_path /= "output.json";
    }
    if (file_path.has_parent_path() && !std::filesystem::exists(file_path.parent_path())) {
        std::filesystem::create_directories(file_path.parent_path());
    }

    if (std::filesystem::exists(file_path)) {
        logger::warn << "File " + file_path.string() + " already exists, it will be overwritten." << logger::endl;
    }

    std::ofstream file(file_path);

    for (auto& output : outputs) {
        auto json_layers = nlohmann::json::array();

        for (auto& out_layer : output) {
            nlohmann::json js;
            js["output_name"] = out_layer.name();
            js["shape"] = out_layer.shape();
            js["data"] = out_layer.data();

            json_layers.push_back(js);
        }

        json_outputs.push_back(json_layers);
    }

    if (file.is_open()) {
        file << std::setw(4) << json_outputs << std::endl;
        logger::info << "Saved output to " << file_path << logger::endl;
    }
    else {
        throw std::runtime_error("Something went wrong, can't open file: " + file_path.string());
    }

    reset_timers();
}