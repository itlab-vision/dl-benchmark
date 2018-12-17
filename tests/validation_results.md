# Результаты проверки корректности вывода с использованием разных режимов

## Результаты классификации

### Тестовое изображение 1

Источник: набор данных [ImageNet][imagenet]

Разрешение: 709 x 510
﻿

<img src="..\data\ILSVRC2012_val_00000023.JPEG" width="150">


   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |  Python (синхронный режим)  |  Python (асинхронный режим)        |
---------------------|---------------------------|---------------------------|-----------------------------|------------------------------------|
alexnet              |                           |                           |                             | 0.9896094 Granny Smith<br>0.0037969 bell pepper<br>0.0013717 piggy bank, penny bank<br>0.0011059 acorn<br>0.0009710 fig|
densenet-121         |                           |                           |                             | 15.7979155 Granny Smith<br>9.9429502 lemon<br>9.3676109 orange<br>8.6181631 banana<br>7.1164064 tennis ball|
densenet-161         |                           |                           |                             | 17.8060360 Granny Smith<br>8.5503101 lemon<br>7.6080236 orange<br>7.2737904 banana<br>7.1114841 fig|
densenet-169         |                           |                           |                             | 15.9379444 Granny Smith<br>6.3490100 banana<br>6.2573524 lemon<br>5.8869252 tennis ball<br>5.7489195 piggy bank, penny bank|
densenet-201         |                           |                           |                             | 13.9142380 Granny Smith<br>7.1571240 bell pepper<br>6.8382263 acorn<br>6.0525231 lemon<br>6.0489964 candle, taper, wax light|
googlenet-v1         |                           |                           |                             | 0.9982972 Granny Smith<br>0.0005613 bell pepper<br>0.0003487 candle, taper, wax light<br>0.0000679 tennis ball<br>0.0000656 piggy bank, penny bank|
googlenet-v2         |                           |                           |                             | 0.9938846 leafhopper<br>0.0042250 police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria<br>0.0005423 ringlet, ringlet butterfly<br>0.0001996 lacewing, lacewing fly<br>0.0000883 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk|
googlenet-v3         |                           |                           |                             | 0.9909641 strawberry<br>0.0007918 binder, ring-binder<br>0.0001872 pill bottle<br>0.0001239 banjo<br>0.0000879 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
googlenet-v4         |                           |                           |                             | 0.9865599 Granny Smith<br>0.0003842 Rhodesian ridgeback<br>0.0002123 hair slide<br>0.0001513 pineapple, ananas<br>0.0001259 banana|
inception-resnet v2  |                           |                           |                             | 0.9982988 Granny Smith<br>0.0000684 orange<br>0.0000573 lemon<br>0.0000441 banana<br>0.0000164 Band Aid|
resnet-v1-50         |                           |                           |                             | 0.1277410 banana<br>0.1127741 Granny Smith<br>0.0634984 tennis ball<br>0.0430243 hook, claw<br>0.0374066 safety pin|
resnet-v1-101        |                           |                           |                             | 0.9928156 Granny Smith<br>0.0040912 fig<br>0.0009257 jackfruit, jak, jack<br>0.0006793 lemon<br>0.0003674 banana|
resnet-v1-152        |                           |                           |                             | 0.7078060 Granny Smith<br>0.1253216 gong, tam-tam<br>0.0107064 water jug<br>0.0105488 tennis ball<br>0.0088276 coffeepot|
squeezenet-1.0       |                           |                           |                             | 0.9988525 Granny Smith<br>0.0004736 fig<br>0.0001965 bell pepper<br>0.0000892 piggy bank, penny bank<br>0.0000732 tennis ball|
squeezenet-1.1       |                           |                           |                             | 0.9937357 Granny Smith<br>0.0014752 lemon<br>0.0013913 fig<br>0.0008874 tennis ball<br>0.0006791 piggy bank, penny bank|
vgg-16               |                           |                           |                             | 0.7317340 Granny Smith<br>0.0350751 bell pepper<br>0.0209236 grocery store, grocery, food market, market<br>0.0137958 saltshaker, salt shaker<br>0.0127183 fig|
vgg-19               |                           |                           |                             | 0.7072726 Granny Smith<br>0.0805918 acorn<br>0.0473263 fig<br>0.0367725 necklace<br>0.0180316 lemon|

