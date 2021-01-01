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
caffenet             |-|-|0.8602297 Granny Smith<br>0.0503849 teapot<br>0.0141509 piggy bank, penny bank<br>0.0113873 saltshaker, salt shaker<br>0.0104464 bell pepper|0.8602297 Granny Smith<br>0.0503849 teapot<br>0.0141509 piggy bank, penny bank<br>0.0113873 saltshaker, salt shaker<br>0.0104464 bell pepper
mobilenet-v1-1.0-224 |-|-|0.9441368 Granny Smith<br>0.0080110 fig<br>0.0042946 lemon<br>0.0042536 custard apple<br>0.0036513 orange|0.9441368 Granny Smith<br>0.0080110 fig<br>0.0042946 lemon<br>0.0042536 custard apple<br>0.0036513 orange|
mobilenet-v2         |-|-|0.9951227 Granny Smith<br>0.0009853 fig<br>0.0007886 lemon<br>0.0006782 pomegranate<br>0.0006098 piggy bank, penny bank| 0.9951227 Granny Smith<br>0.0009853 fig<br>0.0007886 lemon<br>0.0006782 pomegranate<br>0.0006098 piggy bank, penny bank|
se-inception         |-|-|0.7325318 leafhopper<br>0.0065269 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0037833 French loaf<br>0.0036166 hand-held computer, hand-held microcomputer<br>0.0033620 ringlet, ringlet butterfly|0.7325318 leafhopper<br>0.0065269 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0037833 French loaf<br>0.0036166 hand-held computer, hand-held microcomputer<br>0.0033620 ringlet, ringlet butterfly|
se-resnet-50         |-|-|0.7362351 leafhopper<br>0.0048966 damselfly<br>0.0036124 lemon<br>0.0030413 lacewing, lacewing fly<br>0.0024559 French loaf|0.7362351 leafhopper<br>0.0048966 damselfly<br>0.0036124 lemon<br>0.0030413 lacewing, lacewing fly<br>0.0024559 French loaf|
se-resnet-101        |-|-|0.8920754 leafhopper<br>0.0057546 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0030191 lemon<br>0.0026400 lacewing, lacewing fly<br>0.0022345 French loaf|0.8920754 leafhopper<br>0.0057546 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0030191 lemon<br>0.0026400 lacewing, lacewing fly<br>0.0022345 French loaf|
se-resnet-152        |-|-|0.9753318 leafhopper<br>0.0012468 French loaf<br>0.0009470 hand-held computer, hand-held microcomputer<br>0.0003147 lemon<br>0.0002425 bannister, banister, balustrade, balusters, handrail|0.9753318 leafhopper<br>0.0012468 French loaf<br>0.0009470 hand-held computer, hand-held microcomputer<br>0.0003147 lemon<br>0.0002425 bannister, banister, balustrade, balusters, handrail|
se-resnext-50        |-|-|0.9946054 leafhopper<br>0.0000740 hand-held computer, hand-held microcomputer<br>0.0000727 cup<br>0.0000670 hair slide<br>0.0000608 partridge|0.9946054 leafhopper<br>0.0000740 hand-held computer, hand-held microcomputer<br>0.0000727 cup<br>0.0000670 hair slide<br>0.0000608 partridge|
se-resnext-101       |-|-|0.9269249 leafhopper<br>0.0008046 ringlet, ringlet butterfly<br>0.0006204 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0005282 lacewing, lacewing fly<br>0.0003041 admiral|0.9269249 leafhopper<br>0.0008046 ringlet, ringlet butterfly<br>0.0006204 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>0.0005282 lacewing, lacewing fly<br>0.0003041 admiral|
efficientnet-b0      |-|-|9.8424797 Granny Smith<br>4.8622112 fig<br>4.3583665 lemon<br>3.8766663 bell pepper<br>3.4526284 orange | 9.8424797 Granny Smith<br>4.8622112 fig<br>4.3583665 lemon<br>3.8766663 bell pepper<br>3.4526284 orange |
efficientnet-b0_auto_aug|-|-| 10.1708317 Granny Smith<br>4.3690400 tennis ball<br>4.2338214 lemon<br>3.8555355 pomegranate<br>3.8175268 fig | 10.1708317 Granny Smith<br>4.3690400 tennis ball<br>4.2338214 lemon<br>3.8555355 pomegranate<br>3.8175268 fig |
efficientnet-b5      |-|-|8.8117380 Granny Smith<br>2.0016692 bee eater<br>1.8805140 green mamba<br>1.6248529 lemon<br>1.5391053 banana | 8.8117380 Granny Smith<br>2.0016692 bee eater<br>1.8805140 green mamba<br>1.6248529 lemon<br>1.5391053 banana |
efficientnet-b7-pytorch |-|-| 8.3249321 Granny Smith<br>1.5543858 lemon<br>1.5019686 green mamba<br>1.4437177 syringe<br>1.4299904 home theater, home theatre | 8.3249321 Granny Smith<br>1.5543858 lemon<br>1.5019686 green mamba<br>1.4437177 syringe<br>1.4299904 home theater, home theatre |
efficientnet-b7_auto_aug |-|-| 8.3249302 Granny Smith<br>1.5543855 lemon<br>1.5019683 green mamba<br>1.4437169 syringe<br>1.4299890 home theater, home theatre | 8.3249302 Granny Smith<br>1.5543855 lemon<br>1.5019683 green mamba<br>1.4437169 syringe<br>1.4299890 home theater, home theatre |
mobilenet-v1-0.50-224 |-|-| 0.9409788 Granny Smith<br>0.0422395 bell pepper<br>0.0039017 fig<br>0.0032237 piggy bank, penny bank<br>0.0029516 tennis ball | 0.9409788 Granny Smith<br>0.0422395 bell pepper<br>0.0039017 fig<br>0.0032237 piggy bank, penny bank<br>0.0029516 tennis ball |
mobilenet-v1-0.50-160 |-|-| 0.9844190 Granny Smith<br>0.0103430 bell pepper<br>0.0013505 fig<br>0.0009318 lemon<br>0.0008557 cucumber, cuke | 0.9844190 Granny Smith<br>0.0103430 bell pepper<br>0.0013505 fig<br>0.0009318 lemon<br>0.0008557 cucumber, cuke |
mobilenet-v1-0.25-128 |-|-| 0.5188023 bell pepper<br>0.1175004 Granny Smith<br>0.0549228 cucumber, cuke<br>0.0392874 strawberry<br>0.0295591 broccoli | 0.5188023 bell pepper<br>0.1175004 Granny Smith<br>0.0549228 cucumber, cuke<br>0.0392874 strawberry<br>0.0295591 broccoli |
mobilenet-v2-1.4-224 |-|-| 0.8810006 Granny Smith<br>0.0252364 fig<br>0.0074156 jackfruit, jak, jack<br>0.0054692 custard apple<br>0.0037351 lemon | 0.8810006 Granny Smith<br>0.0252364 fig<br>0.0074156 jackfruit, jak, jack<br>0.0054692 custard apple<br>0.0037351 lemon |
densenet-121-tf      |-|-| 0.9993860 Granny Smith<br>0.0004290 lemon<br>0.0000779 orange<br>0.0000480 banana<br>0.0000217 tennis ball | 0.9993860 Granny Smith<br>0.0004290 lemon<br>0.0000779 orange<br>0.0000480 banana<br>0.0000217 tennis ball |
densenet-161-tf      |-|-| 0.9999733 Granny Smith<br>0.0000084 lemon<br>0.0000032 fig<br>0.0000021 orange<br>0.0000021 banana | 0.9999733 Granny Smith<br>0.0000084 lemon<br>0.0000032 fig<br>0.0000021 orange<br>0.0000021 banana |
densenet-169-tf      |-|-| 0.9999826 Granny Smith<br>0.0000046 tennis ball<br>0.0000041 banana<br>0.0000033 lemon<br>0.0000012 fig | 0.9999826 Granny Smith<br>0.0000046 tennis ball<br>0.0000041 banana<br>0.0000033 lemon<br>0.0000012 fig |
googlenet-v1-tf      |-|-| 0.8873318 Granny Smith<br>0.0083221 lemon<br>0.0073108 piggy bank, penny bank<br>0.0063511 pomegranate<br>0.0033214 banana | 0.8873318 Granny Smith<br>0.0083221 lemon<br>0.0073108 piggy bank, penny bank<br>0.0063511 pomegranate<br>0.0033214 banana |
inception-resnet-v2-tf |-|-| 9.1892214 Granny Smith<br>4.2343903 pomegranate<br>3.3494303 lemon<br>3.2723582 crate<br>3.2125196 orange | 9.1892214 Granny Smith<br>4.2343903 pomegranate<br>3.3494303 lemon<br>3.2723582 crate<br>3.2125196 orange |
mobilenet-v1-1.0-224-tf |-|-| 0.7547237 Granny Smith<br>0.0404326 saltshaker, salt shaker<br>0.0232464 lemon<br>0.0218173 fig<br>0.0153219 rubber eraser, rubber, pencil eraser | 0.7547237 Granny Smith<br>0.0404326 saltshaker, salt shaker<br>0.0232464 lemon<br>0.0218173 fig<br>0.0153219 rubber eraser, rubber, pencil eraser |
mobilenet-v2-1.0-224 |-|-| 0.9844691 Granny Smith<br>0.0003918 piggy bank, penny bank<br>0.0002854 green snake, grass snake<br>0.0002140 bell pepper<br>0.0001963 acorn | 0.9844691 Granny Smith<br>0.0003918 piggy bank, penny bank<br>0.0002854 green snake, grass snake<br>0.0002140 bell pepper<br>0.0001963 acorn |
resnet-50-tf         |-|-| 0.9986790 Granny Smith<br>0.0001879 banana<br>0.0001561 acorn<br>0.0001348 lemon<br>0.0000943 fig | 0.9986790 Granny Smith<br>0.0001879 banana<br>0.0001561 acorn<br>0.0001348 lemon<br>0.0000943 fig |
octave-densenet-121-0.125 |-|-| 0.9995084 Granny Smith<br>0.0000520 lemon<br>0.0000359 chime, bell, gong<br>0.0000283 banana<br>0.0000264 gong, tam-tam | 0.9995084 Granny Smith<br>0.0000520 lemon<br>0.0000359 chime, bell, gong<br>0.0000283 banana<br>0.0000264 gong, tam-tam |
octave-resnet-26-0.25 |-|-| 0.9997838 Granny Smith<br>0.0000560 banana<br>0.0000269 lemon<br>0.0000162 crate<br>0.0000125 orange | 0.9997838 Granny Smith<br>0.0000560 banana<br>0.0000269 lemon<br>0.0000162 crate<br>0.0000125 orange |
octave-resnet-50-0.125 |-|-| 0.9987932 Granny Smith<br>0.0002198 banana<br>0.0000979 fig<br>0.0000671 lemon<br>0.0000446 orange | 0.9987932 Granny Smith<br>0.0002198 banana<br>0.0000979 fig<br>0.0000671 lemon<br>0.0000446 orange |
octave-resnet-101-0.125 |-|-| 0.9998088 Granny Smith<br>0.0000348 banana<br>0.0000220 orange<br>0.0000166 lemon<br>0.0000066 strainer | 0.9998088 Granny Smith<br>0.0000348 banana<br>0.0000220 orange<br>0.0000166 lemon<br>0.0000066 strainer |
octave-resnet-200-0.125 |-|-| 0.9997168 Granny Smith<br>0.0000941 banana<br>0.0000320 lemon<br>0.0000292 orange<br>0.0000138 tennis ball | 0.9997168 Granny Smith<br>0.0000941 banana<br>0.0000320 lemon<br>0.0000292 orange<br>0.0000138 tennis ball |
octave-resnext-50-0.25 |-|-| 0.9999181 Granny Smith<br>0.0000171 banana<br>0.0000088 lemon<br>0.0000083 orange<br>0.0000043 mixing bowl | 0.9999181 Granny Smith<br>0.0000171 banana<br>0.0000088 lemon<br>0.0000083 orange<br>0.0000043 mixing bowl |
octave-resnext-101-0.25 |-|-| 0.9998198 Granny Smith<br>0.0000291 orange<br>0.0000121 lemon<br>0.0000120 banana<br>0.0000108 crate | 0.9998198 Granny Smith<br>0.0000291 orange<br>0.0000121 lemon<br>0.0000120 banana<br>0.0000108 crate |
octave-se-resnet-50-0.125 |-|-| 0.9986583 Granny Smith<br>0.0001571 lemon<br>0.0000922 banana<br>0.0000831 tennis ball<br>0.0000627 orange | 0.9986583 Granny Smith<br>0.0001571 lemon<br>0.0000922 banana<br>0.0000831 tennis ball<br>0.0000627 orange |
efficientnet-b0-pytorch |-|-| 9.7391472 Granny Smith<br>3.5226305 orange<br>3.3632121 acorn<br>3.3613660 bell pepper<br>3.1544685 lemon | 9.7391472 Granny Smith<br>3.5226305 orange<br>3.3632121 acorn<br>3.3613660 bell pepper<br>3.1544685 lemon|
efficientnet-b5-pytorch |-|-| 8.3842010 Granny Smith<br>1.5558447 crate<br>1.5187881 velvet<br>1.4974675 orange<br>1.4194057 syringe | 8.3842010 Granny Smith<br>1.5558447 crate<br>1.5187881 velvet<br>1.4974675 orange<br>1.4194057 syringe |
googlenet-v3-pytorch |-|-| 12.0507536 Granny Smith<br>4.8499713 bikini, two-piece<br>2.9098036 piggy bank, penny bank<br>2.9065435 Band Aid<br>2.5095935 brassiere, bra, bandeau | 12.0507536 Granny Smith<br>4.8499713 bikini, two-piece<br>2.9098036 piggy bank, penny bank<br>2.9065435 Band Aid<br>2.5095935 brassiere, bra, bandeau |
googlenet-v4-tf |-|-| 0.9901000 Granny Smith<br>0.0003072 Rhodesian ridgeback<br>0.0001467 hair slide<br>0.0001104 pineapple, ananas<br>0.0000988 banana | 0.9901000 Granny Smith<br>0.0003072 Rhodesian ridgeback<br>0.0001467 hair slide<br>0.0001104 pineapple, ananas<br>0.0000988 banana |
mobilenet-v2-pytorch |-|-| 15.8923168 Granny Smith<br>9.9170008 fig<br>9.8310204 banana<br>9.0233030 lemon<br>8.7704887 custard apple | 15.8923168 Granny Smith<br>9.9170008 fig<br>9.8310204 banana<br>9.0233030 lemon<br>8.7704887 custard apple |
resnet-18-pytorch |-|-| 11.1563597 Granny Smith<br>7.9655943 piggy bank, penny bank<br>7.2275891 teapot<br>7.1502724 lemon<br>7.0498838 saltshaker, salt shaker | 11.1563597 Granny Smith<br>7.9655943 piggy bank, penny bank<br>7.2275891 teapot<br>7.1502724 lemon<br>7.0498838 saltshaker, salt shaker |
resnet-50-pytorch |-|-| 14.6118250 Granny Smith<br>8.5581856 fig<br>7.5287142 acorn<br>6.9782810 orange<br>6.8520732 custard apple | 14.6118250 Granny Smith<br>8.5581856 fig<br>7.5287142 acorn<br>6.9782810 orange<br>6.8520732 custard apple |
squeezenet-1.1-caffe2 |-|-| 0.9936372 Granny Smith<br>0.0014997 lemon<br>0.0013604 fig<br>0.0009127 tennis ball<br>0.0007328 piggy bank, penny bank<br> |0.9936372 Granny Smith<br>0.0014997 lemon<br>0.0013604 fig<br>0.0009127 tennis ball<br>0.0007328 piggy bank, penny bank<br> |
resnet-50-caffe2 |-|-| 0.9997731 Granny Smith<br>0.0000315 fig<br>0.0000229 piggy bank, penny bank<br>0.0000163 bell pepper<br>0.0000142 banana<br> |0.9997731 Granny Smith<br>0.0000315 fig<br>0.0000229 piggy bank, penny bank<br>0.0000163 bell pepper<br>0.0000142 banana<br> |
vgg19-caffe2 |-|-| 0.7076496 Granny Smith<br>0.0804374 acorn<br>0.0471763 fig<br>0.0367173 necklace<br>0.0180223 lemon<br> |0.7076496 Granny Smith<br>0.0804374 acorn<br>0.0471763 fig<br>0.0367173 necklace<br>0.0180223 lemon<br> |
densenet-121-caffe2 |-|-| 15.7890606 Granny Smith<br>9.9466267 lemon<br>9.3717031 orange<br>8.6204128 banana<br>7.1169806 tennis ball<br> |15.7890606 Granny Smith<br>9.9466267 lemon<br>9.3717031 orange<br>8.6204128 banana<br>7.1169806 tennis ball<br> |
googlenet-v2-tf |-|-| 0.9925616 Granny Smith<br>0.0003350 lemon<br>0.0002447 pomegranate<br>0.0002070 tennis ball<br>0.0001847 banana<br> | 0.9925616 Granny Smith<br>0.0003350 lemon<br>0.0002447 pomegranate<br>0.0002070 tennis ball<br>0.0001847 banana<br> |
mobilenet-v3-large-1.0-224-tf |-|-| 0.9964523 Granny Smith<br>0.0002238 bell pepper<br>0.0001825 lemon<br>0.0001672 tennis ball<br>0.0001623 fig<br> | 0.9964523 Granny Smith<br>0.0002238 bell pepper<br>0.0001825 lemon<br>0.0001672 tennis ball<br>0.0001623 fig<br> |
mobilenet-v3-small-1.0-224-tf |-|-| 0.8031732 Granny Smith<br>0.0285428 fig<br>0.0175287 lemon<br>0.0164089 bell pepper<br>0.0091023 strawberry<br> | 0.8031732 Granny Smith<br>0.0285428 fig<br>0.0175287 lemon<br>0.0164089 bell pepper<br>0.0091023 strawberry<br> |
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
mobilenet-v1-0.50-224 |-|-|0.9531036 junco, snowbird<br>0.0448372 chickadee<br>0.0009637 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0007092 jay<br>0.0002787 brambling, Fringilla montifringilla| 0.9531036 junco, snowbird<br>0.0448372 chickadee<br>0.0009637 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0007092 jay<br>0.0002787 brambling, Fringilla montifringilla |
mobilenet-v1-0.50-160 |-|-| 0.8880324 junco, snowbird<br>0.0335562 chickadee<br>0.0318311 coucal<br>0.0251927 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0153771 brambling, Fringilla montifringilla | 0.8880324 junco, snowbird<br>0.0335562 chickadee<br>0.0318311 coucal<br>0.0251927 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0153771 brambling, Fringilla montifringilla |
mobilenet-v1-0.25-128 |-|-| 0.9801749 junco, snowbird<br>0.0190141 chickadee<br>0.0003644 brambling, Fringilla montifringilla<br>0.0002570 jay<br>0.0000603 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9801749 junco, snowbird<br>0.0190141 chickadee<br>0.0003644 brambling, Fringilla montifringilla<br>0.0002570 jay<br>0.0000603 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
mobilenet-v2-1.4-224 |-|-| 0.8708093 junco, snowbird<br>0.0020907 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0017842 water ouzel, dipper<br>0.0014236 brambling, Fringilla montifringilla<br>0.0013358 chickadee | 0.8708093 junco, snowbird<br>0.0020907 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0017842 water ouzel, dipper<br>0.0014236 brambling, Fringilla montifringilla<br>0.0013358 chickadee |
densenet-121-tf      |-|-| 0.9999087 junco, snowbird<br>0.0000453 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000382 brambling, Fringilla montifringilla<br>0.0000042 chickadee<br>0.0000009 magpie | 0.9999087 junco, snowbird<br>0.0000453 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000382 brambling, Fringilla montifringilla<br>0.0000042 chickadee<br>0.0000009 magpie |
densenet-161-tf      |-|-| 0.9999852 junco, snowbird<br>0.0000114 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000026 chickadee<br>0.0000005 brambling, Fringilla montifringilla<br>0.0000001 goldfinch, Carduelis carduelis | 0.9999852 junco, snowbird<br>0.0000114 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000026 chickadee<br>0.0000005 brambling, Fringilla montifringilla<br>0.0000001 goldfinch, Carduelis carduelis |
densenet-169-tf      |-|-| 0.9999551 junco, snowbird<br>0.0000291 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000017 goldfinch, Carduelis carduelis<br>0.0000008 chickadee | 0.9999551 junco, snowbird<br>0.0000291 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000017 goldfinch, Carduelis carduelis<br>0.0000008 chickadee |
googlenet-v1-tf      |-|-| 0.8905121 junco, snowbird<br>0.0376493 brambling, Fringilla montifringilla<br>0.0115120 chickadee<br>0.0029901 goldfinch, Carduelis carduelis<br>0.0027506 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.8905121 junco, snowbird<br>0.0376493 brambling, Fringilla montifringilla<br>0.0115120 chickadee<br>0.0029901 goldfinch, Carduelis carduelis<br>0.0027506 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
inception-resnet-v2-tf |-|-| 10.2546673 junco, snowbird<br>5.3206644 brambling, Fringilla montifringilla<br>3.7312546 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>2.8738835 hamster<br>2.7935846 chickadee | 10.2546673 junco, snowbird<br>5.3206644 brambling, Fringilla montifringilla<br>3.7312546 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>2.8738835 hamster<br>2.7935846 chickadee |
mobilenet-v1-1.0-224-tf |-|-| 0.9979226 junco, snowbird<br>0.0014879 chickadee<br>0.0005082 brambling, Fringilla montifringilla<br>0.0000585 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000071 jay | 0.9979226 junco, snowbird<br>0.0014879 chickadee<br>0.0005082 brambling, Fringilla montifringilla<br>0.0000585 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000071 jay |
mobilenet-v2-1.0-224 |-|-| 0.9005620 junco, snowbird<br>0.0027264 chickadee<br>0.0021331 water ouzel, dipper<br>0.0018665 brambling, Fringilla montifringilla<br>0.0008477 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9005620 junco, snowbird<br>0.0027264 chickadee<br>0.0021331 water ouzel, dipper<br>0.0018665 brambling, Fringilla montifringilla<br>0.0008477 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
resnet-50-tf         |-|-| 0.9999458 junco, snowbird<br>0.0000307 chickadee<br>0.0000170 brambling, Fringilla montifringilla<br>0.0000028 goldfinch, Carduelis carduelis<br>0.0000013 water ouzel, dipper | 0.9999458 junco, snowbird<br>0.0000307 chickadee<br>0.0000170 brambling, Fringilla montifringilla<br>0.0000028 goldfinch, Carduelis carduelis<br>0.0000013 water ouzel, dipper |
octave-densenet-121-0.125 |-|-| 0.9990376 junco, snowbird<br>0.0004191 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003006 brambling, Fringilla montifringilla<br>0.0000517 chickadee<br>0.0000381 house finch, linnet, Carpodacus mexicanus | 0.9990376 junco, snowbird<br>0.0004191 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003006 brambling, Fringilla montifringilla<br>0.0000517 chickadee<br>0.0000381 house finch, linnet, Carpodacus mexicanus |
octave-resnet-26-0.25 |-|-| 0.9870269 junco, snowbird<br>0.0043860 chickadee<br>0.0023245 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0019623 brambling, Fringilla montifringilla<br>0.0008628 water ouzel, dipper | 0.9870269 junco, snowbird<br>0.0043860 chickadee<br>0.0023245 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0019623 brambling, Fringilla montifringilla<br>0.0008628 water ouzel, dipper |
octave-resnet-50-0.125 |-|-| 0.9992077 junco, snowbird<br>0.0001750 chickadee<br>0.0001212 brambling, Fringilla montifringilla<br>0.0000617 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000477 water ouzel, dipper | 0.9992077 junco, snowbird<br>0.0001750 chickadee<br>0.0001212 brambling, Fringilla montifringilla<br>0.0000617 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000477 water ouzel, dipper |
octave-resnet-101-0.125 |-|-| 0.9984739 junco, snowbird<br>0.0002324 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001517 stingray<br>0.0000917 brambling, Fringilla montifringilla<br>0.0000887 chickadee | 0.9984739 junco, snowbird<br>0.0002324 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001517 stingray<br>0.0000917 brambling, Fringilla montifringilla<br>0.0000887 chickadee |
octave-resnet-200-0.125 |-|-| 0.9989060 junco, snowbird<br>0.0001503 chickadee<br>0.0001235 water ouzel, dipper<br>0.0001158 brambling, Fringilla montifringilla<br>0.0000482 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9989060 junco, snowbird<br>0.0001503 chickadee<br>0.0001235 water ouzel, dipper<br>0.0001158 brambling, Fringilla montifringilla<br>0.0000482 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
octave-resnext-50-0.25 |-|-| 0.9998038 junco, snowbird<br>0.0000257 water ouzel, dipper<br>0.0000235 chickadee<br>0.0000088 brambling, Fringilla montifringilla<br>0.0000084 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9998038 junco, snowbird<br>0.0000257 water ouzel, dipper<br>0.0000235 chickadee<br>0.0000088 brambling, Fringilla montifringilla<br>0.0000084 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
octave-resnext-101-0.25 |-|-| 0.9993037 junco, snowbird<br>0.0001226 chickadee<br>0.0000465 water ouzel, dipper<br>0.0000303 brambling, Fringilla montifringilla<br>0.0000250 American coot, marsh hen, mud hen, water hen, Fulica americana | 0.9993037 junco, snowbird<br>0.0001226 chickadee<br>0.0000465 water ouzel, dipper<br>0.0000303 brambling, Fringilla montifringilla<br>0.0000250 American coot, marsh hen, mud hen, water hen, Fulica americana |
octave-se-resnet-50-0.125 |-|-| 0.9998600 junco, snowbird<br>0.0000210 American coot, marsh hen, mud hen, water hen, Fulica americana<br>0.0000168 chickadee<br>0.0000152 water ouzel, dipper<br>0.0000130 brambling, Fringilla montifringilla | 0.9998600 junco, snowbird<br>0.0000210 American coot, marsh hen, mud hen, water hen, Fulica americana<br>0.0000168 chickadee<br>0.0000152 water ouzel, dipper<br>0.0000130 brambling, Fringilla montifringilla |
efficientnet-b0-pytorch |-|-| 10.1476469 junco, snowbird<br>3.6771660 chickadee<br>2.6902854 water ouzel, dipper<br>2.3145211 magpie<br>2.3114707 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 10.1476469 junco, snowbird<br>3.6771660 chickadee<br>2.6902854 water ouzel, dipper<br>2.3145211 magpie<br>2.3114707 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
efficientnet-b5-pytorch |-|-| 8.4623203 junco, snowbird<br>3.4612336 brambling, Fringilla montifringilla<br>2.5436187 water ouzel, dipper<br>2.5078721 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>1.7481347 chickadee | 8.4623203 junco, snowbird<br>3.4612336 brambling, Fringilla montifringilla<br>2.5436187 water ouzel, dipper<br>2.5078721 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>1.7481347 chickadee |
googlenet-v3-pytorch |-|-| 9.4771719 junco, snowbird<br>2.3352063 cleaver, meat cleaver, chopper<br>2.2170811 iron, smoothing iron<br>2.1353395 American coot, marsh hen, mud hen, water hen, Fulica americana<br>1.9554796 water ouzel, dipper | 9.4771719 junco, snowbird<br>2.3352063 cleaver, meat cleaver, chopper<br>2.2170811 iron, smoothing iron<br>2.1353395 American coot, marsh hen, mud hen, water hen, Fulica americana<br>1.9554796 water ouzel, dipper |
googlenet-v4-tf |-|-| 0.9426626 junco, snowbird<br>0.0005340 chickadee<br>0.0004552 hamster<br>0.0004131 brambling, Fringilla montifringilla<br>0.0003347 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9426626 junco, snowbird<br>0.0005340 chickadee<br>0.0004552 hamster<br>0.0004131 brambling, Fringilla montifringilla<br>0.0003347 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
mobilenet-v2-pytorch |-|-| 24.4762611 junco, snowbird<br>17.2693577 brambling, Fringilla montifringilla<br>15.7566624 chickadee<br>14.8050203 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>13.3634481 jay | 124.4762611 junco, snowbird<br>17.2693577 brambling, Fringilla montifringilla<br>15.7566624 chickadee<br>14.8050203 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>13.3634481 jay |
resnet-18-pytorch |-|-| 26.9606190 junco, snowbird<br>18.8664570 chickadee<br>17.9463902 brambling, Fringilla montifringilla<br>14.6226025 house finch, linnet, Carpodacus mexicanus<br>14.5083055 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 26.9606190 junco, snowbird<br>18.8664570 chickadee<br>17.9463902 brambling, Fringilla montifringilla<br>14.6226025 house finch, linnet, Carpodacus mexicanus<br>14.5083055 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
resnet-50-pytorch |-|-| 18.4067059 junco, snowbird<br>10.4681416 chickadee<br>9.9149208 goldfinch, Carduelis carduelis<br>9.8933001 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.5323343 brambling, Fringilla montifringilla | 18.4067059 junco, snowbird<br>10.4681416 chickadee<br>9.9149208 goldfinch, Carduelis carduelis<br>9.8933001 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.5323343 brambling, Fringilla montifringilla |
squeezenet-1.1-caffe2 |-|-| 0.9936494 junco, snowbird<br>0.0061753 chickadee<br>0.0000763 jay<br>0.0000375 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000267 brambling, Fringilla montifringilla<br> |0.9936494 junco, snowbird<br>0.0061753 chickadee<br>0.0000763 jay<br>0.0000375 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000267 brambling, Fringilla montifringilla<br> |
resnet-50-caffe2 |-|-| 0.9979601 junco, snowbird<br>0.0007472 chickadee<br>0.0006533 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0004094 brambling, Fringilla montifringilla<br>0.0000683 goldfinch, Carduelis carduelis<br> |0.9979601 junco, snowbird<br>0.0007472 chickadee<br>0.0006533 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0004094 brambling, Fringilla montifringilla<br>0.0000683 goldfinch, Carduelis carduelis<br> |
vgg19-caffe2 |-|-| 0.9999392 junco, snowbird<br>0.0000582 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br> |0.9999392 junco, snowbird<br>0.0000582 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br> |
densenet-121-caffe2 |-|-| 17.8101349 junco, snowbird<br>11.4563322 brambling, Fringilla montifringilla<br>11.3156567 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3476629 chickadee<br>8.2407246 magpie<br> |17.8101349 junco, snowbird<br>11.4563322 brambling, Fringilla montifringilla<br>11.3156567 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3476629 chickadee<br>8.2407246 magpie<br> |
googlenet-v2-tf |-|-| 0.9513915 junco, snowbird<br>0.0017740 chickadee<br>0.0015845 brambling, Fringilla montifringilla<br>0.0009359 loupe, jeweler's loupe<br>0.0007033 American coot, marsh hen, mud hen, water hen, Fulica americana<br> | 0.9513915 junco, snowbird<br>0.0017740 chickadee<br>0.0015845 brambling, Fringilla montifringilla<br>0.0009359 loupe, jeweler's loupe<br>0.0007033 American coot, marsh hen, mud hen, water hen, Fulica americana<br> |
mobilenet-v3-large-1.0-224-tf |-|-| 0.8878838 junco, snowbird<br>0.0007329 American coot, marsh hen, mud hen, water hen, Fulica americana<br>0.0007141 brambling, Fringilla montifringilla<br>0.0006302 water ouzel, dipper<br>0.0005295 wood rabbit, cottontail, cottontail rabbit<br> | 0.8878838 junco, snowbird<br>0.0007329 American coot, marsh hen, mud hen, water hen, Fulica americana<br>0.0007141 brambling, Fringilla montifringilla<br>0.0006302 water ouzel, dipper<br>0.0005295 wood rabbit, cottontail, cottontail rabbit<br> |
mobilenet-v3-small-1.0-224-tf |-|-| 0.9574909 junco, snowbird<br>0.0016714 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0016443 chickadee<br>0.0009580 jay<br>0.0006632 brambling, Fringilla montifringilla<br> | 0.9574909 junco, snowbird<br>0.0016714 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0016443 chickadee<br>0.0009580 jay<br>0.0006632 brambling, Fringilla montifringilla<br> |

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
mobilenet-v1-0.50-224 |-|-|0.9207528 lifeboat<br>0.0332536 container ship, containership, container vessel<br>0.0132192 liner, ocean liner<br>0.0109554 pirate, pirate ship<br>0.0074297 fireboat| 0.9207528 lifeboat<br>0.0332536 container ship, containership, container vessel<br>0.0132192 liner, ocean liner<br>0.0109554 pirate, pirate ship<br>0.0074297 fireboat |
mobilenet-v1-0.50-160 |-|-| 0.9510298 lifeboat<br>0.0139963 container ship, containership, container vessel<br>0.0101495 drilling platform, offshore rig<br>0.0084767 pirate, pirate ship<br>0.0035462 liner, ocean liner | 0.9510298 lifeboat<br>0.0139963 container ship, containership, container vessel<br>0.0101495 drilling platform, offshore rig<br>0.0084767 pirate, pirate ship<br>0.0035462 liner, ocean liner |
mobilenet-v1-0.25-128 |-|-| 0.8000437 lifeboat<br>0.0681745 container ship, containership, container vessel<br>0.0423642 pirate, pirate ship<br>0.0320394 liner, ocean liner<br>0.0205678 fireboat | 0.8000437 lifeboat<br>0.0681745 container ship, containership, container vessel<br>0.0423642 pirate, pirate ship<br>0.0320394 liner, ocean liner<br>0.0205678 fireboat |
mobilenet-v2-1.4-224 |-|-| 0.8931452 lifeboat<br>0.0078881 container ship, containership, container vessel<br>0.0038566 liner, ocean liner<br>0.0020695 dock, dockage, docking facility<br>0.0017923 pirate, pirate ship | 0.8931452 lifeboat<br>0.0078881 container ship, containership, container vessel<br>0.0038566 liner, ocean liner<br>0.0020695 dock, dockage, docking facility<br>0.0017923 pirate, pirate ship |
densenet-121-tf      |-|-| 0.9997229 lifeboat<br>0.0000948 container ship, containership, container vessel<br>0.0000550 drilling platform, offshore rig<br>0.0000301 liner, ocean liner<br>0.0000284 pirate, pirate ship | 0.9997229 lifeboat<br>0.0000948 container ship, containership, container vessel<br>0.0000550 drilling platform, offshore rig<br>0.0000301 liner, ocean liner<br>0.0000284 pirate, pirate ship |
densenet-161-tf      |-|-| 0.9999855 lifeboat<br>0.0000066 liner, ocean liner<br>0.0000014 stretcher<br>0.0000011 fireboat<br>0.0000011 ambulance | 0.9999855 lifeboat<br>0.0000066 liner, ocean liner<br>0.0000014 stretcher<br>0.0000011 fireboat<br>0.0000011 ambulance |
densenet-169-tf      |-|-| 0.9953577 lifeboat<br>0.0016744 beacon, lighthouse, beacon light, pharos<br>0.0011535 container ship, containership, container vessel<br> 0.0008674 drilling platform, offshore rig<br>0.0001324 dock, dockage, docking facility | 0.9953577 lifeboat<br>0.0016744 beacon, lighthouse, beacon light, pharos<br>0.0011535 container ship, containership, container vessel<br>0.0008674 drilling platform, offshore rig<br>0.0001324 dock, dockage, docking facility |
googlenet-v1-tf      |-|-| 0.5706096 lifeboat<br>0.0325632 fireboat<br>0.0318643 drilling platform, offshore rig<br>0.0204104 container ship, containership, container vessel<br>0.0166424 breakwater, groin, groyne, mole, bulwark, seawall, jetty | 0.5706096 lifeboat<br>0.0325632 fireboat<br>0.0318643 drilling platform, offshore rig<br>0.0204104 container ship, containership, container vessel<br>0.0166424 breakwater, groin, groyne, mole, bulwark, seawall, jetty |
inception-resnet-v2-tf |-|-| 8.9238806 lifeboat<br>5.3607121 fireboat<br>4.2531099 beacon, lighthouse, beacon light, pharos<br>3.9253387 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>3.2657926 ambulance | 8.9238806 lifeboat<br>5.3607121 fireboat<br>4.2531099 beacon, lighthouse, beacon light, pharos<br>3.9253387 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>3.2657926 ambulance |
mobilenet-v1-1.0-224-tf |-|-| 0.9885072 lifeboat<br>0.0053199 fireboat<br>0.0021362 liner, ocean liner<br>0.0006076 pirate, pirate ship<br>0.0005722 submarine, pigboat, sub, U-boat | 0.9885072 lifeboat<br>0.0053199 fireboat<br>0.0021362 liner, ocean liner<br>0.0006076 pirate, pirate ship<br>0.0005722 submarine, pigboat, sub, U-boat |
mobilenet-v2-1.0-224 |-|-| 0.2958112 lifeboat<br>0.1187274 wreck<br>0.0404658 beacon, lighthouse, beacon light, pharos<br>0.0361662 liner, ocean liner<br>0.0325511 pirate, pirate ship | 0.2958112 lifeboat<br>0.1187274 wreck<br>0.0404658 beacon, lighthouse, beacon light, pharos<br>0.0361662 liner, ocean liner<br>0.0325511 pirate, pirate ship |
resnet-50-tf         |-|-| 0.9849118 lifeboat<br>0.0031136 drilling platform, offshore rig<br>0.0026399 pirate, pirate ship<br>0.0016441 submarine, pigboat, sub, U-boat<br>0.0013418 liner, ocean liner | 0.9849118 lifeboat<br>0.0031136 drilling platform, offshore rig<br>0.0026399 pirate, pirate ship<br>0.0016441 submarine, pigboat, sub, U-boat<br>0.0013418 liner, ocean liner |
octave-densenet-121-0.125 |-|-| 0.9545669 lifeboat<br>0.0113774 drilling platform, offshore rig<br>0.0054029 pirate, pirate ship<br>0.0053649 fireboat<br>0.0029413 submarine, pigboat, sub, U-boat | 0.9545669 lifeboat<br>0.0113774 drilling platform, offshore rig<br>0.0054029 pirate, pirate ship<br>0.0053649 fireboat<br>0.0029413 submarine, pigboat, sub, U-boat |
octave-resnet-26-0.25 |-|-| 0.9636158 lifeboat<br>0.0068367 pirate, pirate ship<br>0.0032900 fireboat<br>0.0030672 drilling platform, offshore rig<br>0.0026319 dock, dockage, docking facility | 0.9636158 lifeboat<br>0.0068367 pirate, pirate ship<br>0.0032900 fireboat<br>0.0030672 drilling platform, offshore rig<br>0.0026319 dock, dockage, docking facility |
octave-resnet-50-0.125 |-|-| 0.9486050 lifeboat<br>0.0069884 drilling platform, offshore rig<br>0.0045387 submarine, pigboat, sub, U-boat<br>0.0042334 beacon, lighthouse, beacon light, pharos<br>0.0032207 fireboat | 0.9486050 lifeboat<br>0.0069884 drilling platform, offshore rig<br>0.0045387 submarine, pigboat, sub, U-boat<br>0.0042334 beacon, lighthouse, beacon light, pharos<br>0.0032207 fireboat |
octave-resnet-101-0.125 |-|-| 0.9119062 lifeboat<br>0.0460690 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0070753 beacon, lighthouse, beacon light, pharos<br>0.0052224 dock, dockage, docking facility<br>0.0043461 container ship, containership, container vessel | 0.9119062 lifeboat<br>0.0460690 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0070753 beacon, lighthouse, beacon light, pharos<br>0.0052224 dock, dockage, docking facility<br>0.0043461 container ship, containership, container vessel |
octave-resnet-200-0.125 |-|-| 0.8956272 lifeboat<br>0.0493709 drilling platform, offshore rig<br>0.0047381 pirate, pirate ship<br>0.0046724 container ship, containership, container vessel<br>0.0043291 breakwater, groin, groyne, mole, bulwark, seawall, jetty | 0.8956272 lifeboat<br>0.0493709 drilling platform, offshore rig<br>0.0047381 pirate, pirate ship<br>0.0046724 container ship, containership, container vessel<br>0.0043291 breakwater, groin, groyne, mole, bulwark, seawall, jetty |
octave-resnext-50-0.25 |-|-| 0.8762087 lifeboat<br>0.0160635 beacon, lighthouse, beacon light, pharos<br>0.0149170 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0149014 drilling platform, offshore rig<br>0.0061156 submarine, pigboat, sub, U-boat | 0.8762087 lifeboat<br>0.0160635 beacon, lighthouse, beacon light, pharos<br>0.0149170 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0149014 drilling platform, offshore rig<br>0.0061156 submarine, pigboat, sub, U-boat |
octave-resnext-101-0.25 |-|-| 0.9993466 lifeboat<br>0.0001624 drilling platform, offshore rig<br>0.0000493 speedboat<br>0.0000416 fireboat<br>0.0000302 breakwater, groin, groyne, mole, bulwark, seawall, jetty | 0.9993466 lifeboat<br>0.0001624 drilling platform, offshore rig<br>0.0000493 speedboat<br>0.0000416 fireboat<br>0.0000302 breakwater, groin, groyne, mole, bulwark, seawall, jetty |
octave-se-resnet-50-0.125 |-|-| 0.9959252 lifeboat<br>0.0019638 drilling platform, offshore rig<br>0.0005667 pirate, pirate ship<br>0.0002329 fireboat<br>0.0002115 container ship, containership, container vessel | 0.9959252 lifeboat<br>0.0019638 drilling platform, offshore rig<br>0.0005667 pirate, pirate ship<br>0.0002329 fireboat<br>0.0002115 container ship, containership, container vessel |
efficientnet-b0-pytorch |-|-| 9.2542114 lifeboat<br>3.7016888 drilling platform, offshore rig<br>2.7736561 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.6344781 submarine, pigboat, sub, U-boat<br>2.6151254 liner, ocean liner | 9.2542114 lifeboat<br>3.7016888 drilling platform, offshore rig<br>2.7736561 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.6344781 submarine, pigboat, sub, U-boat<br>2.6151254 liner, ocean liner   |
efficientnet-b5-pytorch |-|-| 8.9733467 lifeboat<br>2.9514761 beacon, lighthouse, beacon light, pharos<br>2.7094901 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.1320240 liner, ocean liner<br>2.1210849 fireboat | 8.9733467 lifeboat<br>2.9514761 beacon, lighthouse, beacon light, pharos<br>2.7094901 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.1320240 liner, ocean liner<br>2.1210849 fireboat |
googlenet-v3-pytorch |-|-| 10.0639114 lifeboat<br>3.8664410 backpack, back pack, knapsack, packsack, rucksack, haversack<br>2.6585104 beacon, lighthouse, beacon light, pharos<br>2.5443556 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.2744753 fireboat | 10.0639114 lifeboat<br>3.8664410 backpack, back pack, knapsack, packsack, rucksack, haversack<br>2.6585104 beacon, lighthouse, beacon light, pharos<br>2.5443556 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.2744753 fireboat |
googlenet-v4-tf |-|-| 0.9516075 lifeboat<br>0.0006138 fireboat<br>0.0005795 submarine, pigboat, sub, U-boat<br>0.0003894 ambulance<br>0.0003887 drilling platform, offshore rig | 0.9516075 lifeboat<br>0.0006138 fireboat<br>0.0005795 submarine, pigboat, sub, U-boat<br>0.0003894 ambulance<br>0.0003887 drilling platform, offshore rig |
mobilenet-v2-pytorch |-|-| 12.1402197 lifeboat<br>9.1929836 liner, ocean liner<br>8.8613186 dock, dockage, docking facility<br>8.1034260 pirate, pirate ship<br>7.8462739 container ship, containership, container vessel | 12.1402197 lifeboat<br>9.1929836 liner, ocean liner<br>8.8613186 dock, dockage, docking facility<br>8.1034260 pirate, pirate ship<br>7.8462739 container ship, containership, container vessel |
resnet-18-pytorch |-|-| 12.5820255 lifeboat<br>8.4857988 submarine, pigboat, sub, U-boat<br>8.3734007 drilling platform, offshore rig<br>8.3499556 pirate, pirate ship<br>8.1648674 liner, ocean liner | 12.5820255 lifeboat<br>8.4857988 submarine, pigboat, sub, U-boat<br>8.3734007 drilling platform, offshore rig<br>8.3499556 pirate, pirate ship<br>8.1648674 liner, ocean liner |
resnet-50-pytorch |-|-| 15.0844460 lifeboat<br>9.2421970 container ship, containership, container vessel<br>9.0593367 drilling platform, offshore rig<br>8.6655445 liner, ocean liner<br>8.5165682 pirate, pirate ship | 15.0844460 lifeboat<br>9.2421970 container ship, containership, container vessel<br>9.0593367 drilling platform, offshore rig<br>8.6655445 liner, ocean liner<br>8.5165682 pirate, pirate ship |
squeezenet-1.1-caffe2 |-|-| 0.9580537 lifeboat<br>0.0206635 container ship, containership, container vessel<br>0.0100353 drilling platform, offshore rig<br>0.0032692 pirate, pirate ship<br>0.0029469 dock, dockage, docking facility<br> |0.9580537 lifeboat<br>0.0206635 container ship, containership, container vessel<br>0.0100353 drilling platform, offshore rig<br>0.0032692 pirate, pirate ship<br>0.0029469 dock, dockage, docking facility<br> |
resnet-50-caffe2 |-|-| 0.9745282 lifeboat<br>0.0084851 drilling platform, offshore rig<br>0.0048212 container ship, containership, container vessel<br>0.0033455 liner, ocean liner<br>0.0024074 wreck<br> |0.9745282 lifeboat<br>0.0084851 drilling platform, offshore rig<br>0.0048212 container ship, containership, container vessel<br>0.0033455 liner, ocean liner<br>0.0024074 wreck<br> |
vgg19-caffe2 |-|-| 0.9965143 lifeboat<br>0.0008843 container ship, containership, container vessel<br>0.0004789 drilling platform, offshore rig<br>0.0003978 dock, dockage, docking facility<br>0.0003630 fireboat<br> |0.9965143 lifeboat<br>0.0008843 container ship, containership, container vessel<br>0.0004789 drilling platform, offshore rig<br>0.0003978 dock, dockage, docking facility<br>0.0003630 fireboat<br> |
densenet-121-caffe2 |-|-| 13.9694653 lifeboat<br>7.8196640 drilling platform, offshore rig<br>7.7403646 liner, ocean liner<br>7.5737677 wreck<br>7.5640950 pirate, pirate ship<br> |13.9694653 lifeboat<br>7.8196640 drilling platform, offshore rig<br>7.7403646 liner, ocean liner<br>7.5737677 wreck<br>7.5640950 pirate, pirate ship<br> |
googlenet-v2-tf |-|-| 0.6411989 lifeboat<br>0.0454055 fireboat<br>0.0321753 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0219396 beacon, lighthouse, beacon light, pharos<br>0.0132107 dock, dockage, docking facility<br> | 0.6411989 lifeboat<br>0.0454055 fireboat<br>0.0321753 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0219396 beacon, lighthouse, beacon light, pharos<br>0.0132107 dock, dockage, docking facility<br> |
mobilenet-v3-large-1.0-224-tf |-|-| 0.8509533 lifeboat<br>0.0020929 drilling platform, offshore rig<br>0.0014489 fireboat<br>0.0013909 freight car<br>0.0013567 yellow lady's slipper, yellow lady-slipper, Cypripedium calceolus, Cypripedium parviflorum<br> | 0.8509533 lifeboat<br>0.0020929 drilling platform, offshore rig<br>0.0014489 fireboat<br>0.0013909 freight car<br>0.0013567 yellow lady's slipper, yellow lady-slipper, Cypripedium calceolus, Cypripedium parviflorum<br> |
mobilenet-v3-small-1.0-224-tf |-|-| 0.7360849 lifeboat<br>0.0156675 liner, ocean liner<br>0.0123008 pirate, pirate ship<br>0.0066379 fireboat<br>0.0059411 beacon, lighthouse, beacon light, pharos<br> | 0.7360849 lifeboat<br>0.0156675 liner, ocean liner<br>0.0123008 pirate, pirate ship<br>0.0066379 fireboat<br>0.0059411 beacon, lighthouse, beacon light, pharos<br> |

