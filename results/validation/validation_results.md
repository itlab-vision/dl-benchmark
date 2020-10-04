# Проверка корректности вывода для публичных моделей с использованием разных режимов

## Результаты классификации

### Тестовое изображение 1

Источник: набор данных [ImageNet][imagenet]

Исходное разрешение: 709 x 510
﻿

Изображение:

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|---------------------------|---------------------------|-----------------------------|------------------------------------|
alexnet              |0.9896095 Granny Smith<br>0.0037969 bell pepper<br>0.0013717 piggy bank, penny bank<br>0.0011059 acorn<br>0.0009710 fig| 0.9896095 Granny Smith<br>0.0037969 bell pepper<br>0.0013717 piggy bank, penny bank<br>0.0011059 acorn<br>0.0009710 fig|0.9896094 Granny Smith<br>0.0037969 bell pepper<br>0.0013717 piggy bank, penny bank<br>0.0011059 acorn<br>0.0009710 fig| 0.9896094 Granny Smith<br>0.0037969 bell pepper<br>0.0013717 piggy bank, penny bank<br>0.0011059 acorn<br>0.0009710 fig|
densenet-121         |15.7979164 Granny Smith<br>9.9429455 lemon<br>9.3676043 orange<br>8.6181612 banana<br>7.1164074 tennis ball| 15.7979164 Granny Smith<br>9.9429455 lemon<br>9.3676043 orange<br>8.6181612 banana<br>7.1164074 tennis ball|15.7979164 Granny Smith<br>9.9429455 lemon<br>9.3676043 orange<br>8.6181612 banana<br>7.1164074 tennis ball| 15.7979155 Granny Smith<br>9.9429502 lemon<br>9.3676109 orange<br>8.6181631 banana<br>7.1164064 tennis ball|
densenet-161         |17.8060474 Granny Smith<br>8.5503120 lemon<br>7.6080256 orange<br>7.2737975 banana<br>7.1114807 fig| 17.8060474 Granny Smith<br>8.5503120 lemon<br>7.6080256 orange<br>7.2737975 banana<br>7.1114807 fig|17.8060474 Granny Smith<br>8.5503120 lemon<br>7.6080256 orange<br>7.2737975 banana<br>7.1114807 fig| 17.8060360 Granny Smith<br>8.5503101 lemon<br>7.6080236 orange<br>7.2737904 banana<br>7.1114841 fig|
densenet-169         |15.9379349 Granny Smith<br>6.3490119 banana<br>6.2573476 lemon<br>5.8869209 tennis ball<br>5.7489214 piggy bank, penny bank| 15.9379349 Granny Smith<br>6.3490119 banana<br>6.2573476 lemon<br>5.8869209 tennis ball<br>5.7489214 piggy bank, penny bank|15.9379349 Granny Smith<br>6.3490119 banana<br>6.2573476 lemon<br>5.8869209 tennis ball<br>5.7489214 piggy bank, penny bank| 15.9379444 Granny Smith<br>6.3490100 banana<br>6.2573524 lemon<br>5.8869252 tennis ball<br>5.7489195 piggy bank, penny bank|
densenet-201         |13.9142466 Granny Smith<br>7.1571245 bell pepper<br>6.8382354 acorn<br>6.0525250 lemon<br>6.0490065 candle, taper, wax light| 13.9142380 Granny Smith<br>7.1571240 bell pepper<br>6.8382263 acorn<br>6.0525231 lemon<br>6.0489964 candle, taper, wax light|13.9142466 Granny Smith<br>7.1571245 bell pepper<br>6.8382354 acorn<br>6.0525250 lemon<br>6.0490065 candle, taper, wax light| 13.9142380 Granny Smith<br>7.1571240 bell pepper<br>6.8382263 acorn<br>6.0525231 lemon<br>6.0489964 candle, taper, wax light|
googlenet-v1         |0.9982976 Granny Smith<br>0.0005613 bell pepper<br>0.0003487 candle, taper, wax light<br>0.0000679 tennis ball<br>0.0000656 piggy bank, penny bank| 0.9982976 Granny Smith<br>0.0005613 bell pepper<br>0.0003487 candle, taper, wax light<br>0.0000679 tennis ball<br>0.0000656 piggy bank, penny bank|0.9982972 Granny Smith<br>0.0005613 bell pepper<br>0.0003487 candle, taper, wax light<br>0.0000679 title tennis ball<br>0.0000656 title piggy bank, penny bank| 0.9982972 Granny Smith<br>0.0005613 bell pepper<br>0.0003487 candle, taper, wax light<br>0.0000679 tennis ball<br>0.0000656 piggy bank, penny bank|
googlenet-v2         |0.9938872 leafhopper<br>0.0042250 police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria<br>0.0005423 ringlet, ringlet butterfly<br>0.0001996 lacewing, lacewing fly<br>0.0000883 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk| 0.9938872 leafhopper<br>0.0042250 police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria<br>0.0005423 ringlet, ringlet butterfly<br>0.0001996 lacewing, lacewing fly<br>0.0000883 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk|0.9938846 leafhopper<br>0.0042250 police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria<br>0.0005423 ringlet, ringlet butterfly<br>0.0001996 lacewing, lacewing fly<br>0.0000883 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk| 0.9938846 leafhopper<br>0.0042250 police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria<br>0.0005423 ringlet, ringlet butterfly<br>0.0001996 lacewing, lacewing fly<br>0.0000883 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk|
googlenet-v3         |0.9909649 strawberry<br>0.0007918 binder, ring-binder<br>0.0001872 pill bottle<br>0.0001239 banjo<br>0.0000879 breakwater, groin, groyne, mole, bulwark, seawall, jetty| 0.9909649 strawberry<br>0.0007918 binder, ring-binder<br>0.0001872 pill bottle<br>0.0001239 banjo<br>0.0000879 breakwater, groin, groyne, mole, bulwark, seawall, jetty|0.9909641 strawberry<br>0.0007918 binder, ring-binder<br>0.0001872 pill bottle<br>0.0001239 banjo<br>0.0000879 breakwater, groin, groyne, mole, bulwark, seawall, jetty| 0.9909641 strawberry<br>0.0007918 binder, ring-binder<br>0.0001872 pill bottle<br>0.0001239 banjo<br>0.0000879 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
googlenet-v4         |0.9865599 Granny Smith<br>0.0003842 Rhodesian ridgeback<br>0.0002123 hair slide<br>0.0001513 pineapple, ananas<br>0.0001259 banana| 0.9865599 Granny Smith<br>0.0003842 Rhodesian ridgeback<br>0.0002123 hair slide<br>0.0001513 pineapple, ananas<br>0.0001259 banana|0.9865599 Granny Smith<br>0.0003842 Rhodesian ridgeback<br>0.0002123 hair slide<br>0.0001513 pineapple, ananas<br>0.0001259 banana| 0.9865599 Granny Smith<br>0.0003842 Rhodesian ridgeback<br>0.0002123 hair slide<br>0.0001513 pineapple, ananas<br>0.0001259 banana|
inception-resnet v2  |0.9982991 Granny Smith<br>0.0000684 orange<br>0.0000573 lemon<br>0.0000441 banana<br>0.0000164 Band Aid| 0.9982991 Granny Smith<br>0.0000684 orange<br>0.0000573 lemon<br>0.0000441 banana<br>0.0000164 Band Aid|0.9982988 Granny Smith<br>0.0000684 orange<br>0.0000573 lemon<br>0.0000441 banana<br>0.0000164 Band Aid| 0.9982988 Granny Smith<br>0.0000684 orange<br>0.0000573 lemon<br>0.0000441 banana<br>0.0000164 Band Aid|
resnet-v1-50         |0.1277409 banana<br>0.1127750 Granny Smith<br>0.0634985 tennis ball<br>0.0430244 hook, claw<br>0.0374065 safety pin| 0.1277411 banana<br>0.1127749 Granny Smith<br>0.0634985 tennis ball<br>0.0430244 hook, claw<br>0.0374065 safety pin|0.1277409 banana<br>0.1127749 Granny Smith<br>0.0634985 tennis ball<br>0.0430244 hook, claw<br>0.0374065 safety pin| 0.1277410 banana<br>0.1127741 Granny Smith<br>0.0634984 tennis ball<br>0.0430243 hook, claw<br>0.0374066 safety pin|
resnet-v1-101        |0.9928160 Granny Smith<br>0.0040912 fig<br>0.0009257 jackfruit, jak, jack<br>0.0006793 lemon<br>0.0003674 banana| 0.9928160 Granny Smith<br>0.0040912 fig<br>0.0009257 jackfruit, jak, jack<br>0.0006793 lemon<br>0.0003674 banana|0.9928156 Granny Smith<br>0.0040912 fig<br>0.0009257 jackfruit, jak, jack<br>0.0006793 lemon<br>0.0003674 banana| 0.9928156 Granny Smith<br>0.0040912 fig<br>0.0009257 jackfruit, jak, jack<br>0.0006793 lemon<br>0.0003674 banana|
resnet-v1-152        |0.7078071 Granny Smith<br>0.1253208 gong, tam-tam<br>0.0107065 water jug<br>0.0105488 tennis ball<br>0.0088276 coffeepot| 0.7078074 Granny Smith<br>0.1253207 gong, tam-tam<br>0.0107064 water jug<br>0.0105488 tennis ball<br>0.0088276 coffeepot|0.7078072 Granny Smith<br>0.1253208 gong, tam-tam<br>0.0107065 water jug<br>0.0105488 tennis ball<br>0.0088276 coffeepot| 0.7078060 Granny Smith<br>0.1253216 gong, tam-tam<br>0.0107064 water jug<br>0.0105488 tennis ball<br>0.0088276 coffeepot|
squeezenet-1.0       |0.9988525 Granny Smith<br>0.0004736 fig<br>0.0001965 bell pepper<br>0.0000892 piggy bank, penny bank<br>0.0000732 tennis ball| 0.9988525 Granny Smith<br>0.0004736 fig<br>0.0001965 bell pepper<br>0.0000892 piggy bank, penny bank<br>0.0000732 tennis ball|0.9988525 Granny Smith<br>0.0004736 fig<br>0.0001965 bell pepper<br>0.0000892 piggy bank, penny bank<br>0.0000732 tennis ball| 0.9988525 Granny Smith<br>0.0004736 fig<br>0.0001965 bell pepper<br>0.0000892 piggy bank, penny bank<br>0.0000732 tennis ball|
squeezenet-1.1       |0.9937358 Granny Smith<br>0.0014752 lemon<br>0.0013913 fig<br>0.0008874 tennis ball<br>0.0006791 piggy bank, penny bank| 0.9937358 Granny Smith<br>0.0014752 lemon<br>0.0013913 fig<br>0.0008874 tennis ball<br>0.0006791 piggy bank, penny bank|0.9937358 Granny Smith<br>0.0014752 lemon<br>0.0013913 fig<br>0.0008874 tennis ball<br>0.0006791 piggy bank, penny bank| 0.9937357 Granny Smith<br>0.0014752 lemon<br>0.0013913 fig<br>0.0008874 tennis ball<br>0.0006791 piggy bank, penny bank|
vgg-16               |0.7317343 Granny Smith<br>0.0350750 bell pepper<br>0.0209236 grocery store, grocery, food market, market<br>0.0137958 saltshaker, salt shaker<br>0.0127183 fig| 0.7317343 Granny Smith<br>0.0350750 bell pepper<br>0.0209236 grocery store, grocery, food market, market<br>0.0137958 saltshaker, salt shaker<br>0.0127183 fig|0.7317342 Granny Smith<br>0.0350750 bell pepper<br>0.0209236 grocery store, grocery, food market, market<br>0.0137958 saltshaker, salt shaker<br>0.0127183 fig| 0.7317340 Granny Smith<br>0.0350751 bell pepper<br>0.0209236 grocery store, grocery, food market, market<br>0.0137958 saltshaker, salt shaker<br>0.0127183 fig|
vgg-19               |0.7072727 Granny Smith<br>0.0805918 acorn<br>0.0473263 fig<br>0.0367725 necklace<br>0.0180316 lemon| 0.7072732 Granny Smith<br>0.0805917 acorn<br>0.0473262 fig<br>0.0367724 necklace<br>0.0180316 lemon|0.7072731 Granny Smith<br>0.0805916 acorn<br>0.0473262 fig<br>0.0367724 necklace<br>0.0180316 lemon| 0.7072726 Granny Smith<br>0.0805918 acorn<br>0.0473263 fig<br>0.0367725 necklace<br>0.0180316 lemon|
caffenet             |-|-|0.8602297 Granny SmithБ<br>0.0503849 teapot<br>0.0141509 piggy bank, penny bank<br>0.0113873 saltshaker, salt shaker<br>0.0104464 bell pepper|0.8602297 Granny Smith<br>0.0503849 teapot<br>0.0141509 piggy bank, penny bank<br>0.0113873 saltshaker, salt shaker<br>0.0104464 bell pepper
mobilenet-v1-1.0-224 |-|-|0.9441368 Granny Smith<br>0.0080110 fig<br>0.0042946 lemon<br>0.0042536 custard apple<br>0.0036513 orange|0.9441368 Granny Smith<br>0.0080110 fig<br>0.0042946 lemon<br>0.0042536 custard apple<br>0.0036513 orange|
mobilenet-v2         |-|-|0.9951227 Granny Smith<br>0.0009853 fig<br>0.0007886 lemon<br>0.0006782 pomegranate<br>0.0006098 piggy bank, penny bank| 0.9951227 Granny Smith<br>0.0009853 fig<br>0.0007886 lemon<br>0.0006782 pomegranate<br>0.0006098 piggy bank, penny bank|
se-inception         |-|-|0.7325318 leafhopper<br>0.0065269 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0037833 French loaf<br>0.0036166 hand-held computer, hand-held microcomputer<br>0.0033620 ringlet, ringlet butterfly|0.7325318 leafhopper<br>0.0065269 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0037833 French loaf<br>0.0036166 hand-held computer, hand-held microcomputer<br>0.0033620 ringlet, ringlet butterfly|
se-resnet-50         |-|-|0.7362351 leafhopper<br>0.0048966 damselfly<br>0.0036124 lemon<br>0.0030413 lacewing, lacewing fly<br>0.0024559 French loaf|0.7362351 leafhopper<br>0.0048966 damselfly<br>0.0036124 lemon<br>0.0030413 lacewing, lacewing fly<br>0.0024559 French loaf|
se-resnet-101        |-|-|0.8920754 leafhopper<br>0.0057546 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0030191 lemon<br>0.0026400 lacewing, lacewing fly<br>0.0022345 French loaf|0.8920754 leafhopper<br>0.0057546 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0030191 lemon<br>0.0026400 lacewing, lacewing fly<br>0.0022345 French loaf|
se-resnet-152        |-|-|0.9753318 leafhopper<br>0.0012468 French loaf<br>0.0009470 hand-held computer, hand-held microcomputer<br>0.0003147 lemon<br>0.0002425 bannister, banister, balustrade, balusters, handrail|0.9753318 leafhopper<br>0.0012468 French loaf<br>0.0009470 hand-held computer, hand-held microcomputer<br>0.0003147 lemon<br>0.0002425 bannister, banister, balustrade, balusters, handrail|
se-resnext-50        |-|-|0.9946054 leafhopper<br>0.0000740 hand-held computer, hand-held microcomputer<br>0.0000727 cup<br>0.0000670 hair slide<br>0.0000608 partridge|0.9946054 leafhopper<br>0.0000740 hand-held computer, hand-held microcomputer<br>0.0000727 cup<br>0.0000670 hair slide<br>0.0000608 partridge|
se-resnext-101       |-|-|0.9269249 leafhopper<br>0.0008046 ringlet, ringlet butterfly<br>0.0006204 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0005282 lacewing, lacewing fly<br>0.0003041 admiral|0.9269249 leafhopper<br>0.0008046 ringlet, ringlet butterfly<br>0.0006204 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0005282 lacewing, lacewing fly<br>0.0003041 admiral|

