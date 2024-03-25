# Конвертер моделей из формата TensorFlow в ONNX

## Запуск скрипта конвертации

Название скрипта:

```bash
convert_tf_to_onnx.py
```

**Аргументы:**

- `--graphdef` - Path to the TensorFlow model graphdef file.
- `--output` - Path to save the converted ONNX model.
- `--input_name` - Name of the input tensor.
- `--input_shape` - Shape of the input tensor as a Python list. Should be in the format "[batch_size, height, width, channels]".
- `--output_name` - Name of the output tensor.

**Пример запуска для resnet-50-tf**

```bash
python convert_tf_to_onnx.py \
--graphdef ./public/resnet-50-tf/resnet_v1-50.pb \
--output ./resnet_v1_1-50.onnx \
--input_name map/TensorArrayStack/TensorArrayGatherV3:0 \
--input_shape [3,224,224,3] \
--output_name softmax_tensor:0
```

## Результаты валидации OMZ моделей 
Ниже приведены результаты запуска вывода исходных моделей в формате TensorFlow
и сконвертированных в ONNX-формат

### Тестовое изображение 1

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000023.JPEG"></img>

|Model|TensorFlow|ONNX|
|-|-|-|
|inception-resnet-v2-tf|9.1747894 Granny Smith<br/>4.0729280 pomegranate<br/>3.7423954 orange<br/>3.7375503 bell pepper<br/>3.6937828 piggy bank, penny bank|9.1747837 Granny Smith<br/>4.0729294 pomegranate<br/>3.7423978 orange<br/>3.7375493 bell pepper<br/>3.6937861 piggy bank, penny bank|
|resnet-50-tf|0.9553036 Granny Smith<br/>0.0052123 lemon<br/>0.0047185 piggy bank, penny bank<br/>0.0045875 orange<br/>0.0044233 necklace|0.9553036 Granny Smith<br/>0.0052123 lemon<br/>0.0047185 piggy bank, penny bank<br/>0.0045875 orange<br/>0.0044233 necklace|
|mobilenet-v1-1.0-224-tf|0.1770512 necklace<br/>0.1632509 saltshaker, salt shaker<br/>0.0681072 pitcher, ewer<br/>0.0600431 syringe<br/>0.0570385 Granny Smith|0.1770517 necklace<br/>0.1632508 saltshaker, salt shaker<br/>0.0681074 pitcher, ewer<br/>0.0600428 syringe<br/>0.0570387 Granny Smith|
|mobilenet-v2-1.0-224|0.8931149 Granny Smith<br/>0.0335340 piggy bank, penny bank<br/>0.0027360 saltshaker, salt shaker<br/>0.0021255 vase<br/>0.0016607 pitcher, ewer|0.8931142 Granny Smith<br/>0.0335344 piggy bank, penny bank<br/>0.0027360 saltshaker, salt shaker<br/>0.0021255 vase<br/>0.0016607 pitcher, ewer|
|mobilenet-v2-1.4-224|0.7240419 Granny Smith<br/>0.0312108 vase<br/>0.0237106 fig<br/>0.0122461 piggy bank, penny bank<br/>0.0118887 saltshaker, salt shaker|0.7240421 Granny Smith<br/>0.0312106 vase<br/>0.0237107 fig<br/>0.0122460 piggy bank, penny bank<br/>0.0118887 saltshaker, salt shaker|
|googlenet-v3|0.8757076 Granny Smith<br/>0.0051826 ping-pong ball<br/>0.0043108 web site, website, internet site, site<br/>0.0029748 lemon<br/>0.0022498 dumbbell|0.8757075 Granny Smith<br/>0.0051826 ping-pong ball<br/>0.0043109 web site, website, internet site, site<br/>0.0029748 lemon<br/>0.0022498 dumbbell|


### Тестовое изображение 2

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000247.JPEG"></img>

