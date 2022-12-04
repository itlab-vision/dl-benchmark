# Model validation and performance analysis status for Intel® Distribution of OpenVINO™ Toolkit

## Public models

### Image classification

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
alexnet|+|+|+|+|
***anti-spoof-mn3***|+|-|-|-|
caffenet|+|+|+|+|
densenet-121|+|+|+|+|
densenet-121-caffe2|+|+|-|+|
densenet-121-tf|+|+|-|+|
densenet-161|+|+|+|+|
densenet-161-tf|+|+|-|-*|
densenet-169|+|+|+|+|
densenet-169-tf|+|+|-|+|
densenet-201|+|+|+|+|
densenet-201-tf|+|+|-|-*|
dla-34|+|+|-|-*|
efficientnet-b0|+|+|-|+|
efficientnet-b0_auto_aug|+|+|-|+|
efficientnet-b0-pytorch|+|+|-|+|
efficientnet-b5|+|+|-|+|
efficientnet-b5-pytorch|+|+|-|+|
efficientnet-b7_auto_aug|+|+|-|+|
efficientnet-b7-pytorch|+|+|-|+|
efficientdet-d0-tf|+|-|-|-*|
efficientdet-d1-tf|+|-|-|-*|
googlenet-v1|+|+|+|+|
googlenet-v1-tf|+|+|-|+|
googlenet-v2|+|+|+|+|
googlenet-v2-tf|+|+|-|+|
googlenet-v3|+|+|+|+|
googlenet-v3-pytorch|+|+|-|+|
googlenet-v4|-|+|+|-*|
googlenet-v4-tf|+|+|-|+|
hbonet-0.25|+|+|-|-*|
***hbonet-0.5***|+|-|-|-|
***hbonet-1.0***|+|-|-|-|
inception-resnet-v2|-|+|+|-*|
inception-resnet-v2-tf|+|+|-|+|
mixnet-l|+|+|-|-*|
mobilenet-v1-0.25-128|+|+|+|+|
mobilenet-v1-0.50-160|+|+|+|+|
mobilenet-v1-0.50-224|+|+|+|+|
mobilenet-v1-1.0-224|+|+|+|+|
mobilenet-v1-1.0-224-tf|+|+|-|+|
mobilenet-v2|+|+|+|+|
mobilenet-v2-1.0-224|+|+|-|+|
mobilenet-v2-1.4-224|+|+|-|+|
mobilenet-v2-pytorch|+|+|-|+|
mobilenet-v3-large-1.0-224-tf|+|+|-|+|
mobilenet-v3-small-1.0-224-tf|+|+|-|+|
***nfnet-f0***|+|-|-|-|
octave-densenet-121-0.125|+|+|-|+|
octave-resnet-101-0.125|+|+|-|+|
octave-resnet-200-0.125|+|+|-|+|
octave-resnet-26-0.25|+|+|-|+|
octave-resnet-50-0.125|+|+|-|+|
octave-resnext-101-0.25|+|+|-|+|
octave-resnext-50-0.25|+|+|-|+|
octave-se-resnet-50-0.125|+|+|-|+|
open-closed-eye-0001|+|+|-|-*|
***regnetx-3.2gf***|+|-|-|-|
***repvgg-a0***|+|-|-|-|
***repvgg-b1***|+|-|-|-|
***repvgg-b3***|+|-|-|-|
***resnest-50-pytorch***|+|-|-|-|
resnet-101|-|called resnet-v1-*|+|-|
resnet-152|-|called resnet-v1-*|+|-|
resnet-18-pytorch|+|+|-|+|
resnet-34-pytorch|+|+|-|-*|
resnet-50|-|called resnet-v1-*|+|-|
resnet-50-caffe2|+|+|-|+|
resnet-50-pytorch|+|+|-|+|
resnet-50-tf|+|+|-|+|
***rexnet-v1-x1.0***|+|-|-|-|
se-inception|+|+|+|+|
se-resnet-101|+|+|+|+|
se-resnet-152|+|+|+|+|
se-resnet-50|+|+|+|-*|
se-resnext-101|+|+|+|-*|
se-resnext-50|+|+|+|-*|
***shufflenet-v2-x1.0***|+|-|-|-|
squeezenet1.0|+|+|+|+|
squeezenet1.1|+|+|+|+|
squeezenet1.1-caffe2|+|+|-|+|
vgg16|+|+|+|+|
vgg19|+|+|+|+|
vgg19-caffe2|+|+|-|+|

