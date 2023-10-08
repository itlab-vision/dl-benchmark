# Model validation and performance analysis status for MXNet

## Public models

### Image classification on ImageNet

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
alexnet|+|+|
darknet53|+|+|
densenet121|+|+|
densenet161|+|+|
densenet169|+|+|
densenet201|+|+|
googlenet|+|+|
hrnet_w18_c|+|+|
hrnet_w18_small_v1_c|+|+|
hrnet_w18_small_v2_c|+|+|
hrnet_w30_c|+|+|
hrnet_w32_c|+|+|
hrnet_w40_c|+|+|
hrnet_w44_c|+|+|
hrnet_w48_c|+|+|
hrnet_w64_c|+|+|
inceptionv3|+|+|
mobilenet0.25|+|+|
mobilenet0.5|+|+|
mobilenet0.75|+|+|
mobilenet1.0|+|+|
mobilenet1.0_int8|+|+|
mobilenetv2_0.25|+|+|
mobilenetv2_0.5|+|+|
mobilenetv2_0.75|+|+|
mobilenetv2_1.0|+|+|
mobilenetv3_large|+|+|
mobilenetv3_small|+|+|
residualattentionnet128|+|Error (Parameter 'residualattentionmodel0_hybridsequential0_conv0_weight' has not been initialized)|
residualattentionnet164|+|Error (Parameter 'residualattentionmodel0_hybridsequential0_conv0_weight' has not been initialized)|
residualattentionnet200|+|Error (Parameter 'residualattentionmodel0_hybridsequential0_conv0_weight' has not been initialized)|
residualattentionnet236|+|Error (Parameter 'residualattentionmodel0_hybridsequential0_conv0_weight' has not been initialized)|
residualattentionnet452|+|Error (Parameter 'residualattentionmodel0_hybridsequential0_conv0_weight' has not been initialized)|
residualattentionnet56|+|Error (Parameter 'residualattentionmodel0_hybridsequential0_conv0_weight' has not been initialized)|
residualattentionnet92|+|Error (Parameter 'residualattentionmodel0_hybridsequential0_conv0_weight' has not been initialized)|
resnest101|+|+|
resnest14|+|+|
resnest200|+|+|
resnest26|+|+|
resnest269|+|+|
resnest50|+|+|
resnet101_v1|+|+|
resnet101_v1b|+|+|
resnet101_v1c|+|+|
resnet101_v1d|+|+|
resnet101_v1d_0.73|+|+|
resnet101_v1d_0.76|+|+|
resnet101_v1e|+|Error (Failed loading Parameter 'resnetv1e_batchnorm2_gamma' from saved params: shape incompatible expected (128,) vs saved (64,))|
resnet101_v1s|+|+|
resnet101_v2|+|+|
resnet152_v1|+|+|
resnet152_v1b|+|+|
resnet152_v1c|+|+|
resnet152_v1d|+|+|
resnet152_v1e|+|Error (Failed loading Parameter 'resnetv1e_batchnorm2_gamma' from saved params: shape incompatible expected (128,) vs saved (64,))|
resnet152_v1s|+|+|
resnet152_v2|+|+|
resnet18_v1|+|+|
resnet18_v1b|+|+|
resnet18_v1b_0.89|+|+|
resnet18_v1b_custom|+|+|
resnet18_v2|+|+|
resnet34_v1|+|+|
resnet34_v1b|+|+|
resnet34_v2|+|+|
resnet50_v1|+|+|
resnet50_v1_int8|+|+|
resnet50_v1b|+|+|
resnet50_v1b_custom|+|+|
resnet50_v1b_gn|+|+|
resnet50_v1c|+|+|
resnet50_v1d|+|+|
resnet50_v1d_0.11|+|+|
resnet50_v1d_0.37|+|+|
resnet50_v1d_0.48|+|+|
resnet50_v1d_0.86|+|+|
resnet50_v1e|+|Error (Failed loading Parameter 'resnetv1e_batchnorm0_gamma' from saved params: shape incompatible expected (64,) vs saved (32,))|
resnet50_v1s|+|+|
resnet50_v2|+|+|
resnext101_32x4d|+|+|
resnext101_64x4d|+|+|
resnext50_32x4d|+|+|
se_resnext101_32x4d|+|+|
se_resnext101_64x4d|+|+|
se_resnext50_32x4d|+|+|
senet_154|+|+|
senet_154e|+|Error (Parameter 'features.11.0.downsample.1.weight' is missing...)|
squeezenet1.0|+|+|
squeezenet1.1|+|+|
shufflenet_v1|+|Error (Parameter 'shufflenetv10_conv0_weight' has not been initialized)|
shufflenet_v2|+|Error (Parameter 'shufflenetv20_conv0_weight' has not been initialized)|
vgg11|+|+|
vgg11_bn|+|+|
vgg13|+|+|
vgg13_bn|+|+|
vgg16|+|+|
vgg16_bn|+|+|
vgg19|+|+|
vgg19_bn|+|+|
xception|+|+|

