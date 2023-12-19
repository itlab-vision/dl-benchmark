# Model validation and performance analysis status for ncnn

## Public models

### Image classification

Model | Availability in ncnn OMZ (2023.12.19)| Availability in the validation table |
-|-|-|
squeezenet|+|+|
shufflenetv2|+|+|

### Object detection

Model | Availability in ncnn OMZ (2023.12.19)| Availability in the validation table |
-|-|-|
faster_rcnn|+|+|
rfcn|+|+|
mobilenet_ssd|+|+|
mobilenetv2_ssdlite|+|+|
mobilenetv3_ssdlite|+|+|
squeezenet_ssd|+|+|
mobilenet_yolov2|+|+|
mobilenetv2_yolov3|+|+|
yolov4_tiny|+|+|
yolov5s|+|+|
yolov8s|+|+|
nanodet|+|IndexError: index 430 is out of bounds for axis 0 with size 80 in ncnn/model_zoo/nanodet.py|
peleenet_ssd|+|Need to add custom process_output fuction for this model.|
yolact|+|Need to add custom process_output fuction for this model.|

### Face detection

Model | Availability in ncnn OMZ (2023.12.19)| Availability in the validation table |
-|-|-|
retinaface|+|-|
