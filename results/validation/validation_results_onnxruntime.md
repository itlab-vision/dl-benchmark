# Validation results for the models inferring using Onnxruntime

## Image classification

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Parameters | Python | C++ |
-|-|-|-|
bvlcalexnet-12-int8 | - | - | 0.8704010 Granny Smith<br>0.0510130 tennis ball<br>0.0309220 candle, taper, wax light<br>0.0096150 whistle<br>0.0058280 acorn |
bvlcalexnet-12 | - | - | 0.9295540 Granny Smith<br>0.0125680 piggy bank, penny bank<br>0.0090160 saltshaker, salt shaker<br>0.0077320 candle, taper, wax light<br>0.0068970 bell pepper |
caffenet-12.onnx | - | - | 0.8508970 Granny Smith<br>0.0712500 candle, taper, wax light<br>0.0116690 tennis ball<br>0.0086440 teapot<br>0.0053500 saltshaker, salt shaker |
densenet-12.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 15.9237710 Granny Smith<br>10.0343250 lemon<br>9.1716430 orange<br>8.5298500 banana<br>7.3588000 tennis ball |
densenet-12-int8.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 15.6389210 Granny Smith<br>9.9765530 lemon<br>9.1676440 orange<br>8.3587340 banana<br>7.8194600 tennis ball |
efficientnet-lite4-11-int8.onnx | Mean values - [0.49,0.49,0.49]<br>scale values - [0.5,0.5,0.5] | - | - |
googlenet-12.onnx | - | - | 0.9977360 Granny Smith<br>0.0009890 bell pepper<br>0.0007630 candle, taper, wax light<br>0.0000700 tennis ball<br>0.0000660 cucumber, cuke |
googlenet-12-int8.onnx | - | - | 0.9957830 Granny Smith<br>0.0017750 bell pepper<br>0.0011640 candle, taper, wax light<br>0.0003280 tennis ball<br>0.0001740 fig |
inception-v1-12.onnx | - | - | 0.9996710 Granny Smith<br>0.0001990 bell pepper<br>0.0001050 candle, taper, wax light<br>0.0000050 tennis ball<br>0.0000040 cucumber, cuke |
inception-v1-12-int8.onnx | - | - | 0.8050320 tennis ball<br>0.1182330 jackfruit, jak, jack<br>0.0379760 green snake, grass snake<br>0.0118990 green mamba<br>0.0104580 window screen |
mobilenetv2-12.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 11.0181300 Granny Smith<br>8.8477180 saltshaker, salt shaker<br>7.8610690 candle, taper, wax light<br>7.8096080 pitcher, ewer<br>7.8034390 safety pin |
mobilenetv2-12-int8.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 10.4093980 pitcher, ewer<br>10.4093980 Granny Smith<br>9.7688200 saltshaker, salt shaker<br>9.1282420 safety pin<br>8.8079520 vase |
resnet152-v1-7.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 12.9891370 Granny Smith<br>8.0929860 candle, taper, wax light<br>7.8016590 piggy bank, penny bank<br>6.6749000 bell pepper<br>6.3451820 teapot |
shufflenet-v2-12.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 8.4884330 Granny Smith<br>6.5554310 safety pin<br>5.2545650 hair slide<br>5.2148540 piggy bank, penny bank<br>5.0002880 digital clock |
shufflenet-v2-12-int8.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 9.1372000 Granny Smith<br>7.4132000 clog, geta, patten, sabot<br>7.4132000 safety pin<br>6.8960000 hair slide<br>6.8960000 perfume, essence |
squeezenet1.0-12.onnx | - | - | 0.9922830 Granny Smith<br>0.0074650 tennis ball<br>0.0000500 fig<br>0.0000490 lemon<br>0.0000480 golf ball |
squeezenet1.0-12-int8.onnx | - | - | 0.8753350 Granny Smith<br>0.1133770 tennis ball<br>0.0022900 custard apple<br>0.0015800 candle, taper, wax light<br>0.0007510 lemon |
vgg16-12.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 15.3299900 Granny Smith<br>10.3456530 tennis ball<br>9.3599100 piggy bank, penny bank<br>9.3400680 maraca<br>9.3206130 teapot |
vgg16-12-int8.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 15.2753050 Granny Smith<br>11.6506570 pool table, billiard table, snooker table<br>11.6506570 tennis ball<br>10.3561390 piggy bank, penny bank<br>9.5794290 whistle |
zfnet512-12.onnx | - | - | 0.5735310 Granny Smith<br>0.0641960 tennis ball<br>0.0496170 acorn<br>0.0455580 bell pepper<br>0.0356390 fig |
zfnet512-12-int8.onnx | - | - | 0.5917680 Granny Smith<br>0.1210350 tennis ball<br>0.0368110 jackfruit, jak, jack<br>0.0247550 lemon<br>0.0247550 acorn |

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python | C++ |
-|-|-|-|
bvlcalexnet-12-int8 | - | - | 0.1778960 junco, snowbird<br>0.1078320 necklace<br>0.0468150 bonnet, poke bonnet<br>0.0468150 weevil<br>0.0396200 barn spider, Araneus cavaticus |
bvlcalexnet-12 | - | - | 0.9175600 junco, snowbird<br>0.0709890 chickadee<br>0.0055200 brambling, Fringilla montifringilla<br>0.0013350 water ouzel, dipper<br>0.0005600 bulbul |
caffenet-12.onnx | - | - | 0.9353690 junco, snowbird<br>0.0581420 chickadee<br>0.0027560 brambling, Fringilla montifringilla<br>0.0006080 house finch, linnet, Carpodacus mexicanus<br>0.0004240 water ouzel, dipper |
densenet-12.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 16.3927940 junco, snowbird<br>11.1731330 brambling, Fringilla montifringilla<br>10.9790870 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.3411000 chickadee<br>7.5422170 robin, American robin, Turdus migratorius |
densenet-12-int8.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 16.0433770 junco, snowbird<br>11.0550990 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>9.7069170 brambling, Fringilla montifringilla<br>9.3024620 chickadee<br>7.9542790 magpie |
efficientnet-lite4-11-int8.onnx | Mean values - [0.49,0.49,0.49]<br>scale values - [0.5,0.5,0.5] | - | - |
googlenet-12.onnx | - | - | 0.9999640 junco, snowbird<br>0.0000300 chickadee<br>0.0000020 house finch, linnet, Carpodacus mexicanus<br>0.0000020 brambling, Fringilla montifringilla<br>0.0000010 water ouzel, dipper |
googlenet-12-int8.onnx | - | - | 0.9971060 junco, snowbird<br>0.0014390 chickadee<br>0.0009440 house finch, linnet, Carpodacus mexicanus<br>0.0002660 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000750 brambling, Fringilla montifringilla |
inception-v1-12.onnx | - | - | 0.9999980 junco, snowbird<br>0.0000020 chickadee<br>0.0000000 toilet tissue, toilet paper, bathroom tissue<br>0.0000000 porcupine, hedgehog<br>0.0000000 wood rabbit, cottontail, cottontail rabbit |
inception-v1-12-int8.onnx | - | - | 0.9153430 window screen<br>0.0653530 fire screen, fireguard<br>0.0053790 shower curtain<br>0.0043200 mosquito net<br>0.0012040 electric fan, blower |
mobilenetv2-12.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 24.5555320 junco, snowbird<br>17.2104700 brambling, Fringilla montifringilla<br>716.0221560 chickadee<br>15.6419510 water ouzel, dipper<br>15.4459110 goldfinch, Carduelis carduelis |
mobilenetv2-12-int8.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 19.5376400 junco, snowbird<br>14.0927230 brambling, Fringilla montifringilla<br>13.7724340 chickadee<br>12.4912780 house finch, linnet, Carpodacus mexicanus<br>11.5304100 goldfinch, Carduelis carduelis |
resnet152-v1-7.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 16.7801360 junco, snowbird<br>13.0216940 brambling, Fringilla montifringilla<br>10.9750260 water ouzel, dipper<br>10.1096920 goldfinch, Carduelis carduelis<br>9.9460330 chickadee |
shufflenet-v2-12.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 19.8042530 junco, snowbird<br>11.9451450 damselfly<br>10.5131190 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>9.8524340 brambling, Fringilla montifringilla<br>9.0652480 goldfinch, Carduelis carduelis |
shufflenet-v2-12-int8.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 17.4124010 junco, snowbird<br>11.5508010 damselfly<br>9.1372000 macaque<br>8.9648010 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>8.9648010 goldfinch, Carduelis carduelis |
squeezenet1.0-12.onnx | - | - | 0.5749820 chickadee<br>0.4248460 junco, snowbird<br>0.0000860 jay<br>0.0000270 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000260 brambling, Fringilla montifringilla |
squeezenet1.0-12-int8.onnx | - | - | 0.8146190 chickadee<br>0.1530020 junco, snowbird<br>0.0094250 quail<br>0.0064990 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0030910 ruffed grouse, partridge, Bonasa umbellus |
vgg16-12.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 30.5324520 junco, snowbird<br>24.8352660 brambling, Fringilla montifringilla<br>22.2450640 chickadee<br>20.4212700 goldfinch, Carduelis carduelis<br>19.6983950 water ouzel, dipper |
vgg16-12-int8.onnx | Mean values - [0.485,0.456,0.406]<br>scale values - [0.229,0.224,0.225] | - | 27.7026710 junco, snowbird<br>23.8191200 brambling, Fringilla montifringilla<br>20.1944710 chickadee<br>19.6766640 goldfinch, Carduelis carduelis<br>18.1232430 house finch, linnet, Carpodacus mexicanus |
zfnet512-12.onnx | - | - | 0.9650780 junco, snowbird<br>0.0333620 chickadee<br>0.0010080 brambling, Fringilla montifringilla<br>0.0001260 bulbul<br>0.0001170 house finch, linnet, Carpodacus mexicanus |
zfnet512-12-int8.onnx | - | - | 0.8073320 junco, snowbird<br>0.1267470 chickadee<br>0.0089990 brambling, Fringilla montifringilla<br>0.0027370 bulbul<br>0.0027370 water ouzel, dipper |