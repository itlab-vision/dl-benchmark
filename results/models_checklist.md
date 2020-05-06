# Статус валидации и анализа производительности моделей

## Публичные модели

### Классификация изображений (image classification)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
alexnet|+|+|+|
**caffenet**|+|-|+|
densenet-121|+|+|+|
densenet-161|+|+|+|
densenet-169|+|+|+|
densenet-201|+|+|+|
efficientnet-b0|+|-|-|
efficientnet-b0_auto_aug|+|-|-|
efficientnet-b5|+|-|-|
efficientnet-b7-pytorch|+|-|-|
efficientnet-b7_auto_aug|+|-|-|
googlenet-v1|+|+|+|
googlenet-v2|+|+|+|
googlenet-v3|+|+|+|
googlenet-v4|+|+|+|
inception-resnet-v2|+|+|+|
**mobilenet-v1-0.25-128**|+|-|+|
**mobilenet-v1-0.50-160**|+|-|+|
**mobilenet-v1-0.50-224**|+|-|+|
**mobilenet-v1-1.0-224**|+|-|+|
**mobilenet-v2**|+|-|+|
mobilenet-v2-1.4-224|+|-|-|
resnet-50|+|название resnet-v1-*|+|
resnet-101|+|название resnet-v1-*|+|
resnet-152|+|название resnet-v1-*|+|
**se-inception**|+|-|+|
**se-resnet-50**|+|-|+|
**se-resnet-101**|+|-|+|
**se-resnet-152**|+|-|+|
**se-resnext-50**|+|-|+|
**se-resnext-101**|+|-|+|
squeezenet1.0|+|+|+|
squeezenet1.1|+|+|+|
vgg16|+|+|+|
vgg19|+|+|+|
octave-densenet-121-0.125|+|-|-|
octave-resnet-26-0.25|+|-|-|
octave-resnet-50-0.125|+|-|-|
octave-resnet-101-0.125|+|-|-|
octave-resnet-200-0.125|+|-|-|
octave-resnext-50-0.25|+|-|-|
octave-resnext-101-0.25|+|-|-|
octave-se-resnet-50-0.125|+|-|-|

### Семантическая сегментация (semantic segmentation)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
**deeplabv3**|+|-|+|

### Сегментация объектов (instance segmentation)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
mask_rcnn_inception_resnet_v2_atrous_coco|+|-|-|
mask_rcnn_inception_v2_coco|+|-|-|
mask_rcnn_resnet50_atrous_coco|+|-|-|
mask_rcnn_resnet101_atrous_coco|+|-|-|

### 3D сегментация (3D segmentation)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
brain-tumor-segmentation-0001|+|-|-|
brain-tumor-segmentation-0002|+|-|-|

### Детектирование объектов (object detection)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
ctpn|+|-|-|
ctdet_coco_dlav0_384|+|-|-|
ctdet_coco_dlav0_512|+|-|-|
faster_rcnn_inception_resnet_v2_atrous_coco|+|-|-|
faster_rcnn_inception_v2_coco|+|-|-|
faster_rcnn_resnet50_coco|+|-|-|
faster_rcnn_resnet101_coco|+|-|-|
mtcnn|+|-|-|
ssd300|+|+|+|
ssd512|+|+|+|
mobilenet-ssd (ssd_mobilenet_v1_coco)|+|+|+|
ssd_mobilenet_v1_fpn_coco|-|-|+|
ssd_mobilenet_v2_coco|-|+|+|
ssdlite_mobilenet_v2|-|-|-|
yolo-v1-tiny-tf|+|-|-|
yolo-v2-tiny-tf|+|-|-|
yolo-v2-tf|+|-|-|
yolo-v3-tf|+|-|-|

### Распознавание лиц (face recognition)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
facenet-20180408-102900|+|-|-|
face-recognition-resnet34-arcface|+|-|-|
face-recognition-resnet50-arcface|+|-|-|
face-recognition-resnet100-arcface|+|-|-|
face-recognition-mobilefacenet-arcface|+|-|-|
Sphereface|+|+|-|

### Оценка позы человека (human pose estimation)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
human-pose-estimation-3d-0001|+|-|-|
single-human-pose-estimation-0001|+|-|-|

### Оценка глубины (monocular depth estimation)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
midasnet|+|-|-|

### Восстановление изображений (image inpainting)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
gmcnn-places2-tf|+|-|-|

### Распознавание движений (action recognition)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
i3d-rgb-tf|+|-|-|

## Модели Intel

