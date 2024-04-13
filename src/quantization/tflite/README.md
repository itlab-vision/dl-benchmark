# TFLITE quantization script

Name of script:

```bash
quantization_tflite.py
```

Required arguments:

- `-c / --config` is a path to the file containing information
  about quantization process in `xml` format. Template of the config
  located in `config_template.xml` file.

Description of parameters:

`Model` contains information about model to be quantized:
- `ModelName` is a name of the model.
- `ModelPath` is a path to the model in tensorflow `saved_model` format.

`Dataset` contains information about dataset for model calibration:
- `DatasetName` is a dataset name.
- `DatasetPath` is a path to the folder with input data.
- `Mean` is a mean value for preprocessing data.
- `Std` is a scale value for preprocessing data.
- `ImageSize` is an image size value for preprocessing data. Example: 224, 224.
- `BatchSize` is an input batch size.
- `Layout` is a dimension sequence for the model input. NCHW, NHWC and etc.
- `Normalization` is a flag to normalize input data.
- `ChannelSwap` is a flag to transpose for image channels. For RGB - 2, 1, 0. For BGR - 0, 1, 2.

`QuantizationParameters` contains information about quantization parameters:
- `Optimizations` is a parameter used to specify quantization optimization.
  Supported optimizations: `['default'], ['latency'], ['size']`.
- `SupportedOperations` is a parameter defines data type of operations inside graph.
  Supported operations: `['int8'], ['int16']`.
- `SupportedTypes` is a parameter defines data type that will be the main one in the
  calculation process inside graph. Supported types: `['float16'], ['int8']`.