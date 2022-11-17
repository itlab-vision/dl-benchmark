#include "statistics.hpp"

#include <algorithm>
#include <numeric>
#include <stdexcept>
#include <vector>

void Metrics::calc_latencies(std::vector<double> latencies, int percentile_boundary) {
    std::sort(latencies.begin(), latencies.end());
    latency.min = latencies[0];
    latency.avg = std::accumulate(latencies.begin(), latencies.end(), 0.0) / latencies.size();
    latency.median = latencies[int(latencies.size() / 100.0 * 50)];
    if (percentile_boundary) {
        latency.percentile = latencies[int(latencies.size() / 100.0 * percentile_boundary)];
    }
    latency.max = latencies.back();
}

void Metrics::calc_fps(double latency, int batch_size) {
    fps = batch_size * 1000.0 / latency;
}

Metrics::Metrics(const std::vector<double> &latencies, int batch_size, int percentile_boundary) {
    if (latencies.empty()) {
        throw std::invalid_argument("Latency metrics class expects non-empty vector of latencies at consturction.");
    }
    calc_latencies(latencies, percentile_boundary);
    calc_fps(latency.median, batch_size);
}
