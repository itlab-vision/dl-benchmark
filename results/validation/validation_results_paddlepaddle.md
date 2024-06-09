# Validation results for the models inferring using PaddlePaddle

## Image classification

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Parameters | Python API |
-|-|-|
resnet-50 |Mean values - [123.675,116.28,103.53],<br>scale value - [58.395,57.12,57.375]|0.9931559 Granny Smith<br>0.0009120 piggy bank, penny bank<br>0.0007721 bell pepper<br>0.0007689 tennis ball<br>0.0005548 candle, taper, wax light|
PPLCNet_x1_0_infer |Mean values - [123.675,116.28,103.53],<br>scale value - [58.395,57.12,57.375]|0.2785943 Granny Smith<br>0.2241544 piggy bank, penny bank<br>0.0404602 saltshaker, salt shaker<br>0.0131707 soap dispenser<br>0.0114298 lemon
|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python API |
-|-|-|
resnet-50 |Mean values - [123.675,116.28,103.53],<br>scale value - [58.395,57.12,57.375]|0.9891654 junco, snowbird<br>0.0044086 chickadee<br>0.0033522 water ouzel, dipper<br>0.0014910 brambling, Fringilla montifringilla<br>0.0003624 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
PPLCNet_x1_0_infer |Mean values - [123.675,116.28,103.53],<br>scale value - [58.395,57.12,57.375]|0.8259031 junco, snowbird<br>0.0340593 brambling, Fringilla montifringilla<br>0.0055266 chickadee<br>0.0050722 house finch, linnet, Carpodacus mexicanus<br>0.0034595 bulbul|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python API |
-|-|-|
resnet-50 |Mean values - [123.675,116.28,103.53],<br>scale value - [58.395,57.12,57.375]|0.3656897 liner, ocean liner<br>0.1008371 container ship, containership, container vessel<br>0.0759774 dock, dockage, docking facility<br>0.0707850 lifeboat<br>0.0556011 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
PPLCNet_x1_0_infer |Mean values - [123.675,116.28,103.53],<br>scale value - [58.395,57.12,57.375]|0.1249109 submarine, pigboat, sub, U-boat<br>0.1198353 breakwater, groin, groyne, mole, bulwark, seawall, jetty <br>0.0568103 liner, ocean liner<br>0.0351734 lifeboat<br>0.0326451 dock, dockage, docking facility|

<!-- LINKS -->
[imagenet]: http://www.image-net.org
[ms_coco]: http://cocodataset.org
[PASCAL_VOC_2012]: http://host.robots.ox.ac.uk/pascal/VOC/voc2012