### Object detection

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
custom_faster_rcnn_fpn|+|TypeError: custom_faster_rcnn_fpn() missing 1 required positional argument: 'classes'|
center_net_dla34_coco|+|Pretrained model for center_net_dla34_coco is not available.|
center_net_dla34_dcnv2_coco|+|Pretrained model for center_net_dla34_dcnv2_coco is not available.|
center_net_dla34_dcnv2_voc|+|Pretrained model for center_net_dla34_dcnv2_voc is not available.|
center_net_dla34_voc|+|Pretrained model for center_net_dla34_voc is not available.|
center_net_mobilenetv3_large_duc_coco|+|+|
center_net_mobilenetv3_large_duc_voc|+|+|
center_net_mobilenetv3_small_duc_coco|+|+|
center_net_mobilenetv3_small_duc_voc|+|+|
center_net_resnet101_v1b_coco|+|+|
center_net_resnet101_v1b_dcnv2_coco|+|+|
center_net_resnet101_v1b_dcnv2_voc|+|+|
center_net_resnet101_v1b_voc|+|+|
center_net_resnet18_v1b_coco|+|+|
center_net_resnet18_v1b_dcnv2_coco|+|+|
center_net_resnet18_v1b_dcnv2_voc|+|+|
center_net_resnet18_v1b_voc|+|+|
center_net_resnet50_v1b_coco|+|+|
center_net_resnet50_v1b_dcnv2_coco|+|+|
center_net_resnet50_v1b_dcnv2_voc|+|+|
center_net_resnet50_v1b_voc|+|+|
doublehead_rcnn_resnet50_v1b_voc|+|RuntimeError: Parameter 'doubleheadrcnn0_double_fc_dense0_weight' has not been initialized.|
dla34|+|-|
faster_rcnn_fpn_resnet101_v1d_coco|+|+|
faster_rcnn_fpn_resnet50_v1b_coco|+|+|
faster_rcnn_fpn_syncbn_resnest101_coco|+|+|
faster_rcnn_fpn_syncbn_resnest269_coco|+|+|
faster_rcnn_fpn_syncbn_resnest50_coco|+|+|
faster_rcnn_fpn_syncbn_resnet101_v1d_coco|+|Pretrained model for faster_rcnn_fpn_syncbn_resnet101_v1d_coco is not available.|
faster_rcnn_fpn_syncbn_resnet50_v1b_coco|+|Pretrained model for faster_rcnn_fpn_syncbn_resnet50_v1b_coco is not available.|
faster_rcnn_resnet101_v1d_coco|+|+|
faster_rcnn_resnet101_v1d_custom|+|TypeError: faster_rcnn_resnet101_v1d_custom() missing 1 required positional argument: 'classes'|
faster_rcnn_resnet101_v1d_voc|+|Pretrained model for faster_rcnn_resnet101_v1d_voc is not available.|
faster_rcnn_resnet50_v1b_coco|+|+|
faster_rcnn_resnet50_v1b_custom|+|TypeError: faster_rcnn_resnet50_v1b_custom() missing 1 required positional argument: 'classes'|
faster_rcnn_resnet50_v1b_voc|+|+|
ssd_300_mobilenet0.25_coco|+|Pretrained model for ssd_300_mobilenet0.25_coco is not available.|
ssd_300_mobilenet0.25_custom|+|TypeError: ssd_300_mobilenet0_25_custom() missing 1 required positional argument: 'classes'|
ssd_300_mobilenet0.25_voc|+|Pretrained model for ssd_300_mobilenet0.25_voc is not available.|
ssd_300_mobilenet1.0_lite_coco|+|Pretrained model for ssd_300_mobilenet1.0_coco is not available.|
ssd_300_resnet34_v1b_coco|+|+|
ssd_300_resnet34_v1b_custom|+|TypeError: ssd_300_resnet34_v1b_custom() missing 1 required positional argument: 'classes'|
ssd_300_resnet34_v1b_voc|+|Pretrained model for ssd_300_resnet34_v1b_voc is not available.|
ssd_300_vgg16_atrous_coco|+|+|
ssd_300_vgg16_atrous_custom|+|TypeError: ssd_300_vgg16_atrous_custom() missing 1 required positional argument: 'classes'|
ssd_300_vgg16_atrous_voc|+|+|
ssd_300_vgg16_atrous_voc_int8|+|-|
ssd_512_mobilenet1.0_coco|+|+|
ssd_512_mobilenet1.0_custom|+|TypeError: ssd_512_mobilenet1_0_custom() missing 1 required positional argument: 'classes'|
ssd_512_mobilenet1.0_voc|+|+|
ssd_512_mobilenet1.0_voc_int8|+|-|
ssd_512_resnet101_v2_voc|+|+|
ssd_512_resnet152_v2_voc|+|Pretrained model for ssd_512_resnet152_v2_voc is not available.|
ssd_512_resnet18_v1_coco|+|Pretrained model for ssd_512_resnet18_v1_coco is not available.|
ssd_512_resnet18_v1_voc|+|Pretrained model for ssd_512_resnet18_v1_voc is not available.|
ssd_512_resnet50_v1_coco|+|+|
ssd_512_resnet50_v1_custom|+|TypeError: ssd_512_resnet50_v1_custom() missing 1 required positional argument: 'classes'|
ssd_512_resnet50_v1_voc|+|+|
ssd_512_resnet50_v1_voc_int8|+|-|
ssd_512_vgg16_atrous_coco|+|+|
ssd_512_vgg16_atrous_custom|+|TypeError: ssd_512_vgg16_atrous_custom() missing 1 required positional argument: 'classes'|
ssd_512_vgg16_atrous_voc|+|+|
ssd_512_vgg16_atrous_voc_int8|+|-|
yolo3_darknet53_coco|+|+|
yolo3_darknet53_custom|+|TypeError: yolo3_darknet53_custom() missing 1 required positional argument: 'classes'|
yolo3_darknet53_voc|+|+|
yolo3_mobilenet0.25_coco|+|Pretrained model for yolo3_mobilenet0.25_coco is not available.|
yolo3_mobilenet0.25_custom|+|TypeError: yolo3_mobilenet0_25_custom() missing 1 required positional argument: 'classes'|
yolo3_mobilenet0.25_voc|+|Pretrained model for yolo3_mobilenet0.25_voc is not available.|
yolo3_mobilenet1.0_coco|+|+|
yolo3_mobilenet1.0_custom|+|TypeError: yolo3_mobilenet1_0_custom() missing 1 required positional argument: 'classes'|
yolo3_mobilenet1.0_voc|+|+|

