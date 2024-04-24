# Конвертер моделей из формата Caffe в ONNX

## Загрузка репозитория с конвертером

Командная строка:

```bash
git clone https://github.com/asiryan/caffe2onnx
```

## Запуск скрипта конвертации

Название скрипта:

```bash
convert_caffe_to_onnx.py
```

**Аргументы:**

- `-pt / --prototxt` - путь до файла .prototxt.
- `-w / --weights` - путь до файла с весами в формате .caffemodel.
- `-od / --output_dir` - путь для сохранения конвертированной модели. 


**Пример запуска для alexnet**

```bash
python convert_caffe_to_onnx.py -pt ../public/alexnet/alexnet.prototxt \
                                -w ../public/alexnet/alexnet.caffemodel \
                                -od ./converted_models
```

## Результаты валидация моделей из OpenVINO - Open Model Zoo

Ниже приведены результаты запуска вывода исходных моделей в формате Caffe
и сконвертированных в ONNX-формат с использованием скриптов `inference_caffe.py`
и `inference_onnx_runtime.py`.

### Тестовое изображение 1

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000023.JPEG"></img>

| Model | PyTorch | ONNX |
|-|-|-|
|alexnet|0.9530122 Granny Smith<br/>0.0064442 piggy bank, penny bank<br/>0.0052059 candle, taper, wax light<br/>0.0034800 saltshaker, salt shaker<br/>0.0031893 bell pepper|0.9521239 Granny Smith<br/>0.0069122 piggy bank, penny bank<br/>0.0054333 candle, taper, wax light<br/>0.0037157 saltshaker, salt shaker<br/>0.0034601 tennis ball|
|googlenet-v1|0.9978739 Granny Smith<br/>0.0007978 bell pepper<br/>0.0007099 candle, taper, wax light<br/>0.0001017 tennis ball<br/>0.0000677 cucumber, cuke|0.9976688 Granny Smith<br/>0.0008829 bell pepper<br/>0.0007544 candle, taper, wax light<br/>0.0001104 tennis ball<br/>0.0000760 cucumber, cuke|
|squeezenet1.0|0.9988393 Granny Smith<br/>0.0002463 tennis ball<br/>0.0002324 piggy bank, penny bank<br/>0.0001979 bell pepper<br/>0.0001874 saltshaker, salt shaker|0.9992465 Granny Smith<br/>0.0001648 tennis ball<br/>0.0001631 bell pepper<br/>0.0001376 saltshaker, salt shaker<br/>0.0001081 piggy bank, penny bank|
|squeezenet1.1|0.9997335 Granny Smith<br/>0.0001555 tennis ball<br/>0.0000471 piggy bank, penny bank<br/>0.0000183 lemon<br/>0.0000110 banana|0.9995995 Granny Smith<br/>0.0002680 tennis ball<br/>0.0000614 fig<br/>0.0000253 lemon<br/>0.0000120 banana|

### Тестовое изображение 2

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000247.JPEG"></img>

| Model | PyTorch | ONNX |
|-|-|-|
|alexnet|0.9074045 junco, snowbird<br/>0.0894968 chickadee<br/>0.0013144 brambling, Fringilla montifringilla<br/>0.0007649 water ouzel, dipper<br/>0.0002242 bulbul|0.8866353 junco, snowbird<br/>0.1086869 chickadee<br/>0.0019401 brambling, Fringilla montifringilla<br/>0.0013517 water ouzel, dipper<br/>0.0002660 bulbul|
|googlenet-v1|0.9999721 junco, snowbird<br/>0.0000215 chickadee<br/>0.0000021 brambling, Fringilla montifringilla<br/>0.0000018 water ouzel, dipper<br/>0.0000016 house finch, linnet, Carpodacus mexicanus|0.9999763 junco, snowbird<br/>0.0000186 chickadee<br/>0.0000017 brambling, Fringilla montifringilla<br/>0.0000014 water ouzel, dipper<br/>0.0000013 house finch, linnet, Carpodacus mexicanus|
|squeezenet1.0|0.9693841 junco, snowbird<br/>0.0273032 chickadee<br/>0.0016394 brambling, Fringilla montifringilla<br/>0.0003912 jay<br/>0.0003850 bulbul|0.9669831 junco, snowbird<br/>0.0299459 chickadee<br/>0.0015737 brambling, Fringilla montifringilla<br/>0.0004190 bulbul<br/>0.0003177 jay|
|squeezenet1.1|0.9897038 junco, snowbird<br/>0.0095834 chickadee<br/>0.0003593 brambling, Fringilla montifringilla<br/>0.0001639 jay<br/>0.0001251 indigo bunting, indigo finch, indigo bird, Passerina cyanea|0.9902445 junco, snowbird<br/>0.0087432 chickadee<br/>0.0005967 brambling, Fringilla montifringilla<br/>0.0002337 jay<br/>0.0001153 indigo bunting, indigo finch, indigo bird, Passerina cyanea|



### Тестовое изображение 3

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00018592.JPEG"></img>

| Model | PyTorch | ONNX |
|-|-|-|
|alexnet|0.9386138 lifeboat<br/>0.0205405 container ship, containership, container vessel<br/>0.0077012 beacon, lighthouse, beacon light, pharos<br/>0.0068646 liner, ocean liner<br/>0.0063829 breakwater, groin, groyne, mole, bulwark, seawall, jetty|0.9570830 lifeboat<br/>0.0145343 container ship, containership, container vessel<br/>0.0057026 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0050276 beacon, lighthouse, beacon light, pharos<br/>0.0043955 liner, ocean liner|
|googlenet-v1|0.4716840 lifeboat<br/>0.1997744 drilling platform, offshore rig<br/>0.0902433 container ship, containership, container vessel<br/>0.0769801 liner, ocean liner<br/>0.0650747 beacon, lighthouse, beacon light, pharos|0.4912079 lifeboat<br/>0.1853296 drilling platform, offshore rig<br/>0.0932138 container ship, containership, container vessel<br/>0.0756837 liner, ocean liner<br/>0.0567754 beacon, lighthouse, beacon light, pharos|
|squeezenet1.0|0.5465039 liner, ocean liner<br/>0.2318359 lifeboat<br/>0.1140094 container ship, containership, container vessel<br/>0.0426976 beacon, lighthouse, beacon light, pharos<br/>0.0176553 drilling platform, offshore rig|0.4751489 liner, ocean liner<br/>0.2905613 lifeboat<br/>0.1737309 container ship, containership, container vessel<br/>0.0127517 beacon, lighthouse, beacon light, pharos<br/>0.0101217 fireboat|
|squeezenet1.1|0.7341899 drilling platform, offshore rig<br/>0.1093835 lifeboat<br/>0.0466753 liner, ocean liner<br/>0.0392822 perfume, essence<br/>0.0237168 beacon, lighthouse, beacon light, pharos|0.6992818 lifeboat<br/>0.1367242 drilling platform, offshore rig<br/>0.0986508 liner, ocean liner<br/>0.0202084 container ship, containership, container vessel<br/>0.0170820 submarine, pigboat, sub, U-boat|