### Тестовое изображение 2

Источник: набор данных [ImageNet][imagenet]

Исходное разрешение: 500 x 500
﻿

Изображение:

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |0.9979284 junco, snowbird<br>0.0020288 chickadee<br>0.0000137 jay<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000104 bulbul| 0.9979284 junco, snowbird<br>0.0020288 chickadee<br>0.0000137 jay<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000104 bulbul|0.9979280 junco, snowbird<br>0.0020288 chickadee<br>0.0000137 jay<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000104 bulbul| 0.9979280 junco, snowbird<br>0.0020288 chickadee<br>0.0000137 jay<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000104 bulbul|
densenet-121         |17.8269768 junco, snowbird<br>11.4734764 brambling, Fringilla montifringilla<br>11.3202286 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3598928 chickadee<br>8.2504864 magpie| 17.8269768 junco, snowbird<br>11.4734764 brambling, Fringilla montifringilla<br>11.3202286 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3598928 chickadee<br>8.2504864 magpie|17.8269768 junco, snowbird<br>11.4734764 brambling, Fringilla montifringilla<br>11.3202286 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3598928 chickadee<br> 8.2504864 magpie| 17.8269730 junco, snowbird<br>11.4734774 brambling, Fringilla montifringilla<br>11.3202305 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3598871 chickadee<br>8.2504835 magpie|
densenet-161         |18.9021969 junco, snowbird<br>12.8945799 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7353125 chickadee<br>9.5253296 brambling, Fringilla montifringilla<br>8.7536564 goldfinch, Carduelis carduelis| 18.9021969 junco, snowbird<br>12.8945799 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7353125 chickadee<br>9.5253296 brambling, Fringilla montifringilla<br>8.7536564 goldfinch, Carduelis carduelis| 18.9021969 junco, snowbird<br>12.8945799 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7353125 chickadee<br>9.5253296 brambling, Fringilla montifringilla<br>8.7536564 goldfinch, Carduelis carduelis|18.9021969 junco, snowbird<br>12.8945799 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7353125 chickadee<br>9.5253296 brambling, Fringilla montifringilla<br>8.7536564 goldfinch, Carduelis carduelis| 18.9021950 junco, snowbird<br>12.8945827 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7353134 chickadee<br>9.5253277 brambling, Fringilla montifringilla<br>8.7536573 goldfinch, Carduelis carduelis|
densenet-169         |18.5059853 junco, snowbird<br>11.6154308 brambling, Fringilla montifringilla<br>11.0603466 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.9430408 goldfinch, Carduelis carduelis<br>8.9175730 chickadee| 18.5059853 junco, snowbird<br>11.6154308 brambling, Fringilla montifringilla<br>11.0603466 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.9430408 goldfinch, Carduelis carduelis<br>8.9175730 chickadee|18.5059853 junco, snowbird<br>11.6154308 brambling, Fringilla montifringilla<br>11.0603466 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.9430408 goldfinch, Carduelis carduelis<br>8.9175730 chickadee| 18.5059853 junco, snowbird<br>11.6154289 brambling, Fringilla montifringilla<br>11.0603485 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.9430408 goldfinch, Carduelis carduelis<br>8.9175758 chickadee|
densenet-201         |17.9479027 junco, snowbird<br>9.7838697 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.6706028 brambling, Fringilla montifringilla<br>8.9102564 house finch, linnet, Carpodacus mexicanus<br>8.2559881 chickadee| 17.9479065 junco, snowbird<br>9.7838707 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.6706047 brambling, Fringilla montifringilla<br>8.9102554 house finch, linnet, Carpodacus mexicanus<br>8.2559891 chickadee|17.9479027 junco, snowbird<br>9.7838697 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.6706028 brambling, Fringilla montifringilla<br>8.9102564 house finch, linnet, Carpodacus mexicanus<br>8.2559881 chickadee| 17.9479065 junco, snowbird<br>9.7838707 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.6706047 brambling, Fringilla montifringilla<br>8.9102554 house finch, linnet, Carpodacus mexicanus<br>8.2559891 chickadee|
googlenet-v1         |0.9999955 junco, snowbird<br>0.0000043 chickadee<br> 0.0000003 brambling, Fringilla montifringilla<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000000 water ouzel, dipper| 0.9999955 junco, snowbird<br>0.0000043 chickadee<br>0.0000003 brambling, Fringilla montifringilla<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000000 water ouzel, dipper|0.9999954 junco, snowbird<br>0.0000043 chickadee<br>0.0000003 brambling, Fringilla montifringilla<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000000 water ouzel, dipper| 0.9999954 junco, snowbird<br>0.0000043 chickadee<br>0.0000003 brambling, Fringilla montifringilla<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000000 water ouzel, dipper|
googlenet-v2         |0.9986873 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004460 title n02641379 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0002120 barracouta, snoek<br>0.0001153 title n02730930 apron<br>0.0000563 basketball| 0.9986873 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004460 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0002120 barracouta, snoek<br>0.0001153 apron<br>0.0000563 basketball|0.9986847 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004460 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0002120 barracouta, snoek<br>0.0001153 apron<br>0.0000563 basketball| 0.9986847 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004460 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0002120 barracouta, snoek<br>0.0001153 apron<br>0.0000563 basketball|
googlenet-v3         |0.9241990 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005938 cliff dwelling<br>0.0005932 bustard<br>0.0005757 jack-o'-lantern<br>0.0005057 kite| 0.9241990 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005938 cliff dwelling<br>0.0005932 junco, snowbird8<br>0.0005757 jack-o'-lantern<br>0.0005057 kite|0.9241987 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005938 cliff dwelling<br>0.0005932 bustard<br>0.0005757 jack-o'-lantern<br>0.0005057 kite| 0.9241988 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005938 cliff dwelling<br>0.0005932 bustard<br>0.0005757 jack-o'-lantern<br>0.0005057 kite|
googlenet-v4         |0.9338058 junco, snowbird<br>0.0005343 hamster<br>0.0005193 chickadee<br>0.0004287 brambling, Fringilla montifringilla<br>0.0003747 koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus| 0.9338058 junco, snowbird<br>0.0005343 hamster<br>0.0005193 chickadee<br>0.0004287 brambling, Fringilla montifringilla<br>0.0003747 brambling, Fringilla montifringilla5|0.9338045 junco, snowbird<br>0.0005343 hamster<br>0.0005193 chickadee<br>0.0004287 brambling, Fringilla montifringilla<br>0.0003747 koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus| 0.9338045 junco, snowbird<br>0.0005343 hamster<br>0.0005193 chickadee<br>0.0004287 brambling, Fringilla montifringilla<br>0.0003747 koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus|
inception-resnet v2  |0.9995078 junco, snowbird<br>0.0000257 brambling, Fringilla montifringilla<br>0.0000219 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000217 chickadee<br>0.0000119 water ouzel, dipper| 0.9995078 junco, snowbird<br>0.0000257 brambling, Fringilla montifringilla<br>0.0000219 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000217 chickadee<br>0.0000119 water ouzel, dipper|0.9995075 junco, snowbird<br>0.0000257 brambling, Fringilla montifringilla<br>0.0000219 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000217 chickadee<br>0.0000119 water ouzel, dipper| 0.9995075 junco, snowbird<br>0.0000257 brambling, Fringilla montifringilla<br>0.0000219 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000217 chickadee<br>0.0000119 water ouzel, dipper|
resnet-v1-50         |0.9975350 junco, snowbird<br>0.0012899 chickadee<br>0.0007322 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003813 brambling, Fringilla montifringilla<br>0.0000160 bulbul| 0.9975350 junco, snowbird<br>0.0012899 chickadee<br>0.0007322 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003813 brambling, Fringilla montifringilla<br>0.0000160 bulbul|0.9975340 junco, snowbird<br>0.0012899 chickadee<br>0.0007322 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003813 brambling, Fringilla montifringilla<br>0.0000160 bulbul| 0.9975340 junco, snowbird<br>0.0012899 chickadee<br>0.0007322 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003813 brambling, Fringilla montifringilla<br>0.0000160 bulbul|
resnet-v1-101        |0.9994699 junco, snowbird<br>0.0001720 brambling, Fringilla montifringilla<br>0.0001495 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001213 chickadee<br>0.0000216 water ouzel, dipper| 0.9994699 junco, snowbird<br>0.0001720 brambling, Fringilla montifringilla<br>0.0001495 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001213 chickadee<br>0.0000216 water ouzel, dipper|0.9994646 junco, snowbird<br>0.0001720 brambling, Fringilla montifringilla<br>0.0001495 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001213 chickadee<br>0.0000216 water ouzel, dipper| 0.9994646 junco, snowbird<br>0.0001720 brambling, Fringilla montifringilla<br>0.0001495 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001213 chickadee<br>0.0000216 water ouzel, dipper|
resnet-v1-152        |0.9961464 junco, snowbird<br>0.0013669 chickadee<br>0.0008338 brambling, Fringilla montifringilla<br>0.0005274 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002985 water ouzel, dipper| 0.9961464 junco, snowbird<br>0.0013669 chickadee<br>0.0008338 brambling, Fringilla montifringilla<br>0.0005274 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002985 water ouzel, dipper|0.9961376 junco, snowbird<br>0.0013669 chickadee<br>0.0008338 brambling, Fringilla montifringilla<br>0.0005274 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002985 water ouzel, dipper| 0.9961376 junco, snowbird<br>0.0013669 chickadee<br>0.0008338 brambling, Fringilla montifringilla<br>0.0005274 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002985 water ouzel, dipper|
squeezenet-1.0       |0.9931428 junco, snowbird<br>0.0064122 chickadee<br>0.0003084 brambling, Fringilla montifringilla<br>0.0000394 bulbul<br>0.0000340 magpie| 0.9931428 junco, snowbird<br>0.0064122 chickadee<br>0.0003084 brambling, Fringilla montifringilla<br>0.0000394 bulbul<br>0.0000340 magpie|0.9931428 junco, snowbird<br>0.0064122 chickadee<br>0.0003084 brambling, Fringilla montifringilla<br>0.0000394 bulbul<br>0.0000340 magpie| 0.9931427 junco, snowbird<br>0.0064122 chickadee<br>0.0003084 brambling, Fringilla montifringilla<br>0.0000394 bulbul<br>0.0000340 magpie|
squeezenet-1.1       |0.9949969 junco, snowbird<br>0.0048572 chickadee<br>0.0000578 jay<br>0.0000297 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000271 brambling, Fringilla montifringilla| 0.9949969 junco, snowbird<br>0.0048572 chickadee<br>0.0000578 jay<br>0.0000297 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000271 brambling, Fringilla montifringilla|0.9949969 junco, snowbird<br>0.0048572 chickadee<br>0.0000578 jay<br>0.0000297 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000271 brambling, Fringilla montifringilla| 0.9949970 junco, snowbird<br>0.0048571 chickadee<br>0.0000578 jay<br>0.0000297 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000271 brambling, Fringilla montifringilla|
vgg-16               |0.9999772 junco, snowbird<br>0.0000132 brambling, Fringilla montifringilla<br>0.0000089 chickadee<br>0.0000006 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea| 0.9999772 junco, snowbird<br>0.0000132 brambling, Fringilla montifringilla<br>0.0000089 chickadee<br>0.0000006 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|0.9999772 junco, snowbird<br>0.0000132 brambling, Fringilla montifringilla<br>0.0000089 chickadee<br>0.0000006 water ouzel, dipper<br>0.0000000 indigo bunting, indigo, indigo bird, Passerina cyanea| 0.9999772 junco, snowbird<br>0.0000132 brambling, Fringilla montifringilla<br>0.0000089 chickadee<br>0.0000006 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
vgg-19               |0.9999394 junco, snowbird<br>0.0000580 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea| 0.9999394 junco, snowbird<br>0.0000580 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|0.9999394 junco, snowbird<br>0.0000580 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea| 0.9999394 junco, snowbird<br>0.0000580 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
caffenet             |-|-|0.9997593 junco, snowbird<br>0.0002351 chickadee<br>0.0000033 brambling, Fringilla montifringilla<br>0.0000010 bulbul<br>0.0000007 jay|0.9997593 junco, snowbird<br>0.0002351 chickadee<br>0.0000033 brambling, Fringilla montifringilla<br>0.0000010 bulbul<br>0.0000007 jay
mobilenet-v1-1.0-224 |-|-|0.9988418 junco, snowbird<br>0.0007267 chickadee<br>0.0002552 brambling, Fringilla montifringilla<br>0.0000451 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000312 bulbul|0.9988418 junco, snowbird<br>0.0007267 chickadee<br>0.0002552 brambling, Fringilla montifringilla<br>0.0000451 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000312 bulbul|
mobilenet-v2         |-|-|0.9998599 junco, snowbird<br>0.0000698 brambling, Fringilla montifringilla<br>0.0000668 chickadee<br>0.0000014 water ouzel, dipper<br>0.0000011 indigo bunting, indigo finch, indigo bird, Passerina cyanea|0.9998599 junco, snowbird<br>0.0000698 brambling, Fringilla montifringilla<br>0.0000668 chickadee<br>0.0000014 water ouzel, dipper<br>0.0000011 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
se-inception         |-|-|0.8893582 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0011496 bell cote, bell cot<br>0.0007226 sturgeon<br>0.0007176 file, file cabinet, filing cabinet<br>0.0007079 barracouta, snoek|0.8893582 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0011496 bell cote, bell cot<br>0.0007226 sturgeon<br>0.0007176 file, file cabinet, filing cabinet<br>0.0007079 barracouta, snoek|
se-resnet-50         |-|-|0.9356345 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004958 hip, rose hip, rosehip<br>0.0004906 barracouta, snoek<br>0.0004670 basketball<br>0.0002704 Labrador retriever|0.9356345 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004958 hip, rose hip, rosehip<br>0.0004906 barracouta, snoek<br>0.0004670 basketball<br>0.0002704 Labrador retriever|
se-resnet-101        |-|-|0.8954772 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0007209 purse<br>0.0005219 flatworm, platyhelminth<br>0.0005196 basketball<br>0.0005054 sarong|0.8954772 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0007209 purse<br>0.0005219 flatworm, platyhelminth<br>0.0005196 basketball<br>0.0005054 sarong|
se-resnet-152        |-|-|0.8786952 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0009026 barracouta, snoek<br>0.0008578 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0006575 rock beauty, Holocanthus tricolor<br>0.0006063 sarong|0.8786952 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0009026 barracouta, snoek<br>0.0008578 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0006575 rock beauty, Holocanthus tricolor<br>0.0006063 sarong|
se-resnext-50        |-|-|0.9980450 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0000507 basketball<br>0.0000314 buckeye, horse chestnut, conker<br>0.0000309 bell pepper<br>0.0000228 beach wagon, station wagon, wagon, estate car, beach waggon, station waggon, waggon|0.9980450 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0000507 basketball<br>0.0000314 buckeye, horse chestnut, conker<br>0.0000309 bell pepper<br>0.0000228 beach wagon, station wagon, wagon, estate car, beach waggon, station waggon, waggon|
se-resnext-101       |-|-|0.9044468 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0005567 basketball<br>0.0004812 beach wagon, station wagon, wagon, estate car, beach waggon, station waggon, waggon<br>0.0004283 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0004192 Yorkshire terrier|0.9044468 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0005567 basketball<br>0.0004812 beach wagon, station wagon, wagon, estate car, beach waggon, station waggon, waggon<br>0.0004283 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0004192 Yorkshire terrier|

