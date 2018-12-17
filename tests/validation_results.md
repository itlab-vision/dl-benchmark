# Результаты проверки корректности вывода с использованием разных режимов

## Результаты классификации

### Тестовое изображение 1

Источник: набор данных [ImageNet][imagenet]

Разрешение: 709 x 510
﻿

<img src="..\data\ILSVRC2012_val_00000023.JPEG" width="150">


   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |                           |                           |0.9896094 label Granny Smith<br>0.0037969 label bell pepper<br>0.0013717 label piggy bank, penny bank<br>0.0011059 label acorn<br>0.0009710 label fig|                            |
densenet-121         |                           |                           |15.7979164 label Granny Smith<br>9.9429455 label lemon<br>9.3676043 label orange<br>8.6181612 label banana<br>7.1164074 label tennis ball|                            |
densenet-161         |                           |                           |17.8060474 label Granny Smith<br>8.5503120 label lemon<br>7.6080256 label orange<br>7.2737975 label banana<br>7.1114807 label fig|                            |
densenet-169         |                           |                           |15.9379349 label Granny Smith<br>6.3490119 label banana<br>6.2573476 label lemon<br>5.8869209 label tennis ball<br>5.7489214 label piggy bank, penny bank|                            |
densenet-201         |                           |                           |                              |                            |
googlenet-v1         |                           |                           |0.9982972 label Granny Smith<br>0.0005613 label bell pepper<br>0.0003487 label candle, taper, wax light<br>0.0000679 label tennis ball<br>0.0000656 label piggy bank, penny bank|                            |
googlenet-v2         |                           |                           |0.0013593 label vault<br>0.0013428 label night snake, Hypsiglena torquata<br>0.0013413 label beacon, lighthouse, beacon light, pharos<br>0.0013358 label bluetick<br>0.0012894 label Afghan hound, Afghan|                            |
googlenet-v3         |                           |                           |0.9909641 label strawberry<br>0.0007918 label binder, ring-binder<br>0.0001872 label pill bottle<br>0.0001239 label banjo|                           |
googlenet-v4         |                           |                           |1.0000000 label scuba diver<br>0.0000000 label Norwich terrier<br>0.0000000 label chain mail, ring mail, mail, chain armor, chain armour, ring armor, ring armour<br>0.0000000 label coral fungus<br>0.0000000 label cardigan|                            |
inception-resnet-v2  |                           |                           |1.0000000 label table lamp<br>0.0000001 label vase<br>0.0000000 label pitcher, ewer<br>0.0000000 label goblet<br>0.0000000 label toilet tissue, toilet paper, bathroom tissue|                            |
resnet-v1-50         |                           |                           |0.1277409 label banana<br>0.1127749 label Granny Smith<br>0.0634985 label tennis ball<br>0.0430244 label hook, claw<br>0.0374065 label safety pin|   |
resnet-v1-101        |                           |                           |0.9928156 label Granny Smith<br>0.0040912 label fig<br>0.0009257 label jackfruit, jak, jack<br>0.0006793 label lemon<br>0.0003674 label banana|    |
resnet-v1-152        |                           |                           |0.7078072 label Granny Smith<br>0.1253208 label gong, tam-tam<br>0.0107065 label water jug<br>0.0105488 label tennis ball<br>0.0088276 label coffeepot|    |   
squeezenet-1.0       |                           |                           |0.9988525 label Granny Smith<br>0.0004736 label fig<br>0.0001965 label bell pepper<br>0.0000892 label piggy bank, penny bank<br>0.0000732 label tennis ball|                            |
squeezenet-1.1       |                           |                           |0.9937358 label Granny Smith<br>0.0014752 label lemon<br>0.0013913 label fig<br>0.0008874 label tennis ball<br>0.0006791 label piggy bank, penny bank|                            |
vgg-16               |                           |                           |0.7317342 label Granny Smith<br>0.0350750 label bell pepper<br>0.0209236 label grocery store, grocery, food market, market<br>0.0137958 label saltshaker, salt shaker<br>0.0127183 label fig|                            |
vgg-19               |                           |                           |0.7072731 label Granny Smith<br>0.0805916 label acorn<br>0.0473262 label fig<br>0.0367724 label necklace<br>0.0180316 label lemon|                            |

### Тестовое изображение 2

Источник: набор данных [ImageNet][imagenet]

Разрешение: 500 x 500
﻿

