#pragma once

#include <tensorflow/lite/mutable_op_resolver.h>

namespace tflite_ops {
void RegisterSelectedOps(::tflite::MutableOpResolver* resolver);
}  // namespace tflite_ops