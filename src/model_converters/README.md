# Model converters

## Supported converters

- `tf2tflite` contains converter to the TensorFlow Lite
  format from TensorFlow and ONNX formats.
- `tvm_converter` contains converter and compiler
  to the TVM format.
- `mmdnn_converter` contains script to install [MMdnn][mmdnn]. Be carefull,
  MMdnn supports old formats that is why you should validate inference results.

## An overview of existing model converters

| from/to | MXNet | Caffe | PyTorch | TensorFlow 1 | TensorFlow 2 | ONNX | PaddlePaddle |
|-|-|-|-|-|-|-|-|
| MXNet   |-| [MMdnn][mmdnn]<br> [MXNet2Caffe][mxnet2caffe]<br> [MXNetToCaffeConverter][mxnettocaffeconverter] | [MMdnn][mmdnn]<br>[gluon2pytorch][gluon2pytorch]| [MMdnn][mmdnn] (through ONNX) |-| [MMdnn][mmdnn]<br> [MXNet tools][mxnet2onnx] |-|
| Caffe   |-|-|-|-|-|-|-|
| PyTorch |-|-|-|-|-|-|-|
| TensorFlow 1 |-|-|-|-|-|-|-|
| TensorFlow 2 |-|-|-|-|-|-|-|
|ONNX     |-|-|-|-|-|-|-|
| PaddlePaddle |-|-|-|-|-|-|-|


<!-- LINKS -->
[mmdnn]: https://github.com/microsoft/MMdnn
[mxnet2caffe]: https://github.com/cypw/MXNet2Caffe
[mxnettocaffeconverter]: https://github.com/pertusa/MXNetToCaffeConverter
[gluon2pytorch]: https://github.com/gmalivenko/gluon2pytorch
[mxnet2onnx]: https://github.com/apache/mxnet/blob/master/python/mxnet/onnx
