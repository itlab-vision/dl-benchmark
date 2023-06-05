# Conversion to TensorFlow Lite

TFLite converter supports conversion to TensorFlow Lite format from TensorFlow and ONNX formats.

## TFLite converter usage

Basic usage of the script:

```sh
python tflite_converter.py --model-path <path/to/input/model> --source-framework <source_framework>
```

This will convert model from `<source_framework>` to TFLite format.

### TFLite converter parameters

- `--model-path` is an absolute path to model in TensorFlow (.pb or .meta files or saved model directory) or ONNX format.
- `--input-names` is a comma-separated names of the input layers.
- `--input-shapes` is a comma-separated shapes of the input blobs. Optional parameter, can be used to set desired shapes.
- `--output-names` is a comma-separated names of the output layers.
- `--freeze-constant-input` is a pair "name"="value", replaces input layer with constant with provided value.
- `--source-framework` is a source framework for convertion to TensorFlow Lite format.

### Examples of usage

```sh
tflite_converter.py --model-path /<full_path_to_models_dir>/_models_dir/public/ssd_mobilenet_v1_coco/ssd_mobilenet_v1_coco_2018_01_28/saved_model --source-framework tf --input-names image_tensor --input-shapes [1, 300, 300, 3]
```

```sh
tflite_converter.py --model-path /<full_path_to_models_dir>/_models_dir/public/yolo-v1-tiny-tf/yolo-v1-tiny.pb --source-framework tf --input-names input_1 --input-shapes [1, 416, 416, 3] --output-names conv2d_9/BiasAdd
```


# Conversion to TF2 saved model format and optimization with TensorRT for NVIDIA devices

TF Converter supports model conversion to TF2 saved model format from frozen graph and meta formats of TF model or from ONNX model

## TF Converter usage

```sh
python tf_converter.py --model-path <path/to/input/model> --tensor_rt_precision <precision>
```

### TF converter parameters

- `--model-path` is an absolute path to model in TensorFlow (.pb or .meta files or saved model directory) or ONNX format.
- `--input-names` is a comma-separated names of the input layers.
- `--input-shapes` is a comma-separated shapes of the input blobs. Optional parameter, can be used to set desired shapes.
- `--output-names` is a comma-separated names of the output layers.
- `--saved_model_dir` is a path where tf2 saved model will be saved. Default <model-path.parent>/saved_model.
- `--tensor_rt_precision` is a Tensor RT precision FP16, FP32. If not defined, no Tensor-RT conversion will be applied.
  Applicable only for hosts with NVIDIA GPU and tensorflow built with Tensor-RT support.
- `--tensor_rt_model_dir` is a path where Tensor RT optimized model will be saved. Default <model-path.parent>
  /tensor_rt_<Precision>


# Converting OMZ models to PyTorch format .pt

To get .pt format models along .onnx, apply the following patch to OMZ converter script:

```sh
diff --git a/tools/model_tools/src/openvino/model_zoo/internal_scripts/pytorch_to_onnx.py b/tools/model_tools/src/openvino/model_zoo/internal_scripts/pytorch_to_onnx.py
index 0449a8f26..65fc2a8d5 100644
--- a/tools/model_tools/src/openvino/model_zoo/internal_scripts/pytorch_to_onnx.py
+++ b/tools/model_tools/src/openvino/model_zoo/internal_scripts/pytorch_to_onnx.py
@@ -163,6 +163,9 @@ def convert_to_onnx(model, input_shapes, output_file, input_names, output_names,
         torch.zeros(input_shape, dtype=INPUT_DTYPE_TO_TORCH[inputs_dtype])
         for input_shape in input_shapes)
     model(*dummy_inputs)
+    pt_output_file = output_file.with_suffix(".pt")
+    traced_model = torch.jit.trace(model, dummy_inputs, strict=False)
+    traced_model.save(pt_output_file)
     torch.onnx.export(model, dummy_inputs, str(output_file), verbose=False, opset_version=opset_version,
                       input_names=input_names.split(','), output_names=output_names.split(','), **conversion_params)
```
