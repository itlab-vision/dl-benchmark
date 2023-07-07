#include "common_launcher/launcher.hpp"

#include "utils/utils.hpp"

#include <algorithm>
#include <numeric>
#include <string>

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