# Конвертер моделей из формата PyTorch в ONNX

## Установка пакета OpenCV AI Model Converter

Командная строка:

```bash
pip install git+https://github.com/opencv-ai/model_converter
```

## Запуск скрипта конвертации

Название скрипта:

```bash
convert_pytorch_to_onnx.py
```

**Аргументы:**

- `-mn / --model_name` - название модели.
- `-w / --weights` - путь до файла с весами в формате .pth.
- `-b / --batch_size` - количество изображений, которые будут обработаны за один проход сети.
  По умолчанию равно 1.
- `-is / --input_size` - разрешение изображений, подаваемых на вход сети, в формате `[w,h]`,
  где `w` - ширина изображения, `h` - высота изображения. Например, `[224,224]`.
- `-ch / --channels` - количество каналов.
- `-od / --output_dir` - путь для сохранения cконвертированной модели.

**Пример запуска для resnet-50-pytorch**

```bash
python convert_pytorch_to_onnx.py -mn resnet50 \
          -w .\public\resnet-50-pytorch\resnet50-19c8e357.pth \
          -b 3 -is [224,224] -ch 3
```

## Результаты валидация моделей из OpenVINO - Open Model Zoo

Ниже приведены результаты запуска вывода исходных моделей в формате PyTorch
и сконвертированных в ONNX-формат с использованием скриптов `inference_pytorch.py`
и `inference_onnx_runtime.py`.

### Тестовое изображение 1

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000023.JPEG"></img>

| Model | PyTorch | ONNX |
|-|-|-|
|alexnet|0.4499776 Granny Smith<br/>0.0933100 dumbbell<br/>0.0876727 ocarina, sweet potato<br/>0.0628701 hair slide<br/>0.0484684 bottlecap|14.6080303 Granny Smith<br/>13.0187969 dumbbell<br/>12.9655638 ocarina, sweet potato<br/>12.6147957 hair slide<br/>12.3638563 bottlecap|
|resnet18|0.1507517 safety pin<br/>0.1102253 piggy bank, penny bank<br/>0.0657375 purse<br/>0.0558251 teapot<br/>0.0341885 hair slide|8.4000969 piggy bank, penny bank<br/>7.7009411 safety pin<br/>6.8714881 dumbbell<br/>6.8444014 shopping basket<br/>6.6449137 teapot|
|resnet34|0.9595405 Granny Smith<br/>0.0054884 banana<br/>0.0043731 orange<br/>0.0035087 piggy bank, penny bank<br/>0.0025557 lemon|12.9089966 Granny Smith<br/>8.0390873 tennis ball<br/>7.6938391 piggy bank, penny bank<br/>7.0527048 vase<br/>6.9314356 orange|
|resnet50|0.9278082 Granny Smith<br/>0.0129411 orange<br/>0.0059574 lemon<br/>0.0042141 necklace<br/>0.0025712 banana|13.5817814 Granny Smith<br/>7.6410184 orange<br/>7.5275822 candle, taper, wax light<br/>7.4113483 croquet ball<br/>6.3414702 lemon|
|mobilenet_v2|0.5066758 Granny Smith<br/>0.0543402 pitcher, ewer<br/>0.0461567 saltshaker, salt shaker<br/>0.0433899 lemon<br/>0.0314980 vase|10.4182053 Granny Smith<br/>8.1723938 pitcher, ewer<br/>8.0274391 saltshaker, salt shaker<br/>7.9590530 lemon<br/>7.6285901 vase|

### Тестовое изображение 2

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000247.JPEG"></img>