### Классификация, нестандартные модели

Источник: набор данных [MRL Eye Dataset][mrl_eye_dataset]



   Название модели   | Изображение |Особенности  |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
open-closed-eye-0001 | <img width="150" src="images\1-closed-eye.png"> |Only batch = 1 works correctly  | 0.9999934 closed <br> 0.0000066 open <br> | 0.9999934 closed <br> 0.0000066 open <br> |
open-closed-eye-0001 | <img width="150" src="images\2-opened-eye.png"> |Only batch = 1 works correctly  | 0.9999905 open <br> 0.0000094 closed <br> | 0.9999905 open <br> 0.0000094 closed <br> |
open-closed-eye-0001 | <img width="150" src="images\3-opened-eye.png"> |Only batch = 1 works correctly  | 1.0000000 open <br> 0.0000000 closed <br> | .0000000 open <br> 0.0000000 closed <br> |

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
ssd_mobilenet_v2_coco     | - | - | Окаймляющий прямоугольник: (76,168), (231,344)| Окаймляющие прямоугольники: (75,165), (232,344),<br> (380,315), (610,410) |
mobilenet-ssd             | - | - | Окаймляющий прямоугольник: (380,315), (630,415) | Окаймляющий прямоугольник: (377,314), (632,415) |
ssd300                    | - | - | Окаймляющий прямоугольник: (380,165), (595,425) | Окаймляющий прямоугольник: (380,165), (595,425) |
ssd512                    | - | - | Окаймляющий прямоугольник: (377,163), (595,425) | Окаймляющий прямоугольник: (380,165), (595,425) |
ssd_mobilenet_v1_fpn_coco | - | - | Окаймляющие прямоугольники: (295, 131), (439, 291),<br> (375, 217), (582, 425),<br> (436, 153), (611, 301) |  Окаймляющие прямоугольники: (295, 131), (439, 291),<br> (375, 217), (582, 425),<br> (436, 153), (611, 301) |

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
ssd_mobilenet_v2_coco     | - | - | Окаймляющий прямоугольник: (90,100), (356,448) | Окаймляющий прямоугольник: (90,100), (350,450)|
mobilenet-ssd             | - | - | Окаймляющий прямоугольник: (92,95), (361,483)  | Окаймляющий прямоугольник: (94,94), (361,480) |
ssd300                    | - | - | Окаймляющий прямоугольник: (68,100), (336,452) | Окаймляющий прямоугольник: (66,98), (340,455) |
ssd512                    | - | - | Окаймляющий прямоугольник: (75,100), (355,445) | Окаймляющий прямоугольник: (75,100), (355,445)|
ssd_mobilenet_v1_fpn_coco | - | - |Окаймляющий прямоугольник: (89, 98), (345, 440) |Окаймляющий прямоугольник: (89, 98), (345, 440)|

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
ssd_mobilenet_v2_coco     | - | - | Окаймляющий прямоугольник: (81,244), (267,376)  | Окаймляющий прямоугольник: (80,244), (267,376)  |
mobilenet-ssd             | - | - | Окаймляющий прямоугольник: (80,140), (270,375)  | Окаймляющий прямоугольник: (80,140), (270,375)  |
ssd300                    | - | - | Окаймляющий прямоугольник: (80,155), (270,375)  | Окаймляющий прямоугольник: (80,157), (274,375)  |
ssd512                    | - | - | Окаймляющий прямоугольник: (75,170), (172,370)  | Окаймляющий прямоугольник: (73,170), (173,371)  |
ssd_mobilenet_v1_fpn_coco | - | - | Окаймляющий прямоугольник: (90, 135), (260, 375)| Окаймляющий прямоугольник: (90, 135), (260, 375)|