### Тестовое изображение 3

Источник: набор данных [ImageNet][imagenet]

Исходное разрешение: 333 x 500
﻿

Изображение:

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |0.9991664 lifeboat<br>0.0003741 container ship, containership, container vessel<br>0.0001206 pirate, pirate ship<br>0.0000820 drilling platform, offshore rig<br>0.0000784 wreck| 0.9991664 lifeboat<br>0.0003741 container ship, containership, container vessel<br>0.0001206 pirate, pirate ship<br>0.0000820 drilling platform, offshore rig<br>0.0000784 wreck|0.9991654 lifeboat<br>0.0003741 container ship, containership, container vessel<br>0.0001206 pirate, pirate ship<br>0.0000820 drilling platform, offshore rig<br>0.0000784 wreck| 0.9991654 lifeboat<br>0.0003741 container ship, containership, container vessel<br>0.0001206 pirate, pirate ship<br>0.0000820 drilling platform, offshore rig<br>0.0000784 wreck|
densenet-121         |13.9662323 lifeboat<br>7.8177419 drilling platform, offshore rig<br>7.7323365 liner, ocean liner<br>7.5702801 wreck<br>7.5621624 pirate, pirate ship| 13.9662323 lifeboat<br>7.8177419 drilling platform, offshore rig<br>7.7323365 liner, ocean liner<br>7.5702801 wreck<br>7.5621624 pirate, pirate ship|13.9662323 lifeboat<br>7.8177419 drilling platform, offshore rig<br>7.7323365 liner, ocean liner<br>7.5702801 wreck<br>7.5621624 pirate, pirate ship| 13.9662342 lifeboat<br>7.8177428 drilling platform, offshore rig<br>7.7323399 liner, ocean liner<br>7.5702839 wreck<br>7.5621653 pirate, pirate ship|
densenet-161         |15.5664644 lifeboat<br>7.2549500 liner, ocean liner<br>6.7164907 fireboat<br>6.2500725 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.2465825 dock, dockage, docking facility| 15.5664644 lifeboat<br>7.2549500 liner, ocean liner<br>6.7164907 fireboat<br>6.2500725 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.2465825 dock, dockage, docking facility|15.5664644 lifeboat<br>7.2549500 liner, ocean liner<br>6.7164907 fireboat<br>6.2500725 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.2465825 dock, dockage, docking facility| 15.5664644 lifeboat<br>7.2549510 liner, ocean liner<br>6.7164927 fireboat<br>6.2500734 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.2465792 dock, dockage, docking facility|
densenet-169         |15.3814850 lifeboat<br>10.0849438 drilling platform, offshore rig<br>9.4490118 container ship, containership, container vessel<br>9.1608114 pirate, pirate ship<br>8.3062391 beacon, lighthouse, beacon light, pharos| 15.3814850 lifeboat<br>10.0849438 drilling platform, offshore rig<br>9.4490118 container ship, containership, container vessel<br>9.1608114 pirate, pirate ship<br>8.3062391 beacon, lighthouse, beacon light, pharos|15.3814850 lifeboat<br>10.0849438 drilling platform, offshore rig<br>9.4490118 container ship, containership, container vessel<br>9.1608114 pirate, pirate ship<br>8.3062391 beacon, lighthouse, beacon light, pharos| 15.3814812 lifeboat<br>10.0849428 drilling platform, offshore rig<br>9.4490099 container ship, containership, container vessel<br>9.1608076 pirate, pirate ship<br>8.3062334 beacon, lighthouse, beacon light, pharos|
densenet-201         |16.1351147 lifeboat<br>8.5620890 fireboat<br>8.3413439 drilling platform, offshore rig<br>8.1058626 liner, ocean liner<br>7.8472042 container ship, containership, container vessel| 16.1351070 lifeboat<br>8.5620880 fireboat<br>8.3413410 drilling platform, offshore rig<br>8.1058598 liner, ocean liner<br>7.8472009 container ship, containership, container vessel|16.1351147 lifeboat<br>8.5620890 fireboat<br>8.3413439 drilling platform, offshore rig<br>8.1058626 liner, ocean liner<br>7.8472042 container ship, containership, container vessel| 16.1351070 lifeboat<br>8.5620880 fireboat<br>8.3413410 drilling platform, offshore rig<br>8.1058598 liner, ocean liner<br>7.8472009 container ship, containership, container vessel|
googlenet-v1         |0.8990629 lifeboat<br>0.0275983 drilling platform, offshore rig<br>0.0209237 beacon, lighthouse, beacon light, pharos<br>0.0196472 container ship, containership, container vessel<br>0.0062734 liner, ocean liner| 0.8990631 lifeboat<br>0.0275983 drilling platform, offshore rig<br>0.0209237 beacon, lighthouse, beacon light, pharos<br>0.0196472 container ship, containership, container vessel<br>0.0062734 liner, ocean liner|0.8990629 lifeboat<br>0.0275983 drilling platform, offshore rig<br>0.0209237 beacon, lighthouse, beacon light, pharos<br>0.0196472 container ship, containership, container vessel<br>0.0062734 liner, ocean liner| 0.8990629 lifeboat<br>0.0275983 drilling platform, offshore rig<br>0.0209237 beacon, lighthouse, beacon light, pharos<br>0.0196472 container ship, containership, container vessel<br>0.0062734 liner, ocean liner|
googlenet-v2         |0.9919646 miniature pinscher<br>0.0011945 pier<br>0.0007551 submarine, pigboat, sub, U-boat<br>0.0005916 Saint Bernard, St Bernard<br>0.0005792 Rottweiler| 0.9919646 miniature pinscher<br>0.0011945 pier<br>0.0007551 submarine, pigboat, sub, U-boat<br>0.0005916 Saint Bernard, St Bernard<br>0.0005792 Rottweiler|0.9919641 miniature pinscher<br>0.0011945 pier<br>0.0007550 submarine, pigboat, sub, U-boat<br>0.0005916 Saint Bernard, St Bernard<br>0.0005792 Rottweiler| 0.9919641 miniature pinscher<br>0.0011945 pier<br>0.0007550 submarine, pigboat, sub, U-boat<br>0.0005916 Saint Bernard, St Bernard<br>0.0005792 Rottweiler|
googlenet-v3         |0.9595632 lighter, light, igniter, ignitor<br>0.0016150 bakery, bakeshop, bakehouse<br>0.0007223 beaker<br>0.0005667 breastplate, aegis, egis<br>0.0003984 fire engine, fire truck| 0.9595632 lighter, light, igniter, ignitor<br>0.0016150 bakery, bakeshop, bakehouse<br>0.0007223 beaker<br>0.0005667 breastplate, aegis, egis<br>0.0003984 fire engine, fire truck|0.9595628 lighter, light, igniter, ignitor<br>0.0016150 bakery, bakeshop, bakehouse<br>0.0007223 beaker<br>0.0005667 breastplate, aegis, egis<br>0.0003984 fire engine, fire truck| 0.9595628 lighter, light, igniter, ignitor<br>0.0016150 bakery, bakeshop, bakehouse<br>0.0007223 beaker<br>0.0005667 breastplate, aegis, egis<br>0.0003984 fire engine, fire truck|
googlenet-v4         |0.9513760 lifeboat<br>0.0005698 fireboat<br>0.0004419 submarine, pigboat, sub, U-boat<br>0.0004226 ambulance<br>0.0004161 drilling platform, offshore rig| 0.9513760 lifeboat<br>0.0005698 fireboat<br>0.0004419 submarine, pigboat, sub, U-boat<br>0.0004226 ambulance<br>0.0004161 drilling platform, offshore rig|0.9513766 lifeboat<br>0.0005698 fireboat<br>0.0004419 submarine, pigboat, sub, U-boat<br>0.0004226 ambulance<br>0.0004161 drilling platform, offshore rig| 0.9513763 lifeboat<br>0.0005698 fireboat<br>0.0004419 submarine, pigboat, sub, U-boat<br>0.0004226 ambulance<br>0.0004161 drilling platform, offshore rig|
inception-resnet v2  |0.9981450 lifeboat<br>0.0006250 beacon, lighthouse, beacon light, pharos<br>0.0001983 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0001903 drilling platform, offshore rig<br>0.0001606 fireboat| 0.9981450 lifeboat<br>0.0006250 beacon, lighthouse, beacon light, pharos<br>0.0001983 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0001903 drilling platform, offshore rig<br>0.0001606 fireboat|0.9981461 lifeboat<br>0.0006250 beacon, lighthouse, beacon light, pharos<br>0.0001983 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0001903 drilling platform, offshore rig<br>0.0001606 fireboat| 0.9981461 lifeboat<br>0.0006250 beacon, lighthouse, beacon light, pharos<br>0.0001983 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0001903 drilling platform, offshore rig<br>0.0001606 fireboat|
resnet-v1-50         |0.8872182 lifeboat<br>0.0398498 liner, ocean liner<br>0.0237536 container ship, containership, container vessel<br>0.0125247 dock, dockage, docking facility<br>0.0107783 drilling platform, offshore rig| 0.8872181 lifeboat<br>0.0398499 liner, ocean liner<br>0.0237536 container ship, containership, container vessel<br>0.0125247 dock, dockage, docking facility<br>0.0107783 drilling platform, offshore rig|0.8872179 lifeboat<br>0.0398498 liner, ocean liner<br>0.0237536 container ship, containership, container vessel<br>0.0125247 dock, dockage, docking facility<br>0.0107783 drilling platform, offshore rig| 0.8872181 lifeboat<br>0.0398498 liner, ocean liner<br>0.0237534 container ship, containership, container vessel<br>0.0125247 dock, dockage, docking facility<br>0.0107783 drilling platform, offshore rig|
resnet-v1-101        |0.6138132 lifeboat<br>0.1049522 drilling platform, offshore rig<br>0.0466762 liner, ocean liner<br>0.0327782 dock, dockage, docking facility<br>0.0284107 aircraft carrier, carrier, flattop, attack aircraft carrier| 0.6138127 lifeboat<br>0.1049523 drilling platform, offshore rig<br>0.0466763 liner, ocean liner<br>0.0327782 dock, dockage, docking facility<br>0.0284106 aircraft carrier, carrier, flattop, attack aircraft carrier|0.6138138 lifeboat<br>0.1049523 drilling platform, offshore rig<br>0.0466763 liner, ocean liner<br>0.0327782 dock, dockage, docking facility<br>0.0284107 aircraft carrier, carrier, flattop, attack aircraft carrier| 0.6138141 lifeboat<br>0.1049523 drilling platform, offshore rig<br>0.0466761 liner, ocean liner<br>0.0327781 dock, dockage, docking facility<br>0.0284106 aircraft carrier, carrier, flattop, attack aircraft carrier|
resnet-v1-152        |0.9505479 lifeboat<br>0.0083380 drilling platform, offshore rig<br>0.0072418 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0049709 container ship, containership, container vessel<br>0.0041877 liner, ocean liner| 0.9505479 lifeboat<br>0.0083380 drilling platform, offshore rig<br>0.0072418 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0049709 container ship, containership, container vessel<br>0.0041877 liner, ocean liner|0.9505481 lifeboat<br>0.0083380 drilling platform, offshore rig<br>0.0072418 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0049709 container ship, containership, container vessel<br>0.0041877 liner, ocean liner| 0.9505481 lifeboat<br>0.0083380 drilling platform, offshore rig<br>0.0072418 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0049709 container ship, containership, container vessel<br>0.0041877 liner, ocean liner|
squeezenet-1.0       |0.9870804 lifeboat<br>0.0061878 container ship, containership, container vessel<br>0.0025447 fireboat<br>0.0024638 liner, ocean liner<br>0.0004083 beacon, lighthouse, beacon light, pharos| 0.9870804 lifeboat<br>0.0061878 container ship, containership, container vessel<br>0.0025447 fireboat<br>0.0024638 liner, ocean liner<br>0.0004083 beacon, lighthouse, beacon light, pharos|0.9870804 lifeboat<br>0.0061878 container ship, containership, container vessel<br>0.0025447 fireboat<br>0.0024638 liner, ocean liner<br>0.0004083 beacon, lighthouse, beacon light, pharos| 0.9870804 lifeboat<br>0.0061878 container ship, containership, container vessel<br>0.0025447 fireboat<br>0.0024638 liner, ocean liner<br>0.0004083 beacon, lighthouse, beacon light, pharos|
squeezenet-1.1       |0.9570305 lifeboat<br>0.0211557 container ship, containership, container vessel<br>0.0102893 drilling platform, offshore rig<br>0.0034316 pirate, pirate ship<br>0.0029377 dock, dockage, docking facility| 0.9570305 lifeboat<br>0.0211557 container ship, containership, container vessel<br>0.0102893 drilling platform, offshore rig<br>0.0034316 pirate, pirate ship<br>0.0029377 dock, dockage, docking facility|0.9570305 lifeboat<br>0.0211557 container ship, containership, container vessel<br>0.0102893 drilling platform, offshore rig<br>0.0034316 pirate, pirate ship<br>0.0029377 dock, dockage, docking facility| 0.9570300 lifeboat<br>0.0211559 container ship, containership, container vessel<br>0.0102894 drilling platform, offshore rig<br>0.0034316 pirate, pirate ship<br>0.0029378 dock, dockage, docking facility|
vgg-16               |0.9821943 lifeboat<br>0.0082832 container ship, containership, container vessel<br>0.0014539 drilling platform, offshore rig<br>0.0014494 pirate, pirate ship<br>0.0009578 liner, ocean liner| 0.9821942 lifeboat<br>0.0082832 container ship, containership, container vessel<br>0.0014539 drilling platform, offshore rig<br>0.0014494 pirate, pirate ship<br>0.0009578 liner, ocean liner|0.9821915 lifeboat<br>0.0082832 container ship, containership, container vessel<br>0.0014539 drilling platform, offshore rig<br>0.0014494 pirate, pirate ship<br>0.0009578 liner, ocean liner| 0.9821915 lifeboat<br>0.0082832 container ship, containership, container vessel<br>0.0014539 drilling platform, offshore rig<br>0.0014494 pirate, pirate ship<br>0.0009578 liner, ocean liner|
vgg-19               |0.9965242 lifeboat<br>0.0008823 container ship, containership, container vessel<br>0.0004778 drilling platform, offshore rig<br>0.0003970 dock, dockage, docking facility<br>0.0003622 fireboat| 0.9965242 lifeboat<br>0.0008823 container ship, containership, container vessel<br>0.0004778 drilling platform, offshore rig<br>0.0003970 dock, dockage, docking facility<br>0.0003622 fireboat|0.9965212 lifeboat<br>0.0008823 container ship, containership, container vessel<br>0.0004778 drilling platform, offshore rig<br>0.0003970 dock, dockage, docking facility<br>0.0003622 fireboat| 0.9965214 lifeboat<br>0.0008823 container ship, containership, container vessel<br>0.0004778 drilling platform, offshore rig<br>0.0003970 dock, dockage, docking facility<br>0.0003622 fireboat|
caffenet             |-|-|0.9839840 lifeboat<br>0.0109296 container ship, containership, container vessel<br>0.0018576 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0007185 wreck<br>0.0007133 pirate, pirate ship|0.9839840 lifeboat<br>0.0109296 container ship, containership, container vessel<br>0.0018576 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0007185 wreck<br>0.0007133 pirate, pirate ship|
mobilenet-v1-1.0-224 |-|-|0.8883278 lifeboat<br>0.0358164 pirate, pirate ship<br>0.0247643 container ship, containership, container vessel<br>0.0106019 drilling platform, offshore rig<br>0.0084066 liner, ocean liner|0.8883278 lifeboat<br>0.0358164 pirate, pirate ship<br>0.0247643 container ship, containership, container vessel<br>0.0106019 drilling platform, offshore rig<br>0.0084066 liner, ocean liner|
mobilenet-v2         |-|-|0.9638824 lifeboat<br>0.0142666 pirate, pirate ship<br>0.0047917 submarine, pigboat, sub, U-boat<br>0.0040148 container ship, containership, container vessel<br>0.0019008 space shuttle|0.9638824 lifeboat<br>0.0142666 pirate, pirate ship<br>0.0047917 submarine, pigboat, sub, U-boat<br>0.0040148 container ship, containership, container vessel<br>0.0019008 space shuttle|
se-inception         |-|-|0.7523978 miniature pinscher<br>0.0948917 Tibetan mastiff<br>0.0089837 Saint Bernard, St Bernard<br>0.0043663 axolotl, mud puppy, Ambystoma mexicanum<br>0.0035432 pick, plectrum, plectron|0.7523978 miniature pinscher<br>0.0948917 Tibetan mastiff<br>0.0089837 Saint Bernard, St Bernard<br>0.0043663 axolotl, mud puppy, Ambystoma mexicanum<br>0.0035432 pick, plectrum, plectron|
se-resnet-50         |-|-|0.9203509 miniature pinscher<br>0.0061232 Polaroid camera, Polaroid Land camera<br>0.0030807 Tibetan mastiff<br>0.0027831 pier<br>0.0024065 bull mastiff|0.9203509 miniature pinscher<br>0.0061232 Polaroid camera, Polaroid Land camera<br>0.0030807 Tibetan mastiff<br>0.0027831 pier<br>0.0024065 bull mastiff|
se-resnet-101        |-|-|0.9360378 miniature pinscher<br>0.0007210 Cardigan, Cardigan Welsh corgi<br>0.0006788 hog, pig, grunter, squealer, Sus scrofa<br>0.0005284 submarine, pigboat, sub, U-boat<br>0.0004462 Tibetan mastiff|0.9360378 miniature pinscher<br>0.0007210 Cardigan, Cardigan Welsh corgi<br>0.0006788 hog, pig, grunter, squealer, Sus scrofa<br>0.0005284 submarine, pigboat, sub, U-boat<br>0.0004462 Tibetan mastiff|
se-resnet-152        |-|-|0.9468850 miniature pinscher<br>0.0012246 wine bottle<br>0.0009628 Polaroid camera, Polaroid Land camera<br>0.0007208 marimba, xylophone<br>0.0005199 submarine, pigboat, sub, U-boat|0.9468850 miniature pinscher<br>0.0012246 wine bottle<br>0.0009628 Polaroid camera, Polaroid Land camera<br>0.0007208 marimba, xylophone<br>0.0005199 submarine, pigboat, sub, U-boat|
se-resnext-50        |-|-|0.9979483 miniature pinscher<br>0.0000302 parachute, chute<br>0.0000281 Cardigan, Cardigan Welsh corgi<br>0.0000280 black widow, Latrodectus mactans<br>0.0000222 hognose snake, puff adder, sand viper|0.9979483 miniature pinscher<br>0.0000302 parachute, chute<br>0.0000281 Cardigan, Cardigan Welsh corgi<br>0.0000280 black widow, Latrodectus mactans<br>0.0000222 hognose snake, puff adder, sand viper|
se-resnext-101       |-|-|0.8982230 miniature pinscher<br>0.0006859 Tibetan mastiff<br>0.0005912 Cardigan, Cardigan Welsh corgi<br>0.0004639 eel<br>0.0004079 parachute, chute|0.8982230 miniature pinscher<br>0.0006859 Tibetan mastiff<br>0.0005912 Cardigan, Cardigan Welsh corgi<br>0.0004639 eel<br>0.0004079 parachute, chute|

