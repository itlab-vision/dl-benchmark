# Validation results for the models inferring using Intel® Optimization for TensorFlow

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
densenet-121-tf              |0.9885473 Granny Smith<br>0.0030248 lemon<br>0.0019818 orange<br>0.0019432 water jug<br>0.0009727 piggy bank, penny bank|
densenet-161-tf              |0.9881073 Granny Smith<br>0.0024773 dumbbell<br>0.0022064 pitcher, ewer<br>0.0009395 piggy bank, penny bank<br>0.0007298 lemon|
densenet-169-tf              |0.9990545 Granny Smith<br>0.0003095 orang<br>0.0002806 lemon<br>0.0001069 banana<br>0.0000673 piggy bank, penny bank|
efficientnet-b0              |10.7337675 Granny Smith<br>4.8936925 lemon<br>4.3447943 bell pepper<br>4.3027472 orange<br>4.2535534 piggy bank, penny bank|
efficientnet-b0_auto_aug     |10.5565243 Granny Smith<br>5.3122606 lemon<br>5.1323676 pomegranate<br>5.0744419 orange<br>4.8147378 pitcher, ewer|
efficientnet-b5              |9.5746241 Granny Smith<br>5.8361979 tennis ball<br>5.3556395 pitcher, ewer<br>4.7100096 vase<br>3.9722917 lemon|
efficientnet-b7_auto_aug     |6.3890204 Granny Smith<br>5.7521944 orange<br>4.6920619 dumbbell<br>4.5902743 mouse, computer mouse<br>4.4482408 wooden spoon|
googlenet-v1-tf              |0.6735924 Granny Smith<br>0.0737857 piggy bank, penny bank<br>0.0155380 vase<br>0.0154004 pitcher, ewer<br>0.0136553 saltshaker, salt shaker|
googlenet-v4-tf              |0.9934986 Granny Smith<br>0.0002234 Rhodesian ridgeback<br>0.0000959 pineapple, ananas<br>0.0000871 hair slide<br>0.0000778 banana|
inception-resnet-v2-tf       |9.1747961 Granny Smith<br>4.0729275 pomegranate<br>3.7423992 orange<br>3.7375555 bell pepper<br>3.6937809 piggy bank, penny bank|
mobilenet-v1-0.25-128        |0.3148140 hair slide<br>0.1282437 bell pepper<br>0.1186993 screw<br>0.0637675 piggy bank, penny bank<br>0.0498881 necklace|
mobilenet-v1-0.50-160        |0.3811020 Granny Smith<br>0.1881481 dumbbell<br>0.0740855 bell pepper<br>0.0498609 teapot<br>0.0485965 vase|
mobilenet-v1-0.50-224        |0.1766144 piggy bank, penny bank<br>0.1696908 hair slide<br>0.0947144 pitcher, ewer<br>0.0688121 dumbbell<br>0.0623832 vase|
mobilenet-v1-1.0-224-tf      |0.1770520 necklace<br>0.1632517 saltshaker, salt shaker<br>0.0681067 pitcher, ewer<br>0.0600439 syringe<br>0.0570383 Granny Smith|
mobilenet-v2-1.0-224         |0.8931143 Granny Smith<br>0.0335342 piggy bank, penny bank<br>0.0027360 saltshaker, salt shaker<br>0.0021255 vase<br>0.0016607 pitcher, ewer|
mobilenet-v2-1.4-224         |0.7240415 Granny Smith<br>0.0312107 vase<br>0.0237108 fig<br>0.0122461 piggy bank, penny bank<br>0.0118887 saltshaker, salt shaker|
resnet-50-tf                 |0.9553046 Granny Smith<br>0.0052122 lemon<br>0.0047184 piggy bank, penny bank<br>0.0045874 orange<br>0.0044232 necklace|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
densenet-121-tf              |0.9993927 junco, snowbird<br>0.0003457 brambling, Fringilla montifringilla<br>0.0000980 chickadee<br>0.0000902 water ouzel, dipper<br>0.0000305 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
densenet-161-tf              |0.9974313 junco, snowbird<br>0.0012504 chickadee<br>0.0005084 brambling, Fringilla montifringilla<br>0.0004443 water ouzel, dipper<br>0.0001865 goldfinch, Carduelis carduelis|
densenet-169-tf              |0.9996991 junco, snowbird<br>0.0001647 brambling, Fringilla montifringilla<br>0.0000364 chickadee<br>0.0000344 water ouzel, dipper<br>0.0000279 house finch, linnet, Carpodacus mexicanus|
efficientnet-b0              |7.7920876 junco, snowbird<br>5.7337279 chickadee<br>5.4845705 water ouzel, dipper<br>3.9789367 brambling, Fringilla montifringilla<br>3.1936724 bulbul|
efficientnet-b0_auto_aug     |8.0755911 junco, snowbird<br>5.0325661 brambling, Fringilla montifringilla<br>4.7968502 goldfinch, Carduelis carduelis<br>4.3766956 chickadee<br>3.6982734 house finch, linnet, Carpodacus mexicanus|
efficientnet-b5              |8.3428783 junco, snowbird<br>7.0666609 chickadee<br>6.5433202 brambling, Fringilla montifringilla<br>6.4925141 house finch, linnet, Carpodacus mexicanus<br>5.4472694 water ouzel, dipper|
efficientnet-b7_auto_aug     |7.6459508 junco, snowbird<br>4.7702551 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>4.3635335 chickadee<br>3.9429338 goldfinch, Carduelis carduelis<br>3.7415361 house finch, linnet, Carpodacus mexicanus|
googlenet-v1-tf              |0.7443165 junco, snowbird<br>0.0474523 brambling, Fringilla montifringilla<br>0.0457435 chickadee<br>0.0213393 goldfinch, Carduelis carduelis<br>0.0085103 house finch, linnet, Carpodacus mexicanus|
googlenet-v4-tf              |0.9399367 junco, snowbird<br>0.0005925 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005340 chickadee<br>0.0005273 brambling, Fringilla montifringilla<br>0.0004121 house finch, linnet, Carpodacus mexicanus|
inception-resnet-v2-tf       |10.2994804 junco, snowbird<br>5.9667954 brambling, Fringilla montifringilla<br>3.8809619 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>3.7881384 house finch, linnet, Carpodacus mexicanus<br>3.4699864 goldfinch, Carduelis carduelis|
mobilenet-v1-0.25-128        |0.8267632 junco, snowbird<br>0.1118992 brambling, Fringilla montifringilla<br>0.0212946 chickadee<br>0.0206253 house finch, linnet, Carpodacus mexicanus<br>0.0116233 hummingbird|
mobilenet-v1-0.50-160        |0.8118837 junco, snowbird<br>0.0478476 goldfinch, Carduelis carduelis<br>0.0369896 house finch, linnet, Carpodacus mexicanus<br>0.0323185 chickadee<br>0.0233682 brambling, Fringilla montifringilla|
mobilenet-v1-0.50-224        |0.8732808 junco, snowbird<br>0.1154338 chickadee<br>0.0051305 brambling, Fringilla montifringilla<br>0.0046064 goldfinch, Carduelis carduelis<br>0.0009232 jay|
mobilenet-v1-1.0-224-tf      |0.9816355 junco, snowbird<br>0.0098165 house finch, linnet, Carpodacus mexicanus<br>0.0030193 brambling, Fringilla montifringilla<br>0.0022969 goldfinch, Carduelis carduelis<br>0.0022402 chickadee|
mobilenet-v2-1.0-224         |0.8770279 junco, snowbird<br>0.0143870 water ouzel, dipper<br>0.0103317 chickadee<br>0.0063064 brambling, Fringilla montifringilla<br>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|
mobilenet-v2-1.4-224         |0.6637309 junco, snowbird<br>0.0811652 chickadee<br>0.0119593 water ouzel, dipper<br>0.0038528 brambling, Fringilla montifringilla<br>0.0022499 goldfinch, Carduelis carduelis|
resnet-50-tf                 |0.9983401 junco, snowbird<br>0.0004680 brambling, Fringilla montifringilla<br>0.0003848 chickadee<br>0.0003656 water ouzel, dipper<br>0.0003383 goldfinch, Carduelis carduelis|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
densenet-121-tf              |0.3662359 liner, ocean liner<br>0.1080203 dock, dockage, docking facility<br>0.0820107 container ship, containership, container vessel<br>0.0713347 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0661764 fireboat|
densenet-161-tf              |0.3889844 lifeboat<br>0.3597548 liner, ocean liner<br>0.0605916 fireboat<br>0.0416730 dock, dockage, docking facility<br>0.0313890 container ship, containership, container vessel|
densenet-169-tf              |0.5010954 drilling platform, offshore rig<br>0.2035182 beacon, lighthouse, beacon light, pharos<br>0.0995142 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0897753 container ship, containership, container vessel<br>0.0466828 dock, dockage, docking facility|
efficientnet-b0              |6.3308659 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>5.6206503 beacon, lighthouse, beacon light, pharos<br>5.5816398 liner, ocean liner<br>5.2046580 submarine, pigboat, sub, U-boat<br>5.1616120 lifeboat|
efficientnet-b0_auto_aug     |7.0502687 lifeboat<br>6.0182433 fireboat<br>5.9369097 liner, ocean liner<br>5.5068717 container ship, containership, container vessel<br>5.3998508 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
efficientnet-b5              |6.4243660 nipple<br>5.5631447 swab, swob, mop<br>4.7420931 airliner<br>4.5451503 liner, ocean liner<br>4.0300856 space shuttle|
efficientnet-b7_auto_aug     |7.1823297 container ship, containership, container vessel<br>7.0720334 liner, ocean liner<br>5.0527415 electric guitar<br>4.5502715 catamaran<br>4.4502201 dock, dockage, docking facility|
googlenet-v1-tf              |0.1235984 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1017590 liner, ocean liner<br>0.0949447 drilling platform, offshore rig<br>0.0817945 container ship, containership, container vessel<br>0.0486890 fireboat|
googlenet-v4-tf              |0.4704956 beacon, lighthouse, beacon light, pharos<br>0.1695946 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0431099 lifeboat<br>0.0307508 fireboat<br>0.0149647 dock, dockage, docking facility|
inception-resnet-v2-tf       |6.6930823 fireboat<br>6.1025157 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.0896254 lifeboat<br>5.7389703 container ship, containership, container vessel<br>5.4940562 dock, dockage, docking facility|
mobilenet-v1-0.25-128        |0.2227534 liner, ocean liner<br>0.1206202 fireboat<br>0.1096154 pirate, pirate ship<br>0.0837730 water bottle<br>0.0468026 container ship, containership, container vessel|
mobilenet-v1-0.50-160        |0.5597361 container ship, containership, container vessel<br>0.2121089 liner, ocean liner<br>0.0326798 beacon, lighthouse, beacon light, pharos<br>0.0295495 lifeboat<br>0.0271855 dock, dockage, docking facility|
mobilenet-v1-0.50-224        |0.2392185 container ship, containership, container vessel<br>0.2232826 liner, ocean liner<br>0.1719750 lifeboat<br>0.0960151 fireboat<br>0.0550007 speedboat|
mobilenet-v1-1.0-224-tf      |0.3753887 liner, ocean liner<br>0.1239904 lifeboat<br>0.1208328 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0891690 beacon, lighthouse, beacon light, pharos<br>0.0568047 fireboat|
mobilenet-v2-1.0-224         |0.1885899 beacon, lighthouse, beacon light, pharos<br>0.1434040 liner, ocean liner<br>0.0768168 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0497302 drilling platform, offshore rig<br>0.0225758 container ship, containership, container vessel|
mobilenet-v2-1.4-224         |0.1300138 container ship, containership, container vessel<br>0.0765785 lifeboat<br>0.0406071 dock, dockage, docking facility<br>0.0393022 drilling platform, offshore rig<br>0.0381023 liner, ocean liner|
resnet-50-tf                 |0.2357707 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1480755 liner, ocean liner<br>0.1104696 container ship, containership, container vessel<br>0.1095414 drilling platform, offshore rig<br>0.0915570 beacon, lighthouse, beacon light, pharos|

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

   Model              |  Python (implementation)         |
