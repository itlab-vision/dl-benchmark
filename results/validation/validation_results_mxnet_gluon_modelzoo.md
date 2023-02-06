# Validation results for the models inferring using MXNet (Gluon API)

## Image classification

Complete information about the supported classification
models is available [here][gluon_modelzoo_classification].

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510

Mean: [0.485, 0.456, 0.406]
Standard deviation: [0.229, 0.224, 0.225]
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

   Model     |  Python (implementation)  |
-------------|---------------------------|
alexnet      |0.4499783 Granny Smith<br>0.0933101 dumbbell<br>0.0876728 ocarina, sweet potato<br>0.0628702 hair slide<br>0.0484683 bottlecap|
densenet121  |0.9523346 Granny Smith<br>0.0132273 orange<br>0.0125171 lemon<br>0.0027910 banana<br>0.0020333 piggy bank, penny bank|
densenet161  |0.9372969 Granny Smith<br>0.0082274 dumbbell<br>0.0056475 piggy bank, penny bank<br>0.0055374 ping-pong ball<br>0.0041915 pitcher, ewer|
densenet169  |0.9811633 Granny Smith<br>0.0033828 piggy bank, penny bank<br>0.0021365 orange<br>0.0019196 lemon<br>0.0017232 pomegranate|
densenet201  |0.9119796 Granny Smith<br>0.0533456 piggy bank, penny bank<br>0.0056831 lemon<br>0.0017810 pool table, billiard table, snooker table<br>0.0015689 tennis ball|
inceptionv3  ||
mobilenet0.25|0.3314433 piggy bank, penny bank<br>0.1333785 maraca<br>0.1262991 croquet ball<br>0.0684097 dumbbell<br>0.0539143 hair slide|
mobilenet0.5 |0.7425038 piggy bank, penny bank<br>0.0554336 saltshaker, salt shaker<br>0.0353432 Granny Smith<br>0.0217170 pencil sharpener<br>0.0169298 rubber eraser, rubber, pencil eraser|
mobilenet0.75|0.2680034 piggy bank, penny bank<br>0.2459760 Granny Smith<br>0.0562553 dumbbell<br>0.0306232 necklace<br>0.0305400 pitcher, ewer|
mobilenet1.0 |0.6145398 Granny Smith<br>0.0852871 piggy bank, penny bank<br>0.0347396 maraca<br>0.0332023 necklace<br>0.0145589 whistle|
mobilenetv2_0.25|0.1190805 bell pepper<br>0.1169647 Granny Smith<br>0.1004419 candle, taper, wax light<br>0.0989920 dumbbell<br>0.0918921 hair slide|
mobilenetv2_0.5 |0.2223127 Granny Smith<br>0.2116509 piggy bank, penny bank<br>0.1656679 saltshaker, salt shaker<br>0.0511496 teapot<br>0.0504719 necklace|
mobilenetv2_0.75|0.6253413 Granny Smith<br>0.0585538 piggy bank, penny bank<br>0.0260610 necklace<br>0.0252774 bell pepper<br>0.0218010 hair slide|
mobilenetv2_1.0 |0.7025163 piggy bank, penny bank<br>0.1278343 Granny Smith<br>0.0542883 hair slide<br>0.0226695 necklace<br>0.0095436 saltshaker, salt shaker|
resnet18_v1 |0.7145673 Granny Smith<br>0.0433349 piggy bank, penny bank<br>0.0343972 saltshaker, salt shaker<br>0.0215941 fig<br>0.0212160 banana|
resnet18_v2 |0.2885317 Granny Smith<br>0.1816196 piggy bank, penny bank<br>0.0722676 saltshaker, salt shaker<br>0.0635363 rubber eraser, rubber, pencil eraser<br>0.0440724 soap dispenser|
resnet34_v1 |0.5898089 piggy bank, penny bank<br>0.3150511 Granny Smith<br>0.0128028 saltshaker, salt shaker<br>0.0093140 candle, taper, wax light<br>0.0089791 pencil sharpener|
resnet34_v2 |0.5082700 Granny Smith<br>0.3873705 piggy bank, penny bank<br>0.0163602 pencil sharpener<br>0.0137499 saltshaker, salt shaker<br>0.0071418 dumbbell|
resnet50_v1 |0.7435529 Granny Smith<br>0.0182989 orange<br>0.0153789 lemon<br>0.0104132 vase<br>0.0097732 pop bottle, soda bottle|
resnet50_v2 |0.9931256 Granny Smith<br>0.0017001 piggy bank, penny bank<br>0.0007180 saltshaker, salt shaker<br>0.0006648 dumbbell<br>0.0002998 tennis ball|
resnet101_v1 |0.8556019 Granny Smith<br>0.0572227 piggy bank, penny bank<br>0.0485176 saltshaker, salt shaker<br>0.0053789 hair slide<br>0.0048319 dumbbell|
resnet101_v2 |0.8972577 Granny Smith<br>0.0401716 candle, taper, wax light<br>0.0074955 nail<br>0.0072345 screw<br>0.0056374 hair slide|
resnet152_v1 |0.9127905 Granny Smith<br>0.0197971 croquet ball<br>0.0119885 piggy bank, penny bank<br>0.0078466 saltshaker, salt shaker<br>0.0043091 analog clock|
resnet152_v2 |0.9972480 Granny Smith<br>0.0010769 piggy bank, penny bank<br>0.0002827 orange<br>0.0002033 pitcher, ewer<br>0.0001509 lemon|
squeezenet1.0 |0.3275063 piggy bank, penny bank<br>0.1791327 dumbbell<br>0.1542634 Granny Smith<br>0.0912991 water bottle<br>0.0385819 rubber eraser, rubber, pencil eraser|
squeezenet1.1 |0.5895361 piggy bank, penny bank<br>0.0677938 Granny Smith<br>0.0610649 necklace<br>0.0610449 lemon<br>0.0490913 bucket, pail|
vgg11 |0.3721453 piggy bank, penny bank<br>0.2952037 Granny Smith<br>0.1076759 tennis ball<br>0.0314685 soap dispenser<br>0.0285692 dumbbell|
vgg11_bn |0.5464050 Granny Smith<br>0.2313121 dumbbell<br>0.0658234 piggy bank, penny bank<br>0.0269569 tennis ball<br>0.0218533 teapot|
vgg13 |0.4068239 Granny Smith<br>0.2272185 dumbbell<br>0.0475026 necklace<br>0.0303710 maraca<br>0.0250665 teapot|
vgg13_bn |0.9389396 Granny Smith<br>0.0383620 tennis ball<br>0.0069443 lemon<br>0.0039320 orange<br>0.0013574 banana|
vgg16 |0.6872565 piggy bank, penny bank<br>0.0687328 Granny Smith<br>0.0588234 teapot<br>0.0392139 tennis ball<br>0.0210059 pitcher, ewer|
vgg16_bn |0.9958423 Granny Smith<br>0.0010665 tennis ball<br>0.0008365 piggy bank, penny bank<br>0.0004831 teapot<br>0.0004004 dumbbell|
vgg19 |0.6034814 Granny Smith<br>0.1175480 piggy bank, penny bank<br>0.0277911 dumbbell<br>0.0249205 whistle<br>0.0218847 teapot|
vgg19_bn |0.9881877 Granny Smith<br>0.0025413 piggy bank, penny bank<br>0.0011374 teapot<br>0.0009895 saltshaker, salt shaker<br>0.0006477 cup|

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
densenet161  |0.9932107 junco, snowbird<br>0.0015922 chickadee<br>0.0012295 brambling, Fringilla montifringilla<br>0.0011838 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0008891 goldfinch, Carduelis carduelis|
densenet169  |0.9640683 junco, snowbird<br>0.0201314 brambling, Fringilla montifringilla<br>0.0044098 chickadee<br>0.0032345 goldfinch, Carduelis carduelis<br>0.0026739 water ouzel, dipper|
densenet201  |0.9515268 junco, snowbird<br>0.0178252 water ouzel, dipper<br>0.0109119 brambling, Fringilla montifringilla<br>0.0077980 house finch, linnet, Carpodacus mexicanus<br>0.0044695 chickadee|
inceptionv3  ||
mobilenet0.25|0.9301481 junco, snowbird<br>0.0466449 chickadee<br>0.0146190 brambling, Fringilla montifringilla<br>0.0027491 bulbul<br>0.0024721 jay|
mobilenet0.5 |0.9290579 junco, snowbird<br>0.0325394 chickadee<br>0.0142417 water ouzel, dipper<br>0.0070296 brambling, Fringilla montifringilla<br>0.0054897 house finch, linnet, Carpodacus mexicanus|
mobilenet0.75|0.9554648 junco, snowbird<br>0.0176056 house finch, linnet, Carpodacus mexicanus<br>0.0163125 brambling, Fringilla montifringilla<br>0.0040996 chickadee<br>0.0029940 goldfinch, Carduelis carduelis|
mobilenet1.0 |0.9746482 junco, snowbird<br>0.0124388 chickadee<br>0.0072107 brambling, Fringilla montifringilla<br>0.0013413 goldfinch, Carduelis carduelis<br>0.0011567 house finch, linnet, Carpodacus mexicanus|
mobilenetv2_0.25|0.9198207 junco, snowbird<br>0.0456813 chickadee<br>0.0230144 house finch, linnet, Carpodacus mexicanus<br>0.0067220 brambling, Fringilla montifringilla<br>0.0012408 bulbul|
mobilenetv2_0.5 |0.9930903 junco, snowbird<br>0.0035467 chickadee<br>0.0017623 brambling, Fringilla montifringilla<br>0.0013532 house finch, linnet, Carpodacus mexicanus<br>0.0000977 goldfinch, Carduelis carduelis|
mobilenetv2_0.75|0.9800993 junco, snowbird<br>0.0092876 chickadee<br>0.0044733 brambling, Fringilla montifringilla<br>0.0028389 house finch, linnet, Carpodacus mexicanus<br>0.0017407 water ouzel, dipper|
mobilenetv2_1.0 |0.9759791 junco, snowbird<br>0.0164687 chickadee<br>0.0048956 brambling, Fringilla montifringilla<br>0.0009601 house finch, linnet, Carpodacus mexicanus<br>0.0008552 water ouzel, dipper|
resnet18_v1 |0.9597615 junco, snowbird<br>0.0103962 chickadee<br>0.0075481 goldfinch, Carduelis carduelis<br>0.0054580 house finch, linnet, Carpodacus mexicanus<br>0.0053979 water ouzel, dipper|
resnet18_v2 |0.9460657 junco, snowbird<br>0.0180776 brambling, Fringilla montifringilla<br>0.0139834 chickadee<br>0.0075304 goldfinch, Carduelis carduelis<br>0.0037932 water ouzel, dipper|
resnet34_v1 |0.9352033 junco, snowbird<br>0.0226503 water ouzel, dipper<br>0.0129960 brambling, Fringilla montifringilla<br>0.0050841 chickadee<br>0.0037434 goldfinch, Carduelis carduelis|
resnet34_v2 |0.6477917 junco, snowbird<br>0.0750232 water ouzel, dipper<br>0.0672592 brambling, Fringilla montifringilla<br>0.0443261 chickadee<br>0.0321975 goldfinch, Carduelis carduelis|
resnet50_v1 |0.9883676 junco, snowbird<br>0.0037137 brambling, Fringilla montifringilla<br>0.0027347 water ouzel, dipper<br>0.0025455 chickadee<br>0.0007354 goldfinch, Carduelis carduelis|
resnet50_v2 |0.9820375 junco, snowbird<br>0.0070083 water ouzel, dipper<br>0.0032555 chickadee<br>0.0021856 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0017496 brambling, Fringilla montifringilla|
resnet101_v1 |0.9215411 junco, snowbird<br>0.0161462 brambling, Fringilla montifringilla<br>0.0113414 water ouzel, dipper<br>0.0096167 chickadee<br>0.0087583 house finch, linnet, Carpodacus mexicanus|
resnet101_v2 |0.9053509 junco, snowbird<br>0.0451527 water ouzel, dipper<br>0.0106367 chickadee<br>0.0089986 brambling, Fringilla montifringilla<br>0.0037001 goldfinch, Carduelis carduelis|
resnet152_v1 |0.9372504 junco, snowbird<br>0.0259636 water ouzel, dipper<br>0.0113407 chickadee<br>0.0088195 brambling, Fringilla montifringilla<br>0.0031848 house finch, linnet, Carpodacus mexicanus|
resnet152_v2 |0.9695247 junco, snowbird<br>0.0054735 brambling, Fringilla montifringilla<br>0.0041750 water ouzel, dipper<br>0.0027560 goldfinch, Carduelis carduelis<br>0.0024612 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
squeezenet1.0 |0.9904419 junco, snowbird<br>0.0045285 chickadee<br>0.0040343 brambling, Fringilla montifringilla<br>0.0003414 water ouzel, dipper<br>0.0002521 house finch, linnet, Carpodacus mexicanus|
squeezenet1.1 |0.9614601 junco, snowbird<br>0.0250982 chickadee<br>0.0040701 brambling, Fringilla montifringilla<br>0.0035157 goldfinch, Carduelis carduelis<br>0.0030858 ruffed grouse, partridge, Bonasa umbellus|
vgg11 |0.9998955 junco, snowbird<br>0.0000967 chickadee<br>0.0000043 brambling, Fringilla montifringilla<br>0.0000023 water ouzel, dipper<br>0.0000006 bulbul|
vgg11_bn |0.9994942 junco, snowbird<br>0.0002460 brambling, Fringilla montifringilla<br>0.0002328 chickadee<br>0.0000130 water ouzel, dipper<br>0.0000100 goldfinch, Carduelis carduelis|
vgg13 |0.9359032 junco, snowbird<br>0.0610290 chickadee<br>0.0012531 brambling, Fringilla montifringilla<br>0.0012155 water ouzel, dipper<br>0.0002740 bulbul|
vgg13_bn |0.9927477 junco, snowbird<br>0.0041162 chickadee<br>0.0028725 brambling, Fringilla montifringilla<br>0.0000676 goldfinch, Carduelis carduelis<br>0.0000641 house finch, linnet, Carpodacus mexicanus|
vgg16 |0.8946120 junco, snowbird<br>0.0953836 chickadee<br>0.0077338 brambling, Fringilla montifringilla<br>0.0018954 water ouzel, dipper<br>0.0001777 bulbul|
vgg16_bn |0.9928787 junco, snowbird<br>0.0052144 chickadee<br>0.0011600 brambling, Fringilla montifringilla<br>0.0005868 water ouzel, dipper<br>0.0000735 house finch, linnet, Carpodacus mexicanus|
vgg19 |0.9538233 junco, snowbird<br>0.0420003 chickadee<br>0.0040804 water ouzel, dipper<br>0.0000727 brambling, Fringilla montifringilla<br>0.0000097 bulbul|
vgg19_bn |0.9974002 junco, snowbird<br>0.0010910 brambling, Fringilla montifringilla<br>0.0008814 chickadee<br>0.0004659 water ouzel, dipper<br>0.0001015 goldfinch, Carduelis carduelis|

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
densenet161  |0.4418390 lifeboat<br>0.1824288 liner, ocean liner<br>0.0596465 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0325273 submarine, pigboat, sub, U-boat<br>0.0298845 dock, dockage, docking facility|
densenet169  |0.2955862 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2342375 drilling platform, offshore rig<br>0.0940931 liner, ocean liner<br>0.0876006 container ship, containership, container vessel<br>0.0717741 dock, dockage, docking facility|
densenet201  |0.5008167 fireboat<br>0.0950200 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0701643 lifeboat<br>0.0622607 liner, ocean liner<br>0.0582344 container ship, containership, container vessel|
inceptionv3  ||
mobilenet0.25|0.2958905 container ship, containership, container vessel<br>0.2101003 drilling platform, offshore rig<br>0.1384616 submarine, pigboat, sub, U-boat<br>0.0863535 liner, ocean liner<br>0.0732720 beacon, lighthouse, beacon light, pharos|
mobilenet0.5 |0.6135703 liner, ocean liner<br>0.1116956 container ship, containership, container vessel<br>0.0976279 submarine, pigboat, sub, U-boat<br>0.0407747 drilling platform, offshore rig<br>0.0312130 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
mobilenet0.75|0.1367185 pirate, pirate ship<br>0.1318326 container ship, containership, container vessel<br>0.1117856 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0865669 lifeboat<br>0.0837456 liner, ocean liner|
mobilenet1.0 |0.4250087 pirate, pirate ship<br>0.1943999 container ship, containership, container vessel<br>0.0818260 drilling platform, offshore rig<br>0.0519248 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0360357 dock, dockage, docking facility|
mobilenetv2_0.25|0.4253865 liner, ocean liner<br>0.2140183 container ship, containership, container vessel<br>0.0672245 drilling platform, offshore rig<br>0.0430525 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0406143 aircraft carrier, carrier, flattop, attack aircraft carrier|
mobilenetv2_0.5 |0.1714408 liner, ocean liner<br>0.1560861 beacon, lighthouse, beacon light, pharos<br>0.1120990 water bottle<br>0.0924766 container ship, containership, container vessel<br>0.0835731 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
mobilenetv2_0.75|0.4084314 container ship, containership, container vessel<br>0.1701521 liner, ocean liner<br>0.1168837 drilling platform, offshore rig<br>0.1098730 beacon, lighthouse, beacon light, pharos<br>0.0329633 lifeboat|
mobilenetv2_1.0 |0.2700136 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1883821 liner, ocean liner<br>0.1121855 drilling platform, offshore rig<br>0.0574179 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0394433 pirate, pirate ship|
resnet18_v1 |0.3416696 container ship, containership, container vessel<br>0.1224417 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1104408 liner, ocean liner<br>0.0661492 lifeboat<br>0.0649565 pirate, pirate ship|
resnet18_v2 |0.2872612 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1359790 beacon, lighthouse, beacon light, pharos<br>0.1248603 container ship, containership, container vessel<br>0.1217949 dock, dockage, docking facility<br>0.0381380 fireboat|
resnet34_v1 |0.5147033 liner, ocean liner<br>0.0504066 submarine, pigboat, sub, U-boat<br>0.0452916 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0438951 sandbar, sand bar<br>0.0422815 fireboat|
resnet34_v2 |0.4267507 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2477048 container ship, containership, container vessel<br>0.0763716 liner, ocean liner<br>0.0696335 dock, dockage, docking facility<br>0.0447003 beacon, lighthouse, beacon light, pharos|
resnet50_v1 |0.1132128 dock, dockage, docking facility<br>0.0919173 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0890666 catamaran<br>0.0592264 seashore, coast, seacoast, sea-coast<br>0.0560082 container ship, containership, container vessel|
resnet50_v2 |0.4814199 container ship, containership, container vessel<br>0.1134713 liner, ocean liner<br>0.0718215 drilling platform, offshore rig<br>0.0571725 dock, dockage, docking facility<br>0.0450073 lifeboat|
resnet101_v1 |0.2196452 beacon, lighthouse, beacon light, pharos<br>0.1348773 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0985295 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0834723 fireboat<br>0.0616940 drilling platform, offshore rig|
resnet101_v2 |0.2760636 pirate, pirate ship<br>0.1350918 wreck<br>0.0808768 liner, ocean liner<br>0.0636322 drilling platform, offshore rig<br>0.0605573 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
resnet152_v1 |0.1550222 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1267105 liner, ocean liner<br>0.1191449 lifeboat<br>0.1074122 beacon, lighthouse, beacon light, pharos<br>0.0826740 pier|
resnet152_v2 |0.1715954 drilling platform, offshore rig<br>0.1319755 beacon, lighthouse, beacon light, pharos<br>0.0740683 dock, dockage, docking facility<br>0.0558942 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0398145 container ship, containership, container vessel|
squeezenet1.0 |0.8105506 liner, ocean liner<br>0.0785145 drilling platform, offshore rig<br>0.0295156 container ship, containership, container vessel<br>0.0153660 dock, dockage, docking facility<br>0.0115069 submarine, pigboat, sub, U-boat|
squeezenet1.1 |0.4413084 liner, ocean liner<br>0.1931022 container ship, containership, container vessel<br>0.1459108 pirate, pirate ship<br>0.0937747 fireboat<br>0.0198683 drilling platform, offshore rig|
vgg11 |0.3343849 container ship, containership, container vessel<br>0.3068860 liner, ocean liner<br>0.0492899 submarine, pigboat, sub, U-boat<br>0.0455568 fireboat<br>0.0391509 lifeboat|
vgg11_bn |0.7272964 container ship, containership, container vessel<br>0.1716903 liner, ocean liner<br>0.0226533 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0206520 dock, dockage, docking facility<br>0.0114507 lifeboat|
vgg13 |0.3224934 container ship, containership, container vessel<br>0.2891446 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1808191 liner, ocean liner<br>0.0591594 beacon, lighthouse, beacon light, pharos<br>0.0270379 dock, dockage, docking facility|
vgg13_bn |0.3478981 container ship, containership, container vessel<br>0.2664557 fireboat<br>0.0766566 lifeboat<br>0.0664669 liner, ocean liner<br>0.0515883 submarine, pigboat, sub, U-boat|
vgg16 |0.2839452 liner, ocean liner<br>0.2079168 fireboat<br>0.1477822 container ship, containership, container vessel<br>0.0909363 lifeboat<br>0.0704186 dock, dockage, docking facility|
vgg16_bn |0.3687426 container ship, containership, container vessel<br>0.3540941 liner, ocean liner<br>0.1349645 fireboat<br>0.0337696 speedboat<br>0.0263291 submarine, pigboat, sub, U-boat|
vgg19 |0.4434196 liner, ocean liner<br>0.1207930 container ship, containership, container vessel<br>0.0979091 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0852779 drilling platform, offshore rig<br>0.0730739 dock, dockage, docking facility|
vgg19_bn |0.5504534 fireboat<br>0.1722971 liner, ocean liner<br>0.0720537 container ship, containership, container vessel<br>0.0406803 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0388017 drilling platform, offshore rig|


<!-- LINKS -->
[imagenet]: http://www.image-net.org
[gluon_modelzoo_classification]: https://cv.gluon.ai/model_zoo/classification.html
