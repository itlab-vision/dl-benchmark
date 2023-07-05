#include "custom_ops.hpp"

#include "selfie_segmetation_custom_ops.hpp"

namespace tflite_ops {
void RegisterSelectedOps(::tflite::MutableOpResolver* resolver) {
    resolver->AddCustom("Convolution2DTransposeBias", RegisterConvolution2DTransposeBias());
}
}  // namespace tflite_ops