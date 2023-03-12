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
mobilenet-v1-1.0-224-tf|-|-|
mobilenet_v2_1.0_224|-|-|
mobilenet-v2-1.4-224|-|-|
inception-resnet-v2-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|8.0107708 Granny Smith<br>4.4552484 piggy bank, penny bank<br>4.2636762 bell pepper<br>3.9343853 candle, taper, wax light<br>3.5531902 pomegranate|

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
mobilenet-v1-1.0-224-tf|-|-|
mobilenet_v2_1.0_224|-|-|
mobilenet-v2-1.4-224|-|-|
inception-resnet-v2-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|10.0273972 junco, snowbird<br>4.6770372 brambling, Fringilla montifringilla<br>4.2079940 goldfinch, Carduelis carduelis<br>4.1425276 water ouzel, dipper<br>4.0244055 chickadee|

#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
mobilenet-v1-1.0-224-tf|-|-|
mobilenet_v2_1.0_224|-|-|
mobilenet-v2-1.4-224|-|-|
inception-resnet-v2-tf|Mean: [123.675,116.28,103.53].<br>Input scale: [58.395,57.12,57.375].|6.4228325 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.0842223 liner, ocean liner<br>5.8280630 fireboat<br>5.7098336 dock, dockage, docking facility<br>5.6666737 container ship, containership, container vessel|

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
lite-model_mobilenet_v1_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.7150755 Granny Smith<br>0.0202576 piggy bank, penny bank<br>0.0088377 teapot<br>0.0072254 bell pepper<br>0.0058900 banana|
lite-model_mobilenet_v2_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.6549551 Granny Smith<br>0.1130055 piggy bank, penny bank<br>0.0566443 teapot<br>0.0250644 saltshaker, salt shaker<br>0.0120769 vase|
lite-model_mobilenet_v3_small_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.5426094 Granny Smith<br>0.0725947 teapot<br>0.0285967 piggy bank, penny bank<br>0.0269885 pitcher, ewer<br>0.0195926 vase|
lite-model_mobilenet_v3_large_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.8494291 Granny Smith<br>0.0085453 piggy bank, penny bank<br>0.0069065 lemon<br>0.0055464 tennis ball<br>0.0027605 pomegranate|
efficientnet_lite0_fp32_2.tflite|-|-|
efficientnet_lite1_fp32_2.tflite|-|-|
efficientnet_lite2_fp32_2.tflite|-|-|
efficientnet_lite3_fp32_2.tflite|-|-|
efficientnet_lite4_fp32_2.tflite|-|-|

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
lite-model_mobilenet_v1_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].| 0.8584890 junco, snowbird<br>0.0235178 brambling, Fringilla montifringilla<br>0.0185745 goldfinch, Carduelis carduelis<br>0.0094353 water ouzel, dipper<br>0.0067247 chickadee|
lite-model_mobilenet_v2_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.8474838 junco, snowbird<br>0.0402333 chickadee<br>0.0112412 brambling, Fringilla montifringilla<br>0.0056867 water ouzel, dipper<br>0.0020902 goldfinch, Carduelis carduelis|
lite-model_mobilenet_v3_small_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].| 0.6117089 junco, snowbird<br>0.0544940 chickadee<br>0.0274826 goldfinch, Carduelis carduelis<br>0.0213195 water ouzel, dipper<br>0.0100568 brambling, Fringilla montifringilla|
lite-model_mobilenet_v3_large_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.6303865 junco, snowbird<br>0.0645584 brambling, Fringilla montifringilla<br>0.0283644 goldfinch, Carduelis carduelis<br>0.0097315 chickadee<br>0.0092374 water ouzel, dipper|
efficientnet_lite0_fp32_2.tflite|-|-|
efficientnet_lite1_fp32_2.tflite|-|-|
efficientnet_lite2_fp32_2.tflite|-|-|
efficientnet_lite3_fp32_2.tflite|-|-|
efficientnet_lite4_fp32_2.tflite|-|-|

#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
lite-model_mobilenet_v1_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.1904013 liner, ocean liner<br>0.0967771 lifeboat<br>0.0881745 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0482143 beacon, lighthouse, beacon light, pharos<br>0.0478232 catamaran|
lite-model_mobilenet_v2_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.0606234 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0568781 container ship, containership, container vessel<br>0.0518561 lifeboat<br>0.0431800 beacon, lighthouse, beacon light, pharos<br>0.0337389 drilling platform, offshore rig|
lite-model_mobilenet_v3_small_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.0724729 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0653515 drilling platform, offshore rig<br>0.0644393 liner, ocean liner<br>0.0580560 container ship, containership, container vessel<br>0.0499799 beacon, lighthouse, beacon light, pharos|
lite-model_mobilenet_v3_large_100_224_fp32_1.tflite|Mean: [127.5,127.5,127.5].<br>Input scale: [127.5,127.5,127.5].|0.2661534 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0744180 beacon, lighthouse, beacon light, pharos<br>0.0523450 container ship, containership, container vessel<br>0.0406797 pirate, pirate ship<br>0.0398768 aircraft carrier, carrier, flattop, attack aircraft carrier|
efficientnet_lite0_fp32_2.tflite|-|-|
efficientnet_lite1_fp32_2.tflite|-|-|
efficientnet_lite2_fp32_2.tflite|-|-|
efficientnet_lite3_fp32_2.tflite|-|-|
efficientnet_lite4_fp32_2.tflite|-|-|

### Other tasks

[TBD]

<!-- LINKS -->
[imagenet]: http://www.image-net.org