## Результаты детектирования

### Тестовое изображение 1

Источник: набор данных [ImageNet][imagenet]

Исходное разрешение: 709 x 510
﻿

Входное изображение и результат детектирования:

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
<img width="150" src="detection\ILSVRC2012_val_00000023.JPEG"></img>
</div>
Окаймляющие прямоугольники (координаты левого верхнего и правого нижнего углов):<br>
(55,155), (236,375)<br>
(190,190), (380,400)<br>
(374,209), (588,422)<br>
(289,111), (440,255)<br>
(435,160), (615,310)<br>

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
----------------------|----------------------------------|----------------------------------|--------------------------------|------------------------------------|
ssd_mobilenet_v2_coco | - | - | Окаймляющий прямоугольник: (76,168), (231,344)| Окаймляющие прямоугольники: (75,165), (232,344),<br> (380,315), (610,410) |
mobilenet-ssd         | - | - | Окаймляющий прямоугольник: (380,315), (630,415) | Окаймляющий прямоугольник: (377,314), (632,415) |
ssd300                | - | - | Окаймляющий прямоугольник: (380,165), (595,425) | Окаймляющий прямоугольник: (380,165), (595,425) |
ssd512                | - | - | Окаймляющий прямоугольник: (377,163), (595,425) | Окаймляющий прямоугольник: (380,165), (595,425) |