### Semantic segmentation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
deeplabv3|+|+|+|+|
***fastseg-large***|+|-|-|-|
***fastseg-small***|+|-|-|-|
***pspnet-pytorch***|+|-|-|-|

### Instance segmentation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
mask_rcnn_inception_resnet_v2_atrous_coco|+|+|-|-*|
mask_rcnn_inception_v2_coco|+|+|-|-*|
mask_rcnn_resnet101_atrous_coco|+|+|-|-*|
mask_rcnn_resnet50_atrous_coco|+|+|-|-*|
***yolact-resnet50-fpn-pytorch***|+|-|-|-|

### 3D segmentation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***brain-tumor-segmentation-0001***|+|there is no data|-|-|
***brain-tumor-segmentation-0002***|+|there is no data|-|-|

### Object detection

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***ctdet_coco_dlav0_384***|+|-|-|-|
***ctdet_coco_dlav0_512***|+|-|-|-|
***ctpn***|+|there is no data|-|-|
***faceboxes-pytorch***|+|-|-|-|
***face-detection-retail-0044***|+|-|-|-|
faster_rcnn_inception_resnet_v2_atrous_coco|+|+|-|-*|
faster_rcnn_inception_v2_coco|+|+|-|-*|
faster_rcnn_resnet101_coco|+|+|-|-*|
faster_rcnn_resnet50_coco|+|+|-|-*|
***mobilefacedet-v1-mxnet***|+|-|-|-|
mobilenet-ssd (ssd_mobilenet_v1_coco)|+|+|+|+|+|
***mtcnn***|+|pipeline|-|-|
pelee-coco|+|+|+|-*|
retinanet-tf|+|+|-|-*|
***rfcn-resnet101-coco-tf***|+|-|-|-|
ssd300|+|+|+|+|
ssd512|+|+|+|+|
***ssdlite_mobilenet_v2***|+|-|-|-|
ssd_mobilenet_v1_fpn_coco|+|+|+|+|
ssd_mobilenet_v2_coco|+|+|+|+|
***ssd-resnet34-1200-onnx***|+|-|-|-|
ssd_resnet50_v1_fpn_coco|+|+|+|+|
***ultra-lightweight-face-detection-rfb-320***|+|-|-|-|
***ultra-lightweight-face-detection-slim-320***|+|-|-|-|
***vehicle-license-plate-detection-barrier-0123***|+|-|-|-|
yolo-v1-tiny-tf|+|+|-|+|
yolo-v2-tiny-tf|+|+|-|+|
yolo-v2-tf|+|+|-|+|
***yolo-v3-tiny-tf***|+|-|-|-|
yolo-v3-tf|+|+|-|-*|
***yolo-v4-tiny-tf***|+|-|-|-|
***yolo-v4-tf***|+|-|-|-|

### Face recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***facenet-20180408-102900***|+|there is no data|-|-|
face-recognition-mobilefacenet-arcface|-|there is no data|-|-|
face-recognition-resnet100-arcface|-|there is no data|-|-|
***face-recognition-resnet100-arcface-onnx***|+|-|-|-|
face-recognition-resnet34-arcface|-|there is no data|-|-|
face-recognition-resnet50-arcface|-|there is no data|-|-|
Sphereface|+|+|-|-*|

### Human pose estimation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***higher-hrnet-w32-human-pose-estimation***|+|-|-|-|
***human-pose-estimation-3d-0001***|+|-|-|-|
***single-human-pose-estimation-0001***|+|-|-|-|