### Тестовое изображение 4
Источник: [MS COCO][ms_coco]

Исходное разрешение: 640 x 480


Входное изображение:

<div style='float: center'>
<img width="300" src="images\9.jpg">
<div style='float: center'>
Входной тензор: 600; 1024; 1

Результат детектирования:
</div>
<img width="300" src="detection\faster_rcnn_out.bmp">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>TV (110, 41), (397, 304)<br>MOUSE (508, 337), (559, 374)<br>KEYBOARD (241, 342), (496, 461)<br>

   Название модели                          |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
--------------------------------------------|----------------------------------|----------------------------------|--------------------------------|------------------------------------|
faster_rcnn_inception_resnet_v2_atrous_coco |-|-| Окаймляющий прямоугольник:<br>TV (110, 41), (397, 304)<br>MOUSE (508, 337), (559, 374)<br>KEYBOARD (241, 342), (496, 461) | Окаймляющий прямоугольник:<br>TV (110, 41), (397, 304)<br>MOUSE (508, 337), (559, 374)<br>KEYBOARD (241, 342), (496, 461)<br>|
faster_rcnn_inception_v2_coco               |-|-| Окаймляющий прямоугольник:<br>DINING TABLE (8, 201), (640, 480)<br>TV (106, 31), (397, 284)<br>MOUSE (509, 336), (560, 377)<br>KEYBOARD (231, 339), (495, 462) | Окаймляющий прямоугольник:<br>DINING TABLE (8, 201), (640, 480)<br>TV (106, 31), (397, 284)<br>MOUSE (509, 336), (560, 377)<br>KEYBOARD (231, 339), (495, 462)<br>|
faster_rcnn_resnet50_coco                   |-|-| Окаймляющий прямоугольник:<br>TV (104, 34), (400, 282)<br>MOUSE (510, 336), (563, 373)<br>KEYBOARD (239, 339), (496, 463) | Окаймляющий прямоугольник:<br>TV (104, 34), (400, 282)<br>MOUSE (510, 336), (563, 373)<br>KEYBOARD (239, 339), (496, 463)<br>|
faster_rcnn_resnet101_coco                  |-|-| Окаймляющий прямоугольник:<br>TV (105, 37), (400, 305)<br>MOUSE (505, 337), (559, 375)<br>KEYBOARD (231, 341), (499, 466) | Окаймляющий прямоугольник:<br>TV (105, 37), (400, 305)<br>MOUSE (505, 337), (559, 375)<br>KEYBOARD (231, 341), (499, 466)<br>|

