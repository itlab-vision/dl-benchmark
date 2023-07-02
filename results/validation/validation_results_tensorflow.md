# Validation results for the models inferring using Intel® Optimizations for TensorFlow

## Image classification

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Parameters | Python API |
-|-|-|
densenet-121-tf |-|-|
efficientnet-b0 |-|-|
googlenet-v1-tf |-|-|
googlenet-v2-tf |-|-|
googlenet-v3 |-|-|
googlenet-v4-tf |-|-|
inception-resnet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|9.1747866 Granny Smith<br>4.0729303 pomegranate<br>3.7423978 orange<br>3.7375512 bell pepper<br>3.6937847 piggy bank, penny bank|
mixnet-l|-|-|
mobilenet-v1-1.0-224-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|0.1775393 necklace<br>0.1625960 saltshaker, salt shaker<br>0.0680758 pitcher, ewer<br>0.0600448 syringe<br>0.0574061 Granny Smith|
mobilenet-v2-1.0-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|0.8931151 Granny Smith<br>0.0335338 piggy bank, penny bank<br>0.0027360 saltshaker, salt shaker<br>0.0021255 vase<br>0.0016607 pitcher, ewer|
mobilenet-v2-1.4-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|0.7240402 Granny Smith<br>0.0312107 vase<br>0.0237109 fig<br>0.0122461 piggy bank, penny bank<br>0.0118888 saltshaker, salt shaker|
mobilenet-v3-small-1.0-224-tf |-|-|
mobilenet-v3-large-1.0-224-tf |-|-|
resnet-50-tf |Channel order is RGB.<br>Mean values - [123.68, 116.78, 103.94]|0.9553044 Granny Smith<br>0.0052123 lemon<br>0.0047184 piggy bank, penny bank<br>0.0045875 orange<br>0.0044232 necklace|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python API |
-|-|-|
densenet-121-tf |-|-|
efficientnet-b0 |-|-|
googlenet-v1-tf |-|-|
googlenet-v2-tf |-|-|
googlenet-v3 |-|-|
googlenet-v4-tf |-|-|
inception-resnet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|10.2994785 junco, snowbird<br>5.9667974 brambling, Fringilla montifringilla<br>3.8809638 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>3.7881403 house finch, linnet, Carpodacus mexicanus<br>3.4699843 goldfinch, Carduelis carduelis|
mixnet-l|-|-|
mobilenet-v1-1.0-224-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.| 0.9818491 junco, snowbird<br>0.0097170 house finch, linnet, Carpodacus mexicanus<br>0.0029993 brambling, Fringilla montifringilla<br>0.0022394 goldfinch, Carduelis carduelis<br>0.0022212 chickadee|
mobilenet-v2-1.0-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|0.8770270 junco, snowbird<br>0.0143872 water ouzel, dipper<br>0.0103318 chickadee<br>0.0063065 brambling, Fringilla montifringilla<br>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|
mobilenet-v2-1.4-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|0.6637316 junco, snowbird<br>0.0811651 chickadee<br>0.0119593 water ouzel, dipper<br>0.0038528 brambling, Fringilla montifringilla<br>0.0022498 goldfinch, Carduelis carduelis|
mobilenet-v3-small-1.0-224-tf |-|-|
mobilenet-v3-large-1.0-224-tf |-|-|
resnet-50-tf |Channel order is RGB.<br>Mean values - [123.68, 116.78, 103.94]|0.9983400 junco, snowbird<br>0.0004680 brambling, Fringilla montifringilla<br>0.0003848 chickadee<br>0.0003656 water ouzel, dipper<br>0.0003383 goldfinch, Carduelis carduelis|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python API |
-|-|-|
densenet-121-tf |-|-|
efficientnet-b0 |-|-|
googlenet-v1-tf |-|-|
googlenet-v2-tf |-|-|
googlenet-v3 |-|-|
googlenet-v4-tf |-|-|
inception-resnet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|6.6930799 fireboat<br>6.1025167 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.0896273 lifeboat<br>5.7389712 container ship, containership, container vessel<br>5.4940562 dock, dockage, docking facility|
mixnet-l|-|-|
mobilenet-v1-1.0-224-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.| 0.3759801 liner, ocean liner<br>0.1252522 lifeboat<br>0.1200093 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0882490 beacon, lighthouse, beacon light, pharos<br>0.0568063 fireboat|
mobilenet-v2-1.0-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|0.1885883 beacon, lighthouse, beacon light, pharos<br>0.1434043 liner, ocean liner<br>0.0768170 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0497303 drilling platform, offshore rig<br>0.0225758 container ship, containership, container vessel|
mobilenet-v2-1.4-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|0.1300134 container ship, containership, container vessel<br>0.0765783 lifeboat<br>0.0406071 dock, dockage, docking facility<br>0.0393021 drilling platform, offshore rig<br>0.0381023 liner, ocean liner|
mobilenet-v3-small-1.0-224-tf |Channel order is RGB.|-|
mobilenet-v3-large-1.0-224-tf |Channel order is RGB.|-|
resnet-50-tf |Channel order is RGB.<br>Mean values - [123.68, 116.78, 103.94]|0.2357705 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1480758 liner, ocean liner<br>0.1104694 container ship, containership, container vessel<br>0.1095414 drilling platform, offshore rig<br>0.0915567 beacon, lighthouse, beacon light, pharos|

