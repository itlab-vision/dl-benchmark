# Validation results for the models inferring using TensorFlow Lite

## Public models (Open Model Zoo)

### Image classification

#### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Parameters | Python (implementation) |
-|-|-|
densenet-121|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.9523314 Granny Smith<br>0.0132282 orange<br>0.0125180 lemon<br>0.0027912 banana<br>0.0020333 piggy bank, penny bank|
googlenet-v1-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v2-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v3|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v4-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.9969806 Granny Smith<br>0.0001207 Rhodesian ridgeback<br>0.0000488 hair slide<br>0.0000473 pineapple, ananas<br>0.0000330 banana|
mobilenet-v1-1.0-224-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
mobilenet_v2_1.0_224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
mobilenet-v2-1.4-224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
inception-resnet-v2-tf|Image resolution: 299x299.<br>Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|8.0107708 Granny Smith<br>4.4552484 piggy bank, penny bank<br>4.2636762 bell pepper<br>3.9343853 candle, taper, wax light<br>3.5531902 pomegranate|
resnet-50-tf|Mean: [123.675,116.28,103.53].| 0.9553038 Granny Smith<br>0.0052123 lemon<br>0.0047185 piggy bank, penny bank<br>0.0045875 orange<br>0.0044233 necklace|

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
densenet-121|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.9841611 junco, snowbird<br>0.0072198 chickadee<br>0.0034962 brambling, Fringilla montifringilla<br>0.0016226 water ouzel, dipper<br>0.0012858 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
googlenet-v1-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v2-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v3|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v4-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].| 0.9339716 junco, snowbird<br>0.0006892 chickadee<br>0.0005481 brambling, Fringilla montifringilla<br>0.0004948 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0004539 water ouzel, dipper|
mobilenet-v1-1.0-224-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
mobilenet_v2_1.0_224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
mobilenet-v2-1.4-224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
inception-resnet-v2-tf|Image resolution: 299x299.<br>Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|10.0273972 junco, snowbird<br>4.6770372 brambling, Fringilla montifringilla<br>4.2079940 goldfinch, Carduelis carduelis<br>4.1425276 water ouzel, dipper<br>4.0244055 chickadee|
resnet-50-tf|Mean: [123.675,116.28,103.53].|0.9983400 junco, snowbird<br>0.0004680 brambling, Fringilla montifringilla<br>0.0003848 chickadee<br>0.0003656 water ouzel, dipper<br>0.0003383 goldfinch, Carduelis carduelis|

#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
densenet-121|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].| 0.3022473 liner, ocean liner<br>0.1322417 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1194588 container ship, containership, container vessel<br>0.0795097 drilling platform, offshore rig<br>0.0723070 dock, dockage, docking facility|
googlenet-v1-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v2-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v3|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
googlenet-v4-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.6737013 lifeboat<br>0.0432948 submarine, pigboat, sub, U-boat<br>0.0322841 fireboat<br>0.0264144 beacon, lighthouse, beacon light, pharos<br>0.0147488 drilling platform, offshore rig|
mobilenet-v1-1.0-224-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
mobilenet_v2_1.0_224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
mobilenet-v2-1.4-224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|-|
inception-resnet-v2-tf|Image resolution: 299x299.<br>Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|6.4228325 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.0842223 liner, ocean liner<br>5.8280630 fireboat<br>5.7098336 dock, dockage, docking facility<br>5.6666737 container ship, containership, container vessel|
resnet-50-tf|Mean: [123.675,116.28,103.53].|0.2357713 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1480762 liner, ocean liner<br>0.1104688 container ship, containership, container vessel<br>0.1095407 drilling platform, offshore rig<br>0.0915569 beacon, lighthouse, beacon light, pharos|

### Other tasks

[TBD]

## Public models (TF hub)

### Image classification

#### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Parameters | Python (implementation) |
-|-|-|
mobilenet_v1_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.7150755 Granny Smith<br>0.0202576 piggy bank, penny bank<br>0.0088377 teapot<br>0.0072254 bell pepper<br>0.0058900 banana|
mobilenet_v2_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.6549551 Granny Smith<br>0.1130055 piggy bank, penny bank<br>0.0566443 teapot<br>0.0250644 saltshaker, salt shaker<br>0.0120769 vase|
mobilenet_v3_small_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.5426094 Granny Smith<br>0.0725947 teapot<br>0.0285967 piggy bank, penny bank<br>0.0269885 pitcher, ewer<br>0.0195926 vase|
mobilenet_v3_large_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.8494291 Granny Smith<br>0.0085453 piggy bank, penny bank<br>0.0069065 lemon<br>0.0055464 tennis ball<br>0.0027605 pomegranate|
mobilenet_v1_100_224_uint8_1|-|248.0000000 Granny Smith<br>1.0000000 lemon<br>0.0000000 sulphur butterfly, sulfur butterfly<br>0.0000000 guinea pig, Cavia cobaya<br>0.0000000 beaver|
mobilenet_v2_100_224_uint8_1|-|242.0000000 Granny Smith<br>2.0000000 piggy bank, penny bank<br>1.0000000 lemon<br>1.0000000 teapot<br>1.0000000 saltshaker, salt shaker|
mobilenet_v3_small_100_224_uint8_1|-|25.0000000 junco, snowbird<br>13.0000000 water ouzel, dipper<br>11.0000000 chickadee<br>8.0000000 brambling, Fringilla montifringilla<br>7.0000000 goldfinch, Carduelis carduelis|
mobilenet_v3_large_100_224_uint8_1|-|204.0000000 Granny Smith<br>6.0000000 piggy bank, penny bank<br>1.0000000 orange<br>1.0000000 teapot<br>1.0000000 vase|
efficientnet_lite0_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite0_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite0_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
mobilenet_v1_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].| 0.8584890 junco, snowbird<br>0.0235178 brambling, Fringilla montifringilla<br>0.0185745 goldfinch, Carduelis carduelis<br>0.0094353 water ouzel, dipper<br>0.0067247 chickadee|
mobilenet_v2_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.8474838 junco, snowbird<br>0.0402333 chickadee<br>0.0112412 brambling, Fringilla montifringilla<br>0.0056867 water ouzel, dipper<br>0.0020902 goldfinch, Carduelis carduelis|
mobilenet_v3_small_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].| 0.6117089 junco, snowbird<br>0.0544940 chickadee<br>0.0274826 goldfinch, Carduelis carduelis<br>0.0213195 water ouzel, dipper<br>0.0100568 brambling, Fringilla montifringilla|
mobilenet_v3_large_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.6303865 junco, snowbird<br>0.0645584 brambling, Fringilla montifringilla<br>0.0283644 goldfinch, Carduelis carduelis<br>0.0097315 chickadee<br>0.0092374 water ouzel, dipper|
mobilenet_v1_100_224_uint8_1|-|181.0000000 junco, snowbird<br>20.0000000 brambling, Fringilla montifringilla<br>12.0000000 goldfinch, Carduelis carduelis<br>3.0000000 chickadee<br>3.0000000 house finch, linnet, Carpodacus mexicanus|
mobilenet_v2_100_224_uint8_1|-|221.0000000 junco, snowbird<br>6.0000000 chickadee<br>3.0000000 brambling, Fringilla montifringilla<br>1.0000000 water ouzel, dipper<br>0.0000000 toilet tissue, toilet paper, bathroom tissue|
mobilenet_v3_small_100_224_uint8_1|-| 97.0000000 Granny Smith<br>27.0000000 tennis ball<br>8.0000000 ping-pong ball<br>5.0000000 candle, taper, wax light<br>5.0000000 saltshaker, salt shaker|
mobilenet_v3_large_100_224_uint8_1|-|144.0000000 junco, snowbird<br>9.0000000 goldfinch, Carduelis carduelis<br>6.0000000 water ouzel, dipper<br>5.0000000 chickadee<br>5.0000000 brambling, Fringilla montifringilla|
efficientnet_lite0_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite0_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite0_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|

#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
mobilenet_v1_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.1904013 liner, ocean liner<br>0.0967771 lifeboat<br>0.0881745 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0482143 beacon, lighthouse, beacon light, pharos<br>0.0478232 catamaran|
mobilenet_v2_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.0606234 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0568781 container ship, containership, container vessel<br>0.0518561 lifeboat<br>0.0431800 beacon, lighthouse, beacon light, pharos<br>0.0337389 drilling platform, offshore rig|
mobilenet_v3_small_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.0724729 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0653515 drilling platform, offshore rig<br>0.0644393 liner, ocean liner<br>0.0580560 container ship, containership, container vessel<br>0.0499799 beacon, lighthouse, beacon light, pharos|
mobilenet_v3_large_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.2661534 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0744180 beacon, lighthouse, beacon light, pharos<br>0.0523450 container ship, containership, container vessel<br>0.0406797 pirate, pirate ship<br>0.0398768 aircraft carrier, carrier, flattop, attack aircraft carrier|
mobilenet_v1_100_224_uint8_1|-|34.0000000 catamaran<br>26.0000000 liner, ocean liner<br>21.0000000 water bottle<br>10.0000000 dock, dockage, docking facility<br>9.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
mobilenet_v2_100_224_uint8_1|-|15.0000000 pirate, pirate ship<br>14.0000000 liner, ocean liner<br>7.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>7.0000000 container ship, containership, container vessel<br>6.0000000 catamaran|
mobilenet_v3_small_100_224_uint8_1|-|25.0000000 drilling platform, offshore rig<br>17.0000000 beacon, lighthouse, beacon light, pharos<br>15.0000000 aircraft carrier, carrier, flattop, attack aircraft carrier<br>12.0000000 container ship, containership, container vessel<br>12.0000000 sandbar, sand bar|
mobilenet_v3_large_100_224_uint8_1|-|67.0000000 beacon, lighthouse, beacon light, pharos<br>40.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>32.0000000 container ship, containership, container vessel<br>10.0000000 fireboat<br>9.0000000 seashore, coast, seacoast, sea-coast|
efficientnet_lite0_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_fp32_2|Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite0_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_int8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite0_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite1_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite2_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite3_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|
efficientnet_lite4_uint8_1|Image resolution: 300x300.<br>Mean: [127,127,127].<br>Input scale: [128,128,128].|-|

### Other tasks

[TBD]

<!-- LINKS -->
[imagenet]: http://www.image-net.org
