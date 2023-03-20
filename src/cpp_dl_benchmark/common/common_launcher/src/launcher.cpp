#include "common_launcher/launcher.hpp"

#include "utils/utils.hpp"

#include <algorithm>
#include <string>

std::vector<double> Launcher::get_latencies() const {
    return latencies;
}

double Launcher::get_total_time_ms() const {
    return utils::ns_to_ms(total_end_time - total_start_time);
}

void Launcher::reset_timers() {
    total_start_time = HighresClock::time_point::max();
    total_end_time = HighresClock::time_point::min();
    latencies.clear();
}