### Тестовое изображение 5
Источник: [MS COCO][ms_coco]

Исходное разрешение: 640 x 427


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" src="images\000000367818.jpg">
<img width="300" src="detection\python_yolo_coco_000000367818.bmp">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>PERSON (86, 84), (394, 188)<br>HORSE (44, 108), (397, 565)<br>

   Название модели                          |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
--------------------------------------------|----------------------------------|----------------------------------|--------------------------------|------------------------------------|
yolo-v3-tf                   |-|-| Окаймляющий прямоугольник:<br>PERSON (86, 84), (394, 188)<br>HORSE (44, 108), (397, 565) | Окаймляющий прямоугольник:<br>PERSON (86, 84), (394, 188)<br>HORSE (44, 108), (397, 565)<br>|
yolo-v2-tf                   |-|-| Окаймляющий прямоугольник:<br>PERSON (96, 74), (379, 173)<br>HORSE (48, 122), (385, 590) | Окаймляющий прямоугольник:<br>PERSON (96, 74), (379, 173)<br>HORSE (48, 122), (385, 590)<br>|
yolo-v2-tiny-tf                   |-|-| Окаймляющий прямоугольник:<br>PERSON (84, 70), (413, 195)<br>HORSE (100, 92), (398, 562) | Окаймляющий прямоугольник:<br>PERSON (84, 70), (413, 195)<br>HORSE (100, 92), (398, 562)<br>|