### Semantic segmentation

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
danet_resnet101_citys|+|+|
danet_resnet50_citys|+|+|
deeplab_resnest101_ade|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnest200_ade|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnest269_ade|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnest50_ade|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnet101_ade|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnet101_citys|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnet101_coco|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnet101_coco_int8|+|-|
deeplab_resnet101_voc|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnet101_voc_int8|+|-|
deeplab_resnet152_coco|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnet152_voc|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnet50_ade|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_resnet50_citys|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,256,60,60]|
deeplab_v3b_plus_wideresnet_citys|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,60,60], got [1,256,80,80]|
fastscnn_citys|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,16,16], got [1,32,32,32]|
fcn_resnet101_ade|+|-|
fcn_resnet101_coco|+|+|
fcn_resnet101_coco_int8|+|-|
fcn_resnet101_voc|+|+|
fcn_resnet101_voc_int8|+|-|
fcn_resnet50_ade|+|-|
fcn_resnet50_voc|+|Pretrained model for fcn_resnet50_voc is not available.|
hrnet_w18_small_v1_s|+|Pretrained model for hrnet_w18_small_v1_seg is not available.|
hrnet_w18_small_v2_s|+|Pretrained model for hrnet_w18_small_v2_seg is not available.|
hrnet_w48_s|+|Pretrained model for hrnet_w48_seg is not available.|
icnet_resnet50_citys|+|MXNetError: Check failed: l == 1 || r == 1: operands could not be broadcast together with shapes [1,128,60,60] [1,128,64,64]|
icnet_resnet50_mhpv1|+|MXNetError: Check failed: l == 1 || r == 1: operands could not be broadcast together with shapes [1,128,60,60] [1,128,64,64]|
nasnet_4_1056|+|Pretrained model for nasnet_4_1056 is not available.|
nasnet_5_1538|+|Pretrained model for nasnet_5_1538 is not available.|
nasnet_6_4032|+|Pretrained model for nasnet_6_4032 is not available.|
nasnet_7_1920|+|Pretrained model for nasnet_7_1920 is not available.|
psp_resnet101_ade|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,512,60,60]|
psp_resnet101_citys|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,512,60,60]|
psp_resnet101_coco|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,512,60,60]|
psp_resnet101_coco_int8|+|-|
psp_resnet101_voc|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,512,60,60]|
psp_resnet101_voc_int8|+|-|
psp_resnet50_ade|+|MXNetError: Check failed: shape_assign(&(*in_shape)[i], dshape): Incompatible input shape: expected [1,-1,64,64], got [1,512,60,60]|

