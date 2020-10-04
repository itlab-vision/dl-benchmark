# Статус валидации и анализа производительности моделей

## Публичные модели

### Классификация изображений (image classification)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
alexnet|+|+|+|
caffenet|+|+|+|
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
googlenet-v4|-|+|+|
inception-resnet-v2|-|+|+|
**mobilenet-v1-0.25-128**|+|-|+|
**mobilenet-v1-0.50-160**|+|-|+|
**mobilenet-v1-0.50-224**|+|-|+|
mobilenet-v1-1.0-224|+|+|+|
mobilenet-v2|+|+|+|
mobilenet-v2-1.4-224|+|-|-|
resnet-50|+|название resnet-v1-*|+|
resnet-101|+|название resnet-v1-*|+|
resnet-152|+|название resnet-v1-*|+|
se-inception|+|+|+|
se-resnet-50|+|+|+|
se-resnet-101|+|+|+|
se-resnet-152|+|+|+|
se-resnext-50|+|+|+|
se-resnext-101|+|+|+|
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

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
**deeplabv3**|+|-|+|

### Сегментация объектов (instance segmentation)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
mask_rcnn_inception_resnet_v2_atrous_coco|+|+|-|
mask_rcnn_inception_v2_coco|+|+|-|
mask_rcnn_resnet50_atrous_coco|+|+|-|
mask_rcnn_resnet101_atrous_coco|+|+|-|

### 3D сегментация (3D segmentation)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
brain-tumor-segmentation-0001|+|отсутствуют данные|-|
brain-tumor-segmentation-0002|+|отсутствуют данные|-|

### Детектирование объектов (object detection)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
ctpn|+|отсутствуют данные|-|
ctdet_coco_dlav0_384|+|-|-|
ctdet_coco_dlav0_512|+|-|-|
faster_rcnn_inception_resnet_v2_atrous_coco|+|-|-|
faster_rcnn_inception_v2_coco|+|-|-|
faster_rcnn_resnet50_coco|+|-|-|
faster_rcnn_resnet101_coco|+|-|-|
mtcnn|+|пайплайн из трех моделей|-|
ssd300|+|+|+|
ssd512|+|+|+|
mobilenet-ssd (ssd_mobilenet_v1_coco)|+|+|+|
*ssd_mobilenet_v1_fpn_coco*|+|-|+|
ssd_mobilenet_v2_coco|+|+|+|
ssdlite_mobilenet_v2|+|-|-|
yolo-v1-tiny-tf|+|-|-|
yolo-v2-tiny-tf|+|-|-|
yolo-v2-tf|+|-|-|
yolo-v3-tf|+|-|-|

### Распознавание лиц (face recognition)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
facenet-20180408-102900|+|не известен тренировочный набор данных|-|
face-recognition-resnet34-arcface|+|не известен тренировочный набор данных|-|
face-recognition-resnet50-arcface|+|не известен тренировочный набор данных|-|
face-recognition-resnet100-arcface|+|не известен тренировочный набор данных|-|
face-recognition-mobilefacenet-arcface|+|не известен тренировочный набор данных|-|
***Sphereface***|+|+|-|

### Оценка позы человека (human pose estimation)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
human-pose-estimation-3d-0001|+|-|-|
single-human-pose-estimation-0001|+|-|-|

### Оценка глубины (monocular depth estimation)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
midasnet|+|-|-|

### Восстановление изображений (image inpainting)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
gmcnn-places2-tf|+|-|-|

### Распознавание движений (action recognition)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
i3d-rgb-tf|+|-|-|

## Модели Intel

