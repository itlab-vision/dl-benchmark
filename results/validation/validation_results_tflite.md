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

Model | Parameters | Python API |
-|-|-|
densenet-121|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.9523314 Granny Smith<br>0.0132282 orange<br>0.0125180 lemon<br>0.0027912 banana<br>0.0020333 piggy bank, penny bank|
googlenet-v1-tf|Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.6735930 Granny Smith<br>0.0737855 piggy bank, penny bank<br>0.0155380 vase<br>0.0154004 pitcher, ewer<br>0.0136552 saltshaker, salt shaker|
googlenet-v2-tf|Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.9849940 Granny Smith<br>0.0010004 lemon<br>0.0009706 pomegranate<br>0.0006835 tennis ball<br>0.0006694 banana|
googlenet-v3|Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.9867674 Granny Smith<br> 0.0008529 bikini, two-piece<br>0.0005354 piggy bank, penny bank<br>0.0003701 pomegranate<br>0.0001682 pool table, billiard table, snooker table|
googlenet-v4-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.9969806 Granny Smith<br>0.0001207 Rhodesian ridgeback<br>0.0000488 hair slide<br>0.0000473 pineapple, ananas<br>0.0000330 banana|
mobilenet-v1-1.0-224-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.2949494 pitcher, ewer<br>0.1867124 saltshaker, salt shaker<br>0.1249271 necklace<br>0.0867643 piggy bank, penny bank<br>0.0360211 Granny Smith|
mobilenet-v2-1.0-224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.4164807 Granny Smith<br>0.3500757 piggy bank, penny bank<br>0.0358796 saltshaker, salt shaker<br>0.0147685 vase<br>0.0131548 pitcher, ewer|
mobilenet-v2-1.4-224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.3428614 saltshaker, salt shaker<br>0.0935006 vase<br>0.0899924 Granny Smith<br>0.0667358 pitcher, ewer<br>0.0666182 piggy bank, penny bank|
inception-resnet-v2-tf|Image resolution: 299x299.<br>Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|8.0107708 Granny Smith<br>4.4552484 piggy bank, penny bank<br>4.2636762 bell pepper<br>3.9343853 candle, taper, wax light<br>3.5531902 pomegranate|
mobilenet-v3-small-1.0-224|-| 0.4481893 Granny Smith<br>0.0884615 lemon<br>0.0727510 pop bottle, soda bottle<br>0.0331238 saltshaker, salt shaker<br>0.0218442 pitcher, ewer|
mobilenet-v3-large-1.0-224|-|0.6718515 Granny Smith<br>0.1939126 piggy bank, penny bank<br>0.0254287 lemon<br>0.0245753 vase<br>0.0090322 teapot|
resnet-50-tf|Mean: [123.675,116.28,103.53].| 0.9553038 Granny Smith<br>0.0052123 lemon<br>0.0047185 piggy bank, penny bank<br>0.0045875 orange<br>0.0044233 necklace|