### Тестовое изображение 2

Источник: набор данных [ImageNet][imagenet]

Разрешение: 500 x 500
﻿

<img src="..\data\ILSVRC2012_val_00000247.JPEG" width="150">

   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |                           |                           |                              | 0.9979280 junco, snowbird<br>0.0020288 chickadee<br>0.0000137 jay<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000104 bulbul|
densenet-121         |                           |                           |                              | 17.8269730 junco, snowbird<br>11.4734774 brambling, Fringilla montifringilla<br>11.3202305 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3598871 chickadee<br>8.2504835 magpie|
densenet-161         |                           |                           |                              | 18.9021950 junco, snowbird<br>12.8945827 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7353134 chickadee<br>9.5253277 brambling, Fringilla montifringilla<br>8.7536573 goldfinch, Carduelis carduelis|
densenet-169         |                           |                           |                              | 18.5059853 junco, snowbird<br>11.6154289 brambling, Fringilla montifringilla<br>11.0603485 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.9430408 goldfinch, Carduelis carduelis<br>8.9175758 chickadee|
densenet-201         |                           |                           |                              | 17.9479065 junco, snowbird<br>9.7838707 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.6706047 brambling, Fringilla montifringilla<br>8.9102554 house finch, linnet, Carpodacus mexicanus<br>8.2559891 chickadee|
googlenet-v1         |                           |                           |                              | 0.9999954 junco, snowbird<br>0.0000043 chickadee<br>0.0000003 brambling, Fringilla montifringilla<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000000 water ouzel, dipper|
googlenet-v2         |                           |                           |                              | 0.9986847 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004460 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0002120 barracouta, snoek<br>0.0001153 apron<br>0.0000563 basketball|
googlenet-v3         |                           |                           |                              | 0.9241988 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005938 cliff dwelling<br>0.0005932 bustard<br>0.0005757 jack-o'-lantern<br>0.0005057 kite|
googlenet-v4         |                           |                           |                              | 0.9338045 junco, snowbird<br>0.0005343 hamster<br>0.0005193 chickadee<br>0.0004287 brambling, Fringilla montifringilla<br>0.0003747 koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus|
inception-resnet v2  |                           |                           |                              | 0.9995075 junco, snowbird<br>0.0000257 brambling, Fringilla montifringilla<br>0.0000219 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000217 chickadee<br>0.0000119 water ouzel, dipper|
resnet-v1-50         |                           |                           |                              | 0.9975340 junco, snowbird<br>0.0012899 chickadee<br>0.0007322 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003813 brambling, Fringilla montifringilla<br>0.0000160 bulbul|
resnet-v1-101        |                           |                           |                              | 0.9994646 junco, snowbird<br>0.0001720 brambling, Fringilla montifringilla<br>0.0001495 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001213 chickadee<br>0.0000216 water ouzel, dipper|
resnet-v1-152        |                           |                           |                              | 0.9961376 junco, snowbird<br>0.0013669 chickadee<br>0.0008338 brambling, Fringilla montifringilla<br>0.0005274 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002985 water ouzel, dipper|
squeezenet-1.0       |                           |                           |                              | 0.9931427 junco, snowbird<br>0.0064122 chickadee<br>0.0003084 brambling, Fringilla montifringilla<br>0.0000394 bulbul<br>0.0000340 magpie|
squeezenet-1.1       |                           |                           |                              | 0.9949970 junco, snowbird<br>0.0048571 chickadee<br>0.0000578 jay<br>0.0000297 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000271 brambling, Fringilla montifringilla|
vgg-16               |                           |                           |                              | 0.9999772 junco, snowbird<br>0.0000132 brambling, Fringilla montifringilla<br>0.0000089 chickadee<br>0.0000006 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
vgg-19               |                           |                           |                              | 0.9999394 junco, snowbird<br>0.0000580 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|

### Тестовое изображение 3

Источник: набор данных [ImageNet][imagenet]

Разрешение: 333 x 500
﻿

<img src="..\data\ILSVRC2012_val_00018592.JPEG" width="150">

   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |                           |                           |                              | 0.9991654 lifeboat<br>0.0003741 container ship, containership, container vessel<br>0.0001206 pirate, pirate ship<br>0.0000820 drilling platform, offshore rig<br>0.0000784 wreck|
