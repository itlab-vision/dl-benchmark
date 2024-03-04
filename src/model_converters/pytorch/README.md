# Установка конвертера

Командная строка:

```bash
pip install git+https://github.com/opencv-ai/model_converter
```

### Аргументы командной строки

Название скрипта:

```bash
convert_pytorch_to_onnx.py
```

Аргументы:

- `-mn / --model_name <Name of model>` - название модели
- `-w / --weights <Path to weights>` - путь до файла с весами в формате .pth
- `-b / --batch_size <Number of images>` - количество изображений, которые будут обработаны за один проход сети. По
  умолчанию равно 1
- `-is / --input_size <Dimensions input image>` - размеры входных изображений в формате [224,224]
- `-ch / --channels <Number of channels>` - количество каналов

**Пример запуска для resnet-50-pytorch**

```bash
python convert_pytorch_to_onnx.py -mn resnet50 \
          -w .\public\resnet-50-pytorch\resnet50-19c8e357.pth \
          -b 3 -is [224,224] -ch 3
```

## Валидация моделей

<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>

| Model    | PyTorch                                                                                                     | ONNX                                                                                                                               |
|:---------|:------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| resnet50 | 0.9278082 Granny Smith<br/>0.0129411 orange<br/>0.0059574 lemon<br/>0.0042141 necklace<br/>0.0025712 banana | 13.5817814 Granny Smith<br/>7.6410184 orange<br/>7.5275822 candle, taper, wax light<br/>7.4113483 croquet ball<br/>6.3414702 lemon |

<img width="150" src="images\ILSVRC2012_val_00000247.JPEG"></img>

| Model    | PyTorch                                                                                                                                                                            | ONNX                                                                                                                                                                                   |
|:---------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| resnet50 | 0.9805016 junco, snowbird<br/>0.0049154 goldfinch, Carduelis carduelis<br/>0.0039196 chickadee<br/>0.0038097 water ouzel, dipper<br/>0.0028983 brambling, Fringilla montifringilla | 15.3113270 junco, snowbird<br/>11.7624531 water ouzel, dipper<br/>10.3148956 brambling, Fringilla montifringilla<br/>10.1793890 chickadee<br/>9.5965061 goldfinch, Carduelis carduelis |


<img width="150" src="images\ILSVRC2012_val_00018592.JPEG"></img>

| Model    | PyTorch                                                                                                                                                                                                                                           | ONNX                                                                                                                                                                                                                                    |
|:---------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| resnet50 | 0.4759626 liner, ocean liner<br/>0.1025398 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0690002 container ship, containership, container vessel<br/>0.0524497 dock, dockage, docking facility<br/>0.0473783 pirate, pirate ship | 10.2766647 liner, ocean liner<br/>9.8022127 container ship, containership, container vessel<br/>8.9234753 drilling platform, offshore rig<br/>8.6592131 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>8.1166019 schooner |