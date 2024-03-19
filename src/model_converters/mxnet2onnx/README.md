# Конвертер моделей из формата MXNet в ONNX

## Установка пакета ...

## Запуск скрипта конвертации

Название скрипта:

```bash
convert_mxnet_to_onnx.py
```

**Обязательные аргументы:**

- `-m / --model` – путь до описания архитектуры обученной модели, которое хранятся в файле расширением `.json`.
- `-w / --weights` – путь до весов обученной модели, которые хранятся в файле расширением `.params`.
- `-is / --input_shape` – размеры входного тензора сети в формате BxCxWxH, B - размер пачки, C - количество каналов
  изображений, W - ширина изображений, H - высота изображений.

**Опциональные аргументы:**

- `-p / --path_save_model` – путь для сохранения модели в файл с расширением `.onnx`. По умолчанию модель в
  файле `model.onnx` сохраняется в текущей директории.

**Пример запуска**

```bash
python3 convert_mxnet_to_onnx.py \
  --model ./mobilenetv2_1.0/mobilenetv2_1.0-symbol.json \
  --weights ./mobilenetv2_1.0/mobilenetv2_1.0-0000.params \
  --input_shape 3 3 224 224 \
  --path_save_model ./mobilenetv2_1.0/mobilenetv2_1.0.onnx
```

## Валидация моделей

### Тестовое изображение 1

<img width="150" src="../../../results/validation/images/ILSVRC2012_val_00000023.JPEG" alt="Granny Smith"/>

| Model | MXNet | ONNX |
|-|-|-|
| alexnet         | 0.4499778 Granny Smith<br/>0.0933102 dumbbell<br/>0.0876724 ocarina, sweet potato<br/>0.0628703 hair slide<br/>0.0484684 bottlecap | 14.5664158 Granny Smith<br/>12.9931412 dumbbell<br/>12.9308310 ocarina, sweet potato<br/>12.5982876 hair slide<br/>12.3381243 bottlecap |
| darknet53       | 0.5883058 Granny Smith<br/>0.0645481 candle, taper, wax light<br/>0.0236042 piggy bank, penny bank<br/>0.0160968 pencil sharpener<br/>0.0060462 vase | 8.0624456 Granny Smith<br/>5.8526053 candle, taper, wax light<br/>4.8466167 piggy bank, penny bank<br/>4.4638152 pencil sharpener<br/>3.4846244 vase |
| densenet121     | 0.9523344 Granny Smith<br/>0.0132273 orange<br/>0.0125171 lemon<br/>0.0027910 banana<br/>0.0020333 piggy bank, penny bank | 13.6940823 Granny Smith<br/>9.4174452 orange<br/>9.3622561 lemon<br/>7.8615537 banana<br/>7.5448380 piggy bank, penny bank |
| densenet161     | 0.9372969 Granny Smith<br/>0.0082274 dumbbell<br/>0.0056475 piggy bank, penny bank<br/>0.0055374 ping-pong ball<br/>0.0041915 pitcher, ewer | 14.1544456 Granny Smith<br/>9.4189034 dumbbell<br/>9.0426502 piggy bank, penny bank<br/>9.0229673 ping-pong ball<br/>8.7444944 pitcher, ewer |
| densenet169     | 0.9811631 Granny Smith<br/>0.0033828 piggy bank, penny bank<br/>0.0021366 orange<br/>0.0019196 lemon<br/>0.0017232 pomegranate | 13.5430756 Granny Smith<br/>7.8730474 piggy bank, penny bank<br/>7.4135370 orange<br/>7.3064761 lemon<br/>7.1985321 pomegranate |
| densenet201     | 0.9119797 Granny Smith<br/>0.0533454 piggy bank, penny bank<br/>0.0056832 lemon<br/>0.0017810 pool table, billiard table, snooker table<br/>0.0015689 tennis ball | 12.3925571 Granny Smith<br/>9.5537291 piggy bank, penny bank<br/>7.3144350 lemon<br/>6.1541257 pool table, billiard table, snooker table<br/>6.0273290 tennis ball |
| googlenet       | 0.2217809 Granny Smith<br/>0.2117919 piggy bank, penny bank<br/>0.0270375 dumbbell<br/>0.0116782 saltshaker, salt shaker<br/>0.0108081 candle, taper, wax light | 6.9259710 Granny Smith<br/>6.8798828 piggy bank, penny bank<br/>4.8215041 dumbbell<br/>3.9819989 saltshaker, salt shaker<br/>3.9045718 candle, taper, wax light |
| mobilenetv2_1.0 | 0.6325442 Granny Smith<br/>0.0556754 piggy bank, penny bank<br/>0.0443766 lemon<br/>0.0086360 teapot<br/>0.0071484 vase | 8.4786644 Granny Smith<br/>6.0484524 piggy bank, penny bank<br/>5.8216305 lemon<br/>4.1848660 teapot<br/>3.9958169 vase |
| resnet50_v1     | 0.7377543 Granny Smith<br/>0.0241721 piggy bank, penny bank<br/>0.0123405 lemon<br/>0.0061283 candle, taper, wax light<br/>0.0051573 orange | 8.7972584 Granny Smith<br/>5.3788500 piggy bank, penny bank<br/>4.7065377 lemon<br/>4.0065680 candle, taper, wax light<br/>3.8340609 orange |

