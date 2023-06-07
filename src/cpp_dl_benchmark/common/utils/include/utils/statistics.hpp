#pragma once
#include <vector>

class Metrics {
private:
    int percentile_boundary = 50;

    void calc_latencies(std::vector<double> latencies, int percentile_boundary);
    void calc_fps(int frames_num, double total_time);

public:
    struct {
        double median = 0;
        double avg = 0;
        double std = 0;
        double min = 0;
        double max = 0;
        double percentile = 0;
    } latency;
    double fps = 0;

    Metrics() = default;
    Metrics(const std::vector<double>& latencies, int batch_size, int percentile_boundary = 50);
};
