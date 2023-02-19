
#include "model.hpp"
#include "utils.hpp"

#include <algorithm>
#include <string>

bool TensorDescr::is_image() const {
    return (layout == "NCHW" || layout == "NHWC" || layout == "CHW" || layout == "HWC") && channels() == 3;
}

bool TensorDescr::is_image_info() const {
    return (layout.size() == 2 && layout.back() == 'C') && channels() >= 2;
}

bool TensorDescr::is_dynamic() const {
    return std::find(shape.begin(), shape.end(), -1) != shape.end();
}

bool TensorDescr::has_batch() const {
    return layout.find("N") != std::string::npos;
}

bool TensorDescr::is_dynamic_batch() const {
    if (has_batch()) {
        return shape[layout.find("N")] == -1;
    }
    return false;
}

void TensorDescr::set_batch(int batch_size) {
    std::size_t batch_index = layout.find("N");
    if (batch_index != std::string::npos) {
        data_shape[batch_index] = batch_size;
    }
}

int64_t TensorDescr::get_dimension_by_layout(char ch) const {
    size_t pos = layout.find(ch);
    if (pos == std::string::npos) {
        throw std::invalid_argument("Can't get " + std::string(ch, 1) + " from layout " + layout);
    }
    return data_shape.at(pos);
}

int64_t TensorDescr::channels() const {
    return get_dimension_by_layout('C');
}

int64_t TensorDescr::width() const {
    return get_dimension_by_layout('W');
}

int64_t TensorDescr::height() const {
    return get_dimension_by_layout('H');
}

// int Model::get_batch_size() const {
//     return batch
// }

std::vector<double> Model::get_latencies() const {
    return latencies;
}

double Model::get_total_time_ms() const {
    return utils::ns_to_ms(total_end_time - total_start_time);
}

void Model::reset_timers() {
    total_start_time = HighresClock::time_point::max();
    total_end_time = HighresClock::time_point::min();
    latencies.clear();
}