## Object detection

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
<img width="150" src="detection\ILSVRC2012_val_00000023.JPEG"></img>
</div>
Bounding boxes (upper left and bottom right corners):<br>
(55, 155), (236, 375)<br>
(190, 190), (380, 400)<br>
(374, 209), (588, 422)<br>
(289, 111), (440, 255)<br>
(435, 160), (615, 310)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00000247.JPEG">
</div>
Bounding box (upper left and bottom right corners):<br>
(117, 86), (365, 465)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00018592.JPEG">
</div>
Bounding box (upper left and bottom right corners):<br>
(82, 262), (269, 376)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #4

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 480

<div style='float: center'>
<img width="300" src="images\9.jpg">
<img width="300" src="detection\faster_rcnn_out.bmp">
</div>
Bounding boxes (upper left and bottom right corners):<br>
TV (110, 41), (397, 304)<br>
MOUSE (508, 337), (559, 374)<br>
KEYBOARD (241, 342), (496, 461)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #5

Data source: [Pascal VOC][PASCAL_VOC_2012]

Image resolution: 500 x 375

<div style='float: center'>
<img width="300" src="images\2011_002352.jpg">
<img width="300" src="detection\python_yolo_voc_2011_002352.bmp">
</div>
Bounding box (upper left and bottom right corners):<br>
AEROPLANE (131, 21), (248, 414)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #6

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 427

<div style='float: center'>
<img width="300" src="images\000000367818.jpg">
<img width="300" src="detection\python_yolo_coco_000000367818.bmp">
</div>

Bounding boxes (upper left and bottom right corners):<br>
PERSON (86, 84), (394, 188)<br>
HORSE (44, 108), (397, 565)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

## Semantic segmentation

### Test image #1

Data source: -

Image resolution: -

Image: -

Segmented images are identical.

 Model | Python API |
-------|-------------------------|
deeplabv3|-|

## Instance segmentation

### Test image #1

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 480

Image:
<div style='float: center'>
<img width="300" src="images\22.jpg"></img>
</div>

Segmented images are identical.

 Model | Python API |
-------|-------------------------|
mask_rcnn_resnet50_atrous_coco|-|
mask_rcnn_inception_resnet_v2_atrous_coco|-|


Color map:

<div style='float: center'>
<img width="300" src="instance_segmentation\mscoco90_colormap.jpg">
</div>


<!-- LINKS -->
[imagenet]: http://www.image-net.org
[ms_coco]: http://cocodataset.org
[PASCAL_VOC_2012]: http://host.robots.ox.ac.uk/pascal/VOC/voc2012
