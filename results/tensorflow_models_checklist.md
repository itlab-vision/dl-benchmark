# Model validation and performance analysis status for Intel® Optimizations for TensorFlow

## Public models (Open Model Zoo)

Represented deep models are available in [Open Model Zoo][omz].

### Image classification

Model | Availability in OMZ (2023.03.04)| Availability in the validation table |
-|-|-|
densenet-121-tf|+|- (Error parsing message with type 'tensorflow.GraphDef')|
efficientnet-b0|+|- ('NoneType' object is not iterable)|
googlenet-v1-tf (inceptionv1)|+|-|
googlenet-v2-tf (inceptionv2)|+|-|
googlenet-v3 (inceptionv3)|+|-|
googlenet-v4-tf (inceptionv4)|+|-|
inception-resnet-v2-tf|+|+|
mixnet-l|+|- ('NoneType' object is not iterable)|
mobilenet-v1-1.0-224-tf|+|+|
mobilenet-v2-1.0-224|+|+|
mobilenet-v2-1.4-224|+|+|
mobilenet-v3-small-1.0-224-tf|+|- (Error parsing message with type 'tensorflow.GraphDef')|
mobilenet-v3-large-1.0-224-tf|+|- (Error parsing message with type 'tensorflow.GraphDef')|
resnet-50-tf|+|+|

**Notes**:

1. Inference implementation for GoogleNet-models supported
   for batch size that equals 1.
1. Inference of densenet-121-tf, efficientnet-b0, mobilenet-v3-*,
   mixnet-l fails.
1. Models stored in ckpt- and h5-formats in OMZ converted into pb-format
   using `omz_converter`:

   ```bash
   omz_downloader --name <model_name>
   # export is required for GoogleNet-models
   export PYTHONPATH=`pwd`:`pwd`/public/<model_name>/models/research/slim
   omz_converter --name <model_name>
   ```

### Object detection

Model | Availability in OMZ (2023.03.04)| Availability in the validation table |
-|-|-|
ctpn|+|-|
efficientdet-d0|+|-|
efficientdet-d1|+|-|
faster_rcnn_inception_resnet_v2_atrous_coco|+|-|
faster_rcnn_resnet50_coco|+|-|
retinanet|+|-|
rfcn-resnet101-coco|+|-|
ssd_mobilenet_v1_coco|+|-|
ssd_mobilenet_v1_fpn_coco|+|-|
ssdlite_mobilenet_v2|+|-|

### Semantic segmentation

Model | Availability in OMZ (2023.03.04)| Availability in the validation table |
-|-|-|
deeplabv3|+|-|

### Instance segmentation

Model | Availability in OMZ (2023.03.04)| Availability in the validation table |
-|-|-|
mask_rcnn_resnet50_atrous_coco|+|-|
mask_rcnn_inception_resnet_v2_atrous_coco|+|-|

### Other models

There are deep models for solving non-classical computer vision tasks. The complete
list is available [here][omz-other].


<!-- LINKS -->
[omz]: https://github.com/openvinotoolkit/open_model_zoo
[omz-other]: https://github.com/openvinotoolkit/open_model_zoo/blob/master/models/public/index.md