### Детектирование объектов (object detection)
Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
faster-rcnn-resnet101-coco-sparse-60-0001|+|-|-|
face-detection-adas-0001|+|+|+|
***face-detection-adas-binary-0001***|+|+|-|
face-detection-retail-0004|+|+|+|
face-detection-retail-0005|+|+|+|
face-detection-0100|+|-|-|
face-detection-0102|+|-|-|
face-detection-0104|+|-|-|
face-detection-0105|+|-|-|
face-detection-0106|+|-|-|
***person-detection-retail-0002***|+|+|-|
person-detection-retail-0013|+|+|+|
***person-detection-action-recognition-0005***|+|+|-|
***person-detection-action-recognition-0006***|+|+|-|
***person-detection-action-recognition-teacher-0002***|+|+|-|
***person-detection-raisinghand-recognition-0001***|+|+|-|
pedestrian-detection-adas-0002|+|+|+|
***pedestrian-detection-adas-binary-0001***|+|+|-|
pedestrian-and-vehicle-detector-adas-0001|+|+|+|
vehicle-detection-adas-0002|+|+|+|
***vehicle-detection-adas-binary-0001***|+|+|-|
person-vehicle-bike-detection-crossroad-0078|+|+|+|
person-vehicle-bike-detection-crossroad-1016|+|+|+|
vehicle-license-plate-detection-barrier-0106|+|+|+|
***product-detection-0001***|+|+|-|
***person-detection-asl-0001***|+|+|-|
yolo-v2-ava-0001|+|-|-|
yolo-v2-ava-sparse-35-0001|+|-|-|
yolo-v2-ava-sparse-70-0001|+|-|-|
yolo-v2-tiny-ava-0001|+|-|-|
yolo-v2-tiny-ava-sparse-30-0001|+|-|-|
yolo-v2-tiny-ava-sparse-60-0001|+|-|-|

### Распознавание объектов (object recognition)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
age-gender-recognition-retail-0013|+|+|+|
head-pose-estimation-adas-0001|+|+|+|
***license-plate-recognition-barrier-0001***|+|+|-|
vehicle-attributes-recognition-barrier-0039|+|отсутствуют данные|-|
emotions-recognition-retail-0003|+|нет доступа к набору данных AffectNet|-|
landmarks-regression-retail-0009|+|+|+|
facial-landmarks-35-adas-0002|+|+|+|
person-attributes-recognition-crossroad-0230|+|+|+|
***gaze-estimation-adas-0002***|+|+|-|

### Идентификация объектов (reidentification)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
person-reidentification-retail-0031|-|нет доступа к набору данных Market-1501|-|
person-reidentification-retail-0079|-|нет доступа к набору данных Market-1501|-|
person-reidentification-retail-0076|-|нет доступа к набору данных Market-1501|-|
***face-reidentification-retail-0095***|-|+|-|

### Семантическая сегментация

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
road-segmentation-adas-0001|+|+|+|
semantic-segmentation-adas-0001|+|+|+|
unet-camvid-onnx-0001|+|-|-|
icnet-camvid-ava-0001|+|-|-|
icnet-camvid-ava-sparse-30-0001|+|-|-|
icnet-camvid-ava-sparse-60-0001|+|-|-|

### Сегментация объектов (instance segmentation)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
instance-segmentation-security-1025|+|-|-|
***instance-segmentation-security-0050***|+|+|-|
***instance-segmentation-security-0083***|+|+|-|
***instance-segmentation-security-0010***|+|+|-|

### Оценка позы человека (human pose estimation)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
***human-pose-estimation-0001***|+|+|-|

### Обработка изображений (image processing)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
***single-image-super-resolution-1032***|+|+|-|
***single-image-super-resolution-1033***|+|+|-|
text-image-super-resolution-0001|+|нет доступа к набору данных ICDAR|-|

### Детектирование текста (text detection)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
text-detection-0003|+|нет доступа к набору данных ICDAR|-|
text-detection-0004|+|нет доступа к набору данных ICDAR|-|

### Распознавание текста (text recognition)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
text-recognition-0012|+|нет доступа к набору данных ICDAR|-|
handwritten-score-recognition-0003|+|отсутствуют данные|-|
handwritten-japanese-recognition-0001|+|-|-|

### Детектирование и распознавание текста (text spotting)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
text-spotting-0002-detector|-|-|-|
text-spotting-0002-recognizer-encoder|-|-|-|
text-spotting-0002-recognizer-decoder|-|-|-|

### Распознавание движений (action recognition)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
***driver-action-recognition-adas-0002-encoder***|-|+|-|
***driver-action-recognition-adas-0002-decoder***|-|+|-|
***action-recognition-0001-encoder***|-|+|-|
***action-recognition-0001-decoder***|-|+|-|
asl-recognition-0004|+|-|-|

### Восстановление изображений (image retrieval)

Модель | Наличие в OMZ (2020.09.23)| Наличие в таблице валидации | Наличие в html-таблице (для R3) |
-|-|-|-|
image-retrieval-0001|+|-|-|

## Модели, требующие валидации

1. mobilenet-v1-0.25-128
1. mobilenet-v1-0.50-160
1. mobilenet-v1-0.50-224
1. deeplabv3
1. ssd_mobilenet_v1_fpn_coco

