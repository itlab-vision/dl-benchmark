# Результаты проверки корректности вывода с использованием разных режимов

## Результаты классификации

### Тестовое изображение 1

Источник: набор данных [ImageNet][imagenet]

Разрешение: 709 x 510
﻿

<img src="..\data\ILSVRC2012_val_00000023.JPEG" width="150">


   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |0.9896095 label #948<br>0.0037969 label #945<br>0.0013717 label #719<br>988 0.0011059 label #988<br>0.0009710 label #952|                           |0.9896094 Granny Smith<br>0.0037969 bell pepper<br>0.0013717 piggy bank, penny bank<br>0.0011059 acorn<br>0.0009710 fig|                            |
densenet-121         |15.7979183 label #948<br>9.9429474 label #951<br>9.3676052 label #950<br>8.6181602 label #954<br>7.1164069 label #852|                           |15.7979164 Granny Smith<br>9.9429455 lemon<br>9.3676043 orange<br>8.6181612 banana<br>7.1164074 tennis ball|                            |
densenet-161         ||                           |17.8060474 Granny Smith<br>8.5503120 lemon<br>7.6080256 orange<br>7.2737975 banana<br>7.1114807 fig|                            |
densenet-169         |                           |                           |15.9379349 Granny Smith<br>6.3490119 banana<br>6.2573476 lemon<br>5.8869209 tennis ball<br>5.7489214 piggy bank, penny bank|                            |
densenet-201         |                           |                           |                              |                            |
googlenet-v1         |0.9982976 label #948<br>0.0005613 label #945<br>0.0003487 label #470<br>0.0000679 label #852<br>0.0000656 label #719|                           |0.9982972 Granny Smith<br>0.0005613 bell pepper<br>0.0003487 candle, taper, wax light<br>0.0000679 label tennis ball<br>0.0000656 label piggy bank, penny bank|                            |
googlenet-v2         |0.9938872 label #317<br>0.0042250 label #734<br>0.0005423 label #322<br>0.0001996 label #318<br>0.0000883 label #319|                           |0.9938846 leafhopper<br>0.0042250 police van, police wagon, paddy wagon, patrol wagon, wagon, black Maria<br>0.0005423 ringlet, ringlet butterfly<br>0.0001996 lacewing, lacewing fly<br>0.0000883 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk|                            |
googlenet-v3         |0.9909649 label #949<br>0.0007918 label #446<br>0.0001872 label #720<br>0.0001239 label #420<br>0.0000879 label #460|                           |0.9909641 strawberry<br>0.0007918 binder, ring-binder<br>0.0001872 pill bottle<br>0.0001239 banjo|                           |
googlenet-v4         |0.9865599 label #948<br>0.0003842 label #159<br>0.0002123 label #584<br>0.0001513 label #953<br>0.0001259 label #954|                           |0.9865599 Granny Smith<br>0.0003842 Rhodesian ridgeback<br>0.0002123 hair slide<br>0.0001513 pineapple, ananas<br>0.0001259 banana|                            |
inception-resnet-v2  |0.9982991 label #948<br>0.0000684 label #950<br>0.0000573 label #951br0.0000441 label #954<br>0.0000164 label #419|                           |0.9982988 Granny Smith<br>0.0000684 orange<br>0.0000573 lemon<br>0.0000441 banana<br>0.0000164 Band Aid|                            |
resnet-v1-50         |0.1277407 label #954<br>0.1127748 label #948<br>0.0634985 label #852<br>0.0430244 label #600<br>0.0374065 label #772|                           |0.1277409 banana<br>0.1127749 Granny Smith<br>0.0634985 tennis ball<br>0.0430244 hook, claw<br>0.0374065 safety pin|   |
resnet-v1-101        |0.9928160 label #948<br>0.0040912 label #952<br>0.0009257 label #955<br>0.0006793 label #951<br>0.0003674 label #954|                           |0.9928156 Granny Smith<br>0.0040912 fig<br>0.0009257 jackfruit, jak, jack<br>0.0006793 lemon<br>0.0003674 banana|    |
resnet-v1-152        |0.7078073 label #948<br>0.1253209 label #577<br>0.0107064 label #899<br>0.0105488 label #852<br>0.0088275 label #505|                           |0.7078072 Granny Smith<br>0.1253208 gong, tam-tam<br>0.0107065 water jug<br>0.0105488 tennis ball<br>0.0088276 coffeepot|    |   
squeezenet-1.0       |0.9988525 label #948<br>0.0004736 label #952<br>0.0001965 label #945<br>0.0000892 label #719<br>0.0000732 label #852|                           |0.9988525 Granny Smith<br>0.0004736 fig<br>0.0001965 bell pepper<br>0.0000892 piggy bank, penny bank<br>0.0000732 tennis ball|                            |
squeezenet-1.1       |0.9937358 label #948<br>0.0014752 label #951<br>0.0013913 label #952<br>0.0008874 label #852<br>0.0006791 label #719|                           |0.9937358 Granny Smith<br>0.0014752 lemon<br>0.0013913 fig<br>0.0008874 tennis ball<br>0.0006791 piggy bank, penny bank|                            |
vgg-16               |0.7317343 label #948<br>0.0350750 label #945<br>0.0209236 label #582<br>0.0137958 label #773<br>0.0127183 label #952|                           |0.7317342 Granny Smith<br>0.0350750 bell pepper<br>0.0209236 grocery store, grocery, food market, market<br>0.0137958 saltshaker, salt shaker<br>0.0127183 fig|                            |
vgg-19               |0.7072727 label #948<br>0.0805918 label #988<br>0.0473263 label #952<br>0.0367725 label #679<br>0.0180316 label #951|                           |0.7072731 Granny Smith<br>0.0805916 acorn<br>0.0473262 fig<br>0.0367724 necklace<br>0.0180316 lemon|                            |

