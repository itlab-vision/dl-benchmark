# Model converters

## Supported converters

- `caffe2onnx` contains script to convert Caffe models to the ONNX format
  using [the caffe2onnx converter][caffe2onnx-2].
- `mmdnn_converter` contains script to install [MMdnn][mmdnn]. Be carefull,
  MMdnn supports old formats that is why you should validate inference results.
- `mxnet2onnx` contains script to convert MXNet models to the ONNX format
  using [the mxnet.onnx package][mxnet2onnx].
- `onnx2mxnet` contains script to convert ONNX models to the MXNet format
  using [the following guide][onnx2mxnet-guide].
- `pytorch2onnx` contains script to convert PyTorch models to the ONNX format
  using [the OpenCV AI model converter][opencv-ai-model_converter].
- `tf2tflite` contains converter to the TensorFlow Lite
  format from TensorFlow and ONNX formats.
- `tvm_converter` contains converter and compiler
  to the TVM format.

## An overview of existing model converters

| from/to | MXNet | Caffe | PyTorch | TensorFlow 1 | TensorFlow 2 | ONNX | PaddlePaddle |
|-|-|-|-|-|-|-|-|
| MXNet   |-| [MMdnn][mmdnn]<br> [MXNet2Caffe][mxnet2caffe]<br> [MXNetToCaffeConverter][mxnettocaffeconverter] | [MMdnn][mmdnn]<br>[gluon2pytorch][gluon2pytorch]| [MMdnn][mmdnn] (through ONNX) |-| [MMdnn][mmdnn]<br> [mxnet.onnx][mxnet2onnx] |-|
| Caffe   | [MMdnn][mmdnn] |-| [MMdnn][mmdnn]<br> [caffemodel2pytorch][caffemodel2pytorch]<br> [Caffe2Pytorch][Caffe2Pytorch] | [MMdnn][mmdnn] | [NN tools][nn_tools]<br> [caffe-tensorflow][caffe-tensorflow] | [MMdnn][mmdnn] <br>[caffe2onnx][caffe2onnx-1]<br> [caffe-onnx][caffe-onnx]<br> [caffe2onnx][caffe2onnx-2] | [X2Paddle][X2Paddle] |
| PyTorch | [MMdnn][mmdnn] | [MMdnn][mmdnn]<br> [brocolli][brocolli]<br> [pytorch2caffe][pytorch2caffe] |-| [MMdnn][mmdnn] | [pytorch2keras][pytorch2keras]<br> [pytorch-tf][pytorch-tf] | [OpenCV AI (model converter)][opencv-ai-model_converter]<br> [brocolli][brocolli] | [paddle-cppt][paddle-cppt] |
| TensorFlow 1 | [MMdnn][mmdnn] | [MMdnn][mmdnn]<br> [tf_to_pytorch_model][tf_to_pytorch_model] | [MMdnn][mmdnn] |-| [TensorFlow Guide][tf-guide] | [tensorflow-onnx][tensorflow-onnx] |-|
| TensorFlow 2 |-| [NN tools][nn_tools] |-|-|-| [tensorflow-onnx][tensorflow-onnx] | [X2Paddle][X2Paddle] |
| ONNX     | [ONNX to MXNet guide][onnx2mxnet-guide] |-| [onnx2torch][onnx2torch] | [onnx-tensorflow][onnx-tensorflow] | [ONNX to TensorFlow2 Guide][onnx-tf]|-| [X2Paddle][X2Paddle] |
| PaddlePaddle |-|-|-|-|-| [Paddle2ONNX][Paddle2ONNX] |-|


<!-- LINKS -->
[mmdnn]: https://github.com/microsoft/MMdnn
[mxnet2caffe]: https://github.com/cypw/MXNet2Caffe
[mxnettocaffeconverter]: https://github.com/pertusa/MXNetToCaffeConverter
[gluon2pytorch]: https://github.com/gmalivenko/gluon2pytorch
[mxnet2onnx]: https://github.com/apache/mxnet/blob/master/python/mxnet/onnx
[caffemodel2pytorch]: https://github.com/vadimkantorov/caffemodel2pytorch
[Caffe2Pytorch]: https://github.com/penguinnnnn/Caffe2Pytorch
[nn_tools]: https://github.com/hahnyuan/nn_tools
[caffe-tensorflow]: https://github.com/ethereon/caffe-tensorflow
[caffe2onnx-1]: https://github.com/inisis/caffe2onnx
[caffe-onnx]: https://github.com/htshinichi/caffe-onnx
[caffe2onnx-2]: https://github.com/asiryan/caffe2onnx
[X2Paddle]: https://github.com/PaddlePaddle/X2Paddle
[brocolli]: https://github.com/inisis/brocolli/tree/master
[pytorch2caffe]: https://github.com/woodsgao/pytorch2caffe
[tf_to_pytorch_model]: https://github.com/ylhz/tf_to_pytorch_model
[tensorflow-onnx]: https://github.com/onnx/tensorflow-onnx
[onnx2torch]: https://github.com/ENOT-AutoDL/onnx2torch
[pytorch2keras]: https://github.com/gmalivenko/pytorch2keras
[pytorch-tf]: https://github.com/leonidk/pytorch-tf
[tf-guide]: https://www.tensorflow.org/guide/migrate/upgrade?hl=ru
[opencv-ai-model_converter]: https://github.com/opencv-ai/model_converter
[paddle-cppt]: https://github.com/wj-Mcat/paddle-cppt?ysclid=lnut6o3o6v87337456
[onnx2mxnet-guide]: https://mxnet.apache.org/versions/1.7/api/python/docs/tutorials/packages/onnx/inference_on_onnx_model.html
[onnx-tensorflow]: https://github.com/onnx/onnx-tensorflow
[onnx-tf]: https://lindevs.com/convert-onnx-format-to-tensorflow-2-model
[Paddle2ONNX]: https://github.com/PaddlePaddle/Paddle2ONNX