### Тестовое изображение 2

<img width="150" src="../../../results/validation/images/ILSVRC2012_val_00000247.JPEG" alt="junco, snowbird"/>

| Model | MXNet | ONNX |
|-|-|-|
| alexnet         | 0.9947649 junco, snowbird<br/>0.0043087 chickadee<br/>0.0002780 water ouzel, dipper<br/>0.0002770 bulbul<br/>0.0001244 brambling, Fringilla montifringilla | 25.8981895 junco, snowbird<br/>20.4563198 chickadee<br/>17.7155762 water ouzel, dipper<br/>17.7121067 bulbul<br/>16.9112091 brambling, Fringilla montifringilla |
| darknet53       | 0.8250283 junco, snowbird<br/>0.0037126 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>0.0019864 brambling, Fringilla montifringilla<br/>0.0017965 water ouzel, dipper<br/>0.0015356 American coot, marsh hen, mud hen, water hen, Fulica americana | 8.7164316 junco, snowbird<br/>3.3127527 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>2.6873569 brambling, Fringilla montifringilla<br/>2.5868781 water ouzel, dipper<br/>2.4299037 American coot, marsh hen, mud hen, water hen, Fulica americana |
| densenet121     | 0.9841599 junco, snowbird<br/>0.0072199 chickadee<br/>0.0034962 brambling, Fringilla montifringilla<br/>0.0016226 water ouzel, dipper<br/>0.0012858 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 16.4804840 junco, snowbird<br/>11.5655289 chickadee<br/>10.8403816 brambling, Fringilla montifringilla<br/>10.0727234 water ouzel, dipper<br/>9.8400936 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
| densenet161     | 0.9932058 junco, snowbird<br/>0.0015922 chickadee<br/>0.0012295 brambling, Fringilla montifringilla<br/>0.0011838 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>0.0008891 goldfinch, Carduelis carduelis | 15.8273029 junco, snowbird<br/>9.3914623 chickadee<br/>9.1329803 brambling, Fringilla montifringilla<br/>9.0950556 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br/>8.8088274 goldfinch, Carduelis carduelis |
| densenet169     | 0.9640697 junco, snowbird<br/>0.0201313 brambling, Fringilla montifringilla<br/>0.0044098 chickadee<br/>0.0032345 goldfinch, Carduelis carduelis<br/>0.0026739 water ouzel, dipper | 14.9900427 junco, snowbird<br/>11.1211624 brambling, Fringilla montifringilla<br/>9.6027203 chickadee<br/>9.2927465 goldfinch, Carduelis carduelis<br/>9.1024170 water ouzel, dipper |
| densenet201     | 0.9515250 junco, snowbird<br/>0.0178252 water ouzel, dipper<br/>0.0109119 brambling, Fringilla montifringilla<br/>0.0077980 house finch, linnet, Carpodacus mexicanus<br/>0.0044695 chickadee | 14.0531406 junco, snowbird<br/>10.0756855 water ouzel, dipper<br/>9.5849304 brambling, Fringilla montifringilla<br/>9.2489452 house finch, linnet, Carpodacus mexicanus<br/>8.6923532 chickadee |
| googlenet       | 0.8450467 junco, snowbird<br/>0.0073040 brambling, Fringilla montifringilla<br/>0.0059225 chickadee<br/>0.0033832 goldfinch, Carduelis carduelis<br/>0.0031529 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 9.3441095 junco, snowbird<br/>4.5931382 brambling, Fringilla montifringilla<br/>4.3834758 chickadee<br/>3.8235426 goldfinch, Carduelis carduelis<br/>3.7530253 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
| mobilenetv2_1.0 | 0.8265611 junco, snowbird<br/>0.0339170 chickadee<br/>0.0146587 brambling, Fringilla montifringilla<br/>0.0095486 water ouzel, dipper<br/>0.0065168 hummingbird | 9.4582558 junco, snowbird<br/>6.2648902 chickadee<br/>5.4260073 brambling, Fringilla montifringilla<br/>4.9973755 water ouzel, dipper<br/>4.6153593 hummingbird |
| resnet50_v1     | 0.8778600 junco, snowbird<br/>0.0045333 water ouzel, dipper<br/>0.0018932 brambling, Fringilla montifringilla<br/>0.0016121 chickadee<br/>0.0005472 magpie | 9.2806330 junco, snowbird<br/>4.0145960 water ouzel, dipper<br/>3.1413941 brambling, Fringilla montifringilla<br/>2.9806654 chickadee<br/>1.9002029 magpie |

