# Conversion to TensorFlow Lite

TFLite converter supports conversion to TensorFlow Lite format from TensorFlow and ONNX formats.

## TFLite converter usage

Basic usage of the script:

```sh
python tflite_converter.py --model-path <path/to/input/model> --source-framework <source_framework>
```

This will convert model from `<source_framework>` to TFLite format.

### TFLite converter parameters

- `--model-path` - Path to model in TensorFlow or ONNX format.
- `--input-names` - Comma-separated names of the input layers.
- `--input-shapes` - Comma-separated shapes of the input blobs. Optional parameter, can be used to set desired shapes.
- `--output-names` - Comma-separated names of the output layers.
- `--freeze-constant-input` - Pair "name"="value", replaces input layer with constant with provided value.
- `--source-framework` - Source framework for convertion to TensorFlow Lite format.