### Monodepth

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***fcrn-dp-nyu-depth-v2-tf***|+|-|-|-|
***midasnet***|+|-|-|-|

### Image inpainting

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***gmcnn-places2-tf***|+|-|-|-|

### Action recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***common-sign-language-0001***|+|-|-|-|
***i3d-rgb-tf***|+|-|-|-|

### Sound classification

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***aclnet***|+|-|-|-|
***aclnet-int8***|+|-|-|-|

### Named entity recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***bert-base-ner***|+|-|-|-|

### Image translation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***cocosnet***|+|-|-|-|

### Colorization

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***colorization-siggraph***|+|-|-|-|
***colorization-v2***|+|-|-|-|

### Image processing
Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***deblurgan-v2***|+|-|-|-|

### Salient object detection

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***f3net***|+|-|-|-|

### Style transfer
Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***fast-neural-style-mosaic-onnx***|+|-|-|-|

### Speech synthesis

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***forward-tacotron-duration-prediction model specification***|+|-|-|-|
***wavernn***|+|-|-|-|

### Speech recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***mozilla-deepspeech-0.6.1***|+|-|-|-|
***mozilla-deepspeech-0.8.2***|+|-|-|-|
***quartznet-15x5-en***|+|-|-|-|

### Place recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***netvlad-tf***|+|-|-|-|

### Face localization

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***retinaface-resnet50-pytorch***|+|-|-|-|

### Scene text recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***text-recognition-resnet-fc***|+|-|-|-|

### Object recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***license-plate-recognition-barrier-0007***|+|-|-|-|

### Vehicle reidentification

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***vehicle-reid-0001***|+|-|-|-|

## Intel models

### Image classification

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
resnet18-xnor-binary-onnx-0001|+|+|-|-*|
***resnet50-binary-0001***|+|-|-|-|
***weld-porosity-detection-0001***|+|-|-|-|

### Object detection

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
face-detection-0100|-|+|-|-|
face-detection-0102|-|+|-|-|
face-detection-0104|-|+|-|-|
face-detection-0105|-|+|-|-|
face-detection-0106|-|-|-|-|
***face-detection-0200***|+|-|-|-|
***face-detection-0202***|+|-|-|-|
***face-detection-0204***|+|-|-|-|
***face-detection-0205***|+|-|-|-|
***face-detection-0206***|+|-|-|-|
face-detection-adas-0001|+|+|+|+|
face-detection-adas-binary-0001|-|+|-|-|
face-detection-retail-0004|+|+|+|+|
face-detection-retail-0005|+|+|+|+|
***faster-rcnn-resnet101-coco-sparse-60-0001***|+|-|-|-|
pedestrian-and-vehicle-detector-adas-0001|+|+|+|+|
pedestrian-detection-adas-0002|+|+|+|+|
pedestrian-detection-adas-binary-0001|-|+|-|-|
***person-detection-0106***|+|-|-|-|
***person-detection-0200***|+|-|-|-|
***person-detection-0201***|+|-|-|-|
***person-detection-0202***|+|-|-|-|
***person-detection-0203***|+|-|-|-|
person-detection-action-recognition-0005|+|+|-|+|
person-detection-action-recognition-0006|+|+|-|+|
person-detection-action-recognition-teacher-0002|+|+|-|+|
person-detection-asl-0001|+|+|-|-*|
person-detection-raisinghand-recognition-0001|+|+|-|-*|
person-detection-retail-0002|+|+|-|+|
person-detection-retail-0013|+|+|+|+|
***person-vehicle-bike-detection-2000***|+|-|-|-|
***person-vehicle-bike-detection-2001***|+|-|-|-|
***person-vehicle-bike-detection-2002***|+|-|-|-|
***person-vehicle-bike-detection-2003***|+|-|-|-|
***person-vehicle-bike-detection-2004***|+|-|-|-|
person-vehicle-bike-detection-crossroad-0078|+|+|+|+|
person-vehicle-bike-detection-crossroad-1016|+|+|+|+|
***person-vehicle-bike-detection-crossroad-yolov3-1020***|+|-|-|-|
product-detection-0001|+|+|-|+|
***vehicle-detection-0200***|+|-|-|-|
***vehicle-detection-0201***|+|-|-|-|
***vehicle-detection-0202***|+|-|-|-|
vehicle-detection-adas-0002|+|+|+|+|
vehicle-detection-adas-binary-0001|-|+|-|-|
vehicle-license-plate-detection-barrier-0106|+|+|+|-*|
yolo-v2-ava-0001|+|+|-|+|
yolo-v2-ava-sparse-35-0001|+|+|-|+|
yolo-v2-ava-sparse-70-0001|+|+|-|+|
***yolo-v2-tiny-vehicle-detection-0001***|+|-|-|-|
yolo-v2-tiny-ava-0001|+|+|-|+|
yolo-v2-tiny-ava-sparse-30-0001|+|+|-|+|
yolo-v2-tiny-ava-sparse-60-0001|+|+|-|+|