### Instance segmentation

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
custom_mask_rcnn_fpn|+|-|
mask_rcnn_fpn_resnet101_v1d_coco|+|-|
mask_rcnn_fpn_resnet18_v1b_coco|+|-|
mask_rcnn_fpn_resnet50_v1b_coco|+|-|
mask_rcnn_fpn_syncbn_mobilenet1_0_coco|+|-|
mask_rcnn_fpn_syncbn_resnet18_v1b_coco|+|-|
mask_rcnn_resnet101_v1d_coco|+|-|
mask_rcnn_resnet18_v1b_coco|+|-|
mask_rcnn_resnet50_v1b_coco|+|-|

### Pose estimation

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
alpha_pose_resnet101_v1b_coco|+|-|
mobile_pose_mobilenet1.0|+|-|
mobile_pose_mobilenetv2_1.0|+|-|
mobile_pose_mobilenetv3_large|+|-|
mobile_pose_mobilenetv3_small|+|-|
mobile_pose_resnet18_v1b|+|-|
mobile_pose_resnet50_v1b|+|-|
simple_pose_resnet101_v1b|+|-|
simple_pose_resnet101_v1b_int8|+|-|
simple_pose_resnet101_v1d|+|-|
simple_pose_resnet101_v1d_int8|+|-|
simple_pose_resnet152_v1b|+|-|
simple_pose_resnet152_v1d|+|-|
simple_pose_resnet18_v1b|+|-|
simple_pose_resnet18_v1b_int8|+|-|
simple_pose_resnet50_v1b|+|-|
simple_pose_resnet50_v1b_int8|+|-|
simple_pose_resnet50_v1d|+|-|
simple_pose_resnet50_v1d_int8|+|-|