## Модели для следующего этапа расширения

### Модели 2020.2
1. resnet18-xnor-binary-onnx-0001
1. face-detection-0100
1. face-detection-0102
1. face-detection-0104
1. face-detection-0105
1. face-detection-0106
1. unet-camvid-onnx-0001
1. yolo-v2-ava-0001
1. yolo-v2-ava-sparse-35-0001
1. yolo-v2-ava-sparse-70-0001
1. yolo-v2-tiny-ava-0001
1. yolo-v2-tiny-ava-sparse-30-0001
1. yolo-v2-tiny-ava-sparse-60-0001
1. instance-segmentation-security-1025
1. asl-recognition-0004
1. faster-rcnn-resnet101-coco-sparse-60-0001
1. handwritten-japanese-recognition-0001
1. person-reidentification-retail-0248
1. icnet-camvid-ava-0001
1. icnet-camvid-ava-sparse-30-0001
1. icnet-camvid-ava-sparse-60-0001
1. text-spotting-0002-detector
1. image-retrieval-0001

### Модели 2020.4
1. bert-small-uncased-whole-word-masking-squad-0001
1. bert-large-uncased-whole-word-masking-squad-fp32-0001
1. bert-large-uncased-whole-word-masking-squad-int8-0001
1. person-detection-0100
1. person-detection-0101
1. person-detection-0102
1. person-detection-0106
1. person-reidentification-retail-0265
1. yolo-v2-tiny-vehicle-detection-0001
1. vehicle-attributes-recognition-barrier-0042
1. weld-porosity-detection-0001
1. person-reidentification-retail-0267
1. person-reidentification-retail-0270
1. text-spotting-0002
1. driver-action-recognition-adas-0002
1. action-recognition-0001



### Public модели
1. yolo-v1-tiny-tf
1. yolo-v2-tiny-tf
1. yolo-v2-tf
1. yolo-v3-tf
1. faster_rcnn_inception_resnet_v2_atrous_coco
1. faster_rcnn_inception_v2_coco
1. faster_rcnn_resnet50_coco
1. faster_rcnn_resnet101_coco
1. efficientnet-b0
1. efficientnet-b0_auto_aug
1. efficientnet-b5
1. efficientnet-b7-pytorch
1. efficientnet-b7_auto_aug
1. mobilenet-v2-1.4-224
1. densenet-121-tf
1. densenet-121-caffe2
1. densenet-161-tf
1. densenet-169-tf
1. efficientnet-b0-pytorch
1. efficientnet-b5-pytorch
1. hbonet-1.0
1. hbonet-0.5
1. hbonet-0.25
1. googlenet-v1-tf
1. googlenet-v2-tf
1. googlenet-v3-pytorch
1. googlenet-v4-tf
1. inception-resnet-v2-tf
1. mobilenet-v1-1.0-224-tf
1. mobilenet-v2-1.0-224
1. mobilenet-v2-pytorch
1. mobilenet-v3-small-1.0-224-tf
1. mobilenet-v3-large-1.0-224-tf
1. octave-densenet-121-0.125
1. octave-resnet-26-0.25
1. octave-resnet-50-0.125
1. octave-resnet-101-0.125
1. octave-resnet-200-0.125
1. octave-resnext-50-0.25
1. octave-resnext-101-0.25
1. octave-se-resnet-50-0.125
1. open-closed-eye-0001
1. resnet-18-pytorch
1. resnet-34-pytorch
1. resnet-50-pytorch
1. resnet-50-caffe2
1. resnet-50-tf
1. squeezenet1.1-caffe2
1. ssdlite_mobilenet_v2
1. vgg19-caffe2
1. mask_rcnn_inception_resnet_v2_atrous_coco
1. ctdet_coco_dlav0_384
1. ctdet_coco_dlav0_512
1. faceboxes-pytorch
1. mobilefacedet-v1-mxnet
1. pelee-coco
1. retinanet-tf
1. rfcn-resnet101-coco-tf
1. ssd_resnet50_v1_fpn_coco
1. ssd-resnet34-1200-onnx
1. retinaface-resnet50
1. retinaface-anti-cov
1. human-pose-estimation-3d-0001
1. single-human-pose-estimation-0001
1. midasnet
1. gmcnn-places2-tf
1. fast-neural-style-mosaic-onnx
1. i3d-rgb-tf
1. colorization-v2
1. colorization-v2-norebal