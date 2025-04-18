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
- `PathPrefix` is a path to the model files without the extensions (.pdmodel, .pdiparams).
- `ModelDir` is a directory with the model.
- `ModelFileName` is a file name of the model description.
- `ParamsFileName` is a file name of the model parameters.
- `SaveDir` is a directory for the quantized model to be saved.

`Dataset` contains information about dataset for the model calibration:
- `Name` is a dataset name.
- `Path` is a path to the directory that contains input data.
- `Mean` is a mean value for preprocessing data.
- `Std` is a scale value for preprocessing data.
- `CropResolution` is a size of the image to which it will be cropped.
- `ResizeResolution` is an image size for preprocessing data. Example: 224, 224.
- `BatchSize` is a batch size.

`QuantizationParameters` contains information about the model input layer:
- `InputShape` is a shape of the model's input layer.
- `InputName` is a name of the model's input layer.


<!-- LINKS -->
[config_path]: ../../configs/paddle_quantization_config_template.xml
