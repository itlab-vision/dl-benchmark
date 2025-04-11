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
- `PathPrefix` path to the model files without the extensions (.pdmodel, .pdiparams).
- `ModelDir` is the name of the directory with the model.
- `ModelFileName` name of the file with the model description.
- `ParamsFileName` name of the file with the model parameters.
- `SaveDir` directory for the quantized model to be saved.

`Dataset` contains information about dataset for the model calibration:
- `Name` is a dataset name.
- `Path` is a path to the folder with input data.
- `Mean` is a mean value for preprocessing data.
- `Std` is a scale value for preprocessing data.
- `CropResolution` is a size for the image to which it will bw cropped.
- `ResizeResolution` is an image size for preprocessing data. Example: 224, 224.
- `BatchSize` is an input batch size.

`Parameters` contains information about model input layer:
- `InputShape` is the shape of the model's input layer.
- `InputName` is the name of the model's input layer.


<!-- LINKS -->
[config_path]: ../../configs/paddle_quantization_config_template.xml
