# Validation results for the models inferring using Intel® Optimizations for TensorFlow

## Image classification

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Parameters | Python (implementation) |
-|-|-|
densenet-121-tf |Channel order: RGB.<br>Mean values - [123.68, 116.78, 103.94],<br>scale values - [58.395,57.12,57.375].|-|
efficientnet-b0 |Channel order: RGB.|-|
googlenet-v1-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v3 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v4-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
inception-resnet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mixnet-l|Channel order: RGB.|-|
mobilenet-v1-1.0-224-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v2-1.0-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v2-1.4-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v3-small-1.0-224-tf |Channel order is RGB.|-|
mobilenet-v3-large-1.0-224-tf |Channel order is RGB.|-|
resnet-50-tf |Channel order is RGB.|-|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
densenet-121-tf |Channel order: RGB.<br>Mean values - [123.68, 116.78, 103.94],<br>scale values - [58.395,57.12,57.375].|-|
efficientnet-b0 |Channel order: RGB.|-|
googlenet-v1-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v3 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v4-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
inception-resnet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mixnet-l|Channel order: RGB.|-|
mobilenet-v1-1.0-224-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v2-1.0-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v2-1.4-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v3-small-1.0-224-tf |Channel order is RGB.|-|
mobilenet-v3-large-1.0-224-tf |Channel order is RGB.|-|
resnet-50-tf |Channel order is RGB.|-|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python (implementation) |
-|-|-|
densenet-121-tf |Channel order: RGB.<br>Mean values - [123.68, 116.78, 103.94],<br>scale values - [58.395,57.12,57.375].|-|
efficientnet-b0 |Channel order: RGB.|-|
googlenet-v1-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v3 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
googlenet-v4-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
inception-resnet-v2-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mixnet-l|Channel order: RGB.|-|
mobilenet-v1-1.0-224-tf |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v2-1.0-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v2-1.4-224 |Channel order is RGB.<br>Mean values - [127.5, 127.5, 127.5],<br>scale value - 127.5.|-|
mobilenet-v3-small-1.0-224-tf |Channel order is RGB.|-|
mobilenet-v3-large-1.0-224-tf |Channel order is RGB.|-|
resnet-50-tf |Channel order is RGB.|-|

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

 Model | Python (implementation) |
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

 Model | Python (implementation) |
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

 Model | Python (implementation) |
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

 Model | Python (implementation) |
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

 Model | Python (implementation) |
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

 Model | Python (implementation) |
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

 Model | Python (implementation) |
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

 Model | Python (implementation) |
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