### Тестовое изображение 2

Источник: набор данных [ImageNet][imagenet]

Исходное разрешение: 500 x 500
﻿

Входное изображение и результат детектирования:

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00000247.JPEG">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
(117,86), (365,465)

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|----------------------------------|----------------------------------|--------------------------------|------------------------------------|
ssd_mobilenet_v2_coco | - | - | Окаймляющий прямоугольник: (90,100), (356,448) | Окаймляющий прямоугольник: (90,100), (350,450) |
mobilenet-ssd         | - | - | Окаймляющий прямоугольник: (92,95), (361,483) | Окаймляющий прямоугольник: (94,94), (361,480) |
ssd300                | - | - | Окаймляющий прямоугольник: (68,100), (336,452) | Окаймляющий прямоугольник: (66,98), (340,455) |
ssd512                | - | - | Окаймляющий прямоугольник: (75,100), (355,445) | Окаймляющий прямоугольник: (75,100), (355,445)|

### Тестовое изображение 3

Источник: набор данных [ImageNet][imagenet]

Исходное разрешение: 333 x 500
﻿

Входное изображение и результат детектирования:

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00018592.JPEG">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
(82,262), (269,376)

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|----------------------------------|----------------------------------|--------------------------------|------------------------------------|
ssd_mobilenet_v2_coco | - | - | Окаймляющий прямоугольник: (81,244), (267,376) | Окаймляющий прямоугольник: (80,244), (267,376) |
mobilenet-ssd         | - | - | Окаймляющий прямоугольник: (80,140), (270,375) | Окаймляющий прямоугольник: (80,140), (270,375) |
ssd300                | - | - | Окаймляющий прямоугольник: (80,155), (270,375) | Окаймляющий прямоугольник: (80,157), (274,375) |
ssd512                | - | - | Окаймляющий прямоугольник: (75,170), (172,370) | Окаймляющий прямоугольник: (73,170), (173,371) |

