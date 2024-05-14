# Model validation and performance analysis status for ncnn

## Public models

### Image classification

Model | Availability in ncnn OMZ (2023.12.19)| Availability in the validation table |
-|-|-|
shufflenetv2|+|+|
squeezenet|+|+|

### Object detection

Model | Availability in ncnn OMZ (2023.12.19)| Availability in the validation table |
-|-|-|
faster_rcnn|+|+|
mobilenet_ssd|+|+|
mobilenetv2_ssdlite|+|+|
mobilenetv3_ssdlite|+|+|
mobilenet_yolov2|+|+|
mobilenetv2_yolov3|+|+|
nanodet|+|IndexError: index 430 is out of bounds for axis 0 with size 80 in ncnn/model_zoo/nanodet.py|
peleenet_ssd|+|Need to add custom process_output fuction for this model.|
rfcn|+|+|
squeezenet_ssd|+|+|
yolact|+|Need to add custom process_output fuction for this model.|
yolov4_tiny|+|+|
yolov5s|+|+|
yolov8s|+|+|

### Face detection

Model | Availability in ncnn OMZ (2023.12.19)| Availability in the validation table |
-|-|-|
retinaface|+|-|
