#include "utils/statistics.hpp"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <stdexcept>
#include <vector>

void Metrics::calc_latencies(std::vector<double> latencies, int percentile_boundary) {
    std::sort(latencies.begin(), latencies.end());
    latency.min = latencies[0];
    latency.avg = std::accumulate(latencies.begin(), latencies.end(), 0.0) / latencies.size();

    latency.std =
        std::sqrt(std::accumulate(latencies.begin(), latencies.end(), 0.0, [avg = latency.avg](double x, double y) {
        return x + (y - avg) * (y - avg);
    }) / latencies.size());

    latency.median = latencies[int(latencies.size() / 100.0 * 50)];
    if (percentile_boundary) {
        latency.percentile = latencies[int(latencies.size() / 100.0 * percentile_boundary)];
    }
    latency.max = latencies.back();
}

void Metrics::calc_fps(int frames_num, double total_time) {
    fps = 1000.0 * frames_num / total_time;
}

Metrics::Metrics(const std::vector<double>& latencies, int batch_size, int percentile_boundary) {
    if (latencies.empty()) {
        throw std::invalid_argument("Latency metrics class expects non-empty vector of latencies at consturction.");
    }
    calc_latencies(latencies, percentile_boundary);
    calc_fps(latencies.size() * batch_size, std::accumulate(latencies.begin(), latencies.end(), 0.0));
}