----------------------|----------------------------------|
mobilenet-ssd         | Bounding box:<br>(46, 133), (657, 445)<br>  |
ssd300                | Bounding box:<br>(66, 163), (235, 356)<br> |
ssd512                | Bounding boxes:<br>(65, 168), (256, 343);<br>(378, 167), (592, 424)<br>|


    Model             |  Python (implementation)  |
----------------------|---------------------------|
ssd_mobilenet_v1_coco | Bounding box:<br>(385, 211), (597, 420)<br> |
ssd_mobilenet_v2_coco | Bounding box:<br>(378, 212), (607, 428)<br> |
ssd_mobilenet_v1_fpn_coco | Bounding boxes:<br>(294, 132), (439, 288);<br>(375, 217), (580, 425);<br>(437, 150), (610, 299)<br>|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500

Image:
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>
Detected objects:
<div style='float: center'>
<img width="150" src="detection\ILSVRC2012_val_00000247.JPEG">
</div>

Bounding box (upper left and bottom right corners):<br>
(117, 86), (365, 465)

    Model             |  Python (implementation)  |
----------------------|---------------------------|
ssd_mobilenet_v1_coco | Bounding box: (83, 114), (362, 424) |
ssd_mobilenet_v2_coco | Bounding box: (89, 98), (359, 446) |
ssd_mobilenet_v1_fpn_coco | Bounding box: (92, 101), (350, 419) |

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500

