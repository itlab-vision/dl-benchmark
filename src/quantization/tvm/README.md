# Apache TVM quantization script

Script name:

```bash
quantization_tvm.py
```

Required arguments:

- `-c / --config` is a path to the file containing information
  about quantization in the xml-format. Template of the configuration file
  located [here][config_path].

Description of parameters:

`Model` contains information about the model to be quantized:
- `Name` is a name of the model.
- `ModelJson` is a path to the model architecture (`.json` file).
- `WeightsParams` is a path to the model weights (`.params` file).

`Dataset` contains information about the dataset for model calibration:
- `Name` is a dataset name.
- `Path` is a path to the folder with input data.
- `Mean` is a mean value for preprocessing data.
- `Std` is a scale value for preprocessing data.
- `ImageResolution` is an image size value for preprocessing data. Example: 224, 224.
- `BatchSize` is an input batch size.
- `Layout` is a dimension sequence for the model input. NCHW, NHWC and etc.
- `Normalization` is a flag to normalize input data.
- `ChannelSwap` is a flag to transpose for image channels. For RGB - 2, 1, 0. For BGR - 0, 1, 2.

`QuantizationParameters` information about quantization parameters:
- `CalibSamples` is a number of input data for model calibration.
- `CalibMode` is a mode of the quantization. Supported modes: `kl_divergence`, `global_scale`.
- `WeightsScale` is a parameter for weights scaling. Supported modes: `power2`, `max`.
- `GlobalScale` is a parameter for the `global_scale` calibration mode.
- `DtypeInput`, `DtypeWeight`, `DtypeActivation` - data types for quantization.
  Supported types: `int8`, `int16`, `int32`.
- `PartitionConversions` is a parameter for TVM specific partition conversion.
  Supported modes: `enabled`, `disabled`, `fully_integral`.
- `OutputDirectory` is a directory for saving quantized model.

**Note:** currently, quantization based on Apache TVM does not work as expected due to
the several reasons:
- `kl_divergence` mode in the quantization process takes a lot of RAM at each
  new iteration of the calibration cycle. The problem is described [here][memory_leak].
  It means that you won't be able to use a lot of data for calibration.
- quantization in most cases breaks model which confirms the incorrectness of validation results.
  The `resnet` class of deep models work almost as expected.
- TVM quantization slows down inference time. This is due to an internal
  problem of the framework.


<!-- LINKS -->
[memory_leak]: https://ru.stackoverflow.com/questions/1569600/%d0%a3%d1%82%d0%b5%d1%87%d0%ba%d0%b0-%d0%bf%d0%b0%d0%bc%d1%8f%d1%82%d0%b8-%d0%b2-%d0%b8%d1%82%d0%b5%d1%80%d0%b0%d1%82%d0%be%d1%80%d0%b5-%d0%bf%d0%be-%d0%b4%d0%b0%d1%82%d0%b0%d1%81%d0%b5%d1%82%d1%83-python
[config_path]: ../../configs/tvm_quantization_config_template.xml
