# Conversion to PaddlePaddle

PaddlePaddle converter supports conversion to Paddle format from PyTorch and ONNX formats.

## PaddlePaddle converter usage

Usage of the script:

```sh
python srcf2paddle.py -m <path/to/input/model> -f <source_framework> -p <PyTorch/module/name> -d <output_directory>
```

This will convert model from `<source_framework>` to Paddle format.

### Paddle converter parameters

- `--model_path` is a path to an .onnx or .pth file with the original model.
- `--framework` is a source framework for convertion to PaddlePaddle format.
- `--pytorch_module_name` is a module name for PyTorch model (necessary if source framework is PyTorch).
- `--save_dir` is a directory for converted model to be saved to.

### Examples of usage

```sh
python srcf2paddle.py -m .\public\googlenet-v3-pytorch\inception_v3_google-1a9a5a14.pth -f pytorch -p InceptionV3 -d pd
```

```sh
python srcf2paddle.py -m .\public\ctdet_coco_dlav0_512\ctdet_coco_dlav0_512.onnx -f onnx -d pd
```

# Conversion from PaddlePaddle

paddle2onnx converter supports conversion to ONNX format from Paddle format.

## PaddlePaddle converter usage

Usage of the script:

```sh
python paddle2onnx.py -d .\pd_pth\inference_model -f model.pdmodel -p model.pdiparams -m inference.onnx -o 11
```

This script will convert model from Paddle to ONNX format.

### Converter parameters

- `--model_dir` is a path to the directory with the original model.
- `--model_filename` is a name of the model file name.
- `--params_filename` is a name of the parameters file name.
- `--model_path` is a path to the resulting .onnx file.
- `--opset_version` is a desired opset version of the resulting ONNX model.

### Examples of usage

```sh
python paddle2onnx.py -d .\pd_pth\inference_model -f model.pdmodel -p model.pdiparams -m inference.onnx -o 11
```