<img src="..\data\ILSVRC2012_val_00000247.JPEG" width="150">

   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |                           |                           |0.9979280 label junco, snowbird<br>0.0020288 label chickadee<br>0.0000137 label jay<br>0.0000119 label brambling, Fringilla montifringilla<br>0.0000104 label bulbul|                            |
densenet-121         |                           |                           |17.8269768 label junco, snowbird<br>11.4734764 label brambling, Fringilla montifringilla<br>11.3202286 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3598928 label chickadee<br> 8.2504864 label magpie|                            |
densenet-161         |                           |                           |18.9021969 label junco, snowbird<br>12.8945799 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7353125 label chickadee<br>9.5253296 label brambling, Fringilla montifringilla<br>8.7536564 label goldfinch, Carduelis carduelis|                            |
densenet-169         |                           |                           |18.5059853 label junco, snowbird<br>11.6154308 label brambling, Fringilla montifringilla<br>11.0603466 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.9430408 label goldfinch, Carduelis carduelis<br>8.9175730 label chickadee|                            |
densenet-201         |                           |                           |                              |                            |
googlenet-v1         |                           |                           |0.9999954 label junco, snowbird<br>0.0000043 label chickadee<br>0.0000003 label brambling, Fringilla montifringilla<br>0.0000000 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000000 label water ouzel, dipper|                            |
googlenet-v2         |                           |                           |0.9986847 label giant panda, panda, panda bear, coon bear, Ailuropoda melanoleuca<br>0.0004460 label gar, garfish, garpike, billfish, Lepisosteus osseus<br>0.0002120 label barracouta, snoek<br>0.0001153 label apron<br>0.0000563 label basketball|                            |
googlenet-v3         |                           |                           |0.9241987 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005938 label cliff dwelling<br>0.0005932 label bustard<br>0.0005757 label jack-o'-lantern<br>0.0005057 label kite|                           |
googlenet-v4         |                           |                           |0.9338045 label junco, snowbird<br>0.0005343 label hamster<br>0.0005193 label chickadee<br>0.0004287 label brambling, Fringilla montifringilla<br>0.0003747 label koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus|                            |
inception-resnet-v2  |                           |                           |1.0000000 label table lamp<br>0.0000000 label vase<br>0.0000000 label goblet<br>0.0000000 label pitcher, ewer<br>0.0000000 label pedestal, plinth, footstall|                            |
resnet-v1-50         |                           |                           |0.9975340 label junco, snowbird<br>0.0012899 label chickadee<br>0.0007322 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003813 label brambling, Fringilla montifringilla<br>0.0000160 label bulbul|   |
resnet-v1-101        |                           |                           |0.9994646 label junco, snowbird<br>0.0001720 label brambling, Fringilla montifringilla<br>0.0001495 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001213 label chickadee<br>0.0000216 label water ouzel, dipper|    | 
resnet-v1-152        |                           |                           |0.9961376 label junco, snowbird<br>0.0013669 label chickadee<br>0.0008338 label brambling, Fringilla montifringilla<br>0.0005274 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002985 label water ouzel, dipper|    | 
squeezenet-1.0       |                           |                           |0.9931428 label junco, snowbird<br>0.0064122 label chickadee<br>0.0003084 label brambling, Fringilla montifringilla<br>0.0000394 label bulbul<br>0.0000340 label magpie|                            |
squeezenet-1.1       |                           |                           |0.9949969 label junco, snowbird<br>0.0048572 label chickadee<br>0.0000578 label jay<br>0.0000297 label indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000271 label brambling, Fringilla montifringilla|                            |
vgg-16               |                           |                           |0.9999772 label junco, snowbird<br>0.0000132 label brambling, Fringilla montifringilla<br>0.0000089 label chickadee<br>0.0000006 label water ouzel, dipper<br>0.0000000 label indigo bunting, indigo finch, indigo bird, Passerina cyanea|                            |
vgg-19               |                           |                           |0.9999394 label junco, snowbird<br>0.0000580 label brambling, Fringilla montifringilla<br>0.0000023 label chickadee<br>0.0000002 label water ouzel, dipper<br>0.0000000 label indigo bunting, indigo finch, indigo bird, Passerina cyanea|                            |

### Тестовое изображение 3

Источник: набор данных [ImageNet][imagenet]

Разрешение: 333 x 500
﻿

<img src="..\data\ILSVRC2012_val_00018592.JPEG" width="150">

   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |                           |                           |0.9991654 label lifeboat<br>0.0003741 label container ship, containership, container vessel<br>0.0001206 label pirate, pirate ship<br>0.0000820 label drilling platform, offshore rig<br>0.0000784 label wreck|                            |