densenet-121         |                           |                           |                              | 13.9662342 lifeboat<br>7.8177428 drilling platform, offshore rig<br>7.7323399 liner, ocean liner<br>7.5702839 wreck<br>7.5621653 pirate, pirate ship|
densenet-161         |                           |                           |                              | 15.5664644 lifeboat<br>7.2549510 liner, ocean liner<br>6.7164927 fireboat<br>6.2500734 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.2465792 dock, dockage, docking facility|
densenet-169         |                           |                           |                              | 15.3814812 lifeboat<br>10.0849428 drilling platform, offshore rig<br>9.4490099 container ship, containership, container vessel<br>9.1608076 pirate, pirate ship<br>8.3062334 beacon, lighthouse, beacon light, pharos|
densenet-201         |                           |                           |                              | 16.1351070 lifeboat<br>8.5620880 fireboat<br>8.3413410 drilling platform, offshore rig<br>8.1058598 liner, ocean liner<br>7.8472009 container ship, containership, container vessel|
googlenet-v1         |                           |                           |                              | 0.8990629 lifeboat<br>0.0275983 drilling platform, offshore rig<br>0.0209237 beacon, lighthouse, beacon light, pharos<br>0.0196472 container ship, containership, container vessel<br>0.0062734 liner, ocean liner|
googlenet-v2         |                           |                           |                              | 0.9919641 miniature pinscher<br>0.0011945 pier<br>0.0007550 submarine, pigboat, sub, U-boat<br>0.0005916 Saint Bernard, St Bernard<br>0.0005792 Rottweiler|
googlenet-v3         |                           |                           |                              | 0.9595628 lighter, light, igniter, ignitor<br>0.0016150 bakery, bakeshop, bakehouse<br>0.0007223 beaker<br>0.0005667 breastplate, aegis, egis<br>0.0003984 fire engine, fire truck|
googlenet-v4         |                           |                           |                              | 0.9513763 lifeboat<br>0.0005698 fireboat<br>0.0004419 submarine, pigboat, sub, U-boat<br>0.0004226 ambulance<br>0.0004161 drilling platform, offshore rig|
inception-resnet v2  |                           |                           |                              | 0.9981461 lifeboat<br>0.0006250 beacon, lighthouse, beacon light, pharos<br>0.0001983 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0001903 drilling platform, offshore rig<br>0.0001606 fireboat|
resnet-v1-50         |                           |                           |                              | 0.8872181 lifeboat<br>0.0398498 liner, ocean liner<br>0.0237534 container ship, containership, container vessel<br>0.0125247 dock, dockage, docking facility<br>0.0107783 drilling platform, offshore rig|
resnet-v1-101        |                           |                           |                              | 0.6138141 lifeboat<br>0.1049523 drilling platform, offshore rig<br>0.0466761 liner, ocean liner<br>0.0327781 dock, dockage, docking facility<br>0.0284106 aircraft carrier, carrier, flattop, attack aircraft carrier|
resnet-v1-152        |                           |                           |                              | 0.9505481 lifeboat<br>0.0083380 drilling platform, offshore rig<br>0.0072418 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0049709 container ship, containership, container vessel<br>0.0041877 liner, ocean liner|
squeezenet-1.0       |                           |                           |                              | 0.9870804 lifeboat<br>0.0061878 container ship, containership, container vessel<br>0.0025447 fireboat<br>0.0024638 liner, ocean liner<br>0.0004083 beacon, lighthouse, beacon light, pharos|
squeezenet-1.1       |                           |                           |                              | 0.9570300 lifeboat<br>0.0211559 container ship, containership, container vessel<br>0.0102894 drilling platform, offshore rig<br>0.0034316 pirate, pirate ship<br>0.0029378 dock, dockage, docking facility|
vgg-16               |                           |                           |                              | 0.9821915 lifeboat<br>0.0082832 container ship, containership, container vessel<br>0.0014539 drilling platform, offshore rig<br>0.0014494 pirate, pirate ship<br>0.0009578 liner, ocean liner|
vgg-19               |                           |                           |                              | 0.9965214 lifeboat<br>0.0008823 container ship, containership, container vessel<br>0.0004778 drilling platform, offshore rig<br>0.0003970 dock, dockage, docking facility<br>0.0003622 fireboat|


<!-- LINKS -->
[imagenet]: http://www.image-net.org