#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python API |
-|-|-|
densenet-121|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.9841611 junco, snowbird<br>0.0072198 chickadee<br>0.0034962 brambling, Fringilla montifringilla<br>0.0016226 water ouzel, dipper<br>0.0012858 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
googlenet-v1-tf|Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.7443183 junco, snowbird<br>0.0474523 brambling, Fringilla montifringilla<br>0.0457429 chickadee<br>0.0213391 goldfinch, Carduelis carduelis<br>0.0085102 house finch, linnet, Carpodacus mexicanus|
googlenet-v2-tf|Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.9265908 junco, snowbird<br>0.0166747 brambling, Fringilla montifringilla<br>0.0058714 chickadee<br>0.0026126 water ouzel, dipper<br>0.0022344 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
googlenet-v3|Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.9488292 junco, snowbird<br>0.0005887 water ouzel, dipper<br>0.0004797 iron, smoothing iron<br>0.0003071 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002692 cleaver, meat cleaver, chopper|
googlenet-v4-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].| 0.9339716 junco, snowbird<br>0.0006892 chickadee<br>0.0005481 brambling, Fringilla montifringilla<br>0.0004948 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0004539 water ouzel, dipper|
mobilenet-v1-1.0-224-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.7099941 junco, snowbird<br>0.2239839 chickadee<br>0.0195020 goldfinch, Carduelis carduelis<br>0.0140457 jay<br>0.0136091 brambling, Fringilla montifringilla|
mobilenet-v2-1.0-224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.3981952 junco, snowbird<br>0.0649636 chickadee<br>0.0456628 brambling, Fringilla montifringilla<br>0.0063850 water ouzel, dipper<br>0.0041957 goldfinch, Carduelis carduelis|
mobilenet-v2-1.4-224|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.7363465 chickadee<br>0.0283495 junco, snowbird<br>0.0117877 brambling, Fringilla montifringilla<br>0.0083691 goldfinch, Carduelis carduelis<br>0.0035830 water ouzel, dipper|
inception-resnet-v2-tf|Image resolution: 299x299.<br>Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|10.0273972 junco, snowbird<br>4.6770372 brambling, Fringilla montifringilla<br>4.2079940 goldfinch, Carduelis carduelis<br>4.1425276 water ouzel, dipper<br>4.0244055 chickadee|
mobilenet-v3-small-1.0-224|-|0.5813942 junco, snowbird<br>0.0588930 brambling, Fringilla montifringilla<br>0.0446762 house finch, linnet, Carpodacus mexicanus<br>0.0411857 goldfinch, Carduelis carduelis<br>0.0150912 chickadee|
mobilenet-v3-large-1.0-224|-|0.7943738 junco, snowbird<br>0.0318200 brambling, Fringilla montifringilla<br>0.0084637 water ouzel, dipper<br>0.0071047 goldfinch, Carduelis carduelis<br>0.0061734 chickadee|
resnet-50-tf|Mean: [123.675,116.28,103.53].|0.9983400 junco, snowbird<br>0.0004680 brambling, Fringilla montifringilla<br>0.0003848 chickadee<br>0.0003656 water ouzel, dipper<br>0.0003383 goldfinch, Carduelis carduelis|


#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters                                                                                        | Python API |
-|---------------------------------------------------------------------------------------------------|-|
densenet-121| Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].| 0.3022473 liner, ocean liner<br>0.1322417 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1194588 container ship, containership, container vessel<br>0.0795097 drilling platform, offshore rig<br>0.0723070 dock, dockage, docking facility|
googlenet-v1-tf| Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.1235979 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br> 0.1017586 liner, ocean liner<br>0.0949444 drilling platform, offshore rig<br>0.0817947 container ship, containership, container vessel<br>0.0486889 fireboat|
googlenet-v2-tf| Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.2662660 container ship, containership, container vessel<br>0.0966037 dock, dockage, docking facility<br> 0.0876837 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0488674 beacon, lighthouse, beacon light, pharos<br>0.0343599 drilling platform, offshore rig|
googlenet-v3| Mean: [127.5, 127.5, 127.5].<br>Input scale: [127.5].|0.4653829 beacon, lighthouse, beacon light, pharos<br>0.3437532 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0512180 submarine, pigboat, sub, U-boat<br>0.0174647 liner, ocean liner<br>0.0134649 lifeboat|
googlenet-v4-tf| Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.6737013 lifeboat<br>0.0432948 submarine, pigboat, sub, U-boat<br>0.0322841 fireboat<br>0.0264144 beacon, lighthouse, beacon light, pharos<br>0.0147488 drilling platform, offshore rig|
mobilenet-v1-1.0-224-tf| Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.1175058 lifeboat<br>0.1106691 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.1055247 liner, ocean liner<br>0.0836357 beacon, lighthouse, beacon light, pharos<br>0.0784211 drilling platform, offshore rig|
mobilenet-v2-1.0-224| Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.2761748 beacon, lighthouse, beacon light, pharos<br>0.1192475 liner, ocean liner<br>0.0864237 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0541655 drilling platform, offshore rig<br>0.0266723 container ship, containership, container vessel|
mobilenet-v2-1.4-224| Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|0.2250047 beacon, lighthouse, beacon light, pharos<br>0.2051269 container ship, containership, container vessel<br>0.1319712 liner, ocean liner<br>0.0256291 dock, dockage, docking facility<br>0.0241968 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
inception-resnet-v2-tf| Image resolution: 299x299.<br>Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|6.4228325 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.0842223 liner, ocean liner<br>5.8280630 fireboat<br>5.7098336 dock, dockage, docking facility<br>5.6666737 container ship, containership, container vessel|
mobilenet-v3-small-1.0-224|-|0.0980954 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0957138 container ship, containership, container vessel<br>0.0853775 pirate, pirate ship<br>0.0690932 drilling platform, offshore rig<br>0.0685616 lifeboat|
mobilenet-v3-large-1.0-224|-|0.1806492 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1449896 lifeboat<br>0.1315165 submarine, pigboat, sub, U-boat<br>0.0884149 dock, dockage, docking facility<br>0.0476540 fireboat|
resnet-50-tf| Mean: [123.675,116.28,103.53].|0.2357713 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1480762 liner, ocean liner<br>0.1104688 container ship, containership, container vessel<br>0.1095407 drilling platform, offshore rig<br>0.0915569 beacon, lighthouse, beacon light, pharos|

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