| Model | PyTorch | ONNX |
|-|-|-|
|alexnet|0.9947647 junco, snowbird<br/>0.0043087 chickadee<br/>0.0002780 water ouzel, dipper<br/>0.0002770 bulbul<br/>0.0001244 brambling, Fringilla montifringilla|25.8481483 junco, snowbird<br/>20.3915386 chickadee<br/>17.6743641 water ouzel, dipper<br/>17.6708565 bulbul<br/>16.9173088 brambling, Fringilla montifringilla|
|resnet18|0.9991090 junco, snowbird<br/>0.0005329 chickadee<br/>0.0002098 water ouzel, dipper<br/>0.0000690 bulbul<br/>0.0000579 brambling, Fringilla montifringilla|22.8877964 junco, snowbird<br/>16.5202446 water ouzel, dipper<br/>16.2626171 chickadee<br/>15.1491690 brambling, Fringilla montifringilla<br/>14.2858706 bulbul|
|resnet34|0.9923637 junco, snowbird<br/>0.0043307 chickadee<br/>0.0011341 water ouzel, dipper<br/>0.0005041 brambling, Fringilla montifringilla<br/>0.0004572 goldfinch, Carduelis carduelis|13.8618135 junco, snowbird<br/>10.3889065 water ouzel, dipper<br/>10.3522301 chickadee<br/>9.1007729 brambling, Fringilla montifringilla<br/>8.2587948 house finch, linnet, Carpodacus mexicanus|
|resnet50|0.9805016 junco, snowbird<br/>0.0049154 goldfinch, Carduelis carduelis<br/>0.0039196 chickadee<br/>0.0038097 water ouzel, dipper<br/>0.0028983 brambling, Fringilla montifringilla|15.3113270 junco, snowbird<br/>11.7624531 water ouzel, dipper<br/>10.3148956 brambling, Fringilla montifringilla<br/>10.1793890 chickadee<br/>9.5965061 goldfinch, Carduelis carduelis|
|mobilenet_v2|0.9989254 junco, snowbird<br/>0.0004260 water ouzel, dipper<br/>0.0004213 chickadee<br/>0.0001264 brambling, Fringilla montifringilla<br/>0.0000537 goldfinch, Carduelis carduelis|23.7004242 junco, snowbird<br/>15.8986778 water ouzel, dipper<br/>15.8818932 chickadee<br/>14.7394953 brambling, Fringilla montifringilla<br/>13.8446255 goldfinch, Carduelis carduelis|

### Тестовое изображение 3

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00018592.JPEG"></img>

| Model | PyTorch | ONNX |
|-|-|-|
|alexnet|0.3216890 container ship, containership, container vessel<br/>0.1360616 drilling platform, offshore rig<br/>0.1140691 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1057471 beacon, lighthouse, beacon light, pharos<br/>0.0471225 liner, ocean liner|14.9870872 container ship, containership, container vessel<br/>14.1610689 drilling platform, offshore rig<br/>13.9586525 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>13.8987427 beacon, lighthouse, beacon light, pharos<br/>13.0810099 liner, ocean liner|
|resnet18|0.1980101 liner, ocean liner<br/>0.1092246 submarine, pigboat, sub, U-boat<br/>0.1024880 container ship, containership, container vessel<br/>0.1021964 drilling platform, offshore rig<br/>0.0800811 breakwater, groin, groyne, mole, bulwark, seawall, jetty|8.8410807 liner, ocean liner<br/>8.0653706 container ship, containership, container vessel<br/>7.9142728 drilling platform, offshore rig<br/>7.8061390 submarine, pigboat, sub, U-boat<br/>7.3510942 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
|resnet34|0.2605784 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1120404 fireboat<br/>0.1080513 liner, ocean liner<br/>0.0992256 pirate, pirate ship<br/>0.0759654 container ship, containership, container vessel|9.0904026 container ship, containership, container vessel<br/>8.5292053 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>8.4778986 liner, ocean liner<br/>8.2272568 fireboat<br/>7.5086846 beacon, lighthouse, beacon light, pharos|
|resnet50|0.4759626 liner, ocean liner<br/>0.1025398 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0690002 container ship, containership, container vessel<br/>0.0524497 dock, dockage, docking facility<br/>0.0473783 pirate, pirate ship|10.2766647 liner, ocean liner<br/>9.8022127 container ship, containership, container vessel<br/>8.9234753 drilling platform, offshore rig<br/>8.6592131 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>8.1166019 schooner|
|mobilenet_v2|0.3933905 container ship, containership, container vessel<br/>0.2136004 liner, ocean liner<br/>0.0991807 beacon, lighthouse, beacon light, pharos<br/>0.0715423 drilling platform, offshore rig<br/>0.0498365 breakwater, groin, groyne, mole, bulwark, seawall, jetty|13.1233625 container ship, containership, container vessel<br/>12.5274086 liner, ocean liner<br/>11.7247705 beacon, lighthouse, beacon light, pharos<br/>11.4184551 drilling platform, offshore rig<br/>11.0241804 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
