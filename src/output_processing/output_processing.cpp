#include <pybind11/pybind11.h>

#include "wrappers.hpp"

PYBIND11_MODULE(output_processing, m) {
    m.def("ClassificationTask", &ClassificationTaskPy);
};