### Тестовое изображение 2

Источник: набор данных [ImageNet][imagenet]

Разрешение: 500 x 500
﻿

<img src="..\data\ILSVRC2012_val_00000247.JPEG" width="150">

   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |0.9979284 label #13<br>0.0020288 label #19<br>0.0000137 label #17<br>0.0000119 label #10<br>0.0000104 label #16|                           |0.9979280 junco, snowbird<br>0.0020288 chickadee<br>0.0000137 jay<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000104 bulbul|                            |
densenet-121         |17.8269806 label #13<br>11.4734783 label #10<br>11.3202286 label #14<br>10.3598919 label #19<br>8.2504883 label #18|                           |17.8269768 junco, snowbird<br>11.4734764 brambling, Fringilla montifringilla<br>11.3202286 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3598928 chickadee<br> 8.2504864 magpie|                            |
densenet-161         |                           |                           |18.9021969 junco, snowbird<br>12.8945799 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7353125 chickadee<br>9.5253296 brambling, Fringilla montifringilla<br>8.7536564 goldfinch, Carduelis carduelis|                            |
densenet-169         |                           |                           |18.5059853 junco, snowbird<br>11.6154308 brambling, Fringilla montifringilla<br>11.0603466 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.9430408 goldfinch, Carduelis carduelis<br>8.9175730 chickadee|                            |
densenet-201         |                           |                           |                              |                            |
googlenet-v1         |0.9999955 label #13<br>0.0000043 label #19<br>0.0000003 label #10<br>0.0000000 label #14<br>0.0000000 label #20|                           |0.9999954 junco, snowbird<br>0.0000043 chickadee<br>0.0000003 brambling, Fringilla montifringilla<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000000 water ouzel, dipper|                            |
googlenet-v2         |0.9986873 label #388<br>0.0004460 label #395<br>0.0002120 label #389<br>0.0001153 label #411<br>0.0000563 label #430|                           |0.9986847 giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004460 gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0002120 barracouta, snoek<br>0.0001153 apron<br>0.0000563 basketball|                            |
googlenet-v3         |0.9241990 label #14<br>0.0005938 label #500<br>0.0005932 label #138<br>0.0005757 label #607<br>0.0005057 label #21|                           |0.9241987 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005938 cliff dwelling<br>0.0005932 bustard<br>0.0005757 jack-o'-lantern<br>0.0005057 kite|                           |
googlenet-v4         |0.9338058 label #13<br>0.0005343 label #333<br>0.0005193 label #19<br>0.0004287 label #10<br>0.0003747 label #105|                           |0.9338045 junco, snowbird<br>0.0005343 hamster<br>0.0005193 chickadee<br>0.0004287 brambling, Fringilla montifringilla<br>0.0003747 koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus|                            |
inception-resnet-v2  |0.9995078 label #13<br>0.0000257 label #10<br>0.0000219 label #14<br>0.0000217 label #19<br>0.0000119 label #20|                           |0.9995075 junco, snowbird<br>0.0000257 brambling, Fringilla montifringilla<br>0.0000219 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000217 chickadee<br>0.0000119 water ouzel, dipper|                            |
resnet-v1-50         |0.9975350 label #13<br>0.0012899 label #19<br>0.0007322 label #14<br>0.0003813 label #10<br>0.0000160 label #16|                           |0.9975340 junco, snowbird<br>0.0012899 chickadee<br>0.0007322 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003813 brambling, Fringilla montifringilla<br>0.0000160 bulbul|   |
resnet-v1-101        |0.9994699 label #13<br>0.0001720 label #10<br>0.0001495 label #14<br>0.0001213 label #19<br>0.0000216 label #20|                           |0.9994646 junco, snowbird<br>0.0001720 brambling, Fringilla montifringilla<br>0.0001495 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001213 chickadee<br>0.0000216 water ouzel, dipper|    | 
resnet-v1-152        |0.9961464 label #13<br>0.0013669 label #19<br>0.0008338 label #10<br>0.0005274 label #14<br>0.0002985 label #20|                           |0.9961376 junco, snowbird<br>0.0013669 chickadee<br>0.0008338 brambling, Fringilla montifringilla<br>0.0005274 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002985 water ouzel, dipper|    | 
squeezenet-1.0       |0.9931428 label #13<br>0.0064122 label #19<br>0.0003084 label #10<br>0.0000394 label #16<br>0.0000340 label #18|                           |0.9931428 junco, snowbird<br>0.0064122 chickadee<br>0.0003084 brambling, Fringilla montifringilla<br>0.0000394 bulbul<br>0.0000340 magpie|                            |
squeezenet-1.1       |0.9949969 label #13<br>0.0048572 label #19<br>0.0000578 label #17<br>0.0000297 label #14<br>0.0000271 label #10|                           |0.9949969 junco, snowbird<br>0.0048572 chickadee<br>0.0000578 jay<br>0.0000297 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000271 brambling, Fringilla montifringilla|                            |
vgg-16               |0.9999772 label #13<br>0.0000132 label #10<br>0.0000089 label #19<br>0.0000006 label #20<br>0.0000000 label #14|                           |0.9999772 junco, snowbird<br>0.0000132 brambling, Fringilla montifringilla<br>0.0000089 chickadee<br>0.0000006 water ouzel, dipper<br>0.0000000 indigo bunting, indigo, indigo bird, Passerina cyanea|                            |
vgg-19               |0.9999394 label #13<br>0.0000580 label #10<br>0.0000023 label #19<br>0.0000002 label #20<br>0.0000000 label #14|                           |0.9999394 junco, snowbird<br>0.0000580 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|                            |

