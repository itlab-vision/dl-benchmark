#include "output_processing/output_handlers.hpp"

#include "output_processing/exception_handler.hpp"
#include "output_processing/utils.hpp"

#include <iostream>
#include <iomanip>


bool ClassificationTask(const std::map<std::string, std::vector<std::vector<float>>>& output_tensors,
                        const size_t number_top, const std::string& label_file) {
    DLB_ASSERT(output_tensors.size() == 1)

    const auto result_tensor = *output_tensors.cbegin();
    const auto layer_name = result_tensor.first;
    const auto data = result_tensor.second;
    const auto labels = read_labels(label_file);
    const auto batch = data.size();

    std::cout << "[ INFO ] Top " + std::to_string(number_top) + " results:\n";

    for (size_t i = 0; i < batch; ++i) {
        const auto batch_result = data[i];
        const auto top_idxs = argsort(batch_result);

        std::cout << "[ INFO ] Result for image " + std::to_string(i + 1) + ":\n";
        for (size_t idx = 0; idx < number_top; ++idx) {
            std::cout.precision(2);
            const auto sorted_index = top_idxs[idx];
            std::cout << std::setw(10) << batch_result[sorted_index] << std::setw(5) << labels[sorted_index] << "\n";
        }
    }
    return true;
}