Image:
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>
Detected objects:
<div style='float: center'>
<img width="150" src="detection\ILSVRC2012_val_00018592.JPEG">
</div>

Bounding box (upper left and bottom right corners):<br>
(82, 262), (269, 376)

    Model             |  Python (implementation)  |
----------------------|---------------------------|
ssd_mobilenet_v1_coco | Bounding box: (87, 143), (263, 372) |
ssd_mobilenet_v2_coco | Bounding box: (83, 147), (265, 377) |
ssd_mobilenet_v1_fpn_coco | Bounding box: (92, 136), (261, 371) |

### Test image #4

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 480

Image:
<div style='float: center'>
<img width="300" src="images\9.jpg">
</div>
Detected objects:
<div style='float: center'>
<img width="300" src="detection\faster_rcnn_out.bmp">
</div>

Bounding boxes (upper left and bottom right corners):<br>
TV (110, 41), (397, 304)<br>
MOUSE (508, 337), (559, 374)<br>
KEYBOARD (241, 342), (496, 461)<br>

    Model             |  Python (implementation)  |
----------------------|---------------------------|
faster_rcnn_inception_resnet_v2_atrous_coco | Bounding boxes: TV (104, 38), (396, 307); MOUSE (508, 337), (559, 373); KEYBOARD (239, 343), (495, 462); DINING TABLE (22, 230), (621, 477) |
faster_rcnn_inception_v2_coco | Bounding boxes: TV (101, 25), (401, 306); FRISBEE (508, 338), (561, 378); KEYBOARD (228, 347),(498, 463) |
faster_rcnn_resnet50_coco | Bounding boxes: TV (94, 15), (413, 290); MOUSE (510, 337), (564, 375); KEYBOARD (240, 339), (514, 468); MICROWAVE (51, 0), (415, 299) |
faster_rcnn_resnet101_coco | Bounding boxes: TV (98, 39), (401, 301); MOUSE (507, 336), (562, 374); KEYBOARD (233, 340), (502, 467) |