Model | Parameters | Python API |
-|-|-|
mobilenet_v1_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.7150755 Granny Smith<br>0.0202576 piggy bank, penny bank<br>0.0088377 teapot<br>0.0072254 bell pepper<br>0.0058900 banana|
mobilenet_v2_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.6549551 Granny Smith<br>0.1130055 piggy bank, penny bank<br>0.0566443 teapot<br>0.0250644 saltshaker, salt shaker<br>0.0120769 vase|
mobilenet_v3_small_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.5426094 Granny Smith<br>0.0725947 teapot<br>0.0285967 piggy bank, penny bank<br>0.0269885 pitcher, ewer<br>0.0195926 vase|
mobilenet_v3_large_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.8494291 Granny Smith<br>0.0085453 piggy bank, penny bank<br>0.0069065 lemon<br>0.0055464 tennis ball<br>0.0027605 pomegranate|
mobilenet_v1_100_224_uint8_1|-|248.0000000 Granny Smith<br>1.0000000 lemon<br>0.0000000 sulphur butterfly, sulfur butterfly<br>0.0000000 guinea pig, Cavia cobaya<br>0.0000000 beaver|
mobilenet_v2_100_224_uint8_1|-|242.0000000 Granny Smith<br>2.0000000 piggy bank, penny bank<br>1.0000000 lemon<br>1.0000000 teapot<br>1.0000000 saltshaker, salt shaker|
mobilenet_v3_small_100_224_uint8_1|-|25.0000000 junco, snowbird<br>13.0000000 water ouzel, dipper<br>11.0000000 chickadee<br>8.0000000 brambling, Fringilla montifringilla<br>7.0000000 goldfinch, Carduelis carduelis|
mobilenet_v3_large_100_224_uint8_1|-|204.0000000 Granny Smith<br>6.0000000 piggy bank, penny bank<br>1.0000000 orange<br>1.0000000 teapot<br>1.0000000 vase|
efficientnet_lite0_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.1806599 dumbbell<br>0.1265180 screw<br>0.0506000 Granny Smith<br>0.0467094 barbell<br>0.0345199 vase|
efficientnet_lite1_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.0281865 wool, woolen, woollen<br>0.0269535 water bottle<br>0.0259669 trilobite<br>0.0250501 Granny Smith<br>0.0229548 teapot|
efficientnet_lite2_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.1039253 vase<br>0.1024296 pitcher, ewer<br>0.0350566 teapot<br>0.0325848 hook, claw<br>0.0292138 cup|
efficientnet_lite3_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.1926491 pitcher, ewer<br>0.1502650 teapot<br>0.1470646 electric fan, blower<br>0.1428124 water jug<br>0.1257372 strainer0.1926491 pitcher, ewer<br>0.1502650 teapot<br>0.1470646 electric fan, blower<br>0.1428124 water jug<br>0.1257372 strainer|
efficientnet_lite4_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.5777039 Granny Smith<br>0.1232639 teapot<br>0.0563486 pitcher, ewer<br>0.0132013 jack-o'-lantern<br>0.0130741 orange|
lite-efficientnet_lite0_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|81.0000000 Granny Smith<br>30.0000000 bell pepper<br>27.0000000 orange<br>17.0000000 pomegranate<br>10.0000000 strawberry|
lite-efficientnet_lite1_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|25.0000000 bell pepper<br>20.0000000 Granny Smith<br>18.0000000 orange<br>16.0000000 candle, taper, wax light<br>11.0000000 piggy bank, penny bank|
lite-efficientnet_lite2_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|39.0000000 Granny Smith<br>27.0000000 orange<br>22.0000000 piggy bank, penny bank<br>13.0000000 bell pepper<br>12.0000000 candle, taper, wax light|
lite-efficientnet_lite3_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|207.0000000 Granny Smith<br>10.0000000 tennis ball<br>9.0000000 orange<br>4.0000000 piggy bank, penny bank<br>3.0000000 lemon|
lite-efficientnet_lite4_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|141.0000000 Granny Smith<br>19.0000000 orange<br>5.0000000 piggy bank, penny bank<br>4.0000000 banana<br>3.0000000 jack-o'-lantern|
efficientnet_lite0_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|81.0000000 Granny Smith<br>30.0000000 bell pepper<br>27.0000000 orange<br>17.0000000 pomegranate<br>10.0000000 strawberry|
efficientnet_lite1_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|25.0000000 bell pepper<br>20.0000000 Granny Smith<br>18.0000000 orange<br>16.0000000 candle, taper, wax light<br>11.0000000 piggy bank, penny bank|
efficientnet_lite2_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|39.0000000 Granny Smith<br>27.0000000 orange<br>22.0000000 piggy bank, penny bank<br>13.0000000 bell pepper<br>12.0000000 candle, taper, wax light|
efficientnet_lite3_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|207.0000000 Granny Smith<br>10.0000000 tennis ball<br>9.0000000 orange<br>4.0000000 piggy bank, penny bank<br>3.0000000 lemon|
efficientnet_lite4_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|141.0000000 Granny Smith<br>19.0000000 orange<br>5.0000000 piggy bank, penny bank<br>4.0000000 banana<br>3.0000000 jack-o'-lantern|

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python API |
-|-|-|
mobilenet_v1_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].| 0.8584890 junco, snowbird<br>0.0235178 brambling, Fringilla montifringilla<br>0.0185745 goldfinch, Carduelis carduelis<br>0.0094353 water ouzel, dipper<br>0.0067247 chickadee|
mobilenet_v2_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.8474838 junco, snowbird<br>0.0402333 chickadee<br>0.0112412 brambling, Fringilla montifringilla<br>0.0056867 water ouzel, dipper<br>0.0020902 goldfinch, Carduelis carduelis|
mobilenet_v3_small_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].| 0.6117089 junco, snowbird<br>0.0544940 chickadee<br>0.0274826 goldfinch, Carduelis carduelis<br>0.0213195 water ouzel, dipper<br>0.0100568 brambling, Fringilla montifringilla|
mobilenet_v3_large_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.6303865 junco, snowbird<br>0.0645584 brambling, Fringilla montifringilla<br>0.0283644 goldfinch, Carduelis carduelis<br>0.0097315 chickadee<br>0.0092374 water ouzel, dipper|
mobilenet_v1_100_224_uint8_1|-|181.0000000 junco, snowbird<br>20.0000000 brambling, Fringilla montifringilla<br>12.0000000 goldfinch, Carduelis carduelis<br>3.0000000 chickadee<br>3.0000000 house finch, linnet, Carpodacus mexicanus|
mobilenet_v2_100_224_uint8_1|-|221.0000000 junco, snowbird<br>6.0000000 chickadee<br>3.0000000 brambling, Fringilla montifringilla<br>1.0000000 water ouzel, dipper<br>0.0000000 toilet tissue, toilet paper, bathroom tissue|
mobilenet_v3_small_100_224_uint8_1|-| 97.0000000 Granny Smith<br>27.0000000 tennis ball<br>8.0000000 ping-pong ball<br>5.0000000 candle, taper, wax light<br>5.0000000 saltshaker, salt shaker|
mobilenet_v3_large_100_224_uint8_1|-|144.0000000 junco, snowbird<br>9.0000000 goldfinch, Carduelis carduelis<br>6.0000000 water ouzel, dipper<br>5.0000000 chickadee<br>5.0000000 brambling, Fringilla montifringilla|
efficientnet_lite0_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.0890195 chickadee<br>0.0884429 bee eater<br>0.0799505 goldfinch, Carduelis carduelis<br>0.0760872 brambling, Fringilla montifringilla<br>0.0670157 hummingbird|
efficientnet_lite1_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.1486115 guenon, guenon monkey<br>0.0709516 three-toed sloth, ai, Bradypus tridactylus<br>0.0540262 marmoset<br>0.0501767 toucan<br>0.0370303 junco, snowbird|
efficientnet_lite2_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.2191649 bulbul<br>0.2073708 three-toed sloth, ai, Bradypus tridactylus<br>0.1857240 chickadee<br>0.0258803 junco, snowbird<br>0.0256731 house finch, linnet, Carpodacus mexicanus|
efficientnet_lite3_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.4806626 junco, snowbird<br>0.1389775 brambling, Fringilla montifringilla<br>0.1015250 house finch, linnet, Carpodacus mexicanus<br>0.0838527 chickadee<br>0.0206517 bulbul|
efficientnet_lite4_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.3836534 chickadee<br>0.3339088 junco, snowbird<br>0.0034993 brambling, Fringilla montifringilla<br>0.0031002 water ouzel, dipper<br>0.0028740 hummingbird|
lite-efficientnet_lite0_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|38.0000000 bee eater<br>31.0000000 chickadee<br>31.0000000 house finch, linnet, Carpodacus mexicanus<br>29.0000000 junco, snowbird<br>24.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
lite-efficientnet_lite1_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|84.0000000 jay<br>28.0000000 junco, snowbird<br>11.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.0000000 chickadee<br>7.0000000 little blue heron, Egretta caerulea|
lite-efficientnet_lite2_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|73.0000000 junco, snowbird<br>26.0000000 chickadee<br>8.0000000 brambling, Fringilla montifringilla<br>4.0000000 bulbul<br>3.0000000 jay|
lite-efficientnet_lite3_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|58.0000000 jay<br>26.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>20.0000000 chickadee<br>17.0000000 jacamar<br>11.0000000 bee eater|
lite-efficientnet_lite4_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|150.0000000 hummingbird<br>20.0000000 junco, snowbird<br>11.0000000 jacamar<br>6.0000000 water ouzel, dipper<br>4.0000000 chickadee|
efficientnet_lite0_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|38.0000000 bee eater<br>31.0000000 chickadee<br>31.0000000 house finch, linnet, Carpodacus mexicanus<br>29.0000000 junco, snowbird<br>24.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
efficientnet_lite1_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|84.0000000 jay<br>28.0000000 junco, snowbird<br>11.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.0000000 chickadee<br>7.0000000 little blue heron, Egretta caerulea|
efficientnet_lite2_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|73.0000000 junco, snowbird<br>26.0000000 chickadee<br>8.0000000 brambling, Fringilla montifringilla<br>4.0000000 bulbul<br>3.0000000 jay|
efficientnet_lite3_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|58.0000000 jay<br>26.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>20.0000000 chickadee<br>17.0000000 jacamar<br>11.0000000 bee eater|
efficientnet_lite4_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|150.0000000 hummingbird<br>20.0000000 junco, snowbird<br>11.0000000 jacamar<br>6.0000000 water ouzel, dipper<br>4.0000000 chickadee|


