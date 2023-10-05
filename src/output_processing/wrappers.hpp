#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "output_processing/output_handlers.hpp"
#include "output_processing/exception_handler.hpp"

#include <string>
#include <vector>
#include <iostream>


namespace py = pybind11;


void ClassificationTaskPy(const py::dict& map, const size_t number_top,
                         const std::string& label_file) {
    std::map<std::string, std::vector<std::vector<float>>> tensors;
    for (const auto& it : map) {
        const std::string& layer_name = py::cast<const std::string>(it.first);
        const py::array& py_tensor = py::cast<const py::array>(it.second);
    }
}