### Action recognition

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
c3d_kinetics400|+|-|
i3d_inceptionv1_kinetics400|+|-|
i3d_inceptionv3_kinetics400|+|-|
i3d_nl10_resnet101_v1_kinetics400|+|-|
i3d_nl10_resnet50_v1_kinetics400|+|-|
i3d_nl5_resnet101_v1_kinetics400|+|-|
i3d_nl5_resnet50_v1_kinetics400|+|-|
i3d_resnet101_v1_kinetics400|+|-|
i3d_resnet50_v1_custom|+|-|
i3d_resnet50_v1_hmdb51|+|-|
i3d_resnet50_v1_kinetics400|+|-|
i3d_resnet50_v1_sthsthv2|+|-|
i3d_resnet50_v1_ucf101|+|-|
i3d_slow_resnet101_f16s4_kinetics700|+|-|
inceptionv1_hmdb51|+|-|
inceptionv1_kinetics400|+|-|
inceptionv1_sthsthv2|+|-|
inceptionv1_ucf101|+|-|
inceptionv3_hmdb51|+|-|
inceptionv3_kinetics400|+|-|
inceptionv3_kinetics400_int8|+|-|
inceptionv3_sthsthv2|+|-|
inceptionv3_ucf101|+|-|
inceptionv3_ucf101_int8|+|-|
p3d_resnet101_kinetics400|+|-|
p3d_resnet50_kinetics400|+|-|
r2plus1d_resnet101_kinetics400|+|-|
r2plus1d_resnet152_kinetics400|+|-|
r2plus1d_resnet18_kinetics400|+|-|
r2plus1d_resnet34_kinetics400|+|-|
r2plus1d_resnet50_kinetics400|+|-|
resnet101_v1b_kinetics400|+|-|
resnet101_v1b_sthsthv2|+|-|
resnet152_v1b_kinetics400|+|-|
resnet152_v1b_sthsthv2|+|-|
resnet18_v1b_kinetics400|+|-|
resnet18_v1b_kinetics400_int8|+|-|
resnet18_v1b_sthsthv2|+|-|
resnet34_v1b_kinetics400|+|-|
resnet34_v1b_sthsthv2|+|-|
resnet50_v1b_hmdb51|+|-|
resnet50_v1b_kinetics400|+|-|
resnet50_v1b_kinetics400_int8|+|-|
resnet50_v1b_sthsthv2|+|-|
resnet50_v1b_ucf101|+|-|
slowfast_16x8_resnet101_50_50_kinetics400|+|-|
slowfast_16x8_resnet101_kinetics400|+|-|
slowfast_4x16_resnet101_kinetics400|+|-|
slowfast_4x16_resnet50_custom|+|-|
slowfast_4x16_resnet50_kinetics400|+|-|
slowfast_8x8_resnet101_kinetics400|+|-|
slowfast_8x8_resnet50_kinetics400|+|-|
vgg16_hmdb51|+|-|
vgg16_kinetics400|+|-|
vgg16_sthsthv2|+|-|
vgg16_ucf101|+|-|
vgg16_ucf101_int8|+|-|

### Depth prediction

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
monodepth2_resnet18_kitti_mono_640x192|+|-|
monodepth2_resnet18_kitti_mono_stereo_640x192|+|-|
monodepth2_resnet18_kitti_stereo_640x192|+|-|
monodepth2_resnet18_posenet_kitti_mono_640x192|+|-|
monodepth2_resnet18_posenet_kitti_mono_stereo_640x192|+|-|

### Image classification on Cifar-10

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
cifar_residualattentionnet452|+|-|
cifar_residualattentionnet56|+|-|
cifar_residualattentionnet92|+|-|
cifar_resnet110_v1|+|-|
cifar_resnet110_v2|+|-|
cifar_resnet20_v1|+|-|
cifar_resnet20_v2|+|-|
cifar_resnet56_v1|+|-|
cifar_resnet56_v2|+|-|
cifar_resnext29_16x64d|+|-|
cifar_resnext29_32x4d|+|-|
cifar_wideresnet16_10|+|-|
cifar_wideresnet28_10|+|-|
cifar_wideresnet40_8|+|-|

### Object tracking

Model | Availability in OMZ (2023.02.24)| Availability in the validation table |
-|-|-|
siamrpn_alexnet_v2_otb15|+|-|
