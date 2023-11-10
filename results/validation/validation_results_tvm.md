# Validation results for the models inferring using TVM

## Public models (Open Model Zoo)

### Image classification

#### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
densenet-121-tf | TensorFlow | Mean: [123.68,116.78,103.94]<br>Std: [58.395,57.12,57.375] | 0.9525882 Granny Smith<br>0.0132317 orange<br>0.0123400 lemon<br>0.0028143 banana<br>0.0020237 piggy bank, penny bank |-|-|
efficientnet-b0 | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] | 10733.9218750 Granny Smith<br>9574.2392578 pomegranate<br>8067.0537109 hip, rose hip, rosehip<br>7369.9067383 brambling, Fringilla montifringilla<br>7041.4887695 ptarmigan |-|-|
googlenet-v1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0] |  0.9979934 Granny Smith<br>0.0007394 bell pepper<br>0.0006985 candle, taper, wax light<br>0.0000942 tennis ball<br>0.0000636 cucumber, cuke |-|-|
googlenet-v4-tf | TensorFlow | Mean: [127.5,127.5,127.5]<br>Std: [127.5,127.5,127.5] | 0.9935190 Granny Smith<br>0.0002230 Rhodesian ridgeback<br>0.0000956 pineapple, ananas<br>0.0000868 hair slide<br>0.0000775 banana |-|-|
resnet-50-pytorch | PyTorch | Source framework<br>Mean: [123.675,116.28,103.53]<br>Std: [58.395,57.12,57.375]<br><br>Inference framework<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229, 0.224, 0.225] | 0.9278084 Granny Smith<br>0.0129410 orange<br>0.0059574 lemon<br>0.0042141 necklace<br>0.0025712 banana | 0.0135990 Granny Smith<br>0.0001897 orange<br>0.0000873 lemon<br>0.0000618 necklace<br>0.0000377 banana|-|
squeezenet1.1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0] | 0.9993550 Granny Smith<br>0.0004808 tennis ball<br>0.0000693 fig<br>0.0000318 lemon<br>0.0000192 piggy bank, penny bank |-|-|

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
densenet-121-tf | TensorFlow | Mean: [123.68,116.78,103.94]<br>Std: [58.395,57.12,57.375] | 0.9847540 junco, snowbird<br>0.0068680 chickadee<br>0.0034511 brambling, Fringilla montifringilla<br>0.0015685 water ouzel, dipper<br>0.0012343 indigo bunting, indigo finch, indigo bird, Passerina cyanea |-|-|
efficientnet-b0 | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] | 2070.9409180 can opener, tin opener<br>1669.3304443 strawberry<br>1631.1007080 packet<br>1586.7080078 bell pepper<br>1466.7904053 clog, geta, patten, sabot |-|-|
googlenet-v1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0] | 0.9999735 junco, snowbird<br>0.0000203 chickadee<br>0.0000020 brambling, Fringilla montifringilla<br>0.0000016 house finch, linnet, Carpodacus mexicanus<br>0.0000016 water ouzel, dipper |-|-|
googlenet-v4-tf | TensorFlow | Mean: [127.5,127.5,127.5]<br>Std: [127.5,127.5,127.5] | 0.9398882 junco, snowbird<br>0.0005928 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005351 chickadee<br>0.0005287 brambling, Fringilla montifringilla<br>0.0004131 house finch, linnet, Carpodacus mexicanus|-|-|
resnet-50-pytorch | PyTorch | Source framework<br>Mean: [123.675,116.28,103.53]<br>Std: [58.395,57.12,57.375]<br><br>Inference framework<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229, 0.224, 0.225] | 0.9805019 junco, snowbird<br>0.0049154 goldfinch, Carduelis carduelis<br>0.0039196 chickadee<br>0.0038097 water ouzel, dipper<br>0.0028983 brambling, Fringilla montifringilla | 0.9474856 junco, snowbird<br>0.0047499 goldfinch, Carduelis carduelis<br>0.0037876 chickadee<br>0.0036815 water ouzel, dipper<br>0.0028008 brambling, Fringilla montifringilla |-|
squeezenet1.1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0] | 0.9897482 junco, snowbird<br>0.0094914 chickadee<br>0.0003794 brambling, Fringilla montifringilla<br>0.0002046 jay<br>0.0001124 indigo bunting, indigo finch, indigo bird, Passerina cyanea |-|-|