## Результаты сегментации

### Тестовое изображение 1

Источник: набор данных [Cityscapes][cityscapes]

Исходное разрешение: 2048 x 1024
﻿

Исходное изображение:

<div style='float: center'>
<img width="300" src="images\berlin_000000_000019_leftImg8bit.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|---------------------------|---------------------------|-----------------------------|------------------------------------|
dilation             |<div style='float: center'><img width="150" src="semantic_segmentation\cpp_sync_berlin_000000_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\cpp_async_berlin_000000_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\python_sync_berlin_000000_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\python_async_berlin_000000_000019_leftImg8bit.bmp"></img></div>|

### Тестовое изображение 2

Источник: набор данных [Cityscapes][cityscapes]

Исходное разрешение: 2048 x 1024
﻿

Исходное изображение:

<div style='float: center'>
<img width="300" src="images\berlin_000488_000019_leftImg8bit.png">
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|---------------------------|---------------------------|-----------------------------|------------------------------------|
dilation             |<div style='float: center'><img width="150" src="semantic_segmentation\cpp_sync_berlin_000488_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\cpp_async_berlin_000488_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\python_sync_berlin_000488_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\python_async_berlin_000488_000019_leftImg8bit.bmp"></img></div>|

### Тестовое изображение 3

Источник: набор данных [Cityscapes][cityscapes]