### Тестовое изображение 3

<img width="150" src="../../../results/validation/images/ILSVRC2012_val_00018592.JPEG" alt="liner, ocean liner"/>

| Model | MXNet | ONNX |
|-|-|-|
| alexnet         | 0.3216886 container ship, containership, container vessel<br/>0.1360614 drilling platform, offshore rig<br/>0.1140694 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1057478 beacon, lighthouse, beacon light, pharos<br/>0.0471224 liner, ocean liner | 15.0291624 container ship, containership, container vessel<br/>14.1686888 drilling platform, offshore rig<br/>13.9923830 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>13.9166307 beacon, lighthouse, beacon light, pharos<br/>13.1083269 liner, ocean liner |
| darknet53       | 0.1329412 liner, ocean liner<br/>0.1074721 dock, dockage, docking facility<br/>0.1047859 drilling platform, offshore rig<br/>0.0996367 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0419424 lifeboat | 6.3090272 liner, ocean liner<br/>6.0963483 dock, dockage, docking facility<br/>6.0710344 drilling platform, offshore rig<br/>6.0206494 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>5.1554117 lifeboat |
| densenet121     | 0.3022410 liner, ocean liner<br/>0.1322484 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1194606 container ship, containership, container vessel<br/>0.0795041 drilling platform, offshore rig<br/>0.0723068 dock, dockage, docking facility | 10.3178215 liner, ocean liner<br/>9.4912720 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>9.3895817 container ship, containership, container vessel<br/>8.9823990 drilling platform, offshore rig<br/>8.8875132 dock, dockage, docking facility |
| densenet161     | 0.4418391 lifeboat<br/>0.1824287 liner, ocean liner<br/>0.0596467 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0325274 submarine, pigboat, sub, U-boat<br/>0.0298845 dock, dockage, docking facility | 9.6051064 lifeboat<br/>8.7205181 liner, ocean liner<br/>7.6025920 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>6.9962387 submarine, pigboat, sub, U-boat<br/>6.9114966 dock, dockage, docking facility |
| densenet169     | 0.2955866 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.2342385 drilling platform, offshore rig<br/>0.0940928 liner, ocean liner<br/>0.0876009 container ship, containership, container vessel<br/>0.0717737 dock, dockage, docking facility | 10.4923067 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>10.2596855 drilling platform, offshore rig<br/>9.3476305 liner, ocean liner<br/>9.2761393 container ship, containership, container vessel<br/>9.0768690 dock, dockage, docking facility |
| densenet201     | 0.5008176 fireboat<br/>0.0950196 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0701646 lifeboat<br/>0.0622607 liner, ocean liner<br/>0.0582344 container ship, containership, container vessel | 11.2358389 fireboat<br/>9.5736847 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>9.2704401 lifeboat<br/>9.1509256 liner, ocean liner<br/>9.0840759 container ship, containership, container vessel |
| googlenet       | 0.0838070 lifeboat<br/>0.0731668 container ship, containership, container vessel<br/>0.0730509 liner, ocean liner<br/>0.0729539 fireboat<br/>0.0689271 drilling platform, offshore rig | 6.2486143 lifeboat<br/>6.1128383 container ship, containership, container vessel<br/>6.1112595 liner, ocean liner<br/>6.1099296 fireboat<br/>6.0531454 drilling platform, offshore rig |
| mobilenetv2_1.0 | 0.1127411 liner, ocean liner<br/>0.1014166 container ship, containership, container vessel<br/>0.0582132 submarine, pigboat, sub, U-boat<br/>0.0552070 lifeboat<br/>0.0221046 breakwater, groin, groyne, mole, bulwark, seawall, jetty | 5.7730365 liner, ocean liner<br/>5.6671801 container ship, containership, container vessel<br/>5.1120577 submarine, pigboat, sub, U-boat<br/>5.0590348 lifeboat<br/>4.1437297 breakwater, groin, groyne, mole, bulwark, seawall, jetty |
| resnet50_v1     | 0.4411839 liner, ocean liner<br/>0.0861827 container ship, containership, container vessel<br/>0.0609572 speedboat<br/>0.0587049 dock, dockage, docking facility<br/>0.0369093 breakwater, groin, groyne, mole, bulwark, seawall, jetty | 8.7759809 liner, ocean liner<br/>7.1429935 container ship, containership, container vessel<br/>6.7966938 speedboat<br/>6.7590456 dock, dockage, docking facility<br/>6.2949839 breakwater, groin, groyne, mole, bulwark, seawall, jetty |
