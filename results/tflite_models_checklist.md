# Model validation and performance analysis status for TensorFlow Lite

## Public models (Open Model Zoo)

### Image classification

Model | Availability in OMZ (2023.03.10) | Availability in the validation table |
-|-|-|
densenet-121|+-| + |
googlenet-v1-tf|+-| + |
googlenet-v2-tf|+-| + |
googlenet-v3|+-| + |
googlenet-v4-tf|+-| + |
mobilenet-v1-1.0-224-tf|+-| + |
mobilenet-v2-1.0-224|+-| + |
mobilenet-v2-1.4-224|+-| + |
mobilenet-v3-small-1.0-224|+-| + |
mobilenet-v3-large-1.0-224|+-| + |
inception-resnet-v2-tf|+| + |
resnet-50-tf|+-| + |

**Notes:**

1. Inference implementation for several GoogleNet-models
   supports batch size that equals 1.
2. "+-" in the column of availability in OMZ (2023.03.10)
   means that model was converted by `omz_converter` from `.ckpt`
   into `.pb` if it is required, and by internal converter
   `src/model_converters/tflite_converter.py` from `.pb`
   into `.tflite`.

### Other tasks

[TBD]

## Public models (TF hub)

### Image classification

Model | Availability in TF hub (2023.03.10) | Availability in the validation table |
-|-|-|
lite-model_mobilenet_v1_100_224_fp32_1.tflite|+ ([link][mobilenet_v1_100_224_fp32_1])| + |
lite-model_mobilenet_v2_100_224_fp32_1.tflite|+ ([link][mobilenet_v2_100_224_fp32_1])| + |
lite-model_mobilenet_v3_small_100_224_fp32_1.tflite|+ ([link][mobilenet_v3_small_100_224_fp32_1])| + |
lite-model_mobilenet_v3_large_100_224_fp32_1.tflite|+ ([link][mobilenet_v3_large_100_224_fp32_1])| + |
lite-model_mobilenet_v1_100_224_uint8_1.tflite|+ ([link][mobilenet_v1_100_224_uint8_1])| + |
lite-model_mobilenet_v2_100_224_uint8_1.tflite|+ ([link][mobilenet_v2_100_224_uint8_1])| + |
lite-model_mobilenet_v3_small_100_224_uint8_1.tflite|+ ([link][mobilenet_v3_small_100_224_uint8_1])| + |
lite-model_mobilenet_v3_large_100_224_uint8_1.tflite|+ ([link][mobilenet_v3_large_100_224_uint8_1])| + |
efficientnet_lite0_fp32_2.tflite|+ ([link][efficientnet_lite0_fp32_2])| + |
efficientnet_lite1_fp32_2.tflite|+ ([link][efficientnet_lite1_fp32_2])| + |
efficientnet_lite2_fp32_2.tflite|+ ([link][efficientnet_lite2_fp32_2])| + |
efficientnet_lite3_fp32_2.tflite|+ ([link][efficientnet_lite3_fp32_2])| + |
efficientnet_lite4_fp32_2.tflite|+ ([link][efficientnet_lite4_fp32_2])| + |
lite-efficientnet_lite0_uint8_2.tflite|+ ([link][efficientnet_lite0_uint8_2])| + |
lite-efficientnet_lite1_uint8_2.tflite|+ ([link][efficientnet_lite1_uint8_2])| + |
lite-efficientnet_lite2_uint8_2.tflite|+ ([link][efficientnet_lite2_uint8_2])| + |
lite-efficientnet_lite3_uint8_2.tflite|+ ([link][efficientnet_lite3_uint8_2])| + |
lite-efficientnet_lite4_uint8_2.tflite|+ ([link][efficientnet_lite4_uint8_2])| + |
efficientnet_lite0_int8_2.tflite|+ ([link][efficientnet_lite0_int8_2])| + |
efficientnet_lite1_int8_2.tflite|+ ([link][efficientnet_lite1_int8_2])| + |
efficientnet_lite2_int8_2.tflite|+ ([link][efficientnet_lite2_int8_2])| + |
efficientnet_lite3_int8_2.tflite|+ ([link][efficientnet_lite3_int8_2])| + |
efficientnet_lite4_int8_2.tflite|+ ([link][efficientnet_lite4_int8_2])| + |

**Note:** inference implementation for EfficientNet-models
supported for batch size that equals 1.

### Other tasks

[TBD]


<!-- LINKS -->
[mobilenet_v1_100_224_fp32_1]: https://tfhub.dev/iree/lite-model/mobilenet_v1_100_224/fp32/1
[mobilenet_v2_100_224_fp32_1]: https://tfhub.dev/iree/lite-model/mobilenet_v2_100_224/fp32/1
[mobilenet_v3_small_100_224_fp32_1]: https://tfhub.dev/iree/lite-model/mobilenet_v3_small_100_224/fp32/1
[mobilenet_v3_large_100_224_fp32_1]: https://tfhub.dev/iree/lite-model/mobilenet_v3_large_100_224/fp32/1
[mobilenet_v1_100_224_uint8_1]: https://tfhub.dev/iree/lite-model/mobilenet_v1_100_224/uint8/1
[mobilenet_v2_100_224_uint8_1]: https://tfhub.dev/iree/lite-model/mobilenet_v2_100_224/uint8/1
[mobilenet_v3_small_100_224_uint8_1]: https://tfhub.dev/iree/lite-model/mobilenet_v3_small_100_224/uint8/1
[mobilenet_v3_large_100_224_uint8_1]: https://tfhub.dev/iree/lite-model/mobilenet_v3_large_100_224/uint8/1
[efficientnet_lite0_fp32_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite0/fp32/2
[efficientnet_lite1_fp32_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite1/fp32/2
[efficientnet_lite2_fp32_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite2/fp32/2
[efficientnet_lite3_fp32_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite3/fp32/2
[efficientnet_lite4_fp32_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite4/fp32/2
[efficientnet_lite0_uint8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite0/uint8/2
[efficientnet_lite1_uint8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite1/uint8/2
[efficientnet_lite2_uint8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite2/uint8/2
[efficientnet_lite3_uint8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite3/uint8/2
[efficientnet_lite4_uint8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite4/uint8/2
[efficientnet_lite0_int8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite0/int8/2
[efficientnet_lite1_int8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite1/int8/2
[efficientnet_lite2_int8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite2/int8/2
[efficientnet_lite3_int8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite3/int8/2
[efficientnet_lite4_int8_2]: https://tfhub.dev/tensorflow/lite-model/efficientnet/lite4/int8/2