### Test image #5

Data source: [Pascal VOC][PASCAL_VOC_2012]

Image resolution: 500 x 375

Image:
<div style='float: center'>
<img width="300" src="images\2011_002352.jpg">
</div>
Detected objects:
<div style='float: center'>
<img width="300" src="detection\python_yolo_voc_2011_002352.bmp">
</div>

Bounding box (upper left and bottom right corners):<br>
AEROPLANE (131, 21), (248, 414)<br>

    Model             |  Python (implementation)  |
----------------------|---------------------------|
yolo-v1-tiny-tf       | Bounding box: AEROPLANE (113, 20), (252, 488) |

### Test image #6

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 427

Image:
<div style='float: center'>
<img width="300" src="images\000000367818.jpg">
</div>
Detected objects:
<div style='float: center'>
<img width="300" src="detection\python_yolo_coco_000000367818.bmp">
</div>

Bounding boxes (upper left and bottom right corners):<br>
PERSON (86, 84), (394, 188)<br>
HORSE (44, 108), (397, 565)<br>

    Model             |  Python (implementation)  |
----------------------|---------------------------|
yolo-v2-tf | Bounding boxes: PERSON (51, 117), (381, 535); HORSE (53, 90), (413, 201)|
yolo-v2-tiny-tf | Bounding box: HORSE (75, 59), (405, 586) |
yolo-v3-tf | Bounding boxes: PERSON (66, 87), (413, 195); HORSE (54, 131), (386, 534) |

## Instance segmentation

### Test image #1

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 480

Image:
<div style='float: center'>
<img width="300" src="images\22.jpg"></img>
</div>

Segmented images are identical.

    Model             |  Python (implementation)  |
----------------------|---------------------------|
mask_rcnn_inception_resnet_v2_atrous_coco | <div style='float: center'><img width="300" src="instance_segmentation\python_sync_22_mask_rcnn_inception_resnet_v2_atrous_coco.bmp"></img></div> |
mask_rcnn_inception_v2_coco | <div style='float: center'><img width="300" src="instance_segmentation\python_sync_22_mask_rcnn_inception_v2_coco.bmp"></img></div> |
mask_rcnn_resnet50_atrous_coco | <div style='float: center'><img width="300" src="instance_segmentation\python_sync_22_mask_rcnn_resnet50_atrous_coco.bmp"></img></div> |
mask_rcnn_resnet101_atrous_coco | <div style='float: center'><img width="300" src="instance_segmentation\python_sync_22_mask_rcnn_resnet101_atrous_coco.bmp"></img></div> |


Color map:

<div style='float: center'>
<img width="300" src="instance_segmentation\mscoco90_colormap.jpg">
</div>


<!-- LINKS -->
[imagenet]: http://www.image-net.org
[ms_coco]: http://cocodataset.org
[PASCAL_VOC_2012]: http://host.robots.ox.ac.uk/pascal/VOC/voc2012
