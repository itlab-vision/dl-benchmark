# NNCF quantization script

Script name:

```bash
quantization_nncf.py
```

Required arguments:

- `-c / --config` is a path to the file containing information
  about quantization process in the xml-format. Template of the configuration file
  located [here][config_path].

Description of parameters:

`Model` contains information about the model to be quantized:
- `Name` is a name of the model.
- `Path` is a path to the model in `.onnx`, `.xml` or `saved_model` formats.
- `WeightsPath` is a path to weights in `.bin` format.
- `InputName` is an input name of the model.
- `OutputName` is an output name of the model.
- `InputShape` is an input shape of the model.
- `Framework` is a source framework of the model.
  Supported frameworks: `onnx`, `tensorflow`, `openvino`.

`Dataset` contains information about the dataset for the model calibration:
- `Name` is a dataset name.
- `Path` is a path to the folder with input data.
- `Mean` is a mean value for preprocessing data.
- `Std` is a scale value for preprocessing data.
- `ImageResolution` is an image size value for preprocessing data. Example: 224, 224.
- `BatchSize` is an input batch size.
- `Layout` is a dimension sequence for the model input. NCHW, NHWC and etc.
- `Normalization` is a flag to normalize input data.
- `ChannelSwap` is a flag to transpose for image channels. For RGB - 2, 1, 0. For BGR - 0, 1, 2.

`QuantizationParameters` contains information about the quantization parameters:
- `ModelType` is a parameter used to specify quantization scheme required for specific type of the model.
  For example, Transformer models (BERT, distillBERT, etc.) require a special quantization
  scheme to preserve accuracy after quantization.
- `Preset` is a parameter which determines quantization scheme for the model.
  Two types of presets are available: `MIXED`, `PERFORMANCE`.
- `SubsetSize` is a parameter which determines the number of samples of the calibration dataset
  that will be used to estimate quantization parameters.


<!-- LINKS -->
[config_path]: ../../configs/nncf_quantization_config_template.xml