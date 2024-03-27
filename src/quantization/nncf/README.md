# NNCF quantization script

Name of script:

```bash
quantization_nncf.py
```

Required arguments:

- `-c / --config` - path to the file containing information
  about quantization process in `xml` format. Template of the config
  located in `config_template.xml` file.

Description of parameters:

`Model` node contains information about model to be quantized:
- `ModelName` - name of the model.
- `ModelPath` - path to model in `.onnx`, `.xml` or `saved_model` formats.
- `WeightsPath` - path to weights in `.bin` format.
- `InputName` - input name of the model.
- `OutputName` - output name of the model.
- `InputShape` - input shape of the model.
- `Framework` - source framework of the model.
  Supported frameworks: onnx, tesnorflow, openvino.

`Dataset` node contains information about dataset for model calibration:
- `DatasetName` - name of dataset.
- `DatasetPath` - path to folder with input data.
- `Mean` - mean value for preprocessing data.
- `Std` - mean value for preprocessing data.
- `ImageSize` - image size value for preprocessing data. Example: 224, 224.
- `BatchSize` - size of input pack for model.
- `Layout` - dimension sequence for model input. NCHW, NHWC and etc.
- `Normalization` - flag to normalize input data.
- `ChannelSwap` - transpose for image channels. For RGB - 2, 1, 0. For BGR - 0, 1, 2.

`QuantizationParameters` node contains information about quantization parameters:
- `ModelType` - used to specify quantization scheme required for specific type of the model.
  For example, Transformer models (BERT, distillBERT, etc.) require a special quantization
  scheme to preserve accuracy after quantization.
- `Preset` - defines quantization scheme for the model.
  Two types of presets are available: MIXED, PERFOMANCE.
- `SubsetSize` - defines the number of samples from the calibration dataset
  that will be used to estimate quantization parameters of activations. 