densenet-121         |                           |                           |13.9662323 label lifeboat<br>7.8177419 label drilling platform, offshore rig<br>7.7323365 label liner, ocean liner<br>7.5702801 label wreck<br>7.5621624 label pirate, pirate ship|      |
densenet-161         |                           |                           |15.5664644 label lifeboat<br>7.2549500 label liner, ocean liner<br>6.7164907 label fireboat<br>6.2500725 label breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.2465825 label dock, dockage, docking facility|                            |
densenet-169         |                           |                           |15.3814850 label lifeboat<br>10.0849438 label drilling platform, offshore rig<br>9.4490118 label container ship, containership, container vessel<br>9.1608114 label pirate, pirate ship<br>8.3062391 label beacon, lighthouse, beacon light, pharos|                            |
densenet-201         |                           |                           |                              |                            |
googlenet-v1         |                           |                           |0.8990629 label lifeboat<br>0.0275983 label drilling platform, offshore rig<br>0.0209237 label beacon, lighthouse, beacon light, pharos<br>0.0196472 label container ship, containership, container vessel
<br>0.0062734 label liner, ocean liner|                            |
googlenet-v2         |                           |                           |0.9919641 label miniature pinscher<br>0.0011945 label pier<br>0.0007550 label submarine, pigboat, sub, U-boat<br>0.0005916 label Saint Bernard, St Bernard<br>0.0005792 label Rottweiler|                            |
googlenet-v3         |                           |                           |0.9595628 label lighter, light, igniter, ignitor<br>0.0016150 label bakery, bakeshop, bakehouse<br>0.0007223 label beaker<br>0.0005667 label breastplate, aegis, egis<br>0.0003984 label fire engine, fire truck|                           |
googlenet-v4         |                           |                           |0.9513766 label lifeboat<br>0.0005698 label fireboat<br>0.0004419 label submarine, pigboat, sub, U-boat<br>0.0004226 label ambulance<br>0.0004161 label drilling platform, offshore rig|                            |
inception-resnet-v2  |                           |                           |1.0000000 label table lamp<br>0.0000000 label vase<br>0.0000000 label goblet<br>0.0000000 label pitcher, ewer<br>0.0000000 label toilet tissue, toilet paper, bathroom tissue|                            |
resnet-v1-50         |                           |                           |0.8872179 label lifeboat<br>0.0398498 label liner, ocean liner<br>0.0237536 label container ship, containership, container vessel<br>0.0125247 label dock, dockage, docking facility<br>0.0107783 label drilling platform, offshore rig|   |
resnet-v1-101        |                           |                           |0.6138138 label lifeboat<br>0.1049523 label drilling platform, offshore rig<br>0.0466763 label liner, ocean liner<br>0.0327782 label dock, dockage, docking facility<br>0.0284107 label aircraft carrier, carrier, flattop, attack aircraft carrier|    |
resnet-v1-152        |                           |                           |0.9505481 label lifeboat<br>0.0083380 label drilling platform, offshore rig<br>0.0072418 label aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0049709 label container ship, containership, container vessel<br>0.0041877 label liner, ocean liner|    |  
squeezenet-1.0       |                           |                           |0.9870804 label lifeboat<br>0.0061878 label container ship, containership, container vessel<br>0.0025447 label fireboat<br>0.0024638 label liner, ocean liner<br>0.0004083 label beacon, lighthouse, beacon light, pharos|                            |
squeezenet-1.1       |                           |                           |0.9570305 label lifeboat<br>0.0211557 label container ship, containership, container vessel<br>0.0102893 label drilling platform, offshore rig<br>0.0034316 label pirate, pirate ship<br>0.0029377 label dock, dockage, docking facility|                            |
vgg-16               |                           |                           |0.9821915 label lifeboat<br>0.0082832 label container ship, containership, container vessel<br>0.0014539 label drilling platform, offshore rig<br>0.0014494 label pirate, pirate ship<br>0.0009578 label liner, ocean liner|                            |
vgg-19               |                           |                           |0.9965212 label lifeboat<br>0.0008823 label container ship, containership, container vessel<br>0.0004778 label drilling platform, offshore rig<br>0.0003970 label dock, dockage, docking facility<br>0.0003622 label fireboat|                            |


<!-- LINKS -->
[imagenet]: http://www.image-net.org