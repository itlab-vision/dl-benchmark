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
| MXNet   |-| [MMdnn][mmdnn]<br> [MXNet2Caffe][mxnet2caffe]<br> [MXNetToCaffeConverter][mxnettocaffeconverter] | [MMdnn][mmdnn]<br>[gluon2pytorch][gluon2pytorch]| [MMdnn][mmdnn] (through ONNX) |-| [MMdnn][mmdnn]<br> [MXNetTools][mxnet2onnx] |-|
| Caffe   | [MMdnn][mmdnn] |-| [MMdnn][mmdnn]<br> [caffemodel2pytorch][caffemodel2pytorch]<br> [Caffe2Pytorch][Caffe2Pytorch] | [MMdnn][mmdnn] | [pytorch2keras][pytorch2keras]<br> [pytorch-tf][pytorch-tf] | [OpenCV AI (model converter)][opencv-ai-model_converter] | [paddle-cppt][paddle-cppt] |
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
[caffemodel2pytorch]: https://github.com/vadimkantorov/caffemodel2pytorch
[Caffe2Pytorch]: https://github.com/penguinnnnn/Caffe2Pytorch
[pytorch2keras]: https://github.com/gmalivenko/pytorch2keras
[pytorch-tf]: https://github.com/leonidk/pytorch-tf
[opencv-ai-model_converter]: https://github.com/opencv-ai/model_converter
[paddle-cppt]: https://github.com/wj-Mcat/paddle-cppt?ysclid=lnut6o3o6v87337456
