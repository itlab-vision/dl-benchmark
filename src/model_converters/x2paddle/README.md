# Conversion to PaddlePaddle

PaddlePaddle converter supports conversion to Paddle format from Pytorch and ONNX formats.

## PaddlePaddle converter usage

Usage of the script:

```sh
python converter.py -m <path/to/input/model> -f <source_framework> -p <Pytorch/module/name> -d <output_directory>
```

This will convert model from `<source_framework>` to Paddle format.

### Paddle converter parameters

- `--model_path` Path to an .onnx or .pth file with the original model.
- `--framework` is a source framework for convertion to PaddlePaddle format.
- `--pytorch_module_name` Module name for PyTorch model (necessary if source framework is Pytorch).
- `--save_dir` Directory for converted model to be saved to.

### Examples of usage

```sh
python converter.py -m .\public\googlenet-v3-pytorch\inception_v3_google-1a9a5a14.pth -f pytorch -p InceptionV3 -d pd
```

```sh
python converter.py -m .\public\ctdet_coco_dlav0_512\ctdet_coco_dlav0_512.onnx -f onnx -d pd
```

# Conversion from PaddlePaddle

paddle2onnx converter supports conversion to ONNX format from Paddle format.

## PaddlePaddle converter usage

Usage of the script:

```sh
python paddle2onnx.py -d .\pd_pth\inference_model -f model.pdmodel -p model.pdiparams -m inference.onnx -o 11
```

This will convert model from Paddle to ONNX format.

### Converter parameters

- `--model_dir` Path to the directory with the original model.
- `--model_filename` Name of the model file name.
- `--params_filename` Name of the parameters file name.
- `--model_path` Path to the resulting .onnx file.
- `--opset_version` Desired opset version of the resulting ONNX model.

### Examples of usage

```sh
python paddle2onnx.py -d .\pd_pth\inference_model -f model.pdmodel -p model.pdiparams -m inference.onnx -o 11
```
