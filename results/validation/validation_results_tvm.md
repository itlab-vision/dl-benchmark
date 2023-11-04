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

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
resnet-50-pytorch | PyTorch |-|-|-|
efficientnet-b0 | TensorFlow |-|-|-|
densenet-121-tf | TensorFlow |-|-|-|
googlenet-v1 | Caffe |-|-|-|
googlenet-v4-tf | TensorFlow |-|-|-|
squeezenet1.1 | Caffe |-|-|-|

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
resnet-50-pytorch | PyTorch |-|-|-|
efficientnet-b0 | TensorFlow |-|-|-|
densenet-121-tf | TensorFlow |-|-|-|
googlenet-v1 | Caffe |-|-|-|
googlenet-v4-tf | TensorFlow |-|-|-|
squeezenet1.1 | Caffe |-|-|-|

#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
resnet-50-pytorch | PyTorch |-|-|-|
efficientnet-b0 | TensorFlow |-|-|-|
densenet-121-tf | TensorFlow |-|-|-|
googlenet-v1 | Caffe |-|-|-|
googlenet-v4-tf | TensorFlow |-|-|-|
squeezenet1.1 | Caffe |-|-|-|

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

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
yolo-v3-onnx | ONNX |-|-|-|
ssdlite_mobilenet_v2 | TensorFlow |-|-|-|

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

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
yolo-v3-onnx | ONNX |-|-|-|
ssdlite_mobilenet_v2 | TensorFlow |-|-|-|

**Note**: ssd_mobilenet_v2 is not available.

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00018592.JPEG">
</div>
Bounding box (upper left anf bottom right corners):<br>
(82,262), (269,376)

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
yolo-v3-onnx | ONNX |-|-|-|
ssdlite_mobilenet_v2 | TensorFlow |-|-|-|

**Note**: ssd_mobilenet_v2 is not available.

## Face localization

### Test image #1

Data source: XXX

Image resolution: XXX x XXX
﻿
Bounding box (upper left anf bottom right corners):<br>
(XX,XX), (XX,XX)

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
retinaface-resnet50-pytorch |PyTorch |-|-|-|

### Test image #2

Data source: XXX

Image resolution: XXX x XXX
﻿
Bounding box (upper left anf bottom right corners):<br>
(XX,XX), (XX,XX)

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
retinaface-resnet50-pytorch |PyTorch |-|-|-|

### Test image #3

Data source: XXX

Image resolution: XXX x XXX
﻿
Bounding box (upper left anf bottom right corners):<br>
(XX,XX), (XX,XX)

Model | Source Framework | Parameters | Python API (source format) | Python API (TVM format) |
-|-|-|-|-|
retinaface-resnet50-pytorch |PyTorch |-|-|-|


<!-- LINKS -->
[imagenet]: http://www.image-net.org