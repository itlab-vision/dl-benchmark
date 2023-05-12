# Conversion to TensorFlow Lite

TFLite converter supports conversion to TensorFlow Lite format from TensorFlow and ONNX formats.

## TFLite converter usage

Basic usage of the script:

```sh
python tflite_converter.py --model-path <path/to/input/model> --source-framework <source_framework>
```

This will convert model from `<source_framework>` to TFLite format.

### TFLite converter parameters

- `--model-path` absolute path to model in TensorFlow (.pb or .meta files or saved model directory) or ONNX format.
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

# Conversion to TF2 saved model format and optimization with TRT for NVIDIA devices

TF Converter supports model conversion to TF2 saved model format from frozen graph and meta formats of TF model or from ONNX model

## TF Converter usage

```sh
python tf_converter.py --model-path <path/to/input/model> --tensor_rt_precision <precision>
```

### TF converter parameters

- `--model-path` absolute path to model in TensorFlow (.pb or .meta files or saved model directory) or ONNX format.
- `--input-names` comma-separated names of the input layers.
- `--input-shapes` comma-separated shapes of the input blobs. Optional parameter, can be used to set desired shapes.
- `--output-names` comma-separated names of the output layers.
- `--saved_model_dir` path where tf2 saved model will be saved. Default <model-path.parent>/saved_model.
- `--tensor_rt_precision` Tensor RT precision FP16, FP32. If not defined, no Tensor-RT conversion will be applied.
  Applicable only for hosts with NVIDIA GPU and tensorflow built with Tensor-RT support.
- `--tensor_rt_model_dir` A path where Tensor RT optimized model will be saved. Default <model-path.parent>
  /tensor_rt_<Precision>

