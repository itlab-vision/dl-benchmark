# PaddlePaddle quantization script

Script name:

```bash
quantization_paddlepaddle.py
```

Required arguments:

- `-c / --config` is a path to the file containing information
  about quantization process in the xml-format. Template of the configuration file
  located [here][config_path].

Description of parameters:

`Model` contains information about model to be quantized:
- `Name` is a name of the model.
- `PathPrefix` is a path to the model files without the extensions (.pdmodel, .pdiparams).
- `ModelDir` is a directory with the model.
- `ModelFileName` is a file name of the model description.
- `ParamsFileName` is a file name of the model parameters.

`Dataset` contains information about dataset for the model calibration:
- `Name` is a dataset name.
- `Path` is a path to the directory that contains input data.
- `Mean` is a mean value for preprocessing data.
- `Std` is a scale value for preprocessing data.
- `ChannelSwap` is a flag to transpose for image channels. For RGB - 2, 1, 0. For BGR - 0, 1, 2.
- `ResizeResolution` is an image size for preprocessing data. Example: 224, 224.
- `BatchSize` is a batch size.
- `BatchNum` is the total number of batches

`QuantizationParameters` contains information about the model input layer:
- `InputShape` is a shape of the model's input layer.
- `InputName` is a name of the model's input layer.
- `SaveDir` is a directory for the quantized model to be saved.
- `Algorithm` specifies method to calculate the quantization scale factor. 
Available:  'KL', 'hist', 'mse', 'avg', 'abs_max'. Default: 'hist'.


<!-- LINKS -->
[config_path]: ../../configs/paddle_quantization_config_template.xml