### Object recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
age-gender-recognition-retail-0013|+|+|+|+|
emotions-recognition-retail-0003|+|there is no data|-|-|
facial-landmarks-35-adas-0002|+|+|+|+|
gaze-estimation-adas-0002|+|+|-|+|
head-pose-estimation-adas-0001|+|+|+|+|
landmarks-regression-retail-0009|+|+|+|+|
license-plate-recognition-barrier-0001|+|+|-|+|
person-attributes-recognition-crossroad-0230|+|+|+|+|
***person-attributes-recognition-crossroad-0234***|+|-|-|-|
***person-attributes-recognition-crossroad-0238***|+|-|-|-|
***vehicle-attributes-recognition-barrier-0039***|+|there is no data|-|-|
***vehicle-attributes-recognition-barrier-0042***|+|-|-|-|

### Reidentification

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
person-reidentification-retail-0031|-|there is no data (Market-1501)|-|-|
person-reidentification-retail-0076|-|there is no data (Market-1501)|-|-|
person-reidentification-retail-0079|-|there is no data (Market-1501)|-|-|
***person-reidentification-retail-0277***|+|-|-|-|
***person-reidentification-retail-0286***|+|-|-|-|
***person-reidentification-retail-0287***|+|-|-|-|
***person-reidentification-retail-0288***|+|-|-|-|
face-reidentification-retail-0095|+|+|-|+|

### Semantic segmentation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
icnet-camvid-ava-0001|+|+|-|-*|
icnet-camvid-ava-sparse-30-0001|+|+|-|-*|
icnet-camvid-ava-sparse-60-0001|+|+|-|-*|
road-segmentation-adas-0001|+|+|+|+|
semantic-segmentation-adas-0001|+|+|+|+|
unet-camvid-onnx-0001|+|+|-|-*|

### Instance segmentation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***instance-segmentation-security-0002***|+|-|-|-|
instance-segmentation-security-0010|-|+|-|-|
instance-segmentation-security-0050|-|+|-|-|
instance-segmentation-security-0083|-|+|-|-|
***instance-segmentation-security-0091***|+|-|-|-|
***instance-segmentation-security-0228***|+|-|-|-|
instance-segmentation-security-1025|-|+|-|-|
***instance-segmentation-security-1039***|+|-|-|-|
***instance-segmentation-security-1040***|+|-|-|-|

### Human pose estimation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
human-pose-estimation-0001|+|+|-|+|
***human-pose-estimation-0005***|+|-|-|-|
***human-pose-estimation-0006***|+|-|-|-|
***human-pose-estimation-0007***|+|-|-|-|

### Image processing

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
single-image-super-resolution-1032|+|+|-|+|
single-image-super-resolution-1033|+|+|-|+|
***text-image-super-resolution-0001***|+|there is no data|-|-|

