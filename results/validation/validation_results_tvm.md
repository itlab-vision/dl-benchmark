# Validation results for the models inferring using Apache TVM

## Public models

We infer models using the following APIs:

1. Source framework (Python API), where these models were trained.
   For example, we represent below the command line for the googlenet-v1
   model trained using Caffe.

   ```bash
   python inference_caffe.py -m googlenet-v1.prototxt \
                             -w googlenet-v1.caffemodel \
                             -i data/ -b 4 -t classification \
                             --mean 104.0 117.0 123.0
   ```

1. TVM (Python API), when we load models directly from source format.

   ```bash
   python inference_tvm_caffe.py -t classification -is 4 3 224 224 \
                                 -m googlenet-v1.prototxt \
                                 -w googlenet-v1.caffemodel \
                                 -i data/ --mean 0.408 0.459 0.482 -b 4 \
                                 -l labels/image_net_synset.txt \
                                 --layout NCHW --channel_swap 2 1 0 \
                                 --not_softmax
   ```

1. TVM (Python API) for models converted from the source format to the TVM one.
   For example, we represent below the command line for the `googlenet-v1`
   model trained using Caffe and converted into TVM format. Supposed that
   converted models should be copied into the `inference` directory.

   ```bash
   cd ../model_converters
   python caffe_to_tvm_converter.py -mn googlenet-v1 -is 4 3 224 224 \
                                 -m googlenet-v1.prototxt \
                                 -w googlenet-v1.caffemodel
   cd ../inference
   python inference_tvm.py -mn googlenet-v1 -m googlenet-v1.json \
                           -w googlenet-v1.params -i data/ -b 4 \
                           -l labels/image_net_synset.txt -is 4 3 224 224 \
                           --not_softmax -t classification \
                           --channel_swap 2 1 0 --layout NCHW \
                           --input_name data --mean 0.408 0.459 0.482
   ```

1. TVM (Python API) for models optimized using TVM tuning methods.
   Supposed that converted models should be copied into
   the `inference` directory.

   ```bash
   cd ../tvm_auto_tuning
   python tvm_meta_schedule.py -m googlenet-v1.json \
                               -p googlenet-v1.params \
                               -t "llvm -mcpu=core-avx2 --num-cores=6" \
                               -n 64 --max_trials_per_task 4 \
                               -o googlenet-v1.so
   cd ../inference
   python inference_tvm.py -mn googlenet-v1 -m googlenet-v1.so \
                           -w googlenet-v1.params -i data/ -b 4 \
                           -l labels/image_net_synset.txt -is 4 3 224 224 \
                           --not_softmax -t classification \
                           --channel_swap 2 1 0 --layout NCHW \
                           --input_name data --mean 0.408 0.459 0.482
   ```

1. TVM (Python API) to run on RISCV-V, we compiled the model on the host.

   ```bash
   cd model_converters/tvm_converter/
   python tvm_compiler.py -m googlenet-v1.json \
                          -p googlenet-v1.params \
                          -t "llvm -mtriple=riscv64-unknown-linux-gnu -mcpu=generic-rv64 -mabi=lp64d -mattr=+64bit,+m,+a,+f,+d,+c" \
                          --opt_level 0 --lib_name googlenet-v1.tar
   ```

   The model compiled into the archive was then launched on the device.

   ```bash
   cd model_converters/tvm_converter/
   python inference_tvm.py -is 1 3 224 224 -i ILSVRC2012_val_00000023.JPEG \
                           -t classification -m caffe_googlenetv1_1_3_224_224_data.tar \
                           -b 1 -l labels/image_net_synset.txt -ol 0 -in data --layout NCHW \
                           --mean 0.408 0.459 0.482 --channel_swap 2 1 0 --not_softmax
   ```

**Notes**:

