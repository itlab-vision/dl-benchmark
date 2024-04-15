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
--output ./resnet_v1-50.onnx \
--input_name map/TensorArrayStack/TensorArrayGatherV3:0 \
--input_shape [3,224,224,3] \
--output_name softmax_tensor:0
```

## Результаты валидации OMZ моделей 
Ниже приведены результаты запуска вывода исходных моделей в формате TensorFlow
и сконвертированных в ONNX-формат

### Тестовое изображение 1

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000023.JPEG"></img>

|Model|TensorFlow|ONNX|TensorFlow|
|-|-|-|-|
|densenet-121-tf|0.9505768 Granny Smith<br/>0.0134135 orange<br/>0.0113246 lemon<br/>0.0029127 banana<br/>0.0024542 piggy bank, penny bank|0.9505770 Granny Smith<br/>0.0134135 orange<br/>0.0113245 lemon<br/>0.0029127 banana<br/>0.0024542 piggy bank, penny bank|0.9505768 Granny Smith<br/>0.0134136 orange<br/>0.0113246 lemon<br/>0.0029127 banana<br/>0.0024542 piggy bank, penny bank|
|efficientnet-b0|10.7337656 Granny Smith<br/>4.8936868 lemon<br/>4.3447986 bell pepper<br/>4.3027477 orange<br/>4.2535620 piggy bank, penny bankenny bank|Error parsing message with type 'tensorflow.GraphDef'|
|googlenet-v1-tf|0.3726300 piggy bank, penny bank<br/>0.0828161 Granny Smith<br/>0.0738412 pitcher, ewer<br/>0.0618702 vase<br/>0.0468659 teapot|0.3726299 piggy bank, penny bank<br/>0.0828162 Granny Smith<br/>0.0738414 pitcher, ewer<br/>0.0618701 vase<br/>0.0468658 teapot|0.3726296 piggy bank, penny bank<br/>0.0828160 Granny Smith<br/>0.0738412 pitcher, ewer<br/>0.0618700 vase<br/>0.0468659 teapot|
|googlenet-v2-tf|0.9865645 Granny Smith<br/>0.0005240 pomegranate<br/>0.0005019 lemon<br/>0.0003612 banana<br/>0.0003478 piggy bank, penny bank|0.9865646 Granny Smith<br/>0.0005240 pomegranate<br/>0.0005019 lemon<br/>0.0003612 banana<br/>0.0003478 piggy bank, penny bank|
|googlenet-v3|0.8757076 Granny Smith<br/>0.0051826 ping-pong ball<br/>0.0043108 web site, website, internet site, site<br/>0.0029748 lemon<br/>0.0022498 dumbbell|0.8757075 Granny Smith<br/>0.0051826 ping-pong ball<br/>0.0043109 web site, website, internet site, site<br/>0.0029748 lemon<br/>0.0022498 dumbbell|
|googlenet-v4-tf|0.9970010 Granny Smith<br/>0.0001195 Rhodesian ridgeback<br/>0.0000487 hair slide<br/>0.0000475 pineapple, ananas<br/>0.0000329 banana|0.9970010 Granny Smith<br/>0.0001195 Rhodesian ridgeback<br/>0.0000487 hair slide<br/>0.0000475 pineapple, ananas<br/>0.0000329 banana|
|inception-resnet-v2-tf|9.1747894 Granny Smith<br/>4.0729280 pomegranate<br/>3.7423954 orange<br/>3.7375503 bell pepper<br/>3.6937828 piggy bank, penny bank|9.1747837 Granny Smith<br/>4.0729294 pomegranate<br/>3.7423978 orange<br/>3.7375493 bell pepper<br/>3.6937861 piggy bank, penny bank|
|mixnet-l|9.9219437 Granny Smith<br/>5.3626161 piggy bank, penny bank<br/>3.6792562 tennis ball<br/>3.5010076 syringe<br/>3.3666766 orange|Error parsing message with type 'tensorflow.GraphDef'|
|mobilenet-v1-1.0-224-tf|0.1770512 necklace<br/>0.1632509 saltshaker, salt shaker<br/>0.0681072 pitcher, ewer<br/>0.0600431 syringe<br/>0.0570385 Granny Smith|0.1770517 necklace<br/>0.1632508 saltshaker, salt shaker<br/>0.0681074 pitcher, ewer<br/>0.0600428 syringe<br/>0.0570387 Granny Smith|
|mobilenet-v2-1.0-224|0.8931149 Granny Smith<br/>0.0335340 piggy bank, penny bank<br/>0.0027360 saltshaker, salt shaker<br/>0.0021255 vase<br/>0.0016607 pitcher, ewer|0.8931142 Granny Smith<br/>0.0335344 piggy bank, penny bank<br/>0.0027360 saltshaker, salt shaker<br/>0.0021255 vase<br/>0.0016607 pitcher, ewer|
|mobilenet-v2-1.4-224|0.7240419 Granny Smith<br/>0.0312108 vase<br/>0.0237106 fig<br/>0.0122461 piggy bank, penny bank<br/>0.0118887 saltshaker, salt shaker|0.7240421 Granny Smith<br/>0.0312106 vase<br/>0.0237107 fig<br/>0.0122460 piggy bank, penny bank<br/>0.0118887 saltshaker, salt shaker|
|mobilenet-v3-small-1.0-224-tf|0.4645286 Granny Smith<br/>0.0864344 fig<br/>0.0757148 lemon<br/>0.0341503 orange<br/>0.0161915 banana|0.4645294 Granny Smith<br/>0.0864341 fig<br/>0.0757149 lemon<br/>0.0341502 orange<br/>0.0161916 banana|
|mobilenet-v3-large-1.0-224-tf|0.7446674 piggy bank, penny bank<br/>0.1191602 Granny Smith<br/>0.0230210 pomegranate<br/>0.0148820 vase<br/>0.0064742 lemon|0.7446690 piggy bank, penny bank<br/>0.1191586 Granny Smith<br/>0.0230210 pomegranate<br/>0.0148821 vase<br/>0.0064742 lemon|
|resnet-50-tf|0.9553036 Granny Smith<br/>0.0052123 lemon<br/>0.0047185 piggy bank, penny bank<br/>0.0045875 orange<br/>0.0044233 necklace|0.9553036 Granny Smith<br/>0.0052123 lemon<br/>0.0047185 piggy bank, penny bank<br/>0.0045875 orange<br/>0.0044233 necklace|0.9553036 Granny Smith<br/>0.0052123 lemon<br/>0.0047185 piggy bank, penny bank<br/>0.0045875 orange<br/>0.0044233 necklace|

### Тестовое изображение 2

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000247.JPEG"></img>

|Model|TensorFlow|ONNX|TensorFlow|
|-|-|-|-|
|densenet-121-tf|0.9821593 junco, snowbird<br/>0.0083621 chickadee<br/>0.0040121 brambling, Fringilla montifringilla<br/>0.0016480 water ouzel, dipper<br/>0.0015073 indigo bunting, indigo finch, indigo bird, Passerina cyanea|0.9821594 junco, snowbird<br/>0.0083621 chickadee<br/>0.0040121 brambling, Fringilla montifringilla<br/>0.0016479 water ouzel, dipper<br/>0.0015073 indigo bunting, indigo finch, indigo bird, Passerina cyanea|0.9821593 junco, snowbird<br/>0.0083621 chickadee<br/>0.0040121 brambling, Fringilla montifringilla<br/>0.0016480 water ouzel, dipper<br/>0.0015073 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
|efficientnet-b0|7.7920890 junco, snowbird<br/>5.7337265 chickadee<br/>5.4845700 water ouzel, dipper<br/>3.9789391 brambling, Fringilla montifringilla<br/>3.1936715 bulbul|Error parsing message with type 'tensorflow.GraphDef'|
|googlenet-v1-tf|0.7841159 junco, snowbird<br/>0.0522054 chickadee<br/>0.0302446 goldfinch, Carduelis carduelis<br/>0.0178083 brambling, Fringilla montifringilla<br/>0.0077449 jay|0.7841162 junco, snowbird<br/>0.0522053 chickadee<br/>0.0302445 goldfinch, Carduelis carduelis<br/>0.0178082 brambling, Fringilla montifringilla<br/>0.0077448 jay|0.7841162 junco, snowbird<br/>0.0522054 chickadee<br/>0.0302446 goldfinch, Carduelis carduelis<br/>0.0178082 brambling, Fringilla montifringilla<br/>0.0077448 jay|
|googlenet-v2-tf|0.9456245 junco, snowbird<br/>0.0047273 brambling, Fringilla montifringilla<br/>0.0040877 chickadee<br/>0.0012795 water ouzel, dipper<br/>0.0009381 loupe, jeweler's loupe|0.9456246 junco, snowbird<br/>0.0047273 brambling, Fringilla montifringilla<br/>0.0040877 chickadee<br/>0.0012795 water ouzel, dipper<br/>0.0009381 loupe, jeweler's loupe|
|googlenet-v3|0.6899885 junco, snowbird<br/>0.0630564 brambling, Fringilla montifringilla<br/>0.0239512 goldfinch, Carduelis carduelis<br/>0.0160590 water ouzel, dipper<br/>0.0052343 chickadee|0.6899880 junco, snowbird<br/>0.0630565 brambling, Fringilla montifringilla<br/>0.0239513 goldfinch, Carduelis carduelis<br/>0.0160590 water ouzel, dipper<br/>0.0052343 chickadee|
|googlenet-v4-tf|0.9349291 junco, snowbird<br/>0.0006724 chickadee<br/>0.0005267 brambling, Fringilla montifringilla<br/>0.0004872 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>0.0004374 water ouzel, dipper|0.9349288 junco, snowbird<br/>0.0006724 chickadee<br/>0.0005267 brambling, Fringilla montifringilla<br/>0.0004872 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>0.0004374 water ouzel, dipper|
|inception-resnet-v2-tf|10.2994804 junco, snowbird<br/>5.9667964 brambling, Fringilla montifringilla<br/>3.8809633 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>3.7881403 house finch, linnet, Carpodacus mexicanus<br/>3.4699862 goldfinch, Carduelis carduelis|10.2994804 junco, snowbird<br/>5.9667964 brambling, Fringilla montifringilla<br/>3.8809628 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>3.7881398 house finch, linnet, Carpodacus mexicanus<br/>3.4699855 goldfinch, Carduelis carduelis|
|mixnet-l|8.8130970 junco, snowbird<br/>6.1616135 brambling, Fringilla montifringilla<br/>6.1076593 water ouzel, dipper<br/>5.8892832 chickadee<br/>3.9943492 jay| Error parsing message with type 'tensorflow.GraphDef'|
|mobilenet-v1-1.0-224-tf|0.9816356 junco, snowbird<br/>0.0098165 house finch, linnet, Carpodacus mexicanus<br/>0.0030192 brambling, Fringilla montifringilla<br/>0.0022969 goldfinch, Carduelis carduelis<br/>0.0022401 chickadee|0.9816353 junco, snowbird<br/>0.0098165 house finch, linnet, Carpodacus mexicanus<br/>0.0030193 brambling, Fringilla montifringilla<br/>0.0022969 goldfinch, Carduelis carduelis<br/>0.0022402 chickadee|
|mobilenet-v2-1.0-224|0.8770279 junco, snowbird<br/>0.0143870 water ouzel, dipper<br/>0.0103317 chickadee<br/>0.0063064 brambling, Fringilla montifringilla<br/>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|0.8770282 junco, snowbird<br/>0.0143869 water ouzel, dipper<br/>0.0103318 chickadee<br/>0.0063063 brambling, Fringilla montifringilla<br/>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|
|mobilenet-v2-1.4-224|0.6637318 junco, snowbird<br/>0.0811646 chickadee<br/>0.0119593 water ouzel, dipper<br/>0.0038528 brambling, Fringilla montifringilla<br/>0.0022499 goldfinch, Carduelis carduelis|0.6637312 junco, snowbird<br/>0.0811648 chickadee<br/>0.0119593 water ouzel, dipper<br/>0.0038528 brambling, Fringilla montifringilla<br/>0.0022499 goldfinch, Carduelis carduelis|
|mobilenet-v3-small-1.0-224-tf|0.2142376 junco, snowbird<br/>0.1144335 brambling, Fringilla montifringilla<br/>0.0722249 chickadee<br/>0.0619252 goldfinch, Carduelis carduelis<br/>0.0210881 house finch, linnet, Carpodacus mexicanus|0.2142362 junco, snowbird<br/>0.1144338 brambling, Fringilla montifringilla<br/>0.0722247 chickadee<br/>0.0619252 goldfinch, Carduelis carduelis<br/>0.0210881 house finch, linnet, Carpodacus mexicanus|
|mobilenet-v3-large-1.0-224-tf|0.2724225 brambling, Fringilla montifringilla<br/>0.0370433 chickadee<br/>0.0286096 junco, snowbird<br/>0.0278493 goldfinch, Carduelis carduelis<br/>0.0167340 house finch, linnet, Carpodacus mexicanus|0.2724231 brambling, Fringilla montifringilla<br/>0.0370433 chickadee<br/>0.0286094 junco, snowbird<br/>0.0278492 goldfinch, Carduelis carduelis<br/>0.0167339 house finch, linnet, Carpodacus mexicanus|
|resnet-50-tf|0.9983400 junco, snowbird<br/>0.0004680 brambling, Fringilla montifringilla<br/>0.0003848 chickadee<br/>0.0003656 water ouzel, dipper<br/>0.0003383 goldfinch, Carduelis carduelis|0.9983401 junco, snowbird<br/>0.0004680 brambling, Fringilla montifringilla<br/>0.0003848 chickadee<br/>0.0003656 water ouzel, dipper<br/>0.0003383 goldfinch, Carduelis carduelis|0.9983400 junco, snowbird<br/>0.0004680 brambling, Fringilla montifringilla<br/>0.0003848 chickadee<br/>0.0003656 water ouzel, dipper<br/>0.0003383 goldfinch, Carduelis carduelis|

### Тестовое изображение 3

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00018592.JPEG"></img>

|Model|TensorFlow|ONNX|TensorFlow|
|-|-|-|-|
|densenet-121-tf|0.3172949 liner, ocean liner<br/>0.1268195 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1153852 container ship, containership, container vessel<br/>0.0765769 drilling platform, offshore rig<br/>0.0727640 dock, dockage, docking facility|0.3172937 liner, ocean liner<br/>0.1268198 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1153852 container ship, containership, container vessel<br/>0.0765764 drilling platform, offshore rig<br/>0.0727642 dock, dockage, docking facility|0.3172949 liner, ocean liner<br/>0.1268195 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1153848 container ship, containership, container vessel<br/>0.0765768 drilling platform, offshore rig<br/>0.0727641 dock, dockage, docking facility|
|efficientnet-b0|6.3308716 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>5.6206541 beacon, lighthouse, beacon light, pharos<br/>5.5816445 liner, ocean liner<br/>5.2046542 submarine, pigboat, sub, U-boat<br/>5.1616168 lifeboat|Error parsing message with type 'tensorflow.GraphDef'|
|googlenet-v1-tf|0.0967501 liner, ocean liner<br/>0.0910910 drilling platform, offshore rig<br/>0.0798566 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0455458 submarine, pigboat, sub, U-boat<br/>0.0451497 container ship, containership, container vessel|0.0967506 liner, ocean liner<br/>0.0910910 drilling platform, offshore rig<br/>0.0798564 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0455458 submarine, pigboat, sub, U-boat<br/>0.0451497 container ship, containership, container vessel|0.0967505 liner, ocean liner<br/>0.0910910 drilling platform, offshore rig<br/>0.0798564 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0455459 submarine, pigboat, sub, U-boat<br/>0.0451498 container ship, containership, container vessel|
|googlenet-v2-tf|0.2603647 container ship, containership, container vessel<br/>0.1645859 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0890378 dock, dockage, docking facility<br/>0.0779068 liner, ocean liner<br/>0.0392493 beacon, lighthouse, beacon light, pharos|0.2603651 container ship, containership, container vessel<br/>0.1645859 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0890375 dock, dockage, docking facility<br/>0.0779066 liner, ocean liner<br/>0.0392492 beacon, lighthouse, beacon light, pharos|
|googlenet-v3|0.5695390 beacon, lighthouse, beacon light, pharos<br/>0.2797679 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0335406 liner, ocean liner<br/>0.0090760 submarine, pigboat, sub, U-boat<br/>0.0064661 wreck|0.5695392 beacon, lighthouse, beacon light, pharos<br/>0.2797675 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0335406 liner, ocean liner<br/>0.0090761 submarine, pigboat, sub, U-boat<br/>0.0064661 wreck|
|googlenet-v4-tf|0.6699104 lifeboat<br/>0.0414714 submarine, pigboat, sub, U-boat<br/>0.0301792 fireboat<br/>0.0262586 beacon, lighthouse, beacon light, pharos<br/>0.0132693 drilling platform, offshore rig|0.6699125 lifeboat<br/>0.0414711 submarine, pigboat, sub, U-boat<br/>0.0301790 fireboat<br/>0.0262584 beacon, lighthouse, beacon light, pharos<br/>0.0132692 drilling platform, offshore rig|
|inception-resnet-v2-tf|6.6930823 fireboat<br/>6.1025157 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>6.0896263 lifeboat<br/>5.7389731 container ship, containership, container vessel<br/>5.4940572 dock, dockage, docking facility|6.6930847 fireboat<br/>6.1025162 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>6.0896235 lifeboat<br/>5.7389698 container ship, containership, container vessel<br/>5.4940567 dock, dockage, docking facility|
|mixnet-l|9.2674913 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>8.2079716 beacon, lighthouse, beacon light, pharos<br/>4.3137717 container ship, containership, container vessel<br/>4.1218119 submarine, pigboat, sub, U-boat<br/>3.9396579 promontory, headland, head, foreland| Error parsing message with type 'tensorflow.GraphDef'|
|mobilenet-v1-1.0-224-tf|0.3753883 liner, ocean liner<br/>0.1239906 lifeboat<br/>0.1208320 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0891696 beacon, lighthouse, beacon light, pharos<br/>0.0568045 fireboat|0.3753898 liner, ocean liner<br/>0.1239900 lifeboat<br/>0.1208323 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0891688 beacon, lighthouse, beacon light, pharos<br/>0.0568043 fireboat|
|mobilenet-v2-1.0-224|0.1885895 beacon, lighthouse, beacon light, pharos<br/>0.1434041 liner, ocean liner<br/>0.0768167 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0497301 drilling platform, offshore rig<br/>0.0225758 container ship, containership, container vessel|0.1885887 beacon, lighthouse, beacon light, pharos<br/>0.1434043 liner, ocean liner<br/>0.0768168 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0497301 drilling platform, offshore rig<br/>0.0225758 container ship, containership, container vessel|
|mobilenet-v2-1.4-224|0.1300137 container ship, containership, container vessel<br/>0.0765783 lifeboat<br/>0.0406069 dock, dockage, docking facility<br/>0.0393022 drilling platform, offshore rig<br/>0.0381022 liner, ocean liner|0.1300134 container ship, containership, container vessel<br/>0.0765785 lifeboat<br/>0.0406070 dock, dockage, docking facility<br/>0.0393022 drilling platform, offshore rig<br/>0.0381023 liner, ocean liner|
|mobilenet-v3-small-1.0-224-tf|0.0979414 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0626709 beacon, lighthouse, beacon light, pharos<br/>0.0593548 drilling platform, offshore rig<br/>0.0590084 container ship, containership, container vessel<br/>0.0566022 liner, ocean liner|0.0979413 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0626709 beacon, lighthouse, beacon light, pharos<br/>0.0593547 drilling platform, offshore rig<br/>0.0590082 container ship, containership, container vessel<br/>0.0566021 liner, ocean liner|
|mobilenet-v3-large-1.0-224-tf|0.2032553 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1777074 liner, ocean liner<br/>0.0806113 submarine, pigboat, sub, U-boat<br/>0.0757664 beacon, lighthouse, beacon light, pharos<br/>0.0406716 dock, dockage, docking facility|0.2032563 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1777067 liner, ocean liner<br/>0.0806108 submarine, pigboat, sub, U-boat<br/>0.0757670 beacon, lighthouse, beacon light, pharos<br/>0.0406716 dock, dockage, docking facility|
|resnet-50-tf|0.2357710 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1480761 liner, ocean liner<br/>0.1104689 container ship, containership, container vessel<br/>0.1095407 drilling platform, offshore rig<br/>0.0915569 beacon, lighthouse, beacon light, pharos|0.2357716 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1480758 liner, ocean liner<br/>0.1104690 container ship, containership, container vessel<br/>0.1095406 drilling platform, offshore rig<br/>0.0915569 beacon, lighthouse, beacon light, pharos|0.2357710 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1480760 liner, ocean liner<br/>0.1104689 container ship, containership, container vessel<br/>0.1095406 drilling platform, offshore rig<br/>0.0915569 beacon, lighthouse, beacon light, pharos|
