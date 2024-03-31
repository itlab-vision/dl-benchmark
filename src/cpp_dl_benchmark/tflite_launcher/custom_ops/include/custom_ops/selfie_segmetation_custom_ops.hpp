#pragma once

#include <tensorflow/lite/kernels/register.h>

namespace tflite_ops {
TfLiteRegistration* RegisterConvolution2DTransposeBias();
}  // namespace tflite_ops