# Conversion to TensorFlow Lite

TFLite converter supports conversion to TensorFlow Lite format from TensorFlow and ONNX formats.

## TFLite converter usage

Basic usage of the script:

```sh
python tflite_converter.py --model-path <path/to/input/model> --source-framework <source_framework>
```

This will convert model from `<source_framework>` to TFLite format.

### TFLite converter parameters

- `--model-path` absolute path to model in TensorFlow or ONNX format.
- `--input-names` comma-separated names of the input layers.
- `--input-shapes` comma-separated shapes of the input blobs. Optional parameter, can be used to set desired shapes.
- `--output-names` comma-separated names of the output layers.
- `--freeze-constant-input` pair "name"="value", replaces input layer with constant with provided value.
- `--source-framework` source framework for convertion to TensorFlow Lite format.

### Examples of usage
```sh
tflite_converter.py --model-path /<full_path_to_models_dir>/_models_dir/public/ssd_mobilenet_v1_coco/ssd_mobilenet_v1_coco_2018_01_28/saved_model --source-framework tf --input-names image_tensor --input-shapes [1, 300, 300, 3]
```

```sh
tflite_converter.py --model-path /<full_path_to_models_dir>/_models_dir/public/yolo-v1-tiny-tf/yolo-v1-tiny.pb --source-framework tf --input-names input_1 --input-shapes [1, 416, 416, 3] --output-names conv2d_9/BiasAdd
```
