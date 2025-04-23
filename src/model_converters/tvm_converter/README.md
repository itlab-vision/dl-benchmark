# Conversion to the TVM format

TVM converter supports conversion to the TVM format
from Caffe, ONNX, MXNet, PyTorch and TensorFlow Lite
formats.

TVM compiler supports compilation from `.json`/`.params` format
to the `.so` format for the Relay API or to the `.so`/`.ro` format
for the VirtualMachine API.

## TVM converter usage

Basic usage of the script:

```sh
tvm_converter.py --model_name <model_name> \
                 --model <model> \
                 --weights <weights> \
                 --module <module> \
                 --input_shape <input_shape> \
                 --source_framework <source_framework> \
                 --batch_size <batch_size> \
                 --input_name <input_name> \
                 --device <device> \
                 --output_dir <output_dir>
```

This script converts model from `<source_framework>` to the TVM format.

### TVM converter parameters

- `-mn / --model_name` is a model name.
- `-m / --model` is a path to an `.json`, `.onnx`, `.pt`, `.prototxt` file
  with a trained model.
- `-w / --weights` is a path to an `.params`, `.caffemodel`, `.pth` file
  with a trained weights.
- `-mm / --module`is a module with the model architecture. It is used
  for PyTorch models and equals `torchvision.models` by default.
- `-is / --input_shape` is an input shape in the format BxWxHxC, where
  B is a batch size, W is an input tensor width, H is an input tensor
  height, C is an input tensor number of channels.
- `-f / --source_framework` is a source framework where the model was trained.
- `-b / --batch_size` is a batch size. It equals 1 by default.
- `-in / --input_name` is an input name. It equals `data` by default.
- `-d / --device` is a target device for inference. It equals `CPU`
  by default.
- `-op / --output_dir` is path to save the model.

### Examples of usage

```sh
python3 ./tvm_converter.py -mn efficientnet-b0 -b 1 \
                           -is 1 224 224 3 -m efficientnet-b0.onnx \
                           -f onnx
```

```sh
python ./tvm_converter.py -mn resnet50 -is 1 3 224 224 \
                          -w resnet50-19c8e357.pth -f pytorch
```

## TVM compiler usage

Basic usage of the script:

```sh
tvm_compiler.py --mod <model> \
                --params <parameters> \
                --target <target> \
                --opt_level <opt_level> \
                --high_level_api <high_level_api> \
                --lib_name <lib_name> \
                --output_dir <output_dir>
```

This script compiles model from `.json`+`.params` to the `.so` format
for the Relay API or to the `.so`+`.ro` format for the VirtualMachine API.

### TVM compiler parameters

- `-m / --mod` is a path to an `.json` file with a model.
- `-p / --params` is a path to an `.params` file with a model parameters.
- `-t / --target` is target device information, for example `llvm` for CPU.
- `--opt_level` is the optimization level of the task extractions.
- `--high_level_api` is a high level API: `Relay`, `RelayVM`, `Relax`.
- `--lib_name` is a file name to save compiled model.
- `-op / --output_dir` is a path to save the model.

### Examples of usage

```sh
python3 ./tvm_compiler.py -m efficientnet-b0.json -p efficientnet-b0.params \
                          -t llvm --opt_level 2 --lib_name efficientnet-b0.so
```

```sh
python3 ./tvm_compiler.py -m resnet50.json -p resnet50.params \
                          -t llvm --opt_level 1 --lib_name resnet50.so
```