Исходное разрешение: 2048 x 1024
﻿

Исходное изображение:

<div style='float: center'>
<img width="300" src="images\berlin_000533_000019_leftImg8bit.png">
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|---------------------------|---------------------------|-----------------------------|------------------------------------|
dilation             |<div style='float: center'><img width="150" src="semantic_segmentation\cpp_sync_berlin_000533_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\cpp_async_berlin_000533_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\python_sync_berlin_000533_000019_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\python_async_berlin_000533_000019_leftImg8bit.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="300" src="semantic_segmentation\cityscapes_colormap.jpg">
</div>

## Результаты экземплярной сегментации

### Тестовое изображение 1

Источник: набор данных [MS COCO][ms_coco]

Исходное разрешение: 640 x 480


Изображение:

<div style='float: center'>
<img width="300" src="images\22.jpg"></img>
</div>
<div style='float: center'>
Входной тензор: 800; 1365; 1
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
mask_rcnn_inception_resnet_v2_atrous_coco             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_22_mask_rcnn_inception_resnet_v2_atrous_coco.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_22_mask_rcnn_inception_resnet_v2_atrous_coco.bmp"></img></div>|
mask_rcnn_inception_v2_coco             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_22_mask_rcnn_inception_v2_coco.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_22_mask_rcnn_inception_v2_coco.bmp"></img></div>|
mask_rcnn_resnet50_atrous_coco             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_22_mask_rcnn_resnet50_atrous_coco.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_22_mask_rcnn_resnet50_atrous_coco.bmp"></img></div>|
mask_rcnn_resnet101_atrous_coco             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_22_mask_rcnn_resnet101_atrous_coco.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_22_mask_rcnn_resnet101_atrous_coco.bmp"></img></div>|


Карта цветов:

<div style='float: center'>
<img width="300" src="instance_segmentation\mscoco90_colormap.jpg">
</div>


<!-- LINKS -->
[imagenet]: http://www.image-net.org
[cityscapes]: https://www.cityscapes-dataset.com
[ms_coco]: http://cocodataset.org