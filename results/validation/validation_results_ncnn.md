# Validation results for the models inferring using ncnn

## Image classification

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model|Python API|
---------------------|---------------------------|
shufflenetv2            |0.5396927 piggy bank, penny bank<br>0.0453512 saltshaker, salt shaker<br>0.0443007 whistle<br>0.0347720 ocarina, sweet potato<br>0.0286027 lemon|
squeezenet              |0.9628906 Granny Smith<br>0.0068016 lemon<br>0.0064964 fig<br>0.0046844 tennis ball<br>0.0038204 piggy bank, penny bank|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model|Python API|
---------------------|---------------------------|
shufflenetv2         |0.9906778 junco, snowbird<br>0.0034630 brambling, Fringilla montifringilla<br>0.0023069 house finch, linnet, Carpodacus mexicanus<br>0.0017143 chickadee<br>0.0006609 goldfinch, Carduelis carduelis|
squeezenet           |0.9804688 junco, snowbird<br>0.0173798 chickadee<br>0.0005875 jay<br>0.0003612 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003293 brambling, Fringilla montifringilla|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model|Python API|
---------------------|---------------------------|
shufflenetv2         |0.2229400 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2029892 liner, ocean liner<br>0.0577048 fireboat<br>0.0493575 dock, dockage, docking facility<br>0.0428826 container ship, containership, container vessel|
squeezenet           |0.8725586 lifeboat<br>0.0500183 container ship, containership, container vessel<br>0.0284729 drilling platform, offshore rig<br>0.0120697 pirate, pirate ship<br>0.0110016 dock, dockage, docking facility|

## Object detection

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00000247.JPEG">
</div>
Bounding box (upper left and bottom right corners):<br>
(117, 86), (365, 465)

Model|Python API|
----------------------|----------------------------------------|
faster_rcnn           | Bounding box:<br>(58, 141), (359, 484) |
mobilenet_ssd         | Bounding box:<br>(94, 93), (359, 481)  |
mobilenetv2_ssdlite   | Bounding box:<br>(76, 100), (347, 460) |
mobilenetv3_ssdlite   | Bounding box:<br>(61, 86), (365, 498)  |
mobilenet_yolov2      | Bounding box:<br>(72, 101), (341, 466) |
mobilenetv2_yolov3    | Bounding box:<br>(84, 92), (354, 473)  |
rfcn                  | Bounding box:<br>(93, 99), (334, 445)  |
squeezenet_ssd        | Bounding box:<br>(98, 103), (350, 449) |
yolov4_tiny           | Bounding box:<br>(74, 85), (243, 425)  |
yolov5s               | Bounding box:<br>(68, 96), (355, 490)  |
yolov8s               | Bounding box:<br>(59, 100), (352, 447) |

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00018592.JPEG">
</div>
Bounding box (upper left and bottom right corners):<br>
(82, 262), (269, 376)

Model|Python API|
----------------------|----------------------------------------|
faster_rcnn           | Bounding box:<br>(58, 180), (282, 418) |
mobilenet_ssd         | Bounding box:<br>(79, 140), (270, 375) |
mobilenetv2_ssdlite   | Bounding box:<br>(82, 265), (267, 376) |
mobilenetv3_ssdlite   | Bounding box:<br>(59, 112), (295, 414) |
mobilenet_yolov2      | Bounding box:<br>(54, 139), (277, 375) |
mobilenetv2_yolov3    | Bounding box:<br>(75, 127), (276, 390) |
rfcn                  | Bounding box:<br>(88, 138), (259, 381) |
squeezenet_ssd        | Bounding box:<br>(78, 149), (260, 357) |
yolov4_tiny           | Bounding box:<br>(96, 265), (244, 371) |
yolov5s               | Bounding box:<br>(81, 249), (267, 377) |
yolov8s               | Bounding box:<br>(82, 242), (269, 378) |

### Test image #3

Data source: [Pascal VOC][pascal_voc]

Image resolution: 500 x 375
﻿

<div style='float: center'>
<img width="500" src="images\2011_002352.jpg">
<img width="375" src="detection\out_yolo_detection.bmp">
</div>
Bounding box (upper left and bottom right corners):<br>
(62, 127), (443, 251)

Model|Python API|
----------------------|----------------------------------------|
faster_rcnn           | Bounding box:<br>(6, 94), (477, 257)   |
mobilenet_ssd         | Bounding box:<br>(54, 128), (447, 244) |
mobilenetv2_ssdlite   | Bounding box:<br>(61, 128), (435, 238) |
mobilenetv3_ssdlite   | Bounding box:<br>(37, 105), (295, 414) |
mobilenet_yolov2      | Bounding box:<br>(59, 112), (433, 239) |
mobilenetv2_yolov3    | Bounding box:<br>(62, 124), (427, 241) |
rfcn                  | Bounding box:<br>(46, 102), (436, 252) |
squeezenet_ssd        | Bounding box:<br>(47, 118), (458, 248) |
yolov4_tiny           | Bounding box:<br>(55, 124), (427, 241) |
yolov5s               | Bounding box:<br>(41, 118), (441, 245) |
yolov8s               | Bounding box:<br>(58, 122), (434, 243) |

<!-- LINKS -->
[imagenet]: http://www.image-net.org
[pascal_voc]: http://host.robots.ox.ac.uk/pascal/VOC