|Model|TensorFlow|ONNX|
|-|-|-|
|inception-resnet-v2-tf|10.2994804 junco, snowbird<br/>5.9667964 brambling, Fringilla montifringilla<br/>3.8809633 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>3.7881403 house finch, linnet, Carpodacus mexicanus<br/>3.4699862 goldfinch, Carduelis carduelis|10.2994804 junco, snowbird<br/>5.9667964 brambling, Fringilla montifringilla<br/>3.8809628 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>3.7881398 house finch, linnet, Carpodacus mexicanus<br/>3.4699855 goldfinch, Carduelis carduelis|
|resnet-50-tf|0.9983400 junco, snowbird<br/>0.0004680 brambling, Fringilla montifringilla<br/>0.0003848 chickadee<br/>0.0003656 water ouzel, dipper<br/>0.0003383 goldfinch, Carduelis carduelis|0.9983401 junco, snowbird<br/>0.0004680 brambling, Fringilla montifringilla<br/>0.0003848 chickadee<br/>0.0003656 water ouzel, dipper<br/>0.0003383 goldfinch, Carduelis carduelis|
|mobilenet-v1-1.0-224-tf|0.9816356 junco, snowbird<br/>0.0098165 house finch, linnet, Carpodacus mexicanus<br/>0.0030192 brambling, Fringilla montifringilla<br/>0.0022969 goldfinch, Carduelis carduelis<br/>0.0022401 chickadee|0.9816353 junco, snowbird<br/>0.0098165 house finch, linnet, Carpodacus mexicanus<br/>0.0030193 brambling, Fringilla montifringilla<br/>0.0022969 goldfinch, Carduelis carduelis<br/>0.0022402 chickadee|
|mobilenet-v2-1.0-224|0.8770279 junco, snowbird<br/>0.0143870 water ouzel, dipper<br/>0.0103317 chickadee<br/>0.0063064 brambling, Fringilla montifringilla<br/>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|0.8770282 junco, snowbird<br/>0.0143869 water ouzel, dipper<br/>0.0103318 chickadee<br/>0.0063063 brambling, Fringilla montifringilla<br/>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|
|mobilenet-v2-1.4-224|0.6637318 junco, snowbird<br/>0.0811646 chickadee<br/>0.0119593 water ouzel, dipper<br/>0.0038528 brambling, Fringilla montifringilla<br/>0.0022499 goldfinch, Carduelis carduelis|0.6637312 junco, snowbird<br/>0.0811648 chickadee<br/>0.0119593 water ouzel, dipper<br/>0.0038528 brambling, Fringilla montifringilla<br/>0.0022499 goldfinch, Carduelis carduelis|
|googlenet-v3|0.6899885 junco, snowbird<br/>0.0630564 brambling, Fringilla montifringilla<br/>0.0239512 goldfinch, Carduelis carduelis<br/>0.0160590 water ouzel, dipper<br/>0.0052343 chickadee|0.6899880 junco, snowbird<br/>0.0630565 brambling, Fringilla montifringilla<br/>0.0239513 goldfinch, Carduelis carduelis<br/>0.0160590 water ouzel, dipper<br/>0.0052343 chickadee|


### Тестовое изображение 3

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00018592.JPEG"></img>

|Model|TensorFlow|ONNX|
|-|-|-|
|inception-resnet-v2-tf|6.6930823 fireboat<br/>6.1025157 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>6.0896263 lifeboat<br/>5.7389731 container ship, containership, container vessel<br/>5.4940572 dock, dockage, docking facility|6.6930847 fireboat<br/>6.1025162 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>6.0896235 lifeboat<br/>5.7389698 container ship, containership, container vessel<br/>5.4940567 dock, dockage, docking facility|
|resnet-50-tf|0.2357710 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1480761 liner, ocean liner<br/>0.1104689 container ship, containership, container vessel<br/>0.1095407 drilling platform, offshore rig<br/>0.0915569 beacon, lighthouse, beacon light, pharos|0.2357716 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1480758 liner, ocean liner<br/>8.9234753 drilling platform, offshore rig<br/>0.1104690 container ship, containership, container vessel<br/>0.1095406 drilling platform, offshore rig<br/>0.0915569 beacon, lighthouse, beacon light, pharos|
|mobilenet-v1-1.0-224-tf|0.3753883 liner, ocean liner<br/>0.1239906 lifeboat<br/>0.1208320 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0891696 beacon, lighthouse, beacon light, pharos<br/>0.0568045 fireboat|0.3753898 liner, ocean liner<br/>0.1239900 lifeboat<br/>0.1208323 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0891688 beacon, lighthouse, beacon light, pharos<br/>0.0568043 fireboat|
|mobilenet-v2-1.0-224|0.1885895 beacon, lighthouse, beacon light, pharos<br/>0.1434041 liner, ocean liner<br/>0.0768167 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0497301 drilling platform, offshore rig<br/>0.0225758 container ship, containership, container vessel|0.1885887 beacon, lighthouse, beacon light, pharos<br/>0.1434043 liner, ocean liner<br/>0.0768168 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0497301 drilling platform, offshore rig<br/>0.0225758 container ship, containership, container vessel|
|mobilenet-v2-1.4-224|0.1300137 container ship, containership, container vessel<br/>0.0765783 lifeboat<br/>0.0406069 dock, dockage, docking facility<br/>0.0393022 drilling platform, offshore rig<br/>0.0381022 liner, ocean liner|0.1300134 container ship, containership, container vessel<br/>0.0765785 lifeboat<br/>0.0406070 dock, dockage, docking facility<br/>0.0393022 drilling platform, offshore rig<br/>0.0381023 liner, ocean liner|
|googlenet-v3|0.5695390 beacon, lighthouse, beacon light, pharos<br/>0.2797679 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0335406 liner, ocean liner<br/>0.0090760 submarine, pigboat, sub, U-boat<br/>0.0064661 wreck|0.5695392 beacon, lighthouse, beacon light, pharos<br/>0.2797675 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0335406 liner, ocean liner<br/>0.0090761 submarine, pigboat, sub, U-boat<br/>0.0064661 wreck|