### Тестовое изображение 6
Источник: [Pascal VOC][PASCAL_VOC_2012]

Исходное разрешение: 500 x 375


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" src="images\2011_002352.jpg">
<img width="300" src="detection\python_yolo_voc_2011_002352.bmp">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>AEROPLANE (131, 21), (248, 414)<br>

   Название модели                          |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
--------------------------------------------|----------------------------------|----------------------------------|--------------------------------|------------------------------------|
yolo-v1-tiny-tf                   |-|-| Окаймляющий прямоугольник:<br>AEROPLANE (131, 21), (248, 414)<br>| Окаймляющий прямоугольник:<br>AEROPLANE (131, 21), (248, 414)<br>|

## Результаты распознавания лиц

### Тестовое изображение 1

Источник: набор данных [VGGFace2][vgg_face2]  

Исходное разрешение: 96 x 112


Изображение:

<div style='float: center'>
<img src="images\sphereface.jpg">
</div>

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|---------------------------|---------------------------|-----------------------------|------------------------------------|
Sphereface           |-|-| 0.77 0.70 0.77 -1.79 1.00<br> -0.02 0.82 -0.44 -0.96 0.37<br> ...<br> -0.74 0.25 -0.35 2.06 1.16<br> 0.56 -1.14 0.50 0.46 -0.91<br> [Полный тензор][sphereface_sync] | 0.77 0.70 0.77 -1.79 1.00<br> -0.02 0.82 -0.44 -0.96 0.37<br> ...<br> -0.74 0.25 -0.35 2.06 1.16<br> 0.56 -1.14 0.50 0.46 -0.91<br> [Полный тензор][sphereface_async] |

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

