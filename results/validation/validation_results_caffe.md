# Validation results for the models inferring using Intel® Optimization for Caffe

## Image classification

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.9521238 Granny Smith<br>0.0069122 piggy bank, penny bank<br>0.0054333 candle, taper, wax light<br>0.0037157 saltshaker, salt shaker<br>0.0034601 tennis ball|
caffenet              |0.8039698 Granny Smith<br>0.0632433 candle, taper, wax light<br>0.0330907 teapot<br>0.0097625 tennis ball<br>0.0090626 saltshaker, salt shaker|
googlenet-v1         |0.9976689 Granny Smith<br>0.0008829 bell pepper<br>0.0007544 candle, taper, wax light<br>0.0001104 tennis ball<br>0.0000760 cucumber, cuke|
googlenet-v2         |1<br>2<br>3<br>4<br>5|
mobilenet-v1-1.0-224         |0.9441363 Granny Smith<br>0.0080110 fig<br>0.0080110 fig<br>0.0042537 custard apple<br>0.0036513 orange|
resnet-50        |0.1277405 banana<br>0.1127745 Granny Smith<br>0.0634981 tennis ball<br>0.0430247 hook, claw<br>0.0374068 safety pin<br>|
resnet-101        |0.9928160 Granny Smith<br>0.0040912 fig<br>0.0009257 jackfruit, jak, jack<br>0.0006793 lemon<br>0.0003674 banana<br>|
resnet-152        |0.7078075 Granny Smith<br>0.1253205 gong, tam-tam<br>0.0107064 water jug<br>0.0105488 tennis ball<br>0.0088275 coffeepot<br>|
squeezenet-1.0       |0.9992466 Granny Smith<br>0.0001648 tennis ball<br>0.0001631 bell pepper<br>0.0001376 saltshaker, salt shaker<br>0.0001081 piggy bank, penny bank<br>|
squeezenet-1.1       |0.9995996 Granny Smith<br>0.0002680 tennis ball<br>0.0000614 fig<br>0.0000253 lemon<br>0.0000120 banana<br>|
vgg-16               |0.9256526 Granny Smith<br>0.0305293 bell pepper<br>0.0080413 saltshaker, salt shaker<br>0.0060264 necklace<br>0.0033264 vase<br>|
vgg-19               |0.7781622 Granny Smith<br>0.0757968 necklace<br>0.0475143 acorn<br>0.0159689 fig<br>0.0130410 lemon<br>|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.8866407 junco, snowbird<br>0.1086869 chickadee<br>0.0019401 brambling, Fringilla montifringilla<br>0.0013517 water ouzel, dipper<br>0.0002660 bulbul|
caffenet              |0.9883578 junco, snowbird<br>0.0000186 chickadee<br>0.0000017 brambling, Fringilla montifringilla<br>0.0000014 water ouzel, dipper<br>0.0000013 house finch, linnet, Carpodacus mexicanus|
googlenet-v1         |0.9999765 junco, snowbird<br>0.0005613 bell pepper<br>0.0003487 candle, taper, wax light<br>0.0000679 tennis ball<br>0.0000656 piggy bank, penny bank|
googlenet-v2         |1<br>2<br>3<br>4<br>5|
mobilenet-v1-1.0-224         |0.9988434 junco, snowbird<br>0.0007267 chickadee<br>0.0002552 brambling, Fringilla montifringilla<br>0.0000451 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000312 bulbul|
resnet-50        |0.9975350 junco, snowbird<br>0.0012899 chickadee<br>0.0007322 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003813 brambling, Fringilla montifringilla<br>0.0000160 bulbul<br>|
resnet-101        |0.9994699 junco, snowbird<br>0.0001720 brambling, Fringilla montifringilla<br>0.0001495 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001213 chickadee<br>0.0000216 water ouzel, dipper<br>|
resnet-152        |0.9961464 junco, snowbird<br>0.0013669 chickadee<br>0.0008338 brambling, Fringilla montifringilla<br>0.0005274 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002985 water ouzel, dipper<br>|
squeezenet-1.0       |0.9669856 junco, snowbird<br>0.0299453 chickadee<br>0.0015737 brambling, Fringilla montifringilla<br>0.0004190 bulbul<br>0.0003177 jay<br>|
squeezenet-1.1       |0.9902450 junco, snowbird<br>0.0087430 chickadee<br>0.0005967 brambling, Fringilla montifringilla<br>0.0002337 jay<br>0.0001153 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
vgg-16               |0.9999917 junco, snowbird<br>0.0000070 chickadee<br>0.0000013 brambling, Fringilla montifringilla<br>0.0000000 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
vgg-19               |0.9999951 junco, snowbird<br>0.0000039 brambling, Fringilla montifringilla<br>0.0000009 chickadee<br>0.0000000 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.9570842 lifeboat<br>0.0145343 container ship, containership, container vessel<br>0.0057027 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0050276 beacon, lighthouse, beacon light, pharos<br>0.0043956 liner, ocean liner|
caffenet              |0.5774223 lifeboat<br>0.2691385 container ship, containership, container vessel<br>0.0526851 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0484550 liner, ocean liner<br>0.0084702 beacon, lighthouse, beacon light, pharos|
googlenet-v1         |0.4912087 lifeboat<br>0.1853294 drilling platform, offshore rig<br>0.0932134 container ship, containership, container vessel<br>0.0756835 liner, ocean liner<br>0.0567751 beacon, lighthouse, beacon light, pharos|
googlenet-v2         |1<br>2<br>3<br>4<br>5<br>|
mobilenet-v1-1.0-224         |0.8883281 lifeboat<br>0.0358162 pirate, pirate ship<br>0.0247643 container ship, containership, container vessel<br>0.0106020 drilling platform, offshore rig<br>0.0084067 liner, ocean liner|
resnet-50        |0.8872180 lifeboat<br>0.0398499 liner, ocean liner<br>0.0237536 container ship, containership, container vessel<br>0.0125248 dock, dockage, docking facility<br>0.0107783 drilling platform, offshore rig<br>|
resnet-101        |0.6138119 lifeboat<br>0.1049526 drilling platform, offshore rig<br>0.0466763 liner, ocean liner<br>0.0327783 dock, dockage, docking facility<br>0.0284108 aircraft carrier, carrier, flattop, attack aircraft carrier<br>|
resnet-152        |0.9505481 lifeboat<br>0.0083380 drilling platform, offshore rig<br>0.0072417 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0049709 container ship, containership, container vessel<br>0.0041877 liner, ocean liner<br>|
squeezenet-1.0       |0.4751488 liner, ocean liner<br>0.2905624 lifeboat<br>0.1737312 container ship, containership, container vessel<br>0.0127517 beacon, lighthouse, beacon light, pharos<br>0.0101218 fireboat<br>|
squeezenet-1.1       |0.6992837 lifeboat<br>0.1367231 drilling platform, offshore rig<br>0.0986509 liner, ocean liner<br>0.0202084 container ship, containership, container vessel<br>0.0170821 submarine, pigboat, sub, U-boat<br>|
vgg-16               |0.5846901 lifeboat<br>0.3716984 container ship, containership, container vessel<br>0.0152381 liner, ocean liner<br>0.0134273 drilling platform, offshore rig<br>0.0037419 dock, dockage, docking facility<br>|
vgg-19               |0.9302235 lifeboat<br>0.0434868 container ship, containership, container vessel<br>0.0111730 liner, ocean liner<br>0.0040760 fireboat<br>0.0028543 drilling platform, offshore rig<br>|

