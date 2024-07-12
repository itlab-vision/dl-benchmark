# TensorFlow Lite quantization script

Script name:

```bash
quantization_tflite.py
```

Required arguments:

- `-c / --config` is a path to the file containing information
  about quantization process in the xml-format. Template of the configuration file
  located [here][config_path].

Description of parameters:

`Model` contains information about model to be quantized:
- `Name` is a name of the model.
- `Path` is a path to the model in the TensorFlow format `saved_model`.

`Dataset` contains information about dataset for the model calibration:
- `Name` is a dataset name.
- `Path` is a path to the folder with input data.
- `Mean` is a mean value for preprocessing data.
- `Std` is a scale value for preprocessing data.
- `ImageResolution` is an image size for preprocessing data. Example: 224, 224.
- `BatchSize` is an input batch size.
- `Layout` is a dimension sequence for the model input. NCHW, NHWC and etc.
- `Normalization` is a flag to normalize input data.
- `ChannelSwap` is a flag to transpose for image channels. For RGB - 2, 1, 0. For BGR - 0, 1, 2.

`QuantizationParameters` contains information about quantization parameters:
- `Optimizations` is a parameter used to specify quantization optimization.
  Supported optimizations: `['default'], ['latency'], ['size']`.
- `SupportedOperations` is a parameter which determines the data type of operations inside graph.
  Supported operations: `['int8'], ['int16']`.
- `SupportedTypes` is a parameter which determines the data type that will be used for
  calculations inside graph. Supported types: `['float16'], ['int8']`.


<!-- LINKS -->
[config_path]: ../../configs/tflite_quantization_config_template.xml