#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
densenet-121-tf | TensorFlow | Mean: [123.68,116.78,103.94]<br>Std: [58.395,57.12,57.375] | 0.3048036 liner, ocean liner<br>0.1327114 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1180263 container ship, containership, container vessel<br>0.0794732 drilling platform, offshore rig<br>0.0718437 dock, dockage, docking facility |-|-|
efficientnet-b0 | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] | 33649.5468750 bow tie, bow-tie, bowtie<br>28028.8417969 cannon<br>20405.7363281 stole<br>20352.2265625 seat belt, seatbelt<br>19862.9375000 picket fence, paling |-|-|
googlenet-v1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0] | 0.4644058 lifeboat<br>0.2018610 drilling platform, offshore rig<br>0.0871761 container ship, containership, container vessel<br>0.0759982 liner, ocean liner<br>0.0714861 beacon, lighthouse, beacon light, pharos |-|-|
googlenet-v4-tf | TensorFlow | Mean: [127.5,127.5,127.5]<br>Std: [127.5,127.5,127.5] | 0.4689647 beacon, lighthouse, beacon light, pharos<br>0.1695168 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0433668 lifeboat<br>0.0310355 fireboat<br>0.0150613 dock, dockage, docking facility |-|-|
resnet-50-pytorch | PyTorch | Source framework<br>Mean: [123.675,116.28,103.53]<br>Std: [58.395,57.12,57.375]<br><br>Inference framework<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229, 0.224, 0.225] | 0.4759621 liner, ocean liner<br>0.1025402 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0690002 container ship, containership, container vessel<br>0.0524496 dock, dockage, docking facility<br>0.0473782 pirate, pirate ship | 0.0020742 liner, ocean liner<br>0.0004469 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0003007 container ship, containership, container vessel<br>0.0002286 dock, dockage, docking facility<br>0.0002065 pirate, pirate ship |-|
squeezenet1.1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0] | 0.5661172 lifeboat<br>0.2700349 drilling platform, offshore rig<br>0.0876362 liner, ocean liner<br>0.0250453 container ship, containership, container vessel<br>0.0135069 submarine, pigboat, sub, U-boat |-|-|

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

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
yolo-v3-onnx | ONNX |-|-|-|-|
ssdlite_mobilenet_v2 | TensorFlow |-|-|-|-|

**Note**: ssd_mobilenet_v2 is not available.

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

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
yolo-v3-onnx | ONNX |-|-|-|-|
ssdlite_mobilenet_v2 | TensorFlow |-|-|-|-|

**Note**: ssd_mobilenet_v2 is not available.

### Test image #3

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 427


<div style='float: center'>
<img width="300" src="images\000000367818.jpg">
<img width="300" src="detection\python_yolo_coco_000000367818.bmp">
</div>
Bounding box (upper left and bottom right corners):<br>PERSON (86, 84), (394, 188)<br>HORSE (44, 108), (397, 565)<br>


Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
yolo-v3-onnx | ONNX |-|-|-|-|
ssdlite_mobilenet_v2 | TensorFlow |-|-|-|-|

**Note**: ssd_mobilenet_v2 is not available.

## Face localization

### Test image #1

Data source: [WIDER FACE Dataset][wider_face_dataset]

Image resolution: 1024 x 768

<div style='float: center'>
<img width="300" src="images\Meeting_294.jpg">
<img width="300" height="225" src="images\Meeting_294_bounding.bmp">
</div>

Bounding box (upper left and bottom right corners):<br>(170, 124), (235, 208)<br>(775, 133), (841, 226)<br>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
retinaface-resnet50-pytorch |PyTorch |-|-|-|-|

### Test image #2

Data source: XXX

Image resolution: XXX x XXX
﻿
Bounding box (upper left and bottom right corners): (XX,XX), (XX,XX)

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
retinaface-resnet50-pytorch |PyTorch |-|-|-|-|

### Test image #3

Data source: XXX

Image resolution: XXX x XXX
﻿
Bounding box (upper left and bottom right corners): (XX,XX), (XX,XX)

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
retinaface-resnet50-pytorch |PyTorch |-|-|-|-|


<!-- LINKS -->
[imagenet]: http://www.image-net.org
[ms_coco]: http://cocodataset.org
[wider_face_dataset]: http://shuoyang1213.me/WIDERFACE