## Object detection

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
<img width="150" src="detection\ILSVRC2012_val_00000023.JPEG"></img>
</div>
Bounding boxes (upper left and bottom right corners):<br>
(55,155), (236,375)<br>
(190,190), (380,400)<br>
(374,209), (588,422)<br>
(289,111), (440,255)<br>
(435,160), (615,310)<br>

   Model              |  Python (implementation)         |
----------------------|----------------------------------|
mobilenet-ssd         | Bounding box: (46, 133), (657, 445)  |
ssd300                | Bounding box: (66, 163), (235, 356) |
ssd512                | Bounding box: (65, 168), (256, 343); (378, 167), (592, 424)  |

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00000247.JPEG">
</div>
Bounding box (upper left and bottom right corners):<br>
(117,86), (365,465)

   Model              |      Python (implementation)     |
----------------------|----------------------------------|
mobilenet-ssd         | Bounding box: (94, 93), (360, 481)  |
ssd300                | Bounding box: (68, 100), (334,451) |
ssd512                | Bounding box: (67, 95), (356, 480) |

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00018592.JPEG">
</div>
Bounding box (upper left and bottom right corners):<br>
(82,262), (269,376)

   Model              |     Python (implementation)      |
----------------------|----------------------------------|
mobilenet-ssd         | Bounding box:  (79, 140), (270, 375)  |
ssd300                | Bounding box:  (79, 150), (270, 373)  |
ssd512                | Bounding box:  (79, 175), (274, 372)  |


<!-- LINKS -->
[imagenet]: http://www.image-net.org
