# Conversion to the PaddlePaddle format

PaddlePaddle converter supports conversion to the PaddlePaddle format
from PyTorch and ONNX formats.

## PaddlePaddle converter usage

Usage of the script:

```bash
python srcf2paddle.py -m <path/to/input/model> -f <source_framework> \
                      -p <PyTorch/module/name> -d <output_directory>
```

### Paddle converter parameters

- `-m / --model_path` is a path to an .onnx or .pth file with the original model.
- `-f / --framework` is a source framework for convertion to the PaddlePaddle format.
- `-p / --pytorch_module_name` is a module name for the PyTorch model (it is required
  if source framework is PyTorch).
- `-d / --save_dir` is a directory for converted model to be saved to.

### Examples of usage

```bash
python srcf2paddle.py -m .\public\googlenet-v3-pytorch\inception_v3_google-1a9a5a14.pth \
                      -f pytorch -p InceptionV3 -d pd
```

```bash
python srcf2paddle.py -m .\public\ctdet_coco_dlav0_512\ctdet_coco_dlav0_512.onnx \
                      -f onnx -d pd
```

# Conversion from the PaddlePaddle to the ONNX format

paddle2onnx converter supports conversion to the ONNX format from the PaddlePaddle
format.

## PaddlePaddle converter usage

Usage of the script:

```bash
python paddle2onnx.py -d .\pd_pth\inference_model -f model.pdmodel \
                      -p model.pdiparams -m inference.onnx -o 11
```

### Converter parameters

- `-d / --model_dir` is a path to the directory with the original model.
- `-f / --model_filename` is a model file name.
- `-p / --params_filename` is a parameters file name.
- `-m / --model_path` is a path to the resulting .onnx file.
- `-o / --opset_version` is a desired opset version of the ONNX model.

### Examples of usage

```bash
python paddle2onnx.py -d .\pd_pth\inference_model -f model.pdmodel \
                      -p model.pdiparams -m inference.onnx -o 11
```
