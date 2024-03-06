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

- `-mn / --model_name` - название модели.
- `-w / --weights` - путь до файла с весами в формате .pth.
- `-b / --batch_size` - количество изображений, которые будут обработаны за один проход сети. По
  умолчанию равно 1.
- `-is / --input_size` - размеры входных изображений в формате [224,224].
- `-ch / --channels` - количество каналов.

**Пример запуска для resnet-50-pytorch**

```bash
python convert_pytorch_to_onnx.py -mn resnet50 \
          -w .\public\resnet-50-pytorch\resnet50-19c8e357.pth \
          -b 3 -is [224,224] -ch 3
```

## Валидация моделей

### Тестовое изображение 1

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000023.JPEG"></img>

| Model        | PyTorch                                                                                                                         | ONNX                                                                                                                               |
|--------------|---------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| resnet50     | 0.9278082 Granny Smith<br/>0.0129411 orange<br/>0.0059574 lemon<br/>0.0042141 necklace<br/>0.0025712 banana                     | 13.5817814 Granny Smith<br/>7.6410184 orange<br/>7.5275822 candle, taper, wax light<br/>7.4113483 croquet ball<br/>6.3414702 lemon |
| mobilenet_v2 | 0.5066758 Granny Smith<br/>0.0543402 pitcher, ewer<br/>0.0461567 saltshaker, salt shaker<br/>0.0433899 lemon<br/>0.0314980 vase | 10.4182053 Granny Smith<br/>8.1723938 pitcher, ewer<br/>8.0274391 saltshaker, salt shaker<br/>7.9590530 lemon<br/>7.6285901 vase   |

### Тестовое изображение 2

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000247.JPEG"></img>

| Model        | PyTorch                                                                                                                                                                            | ONNX                                                                                                                                                                                    |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| resnet50     | 0.9805016 junco, snowbird<br/>0.0049154 goldfinch, Carduelis carduelis<br/>0.0039196 chickadee<br/>0.0038097 water ouzel, dipper<br/>0.0028983 brambling, Fringilla montifringilla | 15.3113270 junco, snowbird<br/>11.7624531 water ouzel, dipper<br/>10.3148956 brambling, Fringilla montifringilla<br/>10.1793890 chickadee<br/>9.5965061 goldfinch, Carduelis carduelis  |
| mobilenet_v2 | 0.9989254 junco, snowbird<br/>0.0004260 water ouzel, dipper<br/>0.0004213 chickadee<br/>0.0001264 brambling, Fringilla montifringilla<br/>0.0000537 goldfinch, Carduelis carduelis | 23.7004242 junco, snowbird<br/>15.8986778 water ouzel, dipper<br/>15.8818932 chickadee<br/>14.7394953 brambling, Fringilla montifringilla<br/>13.8446255 goldfinch, Carduelis carduelis |

### Тестовое изображение 3

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00018592.JPEG"></img>

| Model        | PyTorch                                                                                                                                                                                                                                                                | ONNX                                                                                                                                                                                                                                                                        |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| resnet50     | 0.4759626 liner, ocean liner<br/>0.1025398 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0690002 container ship, containership, container vessel<br/>0.0524497 dock, dockage, docking facility<br/>0.0473783 pirate, pirate ship                      | 10.2766647 liner, ocean liner<br/>9.8022127 container ship, containership, container vessel<br/>8.9234753 drilling platform, offshore rig<br/>8.6592131 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>8.1166019 schooner                                     |
| mobilenet_v2 | 0.3933905 container ship, containership, container vessel<br/>0.2136004 liner, ocean liner<br/>0.0991807 beacon, lighthouse, beacon light, pharos<br/>0.0715423 drilling platform, offshore rig<br/>0.0498365 breakwater, groin, groyne, mole, bulwark, seawall, jetty | 13.1233625 container ship, containership, container vessel<br/>12.5274086 liner, ocean liner<br/>11.7247705 beacon, lighthouse, beacon light, pharos<br/>11.4184551 drilling platform, offshore rig<br/>11.0241804 breakwater, groin, groyne, mole, bulwark, seawall, jetty |