### Тестовое изображение 4

Источник: набор данных [PASCAL VOC 2012][PASCAL_VOC_2012]

Исходное разрешение: 500 x 375
﻿

Исходное изображение:

<div style='float: center'>
<img width="300" src="images\Sheep.jpg">
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   C++ (latency mode, пример из OpenVINO)  |  C++ (throughput mode, пример из OpenVINO)  |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|---------------------------|---------------------------|-----------------------------|------------------------------------|
deeplabv3             |-|-|<div style='float: center'><img width="150" src="semantic_segmentation\python_sync_sheep.bmp"></img></div>|<div style='float: center'><img width="150" src="semantic_segmentation\python_sync_sheep.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="300" src="semantic_segmentation\pascal_colormap.jpg">
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
[ms_coco]: http://cocodataset.org
[PASCAL_VOC_2012]: http://host.robots.ox.ac.uk/pascal/VOC/voc2012
[vgg_face2]:http://www.robots.ox.ac.uk/~vgg/data/vgg_face2
[sphereface_sync]:recognition/sphereface_out_sync.csv
[sphereface_async]:recognition/sphereface_out_async.csv
[cityscapes]: https://www.cityscapes-dataset.com
[mrl_eye_dataset]: http://mrl.cs.vsb.cz/eyedataset