### Text detection

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***horizontal-text-detection-0001***|+|-|-|-|
***text-detection-0003***|+|there is no data (ICDAR)|-|-|
***text-detection-0004***|+|there is no data (ICDAR)|-|-|

### Text recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***formula-recognition-medium-scan-0001***|+|-|-|-|
***formula-recognition-polynomials-handwritten-0001***|+|-|-|-|
***handwritten-japanese-recognition-0001***|+|there is no data (HANDS-nakayosi_t-98-09, HANDS-kondate-14-09-01)|-|-|
***handwritten-score-recognition-0003***|+|there is no data|-|-|
***handwritten-simplified-chinese-recognition-0001***|+|-|-|-|
***text-recognition-0012***|+|there is no data (ICDAR)|-|-|
***text-recognition-0014***|+|-|-|-|
***text-recognition-0015***|+|-|-|-|

### Text spotting

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
text-spotting-0002-detector|-|pipeline|-|-|
text-spotting-0002-recognizer-decoder|-|-|-|-|
text-spotting-0002-recognizer-encoder|-|-|-|-|
***text-spotting-0005***|+|-|-|-|

### Action recognition

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
action-recognition-0001-decoder|+ (action-recognition-0001)|+|-|-*|
action-recognition-0001-encoder|+ (action-recognition-0001)|+|-|-*|
***asl-recognition-0004***|+|-|-|-|
***common-sign-language-0002***|+|-|-|-|
driver-action-recognition-adas-0002-decoder|+ (driver-action-recognition-adas-0002)|+|-|-*|
driver-action-recognition-adas-0002-encoder|+ (driver-action-recognition-adas-0002)|+|-|-*|

### Image retrieval

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
image-retrieval-0001|+|+|-|-*|

### Question answering

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***bert-large-uncased-whole-word-masking-squad-0001***|+|-|-|-|
***bert-large-uncased-whole-word-masking-squad-emb-0001***|+|-|-|-|
***bert-large-uncased-whole-word-masking-squad-int8-0001***|+|-|-|-|
***bert-small-uncased-whole-word-masking-squad-0001***|+|-|-|-|
***bert-small-uncased-whole-word-masking-squad-0002***|+|-|-|-|
***bert-small-uncased-whole-word-masking-squad-emb-int8-0001***|+|-|-|-|
***bert-small-uncased-whole-word-masking-squad-int8-0002***|+|-|-|-|

### Machine translation

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***machine-translation-nar-de-en-0002***|+|-|-|-|
***machine-translation-nar-en-de-0002***|+|-|-|-|
***machine-translation-nar-en-ru-0001***|+|-|-|-|
***machine-translation-nar-ru-en-0001***|+|-|-|-|

### Noise suppression

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***noise-suppression-poconetlike-0001***|+|-|-|-|

### Speech synthesis

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***text-to-speech-en-0001***|+|-|-|-|
***text-to-speech-en-multi-0001***|+|-|-|-|

### Time series forecasting

Model | Availability in OMZ (2021.10.19)| Availability in the validation table | Availability in the html table (R3) | Availability in the html table (2021.4) |
-|-|-|-|-|
***time-series-forecasting-electricity-0001***|+|-|-|-|

\* "-\*" in the column "Availability in the html table..."
means that the model was checked but there is no in
the performance table.

## Models for the further checking

### Intel models

