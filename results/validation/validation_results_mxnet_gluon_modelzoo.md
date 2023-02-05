# Validation results for the models inferring using MXNet (Gluon API)

## Image classification

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

   Model     |  Python (implementation)  |
-------------|---------------------------|
alexnet      |0.4499783 Granny Smith<br>0.0933101 dumbbell<br>0.0876728 ocarina, sweet potato<br>0.0628702 hair slide<br>0.0484683 bottlecap|
densenet121  |0.9523346 Granny Smith<br>0.0132273 orange<br>0.0125171 lemon<br>0.0027910 banana<br>0.0020333 piggy bank, penny bank|
densenet161  ||
densenet169  ||
densenet201  ||
inceptionv3  ||
mobilenet0.25|0.3314433 piggy bank, penny bank<br>0.1333785 maraca<br>0.1262991 croquet ball<br>0.0684097 dumbbell<br>0.0539143 hair slide|
mobilenet0.5 ||
mobilenet0.75||
mobilenet1.0 ||
mobilenetv2_0.25||
mobilenetv2_0.5 ||
mobilenetv2_0.75||
mobilenetv2_1.0 ||
resnet101_v1 ||
resnet101_v2 ||
resnet152_v1 ||
resnet152_v2 ||
resnet18_v1 |0.7145673 Granny Smith<br>0.0433349 piggy bank, penny bank<br>0.0343972 saltshaker, salt shaker<br>0.0215941 fig<br>0.0212160 banana|
resnet18_v2 ||
resnet34_v1 ||
resnet34_v2 ||
resnet50_v1 ||
resnet50_v2 ||
squeezenet1.0 ||
squeezenet1.1 ||
vgg11 ||
vgg11_bn ||
vgg13 ||
vgg13_bn ||
vgg16 ||
vgg16_bn ||
vgg19 ||
vgg19_bn ||

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

   Model     |  Python (implementation)  |
---------------------|---------------------------|
alexnet      |0.9947656 junco, snowbird<br>0.0043087 chickadee<br>0.0002780 water ouzel, dipper<br>0.0002770 bulbul<br>0.0001244 brambling, Fringilla montifringilla|
densenet121  |0.9841659 junco, snowbird<br>0.0072199 chickadee<br>0.0034963 brambling, Fringilla montifringilla<br>0.0016226 water ouzel, dipper<br>0.0012858 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
densenet161  ||
densenet169  ||
densenet201  ||
inceptionv3  ||
mobilenet0.25|0.9301481 junco, snowbird<br>0.0466449 chickadee<br>0.0146190 brambling, Fringilla montifringilla<br>0.0027491 bulbul<br>0.0024721 jay|
mobilenet0.5 ||
mobilenet0.75||
mobilenet1.0 ||
mobilenetv2_0.25||
mobilenetv2_0.5 ||
mobilenetv2_0.75||
mobilenetv2_1.0 ||
resnet101_v1 ||
resnet101_v2 ||
resnet152_v1 ||
resnet152_v2 ||
resnet18_v1 |0.9597615 junco, snowbird<br>0.0103962 chickadee<br>0.0075481 goldfinch, Carduelis carduelis<br>0.0054580 house finch, linnet, Carpodacus mexicanus<br>0.0053979 water ouzel, dipper|
resnet18_v2 ||
resnet34_v1 ||
resnet34_v2 ||
resnet50_v1 ||
resnet50_v2 ||
squeezenet1.0 ||
squeezenet1.1 ||
vgg11 ||
vgg11_bn ||
vgg13 ||
vgg13_bn ||
vgg16 ||
vgg16_bn ||
vgg19 ||
vgg19_bn ||

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

   Model     |  Python (implementation)  |
---------------------|---------------------------|
alexnet      |0.3216891 container ship, containership, container vessel<br>0.1360617 drilling platform, offshore rig<br>0.1140692 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1057475 beacon, lighthouse, beacon light, pharos<br>0.0471224 liner, ocean liner|
densenet121  |0.3022416 liner, ocean liner<br>0.1322481 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1194608 container ship, containership, container vessel<br>0.0795039 drilling platform, offshore rig<br>0.0723068 dock, dockage, docking facility|
densenet161  ||
densenet169  ||
densenet201  ||
inceptionv3  ||
mobilenet0.25|0.2958905 container ship, containership, container vessel<br>0.2101003 drilling platform, offshore rig<br>0.1384616 submarine, pigboat, sub, U-boat<br>0.0863535 liner, ocean liner<br>0.0732720 beacon, lighthouse, beacon light, pharos|
mobilenet0.5 ||
mobilenet0.75||
mobilenet1.0 ||
mobilenetv2_0.25||
mobilenetv2_0.5 ||
mobilenetv2_0.75||
mobilenetv2_1.0 ||
resnet101_v1 ||
resnet101_v2 ||
resnet152_v1 ||
resnet152_v2 ||
resnet18_v1 |0.3416696 container ship, containership, container vessel<br>0.1224417 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1104408 liner, ocean liner<br>0.0661492 lifeboat<br>0.0649565 pirate, pirate ship|
resnet18_v2 ||
resnet34_v1 ||
resnet34_v2 ||
resnet50_v1 ||
resnet50_v2 ||
squeezenet1.0 ||
squeezenet1.1 ||
vgg11 ||
vgg11_bn ||
vgg13 ||
vgg13_bn ||
vgg16 ||
vgg16_bn ||
vgg19 ||
vgg19_bn ||


<!-- LINKS -->
[imagenet]: http://www.image-net.org