#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python API |
-|-|-|
mobilenet_v1_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.1904013 liner, ocean liner<br>0.0967771 lifeboat<br>0.0881745 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0482143 beacon, lighthouse, beacon light, pharos<br>0.0478232 catamaran|
mobilenet_v2_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.0606234 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0568781 container ship, containership, container vessel<br>0.0518561 lifeboat<br>0.0431800 beacon, lighthouse, beacon light, pharos<br>0.0337389 drilling platform, offshore rig|
mobilenet_v3_small_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.0724729 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0653515 drilling platform, offshore rig<br>0.0644393 liner, ocean liner<br>0.0580560 container ship, containership, container vessel<br>0.0499799 beacon, lighthouse, beacon light, pharos|
mobilenet_v3_large_100_224_fp32_1|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.2661534 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0744180 beacon, lighthouse, beacon light, pharos<br>0.0523450 container ship, containership, container vessel<br>0.0406797 pirate, pirate ship<br>0.0398768 aircraft carrier, carrier, flattop, attack aircraft carrier|
mobilenet_v1_100_224_uint8_1|-|34.0000000 catamaran<br>26.0000000 liner, ocean liner<br>21.0000000 water bottle<br>10.0000000 dock, dockage, docking facility<br>9.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
mobilenet_v2_100_224_uint8_1|-|15.0000000 pirate, pirate ship<br>14.0000000 liner, ocean liner<br>7.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>7.0000000 container ship, containership, container vessel<br>6.0000000 catamaran|
mobilenet_v3_small_100_224_uint8_1|-|25.0000000 drilling platform, offshore rig<br>17.0000000 beacon, lighthouse, beacon light, pharos<br>15.0000000 aircraft carrier, carrier, flattop, attack aircraft carrier<br>12.0000000 container ship, containership, container vessel<br>12.0000000 sandbar, sand bar|
mobilenet_v3_large_100_224_uint8_1|-|67.0000000 beacon, lighthouse, beacon light, pharos<br>40.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>32.0000000 container ship, containership, container vessel<br>10.0000000 fireboat<br>9.0000000 seashore, coast, seacoast, sea-coast|
efficientnet_lite0_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.1718010 liner, ocean liner<br>0.1557053 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.1440452 submarine, pigboat, sub, U-boat<br>0.0589084 beacon, lighthouse, beacon light, pharos<br>0.0228401 space shuttle|
efficientnet_lite1_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.1246776 beacon, lighthouse, beacon light, pharos<br>0.0895273 liner, ocean liner<br>0.0312974 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0166320 submarine, pigboat, sub, U-boat<br>0.0145705 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
efficientnet_lite2_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.2495511 beacon, lighthouse, beacon light, pharos<br>0.1150195 submarine, pigboat, sub, U-boat<br>0.0678146 liner, ocean liner<br>0.0312395 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0109627 catamaran|
efficientnet_lite3_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.0830593 liner, ocean liner<br>0.0747621 beacon, lighthouse, beacon light, pharos<br>0.0370711 container ship, containership, container vessel<br>0.0300901 sewing machine<br>0.0277146 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
efficientnet_lite4_fp32_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|0.9409395 liner, ocean liner<br>0.0027906 container ship, containership, container vessel<br>0.0024161 dock, dockage, docking facility<br>0.0019609 fireboat<br>0.0011747 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
lite-efficientnet_lite0_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|53.0000000 lifeboat<br>34.0000000 catamaran<br>23.0000000 speedboat<br>15.0000000 liner, ocean liner<br>12.0000000 fireboat|
lite-efficientnet_lite1_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|12.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>11.0000000 beacon, lighthouse, beacon light, pharos<br>10.0000000 stupa, tope<br>9.0000000 liner, ocean liner<br>8.0000000 catamaran|
lite-efficientnet_lite2_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|19.0000000 liner, ocean liner<br>11.0000000 fireboat<br>10.0000000 beacon, lighthouse, beacon light, pharos<br>9.0000000 dock, dockage, docking facility<br>9.0000000 drilling platform, offshore rig|
lite-efficientnet_lite3_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|47.0000000 beacon, lighthouse, beacon light, pharos<br>33.0000000 liner, ocean liner<br>15.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>8.0000000 container ship, containership, container vessel<br>7.0000000 lifeboat|
lite-efficientnet_lite4_uint8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|68.0000000 drilling platform, offshore rig<br>38.0000000 container ship, containership, container vessel<br>14.0000000 lifeboat<br>13.0000000 fireboat<br>12.0000000 dock, dockage, docking facility|
efficientnet_lite0_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|53.0000000 lifeboat<br>34.0000000 catamaran<br>23.0000000 speedboat<br>15.0000000 liner, ocean liner<br>12.0000000 fireboat|
efficientnet_lite1_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|12.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>11.0000000 beacon, lighthouse, beacon light, pharos<br>10.0000000 stupa, tope<br>9.0000000 liner, ocean liner<br>8.0000000 catamaran|
efficientnet_lite2_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|19.0000000 liner, ocean liner<br>11.0000000 fireboat<br>10.0000000 beacon, lighthouse, beacon light, pharos<br>9.0000000 dock, dockage, docking facility<br>9.0000000 drilling platform, offshore rig|
efficientnet_lite3_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|47.0000000 beacon, lighthouse, beacon light, pharos<br>33.0000000 liner, ocean liner<br>15.0000000 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>8.0000000 container ship, containership, container vessel<br>7.0000000 lifeboat|
efficientnet_lite4_int8_2.tflite| Mean: [127.0, 127.0, 127.0].<br>Input scale: [128.0].|68.0000000 drilling platform, offshore rig<br>38.0000000 container ship, containership, container vessel<br>14.0000000 lifeboat<br>13.0000000 fireboat<br>12.0000000 dock, dockage, docking facility|


### Other tasks

[TBD]

<!-- LINKS -->
[imagenet]: http://www.image-net.org