1. asl-recognition-0004
1. bert-small-uncased-whole-word-masking-squad-0001
1. bert-small-uncased-whole-word-masking-squad-0002
1. bert-small-uncased-whole-word-masking-squad-emb-int8-0001
1. bert-small-uncased-whole-word-masking-squad-int8-0002
1. bert-large-uncased-whole-word-masking-squad-emb-0001
1. bert-large-uncased-whole-word-masking-squad-int8-0001
1. bert-large-uncased-whole-word-masking-squad-fp32-0001
1. common-sign-language-0002
1. face-detection-0200
1. face-detection-0202
1. face-detection-0204
1. face-detection-0205
1. face-detection-0206
1. faster-rcnn-resnet101-coco-sparse-60-0001
1. formula-recognition-medium-scan-0001
1. formula-recognition-polynomials-handwritten-0001
1. handwritten-simplified-chinese-recognition-0001
1. horizontal-text-detection-0001
1. human-pose-estimation-0005
1. human-pose-estimation-0006
1. human-pose-estimation-0007
1. instance-segmentation-security-0002
1. instance-segmentation-security-0091
1. instance-segmentation-security-0228
1. instance-segmentation-security-1039
1. instance-segmentation-security-1040
1. machine-translation-nar-de-en-0002
1. machine-translation-nar-en-de-0002
1. machine-translation-nar-en-ru-0001
1. machine-translation-nar-ru-en-0001
1. noise-suppression-poconetlike-0001
1. person-attributes-recognition-crossroad-0234
1. person-attributes-recognition-crossroad-0238
1. person-detection-0106
1. person-detection-0200
1. person-detection-0201
1. person-detection-0202
1. person-detection-0203
1. person-reidentification-retail-0277
1. person-reidentification-retail-0286
1. person-reidentification-retail-0287
1. person-reidentification-retail-0288
1. person-vehicle-bike-detection-2000
1. person-vehicle-bike-detection-2001
1. person-vehicle-bike-detection-2002
1. person-vehicle-bike-detection-2003
1. person-vehicle-bike-detection-2004
1. person-vehicle-bike-detection-crossroad-yolov3-1020
1. text-recognition-0014
1. text-recognition-0015
1. text-to-speech-en-0001
1. text-to-speech-en-multi-0001
1. time-series-forecasting-electricity-0001
1. vehicle-attributes-recognition-barrier-0042
1. vehicle-detection-0200
1. vehicle-detection-0201
1. vehicle-detection-0202
1. weld-porosity-detection-0001
1. resnet50-binary-0001
1. text-spotting-0005
1. yolo-v2-tiny-vehicle-detection-0001

### Public models

1. aclnet
1. aclnet-int8
1. anti-spoof-mn3
1. bert-base-ner
1. cocosnet
1. colorization-siggraph
1. colorization-v2
1. common-sign-language-0001
1. ctdet_coco_dlav0_384
1. ctdet_coco_dlav0_512
1. deblurgan-v2
1. efficientdet-d0-tf
1. efficientdet-d1-tf
1. f3net
1. faceboxes-pytorch
1. face-detection-retail-0044
1. face-recognition-resnet100-arcface-onnx
1. fastseg-large
1. fastseg-small
1. fast-neural-style-mosaic-onnx
1. fcrn-dp-nyu-depth-v2-tf
1. forward-tacotron
1. gmcnn-places2-tf
1. hbonet-0.5
1. hbonet-1.0
1. higher-hrnet-w32-human-pose-estimation
1. human-pose-estimation-3d-0001
1. i3d-rgb-tf
1. license-plate-recognition-barrier-0007
1. midasnet
1. mobilefacedet-v1-mxnet
1. mozilla-deepspeech-0.6.1
1. mozilla-deepspeech-0.8.2
1. netvlad-tf
1. nfnet-f0
1. pspnet-pytorch
1. quartznet-15x5-en
1. regnetx-3.2gf
1. repvgg-a0
1. repvgg-b1
1. repvgg-b3
1. retinaface-resnet50-pytorch
1. rexnet-v1-x1.0
1. rfcn-resnet101-coco-tf
1. shufflenet-v2-x1.0
1. single-human-pose-estimation-0001
1. ssdlite_mobilenet_v2
1. ssd-resnet34-1200-onnx
1. text-recognition-resnet-fc
1. ultra-lightweight-face-detection-rfb-320
1. ultra-lightweight-face-detection-slim-320
1. vehicle-license-plate-detection-barrier-0123
1. vehicle-reid-0001
1. wavernn
1. yolact-resnet50-fpn-pytorch
1. yolo-v3-tiny-tf
1. yolo-v4-tiny-tf
1. yolo-v4-tf