### Тестовое изображение 3

Источник: набор данных [ImageNet][imagenet]

Разрешение: 333 x 500
﻿

<img src="..\data\ILSVRC2012_val_00018592.JPEG" width="150">

   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |0.9991664 label #625<br>0.0003741 label #510<br>0.0001206 label #724<br>0.0000820 label #540<br>0.0000784 label #913|                           |0.9991654 lifeboat<br>0.0003741 container ship, containership, container vessel<br>0.0001206 pirate, pirate ship<br>0.0000820 drilling platform, offshore rig<br>0.0000784 wreck|                            |
densenet-121         |13.9662304 label #625<br>7.8177419 label #540<br>7.7323370 label #628<br>7.5702801 label #913<br>7.5621634 label #724|                           |13.9662323 lifeboat<br>7.8177419 drilling platform, offshore rig<br>7.7323365 liner, ocean liner<br>7.5702801 wreck<br>7.5621624 pirate, pirate ship|      |
densenet-161         |                           |                           |15.5664644 lifeboat<br>7.2549500 liner, ocean liner<br>6.7164907 fireboat<br>6.2500725 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.2465825 dock, dockage, docking facility|                            |
densenet-169         |                           |                           |15.3814850 lifeboat<br>10.0849438 drilling platform, offshore rig<br>9.4490118 container ship, containership, container vessel<br>9.1608114 pirate, pirate ship<br>8.3062391 beacon, lighthouse, beacon light, pharos|                            |
densenet-201         |                           |                           |                              |                            |
googlenet-v1         |0.8990629 label #625<br>0.0275983 label #540<br>0.0209237 label #437<br>0.0196472 label #510<br>0.0062734 label #628|                           |0.8990629 lifeboat<br>0.0275983 drilling platform, offshore rig<br>0.0209237 beacon, lighthouse, beacon light, pharos<br>0.0196472 container ship, containership, container vessel
<br>0.0062734 liner, ocean liner|                            |
googlenet-v2         |0.9919646 label #237<br>0.0011945 label #718<br>0.0007550 label #833<br>0.0005916 label #247<br>0.0005792 label #234|                           |0.9919641 miniature pinscher<br>0.0011945 pier<br>0.0007550 submarine, pigboat, sub, U-boat<br>0.0005916 Saint Bernard, St Bernard<br>0.0005792 Rottweiler|                            |
googlenet-v3         |0.9595632 label #626<br>0.0016150 label #415<br>0.0007223 label #438<br>0.0005667 label #461<br>0.0003984 label #555|                           |0.9595628 lighter, light, igniter, ignitor<br>0.0016150 bakery, bakeshop, bakehouse<br>0.0007223 beaker<br>0.0005667 breastplate, aegis, egis<br>0.0003984 fire engine, fire truck|       |
googlenet-v4         |0.9513760 label #625<br>0.0005698 label #554<br>0.0004419 label #833<br>0.0004226 label #407<br>0.0004161 label #540|                           |0.9513766 lifeboat<br>0.0005698 fireboat<br>0.0004419 submarine, pigboat, sub, U-boat<br>0.0004226 ambulance<br>0.0004161 drilling platform, offshore rig|                            |
inception-resnet-v2  |0.9981450 label #625<br>0.0006250 label #437<br>0.0001983 label #460<br>0.0001903 label #540<br>0.0001606 label #554|                           |0.9981461 lifeboat<br>0.0006250 beacon, lighthouse, beacon light, pharos<br>0.0001983 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0001903 drilling platform, offshore rig<br>0.0001606 fireboat|                            |
resnet-v1-50         |0.8872184 label #625<br>0.0398498 label #628<br>0.0237535 label #510<br>0.0125247 label #536<br>0.0107783 label #540|                           |0.8872179 lifeboat<br>0.0398498 liner, ocean liner<br>0.0237536 container ship, containership, container vessel<br>0.0125247 dock, dockage, docking facility<br>0.0107783 drilling platform, offshore rig|   |
resnet-v1-101        |0.6138124 label #625<br>0.1049524 label #540<br>0.0466762 label #628<br>0.0327782 label #536<br>0.0284107 label #403|                           |0.6138138 lifeboat<br>0.1049523 drilling platform, offshore rig<br>0.0466763 liner, ocean liner<br>0.0327782 dock, dockage, docking facility<br>0.0284107 aircraft carrier, carrier, flattop, attack aircraft carrier|    |
resnet-v1-152        |0.9505479 label #625<br>0.0083380 label #540<br>0.0072418 label #403<br>0.0049709 label #510<br>0.0041877 label #628|                           |0.9505481 lifeboat<br>0.0083380 drilling platform, offshore rig<br>0.0072418 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0049709 container ship, containership, container vessel<br>0.0041877 liner, ocean liner|    |  
squeezenet-1.0       |0.9870804 label #625<br>0.0061878 label #510<br>0.0025447 label #554<br>0.0024638 label #628<br>0.0004083 label #437|                           |0.9870804 lifeboat<br>0.0061878 container ship, containership, container vessel<br>0.0025447 fireboat<br>0.0024638 liner, ocean liner<br>0.0004083 beacon, lighthouse, beacon light, pharos|                            |
squeezenet-1.1       |0.9570305 label #625<br>0.0211557 label #510<br>0.0102893 label #540<br>0.0034316 label #724<br>0.0029377 label #536|                           |0.9570305 lifeboat<br>0.0211557 container ship, containership, container vessel<br>0.0102893 drilling platform, offshore rig<br>0.0034316 pirate, pirate ship<br>0.0029377 dock, dockage, docking facility|                            |
vgg-16               |0.9821943 label #625<br>0.0082832 label #510<br>0.0014539 label #540<br>0.0014494 label #724<br>0.0009578 label #628|                           |0.9821915 lifeboat<br>0.0082832 container ship, containership, container vessel<br>0.0014539 drilling platform, offshore rig<br>0.0014494 pirate, pirate ship<br>0.0009578 liner, ocean liner|                            |
vgg-19               |0.9965242 label #625<br>0.0008823 label #510<br>0.0004778 label #540<br>0.0003970 label #536<br>0.0003622 label #554|                           |0.9965212 lifeboat<br>0.0008823 container ship, containership, container vessel<br>0.0004778 drilling platform, offshore rig<br>0.0003970 dock, dockage, docking facility<br>0.0003622 fireboat|                            |


<!-- LINKS -->
[imagenet]: http://www.image-net.org