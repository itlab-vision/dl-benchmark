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
resnet-50-pytorch | PyTorch | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
efficientnet-b0 | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
densenet-121-tf | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
googlenet-v1 | Caffe | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
googlenet-v4-tf | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
squeezenet1.1 | Caffe | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
resnet-50-pytorch | PyTorch | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
efficientnet-b0 | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
densenet-121-tf | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
googlenet-v1 | Caffe | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
googlenet-v4-tf | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
squeezenet1.1 | Caffe | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|

#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) |
-|-|-|-|-|-|
resnet-50-pytorch | PyTorch | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
efficientnet-b0 | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
densenet-121-tf | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
googlenet-v1 | Caffe | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
googlenet-v4-tf | TensorFlow | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|
squeezenet1.1 | Caffe | Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] |-|-|-|

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