1. TensorFlow models were converted to ONNX format using
   [tensorflow-onnx](https://github.com/onnx/tensorflow-onnx) according
   to the developers' recommendations. We represent below command lines
   to convert several validated models. Supposed that all commands
   are executed from the directory used to download models from OMZ.
   
   ```bash
   cd public/densenet-121-tf
   python -m tf2onnx.convert --saved-model densenet-121.savedmodel/ --output densenet-121-tf.onnx

   cd public/efficientnet-b0/efficientnet-b0
   python -m tf2onnx.convert --saved-model saved_model/ --output efficientnet-b0.onnx

   cd public/googlenet-v4-tf
   python -m tf2onnx.convert --graphdef inception_v4.frozen.pb \
          --output inception_v4.onnx \
          --inputs input:0 --outputs InceptionV4/Logits/Predictions:0
   ```

### Image classification

#### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) | Python API (TVM, TVM format, optimized) | Python API (TVM, TVM format, RISC-V)  |
-|-|-|-|-|-|-|-|
densenet-121-tf | TensorFlow | Source and inference frameworks<br>Mean: [123.68,116.78,103.94]<br>Std: [58.395,57.12,57.375] | 0.9525882 Granny Smith<br>0.0132317 orange<br>0.0123400 lemon<br>0.0028143 banana<br>0.0020237 piggy bank, penny bank | 0.9525879 Granny Smith<br>0.0132317 orange<br>0.0123400 lemon<br>0.0028143 banana<br>0.0020238 piggy bank, penny bank | 0.9525879 Granny Smith<br>0.0132317 orange<br>0.0123400 lemon<br>0.0028143 banana<br>0.0020238 piggy bank, penny bank | 0.9525878 Granny Smith<br>0.0132318 orange<br>0.0123400 lemon<br>0.0028143 banana<br>0.0020237 piggy bank, penny bank | 0.9525879 Granny Smith<br>0.0132317 orange<br>0.0123400 lemon<br>0.0028143 banana<br>0.0020238 piggy bank, penny bank |
efficientnet-b0 | TensorFlow | Source and inference frameworks<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] | 10733.9218750 Granny Smith<br>9574.2392578 pomegranate<br>8067.0537109 hip, rose hip, rosehip<br>7369.9067383 brambling, Fringilla montifringilla<br>7041.4887695 ptarmigan | 10733.8427734 Granny Smith<br>9574.1689453 pomegranate<br>8067.0004883 hip, rose hip, rosehip<br>7369.8447266 brambling, Fringilla montifringilla<br>7041.4487305 ptarmigan | 10733.8427734 Granny Smith<br>9574.1689453 pomegranate<br>8067.0004883 hip, rose hip, rosehip<br>7369.8447266 brambling, Fringilla montifringilla<br>7041.4487305 ptarmigan | 10733.8427734 Granny Smith<br>9574.1708984 pomegranate<br>8067.0019531 hip, rose hip, rosehip<br>7369.8471680 brambling, Fringilla montifringilla<br>7041.4467773 ptarmigan | 10733.8300781 Granny Smith<br>9574.1572266 pomegranate<br>8066.9912109 hip, rose hip, rosehip<br>7369.8349609 brambling, Fringilla montifringilla<br>7041.4394531 ptarmigan |
googlenet-v1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0]<br><br>Inference framework<br>Mean: [0.408,0.459,0.482]<br>Std: None |  0.9979934 Granny Smith<br>0.0007394 bell pepper<br>0.0006985 candle, taper, wax light<br>0.0000942 tennis ball<br>0.0000636 cucumber, cuke | 0.9976785 Granny Smith<br>0.0008789 bell pepper<br>0.0007508 candle, taper, wax light<br>0.0001099 tennis ball<br>0.0000757 cucumber, cuke | 0.9976785 Granny Smith<br>0.0008789 bell pepper<br>0.0007508 candle, taper, wax light<br>0.0001099 tennis ball<br>0.0000757 cucumber, cuke | 0.9976785 Granny Smith<br>0.0008789 bell pepper<br>0.0007508 candle, taper, wax light<br>0.0001099 tennis ball<br>0.0000757 cucumber, cuke | 0.9976785 Granny Smith<br>0.0008789 bell pepper<br>0.0007508 candle, taper, wax light<br>0.0001099 tennis ball<br>0.0000757 cucumber, cuke |
googlenet-v4-tf | TensorFlow | Source and inference frameworks<br>Mean: [127.5,127.5,127.5]<br>Std: [127.5,127.5,127.5] | 0.9935190 Granny Smith<br>0.0002230 Rhodesian ridgeback<br>0.0000956 pineapple, ananas<br>0.0000868 hair slide<br>0.0000775 banana | 0.9934986 Granny Smith<br>0.0002234 Rhodesian ridgeback<br>0.0000959 pineapple, ananas<br>0.0000871 hair slide<br>0.0000778 banana | 0.9934986 Granny Smith<br>0.0002234 Rhodesian ridgeback<br>0.0000959 pineapple, ananas<br>0.0000871 hair slide<br>0.0000778 banana | 0.9934986 Granny Smith<br>0.0002234 Rhodesian ridgeback<br>0.0000959 pineapple, ananas<br>0.0000871 hair slide<br>0.0000778 banana | 0.9934986 Granny Smith<br>0.0002234 Rhodesian ridgeback<br>0.0000959 pineapple, ananas<br>0.0000871 hair slide<br>0.0000778 banana|
resnet-50-pytorch | PyTorch | Source framework<br>Mean: [123.675,116.28,103.53]<br>Std: [58.395,57.12,57.375]<br><br>Inference framework<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229, 0.224, 0.225] | 0.9278084 Granny Smith<br>0.0129410 orange<br>0.0059574 lemon<br>0.0042141 necklace<br>0.0025712 banana | 0.9278086 Granny Smith<br>0.0129410 orange<br>0.0059573 lemon<br>0.0042141 necklace<br>0.0025712 banana | 0.9278079 Granny Smith<br>0.0129411 orange<br>0.0059574 lemon<br>0.0042141 necklace<br>0.0025712 banana | 0.9278075 Granny Smith<br>0.0129411 orange<br>0.0059574 lemon<br>0.0042142 necklace<br>0.0025712 banana | 11.9825869 Granny Smith<br>7.7101669 orange<br>6.9343958 lemon<br>6.5882053 necklace<br>6.0941405 banana |
squeezenet1.1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0]<br><br>Inference framework<br>Mean: [0.408,0.459,0.482]<br>Std: None | 0.9993550 Granny Smith<br>0.0004808 tennis ball<br>0.0000693 fig<br>0.0000318 lemon<br>0.0000192 piggy bank, penny bank | 0.9995996 Granny Smith<br>0.0002680 tennis ball<br>0.0000614 fig<br>0.0000253 lemon<br>0.0000120 banana | 0.9995933 Granny Smith<br>0.0002719 tennis ball<br>0.0000625 fig<br>0.0000258 lemon<br>0.0000121 piggy bank, penny bank | 0.9995933 Granny Smith<br>0.0002719 tennis ball<br>0.0000625 fig<br>0.0000258 lemon<br>0.0000121 piggy bank, penny bank | 0.9995933 Granny Smith<br>0.0002719 tennis ball<br>0.0000625 fig<br>0.0000258 lemon<br>0.0000121 piggy bank, penny bank |

#### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) | Python API (TVM, TVM format, optimized) | Python API (TVM, TVM format, RISC-V) |
-|-|-|-|-|-|-|-|
densenet-121-tf | TensorFlow | Source and inference frameworks<br>Mean: [123.68,116.78,103.94]<br>Std: [58.395,57.12,57.375] | 0.9847540 junco, snowbird<br>0.0068680 chickadee<br>0.0034511 brambling, Fringilla montifringilla<br>0.0015685 water ouzel, dipper<br>0.0012343 indigo bunting, indigo finch, indigo bird, Passerina cyanea |  0.9847607 junco, snowbird<br>0.0068680 chickadee<br>0.0034511 brambling, Fringilla montifringilla<br>0.0015686 water ouzel, dipper<br>0.0012343 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9847607 junco, snowbird<br>0.0068680 chickadee<br>0.0034511 brambling, Fringilla montifringilla<br>0.0015686 water ouzel, dipper<br>0.0012343 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9847606 junco, snowbird<br>0.0068680 chickadee<br>0.0034511 brambling, Fringilla montifringilla<br>0.0015685 water ouzel, dipper<br>0.0012343 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9847606 junco, snowbird<br>0.0068680 chickadee<br>0.0034511 brambling, Fringilla montifringilla<br>0.0015685 water ouzel, dipper<br>0.0012343 indigo bunting, indigo finch, indigo bird, Passerina cyanea |
efficientnet-b0 | TensorFlow | Source and inference frameworks<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] | 2070.9409180 can opener, tin opener<br>1669.3304443 strawberry<br>1631.1007080 packet<br>1586.7080078 bell pepper<br>1466.7904053 clog, geta, patten, sabot | 2070.9316406 can opener, tin opener<br>1669.8526611 strawberry<br>1631.7509766 packet<br>1587.4012451 bell pepper<br>1467.0465088 clog, geta, patten, sabot | 2070.9316406 can opener, tin opener<br>1669.8526611 strawberry<br>1631.7509766 packet<br>1587.4012451 bell pepper<br>1467.0465088 clog, geta, patten, sabot |  2070.9113770 can opener, tin opener<br>1670.3059082 strawberry<br>1632.3061523 packet<br>1587.9982910 bell pepper<br>1467.2674561 clog, geta, patten, sabot | 2070.9294434 can opener, tin opener<br>1670.0102539 strawberry<br>1631.9293213 packet<br>1587.5979004 bell pepper<br>1467.1268311 clog, geta, patten, sabot | 
googlenet-v1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0]<br><br>Inference framework<br>Mean: [0.408,0.459,0.482]<br>Std: None | 0.9999735 junco, snowbird<br>0.0000203 chickadee<br>0.0000020 brambling, Fringilla montifringilla<br>0.0000016 house finch, linnet, Carpodacus mexicanus<br>0.0000016 water ouzel, dipper | 0.9999769 junco, snowbird<br>0.0000183 chickadee<br>0.0000017 brambling, Fringilla montifringilla<br>0.0000013 water ouzel, dipper<br>0.0000012 house finch, linnet, Carpodacus mexicanus | 0.9999769 junco, snowbird<br>0.0000183 chickadee<br>0.0000017 brambling, Fringilla montifringilla<br>0.0000013 water ouzel, dipper<br>0.0000012 house finch, linnet, Carpodacus mexicanus | 0.9999769 junco, snowbird<br>0.0000183 chickadee<br>0.0000017 brambling, Fringilla montifringilla<br>0.0000013 water ouzel, dipper<br>0.0000012 house finch, linnet, Carpodacus mexicanus | 0.9999769 junco, snowbird<br>0.0000183 chickadee<br>0.0000017 brambling, Fringilla montifringilla<br>0.0000013 water ouzel, dipper<br>0.0000012 house finch, linnet, Carpodacus mexicanus |
googlenet-v4-tf | TensorFlow | Source and inference frameworks<br>Mean: [127.5,127.5,127.5]<br>Std: [127.5,127.5,127.5] | 0.9398882 junco, snowbird<br>0.0005928 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005351 chickadee<br>0.0005287 brambling, Fringilla montifringilla<br>0.0004131 house finch, linnet, Carpodacus mexicanus | 0.9399365 junco, snowbird<br>0.0005925 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005340 chickadee<br>0.0005273 brambling, Fringilla montifringilla<br>0.0004121 house finch, linnet, Carpodacus mexicanus | 0.9399365 junco, snowbird<br>0.0005925 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005340 chickadee<br>0.0005273 brambling, Fringilla montifringilla<br>0.0004121 house finch, linnet, Carpodacus mexicanus | 0.9399366 junco, snowbird<br>0.0005925 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005340 chickadee<br>0.0005273 brambling, Fringilla montifringilla<br>0.0004121 house finch, linnet, Carpodacus mexicanus | 0.9399366 junco, snowbird<br>0.0005925 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005340 chickadee<br>0.0005273 brambling, Fringilla montifringilla<br>0.0004121 house finch, linnet, Carpodacus mexicanus |
resnet-50-pytorch | PyTorch | Source framework<br>Mean: [123.675,116.28,103.53]<br>Std: [58.395,57.12,57.375]<br><br>Inference framework<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229, 0.224, 0.225] | 0.9805019 junco, snowbird<br>0.0049154 goldfinch, Carduelis carduelis<br>0.0039196 chickadee<br>0.0038097 water ouzel, dipper<br>0.0028983 brambling, Fringilla montifringilla | 0.9805013 junco, snowbird<br>0.0049155 goldfinch, Carduelis carduelis<br>0.0039196 chickadee<br>0.0038098 water ouzel, dipper<br>0.0028983 brambling, Fringilla montifringilla | 0.9805013 junco, snowbird<br>0.0049154 goldfinch, Carduelis carduelis<br>0.0039196 chickadee<br>0.0038098 water ouzel, dipper<br>0.0028983 brambling, Fringilla montifringilla | 0.9805013 junco, snowbird<br>0.0049155 goldfinch, Carduelis carduelis<br>0.0039196 chickadee<br>0.0038098 water ouzel, dipper<br>0.0028983 brambling, Fringilla montifringilla | 16.2264042 junco, snowbird<br>10.9307261 goldfinch, Carduelis carduelis<br>10.7043276 chickadee<br>10.6759119 water ouzel, dipper<br>10.4024792 brambling, Fringilla montifringilla |
squeezenet1.1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0]<br><br>Inference framework<br>Mean: [0.408,0.459,0.482]<br>Std: None | 0.9897482 junco, snowbird<br>0.0094914 chickadee<br>0.0003794 brambling, Fringilla montifringilla<br>0.0002046 jay<br>0.0001124 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9902447 junco, snowbird<br>0.0087432 chickadee<br>0.0005967 brambling, Fringilla montifringilla<br>0.0002337 jay<br>0.0001153 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9904969 junco, snowbird<br>0.0084961 chickadee<br>0.0005932 brambling, Fringilla montifringilla<br>0.0002311 jay<br>0.0001166 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9904970 junco, snowbird<br>0.0084961 chickadee<br>0.0005932 brambling, Fringilla montifringilla<br>0.0002311 jay<br>0.0001166 indigo bunting, indigo finch, indigo bird, Passerina cyanea | 0.9904970 junco, snowbird<br>0.0084961 chickadee<br>0.0005932 brambling, Fringilla montifringilla<br>0.0002311 jay<br>0.0001166 indigo bunting, indigo finch, indigo bird, Passerina cyanea |

#### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿
<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Source Framework | Parameters | Python API (source framework) | Python API (TVM, source format) | Python API (TVM, TVM format) | Python API (TVM, TVM format, optimized) | Python API (TVM, TVM format, RISC-V) |
-|-|-|-|-|-|-|-|
densenet-121-tf | TensorFlow | Source and inference frameworks<br>Mean: [123.68,116.78,103.94]<br>Std: [58.395,57.12,57.375] | 0.3048036 liner, ocean liner<br>0.1327114 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1180263 container ship, containership, container vessel<br>0.0794732 drilling platform, offshore rig<br>0.0718437 dock, dockage, docking facility | 0.3048043 liner, ocean liner<br>0.1327112 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1180268 container ship, containership, container vessel<br>0.0794735 drilling platform, offshore rig<br>0.0718434 dock, dockage, docking facility | 0.3048043 liner, ocean liner<br>0.1327112 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1180268 container ship, containership, container vessel<br>0.0794735 drilling platform, offshore rig<br>0.0718434 dock, dockage, docking facility | 0.3048046 liner, ocean liner<br>0.1327105 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1180269 container ship, containership, container vessel<br>0.0794733 drilling platform, offshore rig<br>0.0718436 dock, dockage, docking facility | 0.3048047 liner, ocean liner<br>0.1327110 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1180270 container ship, containership, container vessel<br>0.0794734 drilling platform, offshore rig<br>0.0718434 dock, dockage, docking facility |
efficientnet-b0 | TensorFlow | Source and inference frameworks<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] | 33649.5468750 bow tie, bow-tie, bowtie<br>28028.8417969 cannon<br>20405.7363281 stole<br>20352.2265625 seat belt, seatbelt<br>19862.9375000 picket fence, paling | 33649.5625000 bow tie, bow-tie, bowtie<br>28028.8437500 cannon<br>20405.7304688 stole<br>20352.2050781 seat belt, seatbelt<br>19862.9296875 picket fence, paling | 33649.5625000 bow tie, bow-tie, bowtie<br>28028.8437500 cannon<br>20405.7304688 stole<br>20352.2050781 seat belt, seatbelt<br>19862.9296875 picket fence, paling | 33649.5273438 bow tie, bow-tie, bowtie<br>28028.8671875 cannon<br>20405.7480469 stole<br>20352.2207031 seat belt, seatbelt<br>19862.9316406 picket fence, paling | 33649.6367188 bow tie, bow-tie, bowtie<br>28028.8105469 cannon<br>20405.7109375 stole<br>20352.2089844 seat belt, seatbelt<br>19862.9707031 picket fence, paling |
googlenet-v1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0]<br><br>Inference framework<br>Mean: [0.408,0.459,0.482]<br>Std: None | 0.4644058 lifeboat<br>0.2018610 drilling platform, offshore rig<br>0.0871761 container ship, containership, container vessel<br>0.0759982 liner, ocean liner<br>0.0714861 beacon, lighthouse, beacon light, pharos | 0.4967317 lifeboat<br>0.1832319 drilling platform, offshore rig<br>0.0923501 container ship, containership, container vessel<br>0.0744570 liner, ocean liner<br>0.0563448 beacon, lighthouse, beacon light, pharos | 0.4967317 lifeboat<br>0.1832319 drilling platform, offshore rig<br>0.0923501 container ship, containership, container vessel<br>0.0744570 liner, ocean liner<br>0.0563448 beacon, lighthouse, beacon light, pharos | 0.4967313 lifeboat<br>0.1832318 drilling platform, offshore rig<br>0.0923506 container ship, containership, container vessel<br>0.0744572 liner, ocean liner<br>0.0563449 beacon, lighthouse, beacon light, pharos | 0.4967318 lifeboat<br>0.1832316 drilling platform, offshore rig<br>0.0923504 container ship, containership, container vessel<br>0.0744568 liner, ocean liner<br>0.0563448 beacon, lighthouse, beacon light, pharos |
googlenet-v4-tf | TensorFlow | Source and inference frameworks<br>Mean: [127.5,127.5,127.5]<br>Std: [127.5,127.5,127.5] | 0.4689647 beacon, lighthouse, beacon light, pharos<br>0.1695168 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0433668 lifeboat<br>0.0310355 fireboat<br>0.0150613 dock, dockage, docking facility | 0.4704958 beacon, lighthouse, beacon light, pharos<br>0.1695943 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0431099 lifeboat<br>0.0307508 fireboat<br>0.0149647 dock, dockage, docking facility |  0.4704958 beacon, lighthouse, beacon light, pharos<br>0.1695943 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0431099 lifeboat<br>0.0307508 fireboat<br>0.0149647 dock, dockage, docking facility | 0.4704947 beacon, lighthouse, beacon light, pharos<br>0.1695949 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0431100 lifeboat<br>0.0307508 fireboat<br>0.0149647 dock, dockage, docking facility | 0.4704950 beacon, lighthouse, beacon light, pharos<br>0.1695948 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0431099 lifeboat<br>0.0307508 fireboat<br>0.0149647 dock, dockage, docking facility |
resnet-50-pytorch | PyTorch | Source framework<br>Mean: [123.675,116.28,103.53]<br>Std: [58.395,57.12,57.375]<br><br>Inference framework<br>Mean: [0.485,0.456,0.406]<br>Std: [0.229,0.224,0.225] | 0.4759621 liner, ocean liner<br>0.1025402 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0690002 container ship, containership, container vessel<br>0.0524496 dock, dockage, docking facility<br>0.0473782 pirate, pirate ship | 0.4759649 liner, ocean liner<br>0.1025411 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0689997 container ship, containership, container vessel<br>0.0524497 dock, dockage, docking facility<br>0.0473772 pirate, pirate ship | 0.4759648 liner, ocean liner<br>0.1025408 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0689995 container ship, containership, container vessel<br>0.0524497 dock, dockage, docking facility<br>0.0473774 pirate, pirate ship | 0.4759627 liner, ocean liner<br>0.1025414 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0689999 container ship, containership, container vessel<br>0.0524496 dock, dockage, docking facility<br>0.0473778 pirate, pirate ship | 10.1021738 liner, ocean liner<br>8.5670938 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>8.1709299 container ship, containership, container vessel<br>7.8966804 dock, dockage, docking facility<br>7.7949758 pirate, pirate ship |
squeezenet1.1 | Caffe | Source framework<br>Mean: [104.0,117.0,123.0]<br><br>Inference framework<br>Mean: [0.408,0.459,0.482]<br>Std: None | 0.5661172 lifeboat<br>0.2700349 drilling platform, offshore rig<br>0.0876362 liner, ocean liner<br>0.0250453 container ship, containership, container vessel<br>0.0135069 submarine, pigboat, sub, U-boat | 0.6992825 lifeboat<br>0.1367239 drilling platform, offshore rig<br>0.0986513 liner, ocean liner<br>0.0202083 container ship, containership, container vessel<br>0.0170821 submarine, pigboat, sub, U-boat | 0.6996598 lifeboat<br>0.1369749 drilling platform, offshore rig<br>0.0978115 liner, ocean liner<br>0.0204584 container ship, containership, container vessel<br>0.0170495 submarine, pigboat, sub, U-boat | 0.6996598 lifeboat<br>0.1369744 drilling platform, offshore rig<br>0.0978120 liner, ocean liner<br>0.0204584 container ship, containership, container vessel<br>0.0170495 submarine, pigboat, sub, U-boat | 0.6996594 lifeboat<br>0.1369754 drilling platform, offshore rig<br>0.0978113 liner, ocean liner<br>0.0204583 container ship, containership, container vessel<br>0.0170496 submarine, pigboat, sub, U-boat |

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
ssd_512_resnet50_v1_coco | MXNet | Source framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225]<br><br>Inference framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225] | Bounding box:<br>APPLE (261, 197), (421, 409); APPLE (50, 167), (168, 345); APPLE (213, 133), (315, 288); APPLE (309, 147), (443, 291); APPLE (177, 134), (440, 396); APPLE (134, 177), (298, 385) | Bounding box:<br>APPLE (261, 197), (421, 409); APPLE (50, 167), (168, 345); APPLE (213, 133), (315, 288); APPLE (309, 147), (443, 291); APPLE (177, 134), (440, 396); APPLE (134, 177), (298, 385) | Bounding box:<br>APPLE (261, 197), (421, 409); APPLE (50, 167), (168, 345); APPLE (213, 133), (315, 288); APPLE (309, 147), (443, 291); APPLE (177, 134), (440, 396); APPLE (134, 177), (298, 385) |
ssd_512_mobilenet1.0_coco | MXNet | Source framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225]<br><br>Inference framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225] | Bounding box:<br>APPLE (280, 209), (422, 414); APPLE (54, 168), (165, 353); APPLE (137, 203), (263, 385); APPLE (215, 133), (316, 292) | Bounding box:<br>APPLE (280, 209), (422, 414); APPLE (54, 168), (165, 353); APPLE (137, 203), (263, 385); APPLE (215, 133), (316, 292) | Bounding box:<br>APPLE (280, 209), (422, 414); APPLE (54, 168), (165, 353); APPLE (137, 203), (263, 385); APPLE (215, 133), (316, 292) | 

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
ssd_512_resnet50_v1_coco | MXNet | Source framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225]<br><br>Inference framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225] | Bounding box:<br> BIRD (65, 94), (354, 486) | Bounding box:<br> BIRD (65, 94), (354, 486) | Bounding box:<br> BIRD (65, 94), (354, 486) |
ssd_512_vgg16_atrous_voc | MXNet | Source framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225]<br><br>Inference framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225] | Bounding box:<br>BIRD (78, 107), (359, 452) | Bounding box:<br>BIRD (78, 107), (359, 452) | Bounding box:<br>BIRD (78, 107), (359, 452) |
ssd_300_vgg16_atrous_voc | MXNet | Source framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225]<br><br>Inference framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225] | Bounding box:<br>BIRD (38, 56), (205, 272) | Bounding box:<br>BIRD (38, 56), (205, 272) | Bounding box:<br>BIRD (38, 56), (205, 272) |
ssd_512_mobilenet1.0_coco | MXNet | Source framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225]<br><br>Inference framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225] | Bounding box:<br>BIRD (86, 100), (347, 450) | Bounding box:<br>BIRD (86, 100), (347, 450) | Bounding box:<br>BIRD (86, 100), (347, 450) |

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
ssd_512_resnet50_v1_coco | MXNet | Source framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225]<br><br>Inference framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225] | Bounding box:<br>PERSON (75, 96), (153, 478); HORSE (121, 58), (424, 454) | Bounding box:<br>PERSON (75, 96), (153, 478); HORSE (121, 58), (424, 454) | Bounding box:<br>PERSON (75, 96), (153, 478); HORSE (121, 58), (424, 454) |
ssd_512_mobilenet1.0_coco | MXNet | Source framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225]<br><br>Inference framework<br>Mean: [0.485, 0.456, 0.406]<br>Std: [0.229, 0.224, 0.225] | Bounding box:<br>PERSON (70, 89), (164, 470); HORSE (126, 57), (391, 469) | Bounding box:<br>PERSON (70, 89), (164, 470); HORSE (126, 57), (391, 469) | Bounding box:<br>PERSON (70, 89), (164, 470); HORSE (126, 57), (391, 469) |


<!-- LINKS -->
[imagenet]: http://www.image-net.org
[ms_coco]: http://cocodataset.org
[wider_face_dataset]: http://shuoyang1213.me/WIDERFACE