### Детектирование объектов (object detection)
Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
faster-rcnn-resnet101-coco-sparse-60-0001|+|-|-|
face-detection-adas-0001|+|-|+|
face-detection-adas-binary-0001|+|-|-|
face-detection-retail-0004|+|-|+|
face-detection-retail-0005|+|-|+|
face-detection-0100|+|-|-|
face-detection-0102|+|-|-|
face-detection-0104|+|-|-|
face-detection-0105|+|-|-|
face-detection-0106|+|-|-|
person-detection-retail-0002|+|-|-|
person-detection-retail-0013|+|-|+|
person-detection-action-recognition-0005|+|-|-|
person-detection-action-recognition-0006|+|-|-|
person-detection-action-recognition-teacher-0002|+|-|-|
person-detection-raisinghand-recognition-0001|+|-|-|
pedestrian-detection-adas-0002|+|-|+|
pedestrian-detection-adas-binary-0001|+|-|-|
pedestrian-and-vehicle-detector-adas-0001|+|+|+|
vehicle-detection-adas-0002|+|+|+|
vehicle-detection-adas-binary-0001|+|+|-|
person-vehicle-bike-detection-crossroad-0078|+|+|+|
person-vehicle-bike-detection-crossroad-1016|+|+|+|
vehicle-license-plate-detection-barrier-0106|+|+|+|
product-detection-0001|+|+|-|
person-detection-asl-0001|+|+|-|
yolo-v2-ava-0001|+|-|-|
yolo-v2-ava-sparse-35-0001|+|-|-|
yolo-v2-ava-sparse-70-0001|+|-|-|
yolo-v2-tiny-ava-0001|+|-|-|
yolo-v2-tiny-ava-sparse-30-0001|+|-|-|
yolo-v2-tiny-ava-sparse-60-0001|+|-|-|

### Распознавание объектов (object recognition)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
age-gender-recognition-retail-0013|+|+|+|
head-pose-estimation-adas-0001|+|+|+|
license-plate-recognition-barrier-0001|+|+|-|
vehicle-attributes-recognition-barrier-0039|+|-|-|
emotions-recognition-retail-0003|+|-|-|
landmarks-regression-retail-0009|+|+|+|
facial-landmarks-35-adas-0002|+|+|+|
person-attributes-recognition-crossroad-0230|+|+|+|
gaze-estimation-adas-0002|+|+|-|

### Идентификация объектов (reidentification)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
person-reidentification-retail-0031|+|-|-|
person-reidentification-retail-0079|+|-|-|
person-reidentification-retail-0076|+|-|-|
face-reidentification-retail-0095|+|+|-|

### Семантическая сегментация

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
road-segmentation-adas-0001|+|+|+|
semantic-segmentation-adas-0001|+|+|+|
unet-camvid-onnx-0001|+|-|-|
icnet-camvid-ava-0001|+|-|-|
icnet-camvid-ava-sparse-30-0001|+|-|-|
icnet-camvid-ava-sparse-60-0001|+|-|-|

### Сегментация объектов (instance segmentation)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
instance-segmentation-security-1025|+|-|-|
instance-segmentation-security-0050|+|+|-|
instance-segmentation-security-0083|+|+|-|
instance-segmentation-security-0010|+|+|-|

### Оценка позы человека (human pose estimation)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
human-pose-estimation-0001|+|+|-|

### Обработка изображений (image processing)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
single-image-super-resolution-1032|+|+|-|
single-image-super-resolution-1033|+|+|-|
text-image-super-resolution-0001|+|-|-|

### Детектирование текста (text detection)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
text-detection-0003|+|-|-|
text-detection-0004|+|-|-|

### Распознавание текста (text recognition)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
text-recognition-0012|+|-|-|
handwritten-score-recognition-0003|+|-|-|
handwritten-japanese-recognition-0001|+|-|-|

### Детектирование и распознавание текста (text spotting)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
text-spotting-0002-detector|+|-|-|
text-spotting-0002-recognizer-encoder|+|-|-|
text-spotting-0002-recognizer-decoder|+|-|-|

### Распознавание движений (action recognition)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
driver-action-recognition-adas-0002-encoder|+|+|-|
driver-action-recognition-adas-0002-decoder|+|+|-|
action-recognition-0001-encoder|+|+|-|
action-recognition-0001-decoder|+|+|-|
asl-recognition-0004|+|-|-|

### Восстановление изображений (image retrieval)

Модель | Наличие в OMZ (2020.05.04)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
image-retrieval-0001|+|-|-|
