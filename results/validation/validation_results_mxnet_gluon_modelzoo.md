# Validation results for the models inferring using MXNet (Gluon API)

## Image classification

Complete information about the supported classification
models is available [here][gluon_modelzoo_classification].

Notes:

- For all classification models input shape BxCxWxH, where
  B is a batch size, C is an image number of channels,
  W is an image width, H is an image height.
  W=H=224 except inceptionv3, for this model W=H=299.
- Values of mean and standard deviation parameters used
  for model validation are represented for each image.

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510

Mean: [0.485, 0.456, 0.406]

Standard deviation: [0.229, 0.224, 0.225]


<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

   Model     |  Python API  |
-------------|---------------------------|
alexnet      |0.4499776 Granny Smith<br>0.0933101 dumbbell<br>0.0876726 ocarina, sweet potato<br>0.0628703 hair slide<br>0.0484683 bottlecap|
darknet53|0.5883058 Granny Smith<br>0.0645481 candle, taper, wax light<br>0.0236042 piggy bank, penny bank<br>0.0160968 pencil sharpener<br>0.0060462 vase|
densenet121  |0.9523344 Granny Smith<br>0.0132273 orange<br>0.0125171 lemon<br>0.0027910 banana<br>0.0020333 piggy bank, penny bank|
densenet161  |0.9372969 Granny Smith<br>0.0082274 dumbbell<br>0.0056475 piggy bank, penny bank<br>0.0055374 ping-pong ball<br>0.0041915 pitcher, ewer|
densenet169  |0.9811631 Granny Smith<br>0.0033828 piggy bank, penny bank<br>0.0021366 orange<br>0.0019196 lemon<br>0.0017232 pomegranate|
densenet201  |0.9119797 Granny Smith<br>0.0533454 piggy bank, penny bank<br>0.0056832 lemon<br>0.0017810 pool table, billiard table, snooker table<br>0.0015689 tennis ball|
googlenet |0.2217809 Granny Smith<br>0.2117919 piggy bank, penny bank<br>0.0270375 dumbbell<br>0.0116782 saltshaker, salt shaker<br>0.0108081 candle, taper, wax light|
hrnet_w18_c|0.5520265 Granny Smith<br>0.3595940 piggy bank, penny bank<br>0.0101424 soap dispenser<br>0.0099333 orange<br>0.0080332 analog clock|
hrnet_w18_small_v1_c|0.2498852 piggy bank, penny bank<br>0.2331266 Granny Smith<br>0.0426585 saltshaker, salt shaker<br>0.0386379 soap dispenser<br>0.0379136 rubber eraser, rubber, pencil eraser|
hrnet_w18_small_v2_c|0.6248410 Granny Smith<br>0.1713923 piggy bank, penny bank<br>0.0333320 hair slide<br>0.0208897 dumbbell<br>0.0133955 lemon|
hrnet_w30_c|0.7287291 Granny Smith<br>0.0418399 safety pin<br>0.0235450 piggy bank, penny bank<br>0.0177420 hook, claw<br>0.0166939 candle, taper, wax light|
hrnet_w32_c|0.7040173 Granny Smith<br>0.0617449 lemon<br>0.0479103 orange<br>0.0105366 piggy bank, penny bank<br>0.0091770 water bottle|
hrnet_w40_c|0.8720709 Granny Smith<br>0.0261122 piggy bank, penny bank<br>0.0044007 rubber eraser, rubber, pencil eraser<br>0.0035225 orange<br>0.0033742 pencil box, pencil case|
hrnet_w44_c|0.4269260 Granny Smith<br>0.0949395 piggy bank, penny bank<br>0.0170920 lemon<br>0.0153640 digital clock<br>0.0148546 orange|
hrnet_w48_c|0.6867532 Granny Smith<br>0.0240540 lemon<br>0.0171518 tennis ball<br>0.0120418 orange<br>0.0086221 banana|
hrnet_w64_c|0.9524294 Granny Smith<br>0.0103368 orange<br>0.0050601 syringe<br>0.0020366 lemon<br>0.0015060 tennis ball|
inceptionv3  |0.9185177 Granny Smith<br>0.0018308 candle, taper, wax light<br>0.0012390 crane<br>0.0009742 orange<br>0.0007275 syringe|
mobilenet0.25|0.1413059 Granny Smith<br>0.0491460 necklace<br>0.0399561 bell pepper<br>0.0370546 hair slide<br>0.0301661 piggy bank, penny bank|
mobilenet0.5 |0.0988460 teapot<br>0.0556895 piggy bank, penny bank<br>0.0552285 saltshaker, salt shaker<br>0.0383402 pitcher, ewer<br>0.0319066 necklace|
mobilenet0.75|0.1711094 Granny Smith<br>0.1602635 piggy bank, penny bank<br>0.0857521 teapot<br>0.0533995 pitcher, ewer<br>0.0354786 soap dispenser|
mobilenet1.0 |0.4475225 Granny Smith<br>0.0954533 piggy bank, penny bank<br>0.0523449 saltshaker, salt shaker<br>0.0358669 pencil sharpener<br>0.0232730 dumbbell|
mobilenet1.0_int8 |0.4552936 Granny Smith<br>0.0632280 piggy bank, penny bank<br>0.0523604 saltshaker, salt shaker<br>0.0327314 pencil sharpener<br>0.0265849 dumbbell|
mobilenetv2_0.25|0.1189503 saltshaker, salt shaker<br>0.0919519 bell pepper<br>0.0862974 Granny Smith<br>0.0828691 piggy bank, penny bank<br>0.0527703 hair slide|
mobilenetv2_0.5 |0.1700138 hair slide<br>0.0890763 dumbbell<br>0.0777359 piggy bank, penny bank<br>0.0521625 saltshaker, salt shaker<br>0.0489330 necklace|
mobilenetv2_0.75|0.3621189 saltshaker, salt shaker<br>0.2135993 Granny Smith<br>0.1286786 piggy bank, penny bank<br>0.0391913 lemon<br>0.0134064 ocarina, sweet potato|
mobilenetv2_1.0 |0.6325442 Granny Smith<br>0.0556754 piggy bank, penny bank<br>0.0443766 lemon<br>0.0086360 teapot<br>0.0071484 vase|
mobilenetV3_large |0.7482075 Granny Smith<br>0.1232551 piggy bank, penny bank<br>0.0285252 saltshaker, salt shaker<br>0.0054824 lemon<br>0.0047922 croquet ball|
mobilenetV3_small |0.5579336 Granny Smith<br>0.0599188 bell pepper<br>0.0381997 piggy bank, penny bank<br>0.0303460 saltshaker, salt shaker<br>0.0262051 lemon|
resnet18_v1 |0.7145669 Granny Smith<br>0.0433350 piggy bank, penny bank<br>0.0343973 saltshaker, salt shaker<br>0.0215942 fig<br>0.0212160 banana|
resnet18_v2 |0.2885310 Granny Smith<br>0.1816195 piggy bank, penny bank<br>0.0722676 saltshaker, salt shaker<br>0.0635361 rubber eraser, rubber, pencil eraser<br>0.0440725 soap dispenser|
resnet18_v1b |0.9093145 Granny Smith<br>0.0187165 saltshaker, salt shaker<br>0.0117636 piggy bank, penny bank<br>0.0104429 pomegranate<br>0.0058578 perfume, essence|
resnet18_v1b_0.89|0.5232244 piggy bank, penny bank<br>0.1546666 Granny Smith<br>0.1040182 saltshaker, salt shaker<br>0.0313044 soap dispenser<br>0.0295205 vase|
resnet18_v1b_custom|0.0051828 African chameleon, Chamaeleo chamaeleon<br>0.0048727 Gila monster, Heloderma suspectum<br>0.0046023 colobus, colobus monkey<br>0.0045542 black widow, Latrodectus mactans<br>0.0044811 flatworm, platyhelminth|
resnet34_v1 |0.5898067 piggy bank, penny bank<br>0.3150526 Granny Smith<br>0.0128028 saltshaker, salt shaker<br>0.0093141 candle, taper, wax light<br>0.0089791 pencil sharpener|
resnet34_v2 |0.5082690 Granny Smith<br>0.3873709 piggy bank, penny bank<br>0.0163602 pencil sharpener<br>0.0137501 saltshaker, salt shaker<br>0.0071418 dumbbell|
resnet34_v1b |0.8592082 Granny Smith<br>0.0595315 piggy bank, penny bank<br>0.0257422 pitcher, ewer<br>0.0107621 saltshaker, salt shaker<br>0.0081604 water jug|
resnet50_v1 |0.7377543 Granny Smith<br>0.0241721 piggy bank, penny bank<br>0.0123405 lemon<br>0.0061283 candle, taper, wax light<br>0.0051573 orange|
resnet50_v1_int8|0.6387886 Granny Smith<br>0.0295431 piggy bank, penny bank<br>0.0144967 lemon<br>0.0125546 candle, taper, wax light<br>0.0110684 saltshaker, salt shaker|
resnet50_v2 |0.9931253 Granny Smith<br>0.0017001 piggy bank, penny bank<br>0.0007180 saltshaker, salt shaker<br>0.0006648 dumbbell<br>0.0002998 tennis ball|
resnet50_v1b |0.5989549 Granny Smith<br>0.1451391 piggy bank, penny bank<br>0.0253168 pitcher, ewer<br>0.0129785 candle, taper, wax light<br>0.0104263 saltshaker, salt shaker|
resnet50_v1b_custom |0.0051049 anemone fish<br>0.0050241 spider monkey, Ateles geoffroyi<br>0.0050122 ibex, Capra ibex<br>0.0049926 cicada, cicala<br>0.0048133 garter snake, grass snake
resnet50_v1b_gn|0.7398045 Granny Smith<br>0.0445737 candle, taper, wax light<br>0.0127276 piggy bank, penny bank<br>0.0120557 safety pin<br>0.0083770 pomegranate|
resnet50_v1c |0.8618550 Granny Smith<br>0.0188060 candle, taper, wax light<br>0.0055579 orange<br>0.0039412 pitcher, ewer<br>0.0034311 lemon|
resnet50_v1d |0.7543250 Granny Smith<br>0.0171997 dumbbell<br>0.0116827 candle, taper, wax light<br>0.0074653 spindle<br>0.0059659 piggy bank, penny bank|
resnet50_v1d_0.11|0.0547115 necklace<br>0.0466139 hair slide<br>0.0440734 dumbbell<br>0.0317605 piggy bank, penny bank<br>0.0290907 bell pepper|
resnet50_v1d_0.37|0.1162345 piggy bank, penny bank<br>0.0520882 pitcher, ewer<br>0.0499831 saltshaker, salt shaker<br>0.0374144 Granny Smith<br>0.0282163 teapot|
resnet50_v1d_0.48|0.1693304 piggy bank, penny bank<br>0.1179273 pitcher, ewer<br>0.0780331 teapot<br>0.0759569 Granny Smith<br>0.0351384 soap dispenser|
resnet50_v1d_0.86|0.1912429 Granny Smith<br>0.1522044 vase<br>0.0466547 pitcher, ewer<br>0.0438114 piggy bank, penny bank<br>0.0387991 teapot|
resnet50_v1s|0.6378097 Granny Smith<br>0.0955320 piggy bank, penny bank<br>0.0187408 candle, taper, wax light<br>0.0173063 pencil sharpener<br>0.0085729 bell pepper|
resnet101_v1 |0.8556004 Granny Smith<br>0.0572233 piggy bank, penny bank<br>0.0485183 saltshaker, salt shaker<br>0.0053788 hair slide<br>0.0048319 dumbbell|
resnet101_v2 |0.8972552 Granny Smith<br>0.0401729 candle, taper, wax light<br>0.0074956 nail<br>0.0072347 screw<br>0.0056376 hair slide|
resnet101_v1b |0.7857985 Granny Smith<br>0.0282332 piggy bank, penny bank<br>0.0049071 pool table, billiard table, snooker table<br>0.0044100 nail<br>0.0031941 orange|
resnet101_v1c |0.8046857 Granny Smith<br>0.0042279 lemon<br>0.0039940 orange<br>0.0035649 piggy bank, penny bank<br>0.0026069 pool table, billiard table, snooker table|
resnet101_v1d |0.8904037 Granny Smith<br>0.0013014 orange<br>0.0011862 candle, taper, wax light<br>0.0011250 lemon<br>0.0007383 syringe|
resnet101_v1d_0.73|0.8738712 Granny Smith<br>0.0117864 orange<br>0.0059453 lemon<br>0.0025753 banana<br>0.0018348 pitcher, ewer|
resnet101_v1d_0.76|0.7294459 Granny Smith<br>0.0140307 pool table, billiard table, snooker table<br>0.0060903 lemon<br>0.0042248 ping-pong ball<br>0.0035100 saltshaker, salt shaker|
resnet101_v1s|0.9420365 Granny Smith<br>0.0060981 piggy bank, penny bank<br>0.0039682 nail<br>0.0038415 tennis ball<br>0.0032590 candle, taper, wax light|
resnet152_v1 |0.9902509 Granny Smith<br>0.0005738 lemon<br>0.0005411 orange<br>0.0004003 banana<br>0.0001558 paper towel|
resnet152_v2 |0.9972478 Granny Smith<br>0.0010769 piggy bank, penny bank<br>0.0002827 orange<br>0.0002033 pitcher, ewer<br>0.0001509 lemon|
resnet152_v1b |0.9882135 Granny Smith<br>0.0015362 orange<br>0.0005067 lemon<br>0.0004334 candle, taper, wax light<br>0.0003944 banana|
resnet152_v1c |0.9887015 Granny Smith<br>0.0004545 lemon<br>0.0002470 orange<br>0.0001788 piggy bank, penny bank<br>0.0001443 banana|
resnet152_v1d |0.9998449 Granny Smith<br>0.0000251 candle, taper, wax light<br>0.0000094 piggy bank, penny bank<br>0.0000013 orange<br>0.0000013 nail|
resnet152_v1s|0.9897671 Granny Smith<br>0.0006710 orange<br>0.0005886 lemon<br>0.0003691 banana<br>0.0002897 paper towel|
resnext50_32x4d |0.5039393 Granny Smith<br>0.1542056 piggy bank, penny bank<br>0.0462400 candle, taper, wax light<br>0.0045215 pitcher, ewer<br>0.0038302 necklace|
resnext101_32x4d |0.9283170 Granny Smith<br>0.0027030 candle, taper, wax light<br>0.0021046 spindle<br>0.0011345 lemon<br>0.0008427 orange|
resnext101_64x4d|0.8459962 Granny Smith<br>0.0009382 syringe<br>0.0007001 lemon<br>0.0006334 orange<br>0.0005562 shower curtain|
se_resnext50_32x4d |0.9321796 Granny Smith<br>0.0013750 candle, taper, wax light<br>0.0006428 piggy bank, penny bank<br>0.0004036 tennis ball<br>0.0004002 lemon|
se_resnext101_32x4d |0.8162102 Granny Smith<br>0.0103485 saltshaker, salt shaker<br>0.0090229 lemon<br>0.0089084 orange<br>0.0052811 candle, taper, wax light|
se_resnext101_64x4d |0.8560185 Granny Smith<br>0.0008338 orange<br>0.0006294 banana<br>0.0005233 syringe<br>0.0005156 piggy bank, penny bank|
resnest14 |0.5492676 piggy bank, penny bank<br>0.1353471 Granny Smith<br>0.0317922 candle, taper, wax light<br>0.0150942 teapot<br>0.0075024 water jug|
resnest26 |0.6255676 Granny Smith<br>0.0436678 piggy bank, penny bank<br>0.0079170 orange<br>0.0076749 pomegranate<br>0.0044506 lemon|
resnest50 |0.8672453 Granny Smith<br>0.0019027 pomegranate<br>0.0018386 orange<br>0.0018165 lemon<br>0.0016820 piggy bank, penny bank|
resnest101 |0.7884610 Granny Smith<br>0.0017616 orange<br>0.0016064 Arabian camel, dromedary, Camelus dromedarius<br>0.0011836 candle, taper, wax light<br>0.0010934 wardrobe, closet, press|
resnest200 |0.8712394 Granny Smith<br>0.0014679 orange<br>0.0013268 candle, taper, wax light<br>0.0011122 lemon<br>0.0006881 Bouvier des Flandres, Bouviers des Flandres|
resnest269 |0.8810812 Granny Smith<br>0.0014211 orange<br>0.0007651 lemon<br>0.0006411 neck brace<br>0.0005766 banana|
squeezenet1.0 |0.3275021 piggy bank, penny bank<br>0.1791335 dumbbell<br>0.1542641 Granny Smith<br>0.0912996 water bottle<br>0.0385820 rubber eraser, rubber, pencil eraser|
squeezenet1.1 |0.5895351 piggy bank, penny bank<br>0.0677937 Granny Smith<br>0.0610657 necklace<br>0.0610450 lemon<br>0.0490915 bucket, pail|
vgg11 |0.3721463 piggy bank, penny bank<br>0.2952025 Granny Smith<br>0.1076758 tennis ball<br>0.0314686 soap dispenser<br>0.0285692 dumbbell|
vgg11_bn |0.5464048 Granny Smith<br>0.2313122 dumbbell<br>0.0658233 piggy bank, penny bank<br>0.0269569 tennis ball<br>0.0218533 teapot|
vgg13 |0.4068233 Granny Smith<br>0.2272184 dumbbell<br>0.0475027 necklace<br>0.0303711 maraca<br>0.0250665 teapot|
vgg13_bn |0.9389399 Granny Smith<br>0.0383621 tennis ball<br>0.0069443 lemon<br>0.0039320 orange<br>0.0013574 banana|
vgg16 |0.6872561 piggy bank, penny bank<br>0.0687330 Granny Smith<br>0.0588234 teapot<br>0.0392138 tennis ball<br>0.0210059 pitcher, ewer|
vgg16_bn |0.9958419 Granny Smith<br>0.0010665 tennis ball<br>0.0008365 piggy bank, penny bank<br>0.0004831 teapot<br>0.0004005 dumbbell|
vgg19 |0.6034821 Granny Smith<br>0.1175481 piggy bank, penny bank<br>0.0277910 dumbbell<br>0.0249204 whistle<br>0.0218847 teapot|
vgg19_bn |0.9881874 Granny Smith<br>0.0025413 piggy bank, penny bank<br>0.0011374 teapot<br>0.0009895 saltshaker, salt shaker<br>0.0006477 cup|
xception |0.9998661 Granny Smith<br>0.0001228 lemon<br>0.0000048 piggy bank, penny bank<br>0.0000015 banana<br>0.0000010 tennis ball|
senet_154 |0.6984364 Granny Smith<br>0.0078498 syringe<br>0.0034595 tennis ball<br>0.0028654 banana<br>0.0025570 hare|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500


<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

   Model     |  Python API  |
-------------|---------------------------|
alexnet      |0.9947649 junco, snowbird<br>0.0043087 chickadee<br>0.0002780 water ouzel, dipper<br>0.0002770 bulbul<br>0.0001244 brambling, Fringilla montifringilla|
darknet53|0.8250283 junco, snowbird<br>0.0037126 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0019864 brambling, Fringilla montifringilla<br>0.0017965 water ouzel, dipper<br>0.0015356 American coot, marsh hen, mud hen, water hen, Fulica americana|
densenet121  |0.9841599 junco, snowbird<br>0.0072199 chickadee<br>0.0034962 brambling, Fringilla montifringilla<br>0.0016226 water ouzel, dipper<br>0.0012858 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
densenet161  |0.9932058 junco, snowbird<br>0.0015922 chickadee<br>0.0012295 brambling, Fringilla montifringilla<br>0.0011838 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0008891 goldfinch, Carduelis carduelis|
densenet169  |0.9640697 junco, snowbird<br>0.0201313 brambling, Fringilla montifringilla<br>0.0044098 chickadee<br>0.0032345 goldfinch, Carduelis carduelis<br>0.0026739 water ouzel, dipper|
densenet201  |0.9515250 junco, snowbird<br>0.0178252 water ouzel, dipper<br>0.0109119 brambling, Fringilla montifringilla<br>0.0077980 house finch, linnet, Carpodacus mexicanus<br>0.0044695 chickadee|
googlenet |0.8450467 junco, snowbird<br>0.0073040 brambling, Fringilla montifringilla<br>0.0059225 chickadee<br>0.0033832 goldfinch, Carduelis carduelis<br>0.0031529 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
hrnet_w18_c|0.9188430 junco, snowbird<br>0.0296666 goldfinch, Carduelis carduelis<br>0.0161022 brambling, Fringilla montifringilla<br>0.0122709 chickadee<br>0.0079102 water ouzel, dipper|
hrnet_w18_small_v1_c|0.9759023 junco, snowbird<br>0.0106352 chickadee<br>0.0046215 water ouzel, dipper<br>0.0039147 brambling, Fringilla montifringilla<br>0.0010362 goldfinch, Carduelis carduelis|
hrnet_w18_small_v2_c|0.9787474 junco, snowbird<br>0.0064078 brambling, Fringilla montifringilla<br>0.0033237 chickadee<br>0.0029915 red-backed sandpiper, dunlin, Erolia alpina<br>0.0026367 goldfinch, Carduelis carduelis|
hrnet_w30_c|0.8702929 junco, snowbird<br>0.0613190 water ouzel, dipper<br>0.0193866 goldfinch, Carduelis carduelis<br>0.0158093 brambling, Fringilla montifringilla<br>0.0101078 house finch, linnet, Carpodacus mexicanus|
hrnet_w32_c|0.9775968 junco, snowbird<br>0.0055817 brambling, Fringilla montifringilla<br>0.0031635 water ouzel, dipper<br>0.0028534 chickadee<br>0.0028298 goldfinch, Carduelis carduelis|
hrnet_w40_c|0.9487124 junco, snowbird<br>0.0197902 brambling, Fringilla montifringilla<br>0.0128434 water ouzel, dipper<br>0.0024431 chickadee<br>0.0020419 red-backed sandpiper, dunlin, Erolia alpina|
hrnet_w44_c|0.9505839 junco, snowbird<br>0.0129691 water ouzel, dipper<br>0.0122351 brambling, Fringilla montifringilla<br>0.0042923 goldfinch, Carduelis carduelis<br>0.0020167 house finch, linnet, Carpodacus mexicanus|
hrnet_w48_c|0.9621018 junco, snowbird<br>0.0160337 water ouzel, dipper<br>0.0087758 chickadee<br>0.0063452 brambling, Fringilla montifringilla<br>0.0013683 red-backed sandpiper, dunlin, Erolia alpina|
hrnet_w64_c|0.9867093 junco, snowbird<br>0.0050804 water ouzel, dipper<br>0.0014207 brambling, Fringilla montifringilla<br>0.0012793 chickadee<br>0.0007804 goldfinch, Carduelis carduelis|
inceptionv3  |0.8331636 junco, snowbird<br>0.0094580 water ouzel, dipper<br>0.0049014 brambling, Fringilla montifringilla<br>0.0012859 chickadee<br>0.0010424 robin, American robin, Turdus migratorius|
mobilenet0.25|0.7976559 junco, snowbird<br>0.0642661 brambling, Fringilla montifringilla<br>0.0495699 chickadee<br>0.0412341 house finch, linnet, Carpodacus mexicanus<br>0.0166411 goldfinch, Carduelis carduelis|
mobilenet0.5 |0.6876235 junco, snowbird<br>0.0567821 chickadee<br>0.0440355 house finch, linnet, Carpodacus mexicanus<br>0.0327330 brambling, Fringilla montifringilla<br>0.0170564 hummingbird|
mobilenet0.75|0.7232150 junco, snowbird<br>0.0267700 brambling, Fringilla montifringilla<br>0.0224716 chickadee<br>0.0173853 water ouzel, dipper<br>0.0107710 house finch, linnet, Carpodacus mexicanus|
mobilenet1.0 |0.3200681 junco, snowbird<br>0.0977401 chickadee<br>0.0255691 brambling, Fringilla montifringilla<br>0.0200887 water ouzel, dipper<br>0.0052986 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
mobilenet1.0_int8 | 0.4458332 junco, snowbird<br>0.0757087 chickadee<br>0.0233120 water ouzel, dipper<br>0.0213673 brambling, Fringilla montifringilla<br>0.0034389 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
mobilenetv2_0.25|0.5445739 junco, snowbird<br>0.1674697 chickadee<br>0.0738745 brambling, Fringilla montifringilla<br>0.0237202 house finch, linnet, Carpodacus mexicanus<br>0.0177469 coucal|
mobilenetv2_0.5 |0.9121019 junco, snowbird<br>0.0402663 chickadee<br>0.0144705 brambling, Fringilla montifringilla<br>0.0111383 house finch, linnet, Carpodacus mexicanus<br>0.0019353 bulbul|
mobilenetv2_0.75|0.4884860 junco, snowbird<br>0.0884391 chickadee<br>0.0189599 brambling, Fringilla montifringilla<br>0.0151568 water ouzel, dipper<br>0.0111601 hummingbird|
mobilenetv2_1.0 |0.8265611 junco, snowbird<br>0.0339170 chickadee<br>0.0146587 brambling, Fringilla montifringilla<br>0.0095486 water ouzel, dipper<br>0.0065168 hummingbird|
mobilenetV3_large |0.8610585 junco, snowbird<br>0.0212062 chickadee<br>0.0043952 house finch, linnet, Carpodacus mexicanus<br>0.0040245 brambling, Fringilla montifringilla<br>0.0034385 goldfinch, Carduelis carduelis|
mobilenetV3_small |0.4654124 junco, snowbird<br>0.0976697 brambling, Fringilla montifringilla<br>0.0351128 goldfinch, Carduelis carduelis<br>0.0220040 house finch, linnet, Carpodacus mexicanus<br>0.0132010 water ouzel, dipper|
resnet18_v1 |0.9597536 junco, snowbird<br>0.0103961 chickadee<br>0.0075481 goldfinch, Carduelis carduelis<br>0.0054579 house finch, linnet, Carpodacus mexicanus<br>0.0053979 water ouzel, dipper|
resnet18_v2 |0.9460587 junco, snowbird<br>0.0180775 brambling, Fringilla montifringilla<br>0.0139834 chickadee<br>0.0075303 goldfinch, Carduelis carduelis<br>0.0037932 water ouzel, dipper|
resnet18_v1b |0.9505776 junco, snowbird<br>0.0350148 brambling, Fringilla montifringilla<br>0.0052746 goldfinch, Carduelis carduelis<br>0.0044680 chickadee<br>0.0029356 house finch, linnet, Carpodacus mexicanus|
resnet18_v1b_0.89|0.9328545 junco, snowbird<br>0.0446809 brambling, Fringilla montifringilla<br>0.0101631 house finch, linnet, Carpodacus mexicanus<br>0.0063039 chickadee<br>0.0027250 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
resnet18_v1b_custom |0.0060174 African chameleon, Chamaeleo chamaeleon<br>0.0054798 American Staffordshire terrier, Staffordshire terrier, American pit bull terrier, pit bull terrier<br>0.0051301 flatworm, platyhelminth<br>0.0050669 prairie chicken, prairie grouse, prairie fowl<br>0.0049658 Shih-Tzu|
resnet34_v1 |0.9352032 junco, snowbird<br>0.0226504 water ouzel, dipper<br>0.0129960 brambling, Fringilla montifringilla<br>0.0050841 chickadee<br>0.0037434 goldfinch, Carduelis carduelis|
resnet34_v2 |0.6477929 junco, snowbird<br>0.0750227 water ouzel, dipper<br>0.0672589 brambling, Fringilla montifringilla<br>0.0443260 chickadee<br>0.0321975 goldfinch, Carduelis carduelis|
resnet34_v1b |0.9445685 junco, snowbird<br>0.0109547 water ouzel, dipper<br>0.0106829 goldfinch, Carduelis carduelis<br>0.0075599 brambling, Fringilla montifringilla<br>0.0043267 chickadee|
resnet50_v1 |0.8778600 junco, snowbird<br>0.0045333 water ouzel, dipper<br>0.0018932 brambling, Fringilla montifringilla<br>0.0016121 chickadee<br>0.0005472 magpie|
resnet50_v1_int8 |0.8986668 junco, snowbird<br>0.0042505 water ouzel, dipper<br>0.0019016 brambling, Fringilla montifringilla<br>0.0012305 chickadee<br>0.0005350 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
resnet50_v2 |0.9820374 junco, snowbird<br>0.0070083 water ouzel, dipper<br>0.0032555 chickadee<br>0.0021856 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0017496 brambling, Fringilla montifringilla|
resnet50_v1b |0.9325832 junco, snowbird<br>0.0022530 water ouzel, dipper<br>0.0019862 chickadee<br>0.0011287 brambling, Fringilla montifringilla<br>0.0005958 goldfinch, Carduelis carduelis|
resnet50_v1b_custom |0.0042406 bullfrog, Rana catesbeiana<br>0.0041815 thunder snake, worm snake, Carphophis amoenus<br>0.0041015 bulbul<br>0.0040439 bustard<br>0.0039271 partridge|
resnet50_v1b_gn|0.8502029 junco, snowbird<br>0.0078807 brambling, Fringilla montifringilla<br>0.0052344 water ouzel, dipper<br>0.0047941 chickadee<br>0.0025184 goldfinch, Carduelis carduelis|
resnet50_v1c |0.9273983 junco, snowbird<br>0.0029364 chickadee<br>0.0021531 water ouzel, dipper<br>0.0007963 brambling, Fringilla montifringilla<br>0.0007281 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
resnet50_v1d |0.8592040 junco, snowbird<br>0.0012552 trilobite<br>0.0008265 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0007142 brambling, Fringilla montifringilla<br>0.0006234 chickadee|
resnet50_v1d_0.11|0.8141757 junco, snowbird<br>0.0476836 brambling, Fringilla montifringilla<br>0.0176680 house finch, linnet, Carpodacus mexicanus<br>0.0174768 goldfinch, Carduelis carduelis<br>0.0137937 chickadee|
resnet50_v1d_0.37|0.7955161 junco, snowbird<br>0.0112076 brambling, Fringilla montifringilla<br>0.0072924 house finch, linnet, Carpodacus mexicanus<br>0.0043970 goldfinch, Carduelis carduelis<br>0.0027637 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
resnet50_v1d_0.48|0.8902636 junco, snowbird<br>0.0054964 brambling, Fringilla montifringilla<br>0.0040026 chickadee<br>0.0018189 water ouzel, dipper<br>0.0011725 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
resnet50_v1d_0.86|0.8838070 junco, snowbird<br>0.0034641 chickadee<br>0.0034094 water ouzel, dipper<br>0.0015349 brambling, Fringilla montifringilla<br>0.0011060 trilobite|
resnet50_v1s|0.9927825 junco, snowbird<br>0.0009136 chickadee<br>0.0007485 brambling, Fringilla montifringilla<br>0.0006094 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0003606 water ouzel, dipper|
resnet101_v1 |0.9215414 junco, snowbird<br>0.0161461 brambling, Fringilla montifringilla<br>0.0113413 water ouzel, dipper<br>0.0096166 chickadee<br>0.0087583 house finch, linnet, Carpodacus mexicanus|
resnet101_v2 |0.9053523 junco, snowbird<br>0.0451527 water ouzel, dipper<br>0.0106367 chickadee<br>0.0089987 brambling, Fringilla montifringilla<br>0.0037001 goldfinch, Carduelis carduelis|
resnet101_v1b |0.9276263 junco, snowbird<br>0.0049964 water ouzel, dipper<br>0.0046615 chickadee<br>0.0030906 brambling, Fringilla montifringilla<br>0.0008694 goldfinch, Carduelis carduelis|
resnet101_v1c |0.8793292 junco, snowbird<br>0.0013544 water ouzel, dipper<br>0.0010500 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0009873 chickadee<br>0.0009162 brambling, Fringilla montifringilla|
resnet101_v1d |0.8917584 junco, snowbird<br>0.0015399 water ouzel, dipper<br>0.0006728 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0006276 loupe, jeweler's loupe<br>0.0005075 brambling, Fringilla montifringilla|
resnet101_v1d_0.73|0.8549845 junco, snowbird<br>0.0013958 water ouzel, dipper<br>0.0009261 chickadee<br>0.0008926 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0007149 brambling, Fringilla montifringilla|
resnet101_v1d_0.76|0.8729864 junco, snowbird<br>0.0017605 water ouzel, dipper<br>0.0005628 chickadee<br>0.0004765 saltshaker, salt shaker<br>0.0004645 American coot, marsh hen, mud hen, water hen, Fulica americana|
resnet101_v1s|0.9577293 junco, snowbird<br>0.0045800 chickadee<br>0.0034216 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0014765 brambling, Fringilla montifringilla<br>0.0012217 water ouzel, dipper|
resnet152_v1 |0.9541085 junco, snowbird<br>0.0007439 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0006390 brambling, Fringilla montifringilla<br>0.0005719 chickadee<br>0.0004141 water ouzel, dipper|
resnet152_v2 |0.9695247 junco, snowbird<br>0.0054735 brambling, Fringilla montifringilla<br>0.0041750 water ouzel, dipper<br>0.0027560 goldfinch, Carduelis carduelis<br>0.0024612 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
resnet152_v1b |0.9181211 junco, snowbird<br>0.0008047 water ouzel, dipper<br>0.0006730 chickadee<br>0.0004612 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0004567 brambling, Fringilla montifringilla|
resnet152_v1c |0.9407274 junco, snowbird<br>0.0019899 water ouzel, dipper<br>0.0008130 chickadee<br>0.0008025 magpie<br>0.0006756 brambling, Fringilla montifringilla|
resnet152_v1d |0.9677259 junco, snowbird<br>0.0004674 water ouzel, dipper<br>0.0003674 brambling, Fringilla montifringilla<br>0.0003074 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001905 redshank, Tringa totanus|
resnet152_v1s|0.9894158 junco, snowbird<br>0.0002875 chickadee<br>0.0002700 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002608 brambling, Fringilla montifringilla<br>0.0002240 American coot, marsh hen, mud hen, water hen, Fulica americana|
resnext50_32x4d |0.8792271 junco, snowbird<br>0.0019800 water ouzel, dipper<br>0.0006261 brambling, Fringilla montifringilla<br>0.0005920 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005325 American coot, marsh hen, mud hen, water hen, Fulica americana|
resnext101_32x4d |0.9276594 junco, snowbird<br>0.0029483 water ouzel, dipper<br>0.0007209 chickadee<br>0.0006452 brambling, Fringilla montifringilla<br>0.0004491 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
resnext101_64x4d|0.8758404 junco, snowbird<br>0.0008728 tiger shark, Galeocerdo cuvieri<br>0.0005660 water ouzel, dipper<br>0.0005565 brambling, Fringilla montifringilla<br>0.0004355 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
se_resnext50_32x4d |0.9159099 junco, snowbird<br>0.0075064 chickadee<br>0.0031539 water ouzel, dipper<br>0.0008047 brambling, Fringilla montifringilla<br>0.0006744 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
se_resnext101_32x4d |0.8849785 junco, snowbird<br>0.0082190 water ouzel, dipper<br>0.0021819 brambling, Fringilla montifringilla<br>0.0016918 chickadee<br>0.0008970 indigo bunting, indigo finch, indigo bird, Passerina cyanea|
se_resnext101_64x4d |0.9599983 junco, snowbird<br>0.0001568 container ship, containership, container vessel<br>0.0001457 water ouzel, dipper<br>0.0001314 oystercatcher, oyster catcher<br>0.0001283 dugong, Dugong dugon|
resnest14 |0.3178357 junco, snowbird<br>0.0798734 chickadee<br>0.0207251 water ouzel, dipper<br>0.0119278 brambling, Fringilla montifringilla<br>0.0053170 goldfinch, Carduelis carduelis|
resnest26 |0.8787090 junco, snowbird<br>0.0026270 chickadee<br>0.0017752 brambling, Fringilla montifringilla<br>0.0011295 water ouzel, dipper<br>0.0008994 goldfinch, Carduelis carduelis|
resnest50 |0.8861975 junco, snowbird<br>0.0022739 water ouzel, dipper<br>0.0017978 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0009528 brambling, Fringilla montifringilla<br>0.0005547 ringlet, ringlet butterfly|
resnest101 |0.8264657 junco, snowbird<br>0.0013493 water ouzel, dipper<br>0.0011776 chickadee<br>0.0010429 diamondback, diamondback rattlesnake, Crotalus adamanteus<br>0.0010088 tiger shark, Galeocerdo cuvieri|
resnest200 |0.9008964 junco, snowbird<br>0.0014222 water ouzel, dipper<br>0.0011092 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0008399 brambling, Fringilla montifringilla<br>0.0007130 chickadee|
resnest269 |0.8601478 junco, snowbird<br>0.0010935 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0008388 brambling, Fringilla montifringilla<br>0.0007640 water ouzel, dipper<br>0.0007627 ski mask|
squeezenet1.0 |0.9904411 junco, snowbird<br>0.0045287 chickadee<br>0.0040343 brambling, Fringilla montifringilla<br>0.0003414 water ouzel, dipper<br>0.0002521 house finch, linnet, Carpodacus mexicanus|
squeezenet1.1 |0.9614584 junco, snowbird<br>0.0250979 chickadee<br>0.0040701 brambling, Fringilla montifringilla<br>0.0035156 goldfinch, Carduelis carduelis<br>0.0030858 ruffed grouse, partridge, Bonasa umbellus|
vgg11 |0.9998955 junco, snowbird<br>0.0000967 chickadee<br>0.0000043 brambling, Fringilla montifringilla<br>0.0000023 water ouzel, dipper<br>0.0000006 bulbul|
vgg11_bn |0.9994940 junco, snowbird<br>0.0002460 brambling, Fringilla montifringilla<br>0.0002328 chickadee<br>0.0000130 water ouzel, dipper<br>0.0000100 goldfinch, Carduelis carduelis|
vgg13 |0.9359031 junco, snowbird<br>0.0610291 chickadee<br>0.0012531 brambling, Fringilla montifringilla<br>0.0012155 water ouzel, dipper<br>0.0002740 bulbul|
vgg13_bn |0.9927477 junco, snowbird<br>0.0041163 chickadee<br>0.0028725 brambling, Fringilla montifringilla<br>0.0000676 goldfinch, Carduelis carduelis<br>0.0000641 house finch, linnet, Carpodacus mexicanus|
vgg16 |0.8946126 junco, snowbird<br>0.0953828 chickadee<br>0.0077339 brambling, Fringilla montifringilla<br>0.0018954 water ouzel, dipper<br>0.0001777 bulbul|
vgg16_bn |0.9928786 junco, snowbird<br>0.0052144 chickadee<br>0.0011600 brambling, Fringilla montifringilla<br>0.0005868 water ouzel, dipper<br>0.0000735 house finch, linnet, Carpodacus mexicanus|
vgg19 |0.9538229 junco, snowbird<br>0.0420008 chickadee<br>0.0040804 water ouzel, dipper<br>0.0000727 brambling, Fringilla montifringilla<br>0.0000097 bulbul|
vgg19_bn |0.9973996 junco, snowbird<br>0.0010910 brambling, Fringilla montifringilla<br>0.0008814 chickadee<br>0.0004659 water ouzel, dipper<br>0.0001015 goldfinch, Carduelis carduelis|
xception |0.9466470 junco, snowbird<br>0.0224749 chickadee<br>0.0208618 brambling, Fringilla montifringilla<br>0.0095579 water ouzel, dipper<br>0.0004126 goldfinch, Carduelis carduelis|
senet_154 |0.8654007 junco, snowbird<br>0.0118391 water ouzel, dipper<br>0.0041501 brambling, Fringilla montifringilla<br>0.0038129 chickadee<br>0.0018405 house finch, linnet, Carpodacus mexicanus|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500


<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

   Model     |  Python API  |
-------------|---------------------------|
alexnet      |0.3216886 container ship, containership, container vessel<br>0.1360614 drilling platform, offshore rig<br>0.1140693 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1057479 beacon, lighthouse, beacon light, pharos<br>0.0471224 liner, ocean liner|
darknet53|0.1329412 liner, ocean liner<br>0.1074721 dock, dockage, docking facility<br>0.1047859 drilling platform, offshore rig<br>0.0996367 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0419424 lifeboat|
densenet121  |0.3022410 liner, ocean liner<br>0.1322484 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1194606 container ship, containership, container vessel<br>0.0795041 drilling platform, offshore rig<br>0.0723068 dock, dockage, docking facility|
densenet161  |0.4418391 lifeboat<br>0.1824287 liner, ocean liner<br>0.0596467 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0325274 submarine, pigboat, sub, U-boat<br>0.0298845 dock, dockage, docking facility|
densenet169  |0.2955866 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2342385 drilling platform, offshore rig<br>0.0940928 liner, ocean liner<br>0.0876009 container ship, containership, container vessel<br>0.0717737 dock, dockage, docking facility|
densenet201  |0.5008176 fireboat<br>0.0950196 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0701646 lifeboat<br>0.0622607 liner, ocean liner<br>0.0582344 container ship, containership, container vessel|
googlenet |0.0838070 lifeboat<br>0.0731668 container ship, containership, container vessel<br>0.0730509 liner, ocean liner<br>0.0729539 fireboat<br>0.0689271 drilling platform, offshore rig|
hrnet_w18_c|0.2656096 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1616489 liner, ocean liner<br>0.0651337 beacon, lighthouse, beacon light, pharos<br>0.0627509 dock, dockage, docking facility<br>0.0541241 lifeboat|
hrnet_w18_small_v1_c|0.2587051 liner, ocean liner<br>0.2280385 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0848167 beacon, lighthouse, beacon light, pharos<br>0.0490974 fireboat<br>0.0474460 lifeboat|
hrnet_w18_small_v2_c|0.3427408 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1242335 beacon, lighthouse, beacon light, pharos<br>0.0695650 liner, ocean liner<br>0.0620095 dock, dockage, docking facility<br>0.0403364 drilling platform, offshore rig|
hrnet_w30_c|0.2000750 drilling platform, offshore rig<br>0.1365042 liner, ocean liner<br>0.1290682 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0799346 catamaran<br>0.0686851 beacon, lighthouse, beacon light, pharos|
hrnet_w32_c|0.3427320 liner, ocean liner<br>0.2963618 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1066358 container ship, containership, container vessel<br>0.0607251 beacon, lighthouse, beacon light, pharos<br>0.0566134 submarine, pigboat, sub, U-boat|
hrnet_w40_c|0.1606531 submarine, pigboat, sub, U-boat<br>0.1538070 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1193006 drilling platform, offshore rig<br>0.1085498 dock, dockage, docking facility<br>0.0998095 liner, ocean liner|
hrnet_w44_c|0.6380179 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1515551 beacon, lighthouse, beacon light, pharos<br>0.0499784 drilling platform, offshore rig<br>0.0288597 lifeboat<br>0.0177580 dock, dockage, docking facility|
hrnet_w48_c|0.3150678 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1881291 lifeboat<br>0.1002933 liner, ocean liner<br>0.0560864 container ship, containership, container vessel<br>0.0427639 fireboat|
hrnet_w64_c|0.4080228 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2256251 lifeboat<br>0.0774634 beacon, lighthouse, beacon light, pharos<br>0.0533113 dock, dockage, docking facility<br>0.0362752 liner, ocean liner|
inceptionv3  |0.1505833 dock, dockage, docking facility<br>0.1179259 drilling platform, offshore rig<br>0.1058787 liner, ocean liner<br>0.0981266 container ship, containership, container vessel<br>0.0621234 lifeboat|
mobilenet0.25|0.1772091 water bottle<br>0.1686604 liner, ocean liner<br>0.0955276 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0937019 submarine, pigboat, sub, U-boat<br>0.0643868 beacon, lighthouse, beacon light, pharos|
mobilenet0.5 |0.1413260 submarine, pigboat, sub, U-boat<br>0.1064001 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0897172 container ship, containership, container vessel<br>0.0690325 liner, ocean liner<br>0.0603464 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
mobilenet0.75|0.1406201 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0317071 liner, ocean liner<br>0.0312595 beacon, lighthouse, beacon light, pharos<br>0.0274736 container ship, containership, container vessel<br>0.0195056 fireboat|
mobilenet1.0 |0.0580719 liner, ocean liner<br>0.0576046 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0517998 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0483820 lifeboat<br>0.0473302 water bottle|
mobilenet1.0_int8 | 0.0885448 liner, ocean liner<br>0.0556101 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0483991 water bottle<br>0.0429513 lifeboat<br>0.0388312 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
mobilenetv2_0.25|0.2591519 liner, ocean liner<br>0.0933797 drilling platform, offshore rig<br>0.0799795 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0531668 fireboat<br>0.0529574 container ship, containership, container vessel|
mobilenetv2_0.5 |0.1369159 container ship, containership, container vessel<br>0.1195146 liner, ocean liner<br>0.0921707 drilling platform, offshore rig<br>0.0855153 submarine, pigboat, sub, U-boat<br>0.0492694 beacon, lighthouse, beacon light, pharos|
mobilenetv2_0.75|0.1567852 liner, ocean liner<br>0.0603636 lifeboat<br>0.0488465 pirate, pirate ship<br>0.0427859 container ship, containership, container vessel<br>0.0276454 drilling platform, offshore rig|
mobilenetv2_1.0 |0.1127411 liner, ocean liner<br>0.1014166 container ship, containership, container vessel<br>0.0582132 submarine, pigboat, sub, U-boat<br>0.0552070 lifeboat<br>0.0221046 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
mobilenetV3_large |0.1392086 fireboat<br>0.0813295 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0483475 submarine, pigboat, sub, U-boat<br>0.0482562 drilling platform, offshore rig<br>0.0418803 aircraft carrier, carrier, flattop, attack aircraft carrier|
mobilenetV3_small |0.0824172 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0700601 drilling platform, offshore rig<br>0.0612908 pirate, pirate ship<br>0.0589956 beacon, lighthouse, beacon light, pharos<br>0.0458271 submarine, pigboat, sub, U-boat|
resnet18_v1 |0.3416699 container ship, containership, container vessel<br>0.1224417 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1104409 liner, ocean liner<br>0.0661493 lifeboat<br>0.0649564 pirate, pirate ship|
resnet18_v2 |0.2872601 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1359790 beacon, lighthouse, beacon light, pharos<br>0.1248601 container ship, containership, container vessel<br>0.1217950 dock, dockage, docking facility<br>0.0381382 fireboat|
resnet18_v1b |0.1451897 liner, ocean liner<br>0.1121958 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0984692 water bottle<br>0.0750244 pop bottle, soda bottle<br>0.0602022 dock, dockage, docking facility|
resnet18_v1b_0.89|0.3873618 liner, ocean liner<br>0.1239402 container ship, containership, container vessel<br>0.1021361 fireboat<br>0.0560824 dock, dockage, docking facility<br>0.0553757 submarine, pigboat, sub, U-boat|
resnet18_v1b_custom |0.0047132 spiny lobster, langouste, rock lobster, crawfish, crayfish, sea crawfish<br>0.0041157 triceratops<br>0.0040319 zebra<br>0.0039745 African chameleon, Chamaeleo chamaeleon<br>0.0039639 African hunting dog, hyena dog, Cape hunting dog, Lycaon pictus|
resnet34_v1 |0.5147043 liner, ocean liner<br>0.0504066 submarine, pigboat, sub, U-boat<br>0.0452913 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0438951 sandbar, sand bar<br>0.0422814 fireboat|
resnet34_v2 |0.4267518 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2477035 container ship, containership, container vessel<br>0.0763714 liner, ocean liner<br>0.0696334 dock, dockage, docking facility<br>0.0447001 beacon, lighthouse, beacon light, pharos|
resnet34_v1b |0.3476998 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1918807 liner, ocean liner<br>0.1346360 drilling platform, offshore rig<br>0.1013912 container ship, containership, container vessel<br>0.0379062 aircraft carrier, carrier, flattop, attack aircraft carrier|
resnet50_v1 |0.4411839 liner, ocean liner<br>0.0861827 container ship, containership, container vessel<br>0.0609572 speedboat<br>0.0587049 dock, dockage, docking facility<br>0.0369093 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
resnet50_v1_int8 |0.3967755 liner, ocean liner<br>0.0905244 container ship, containership, container vessel<br>0.0735052 dock, dockage, docking facility<br>0.0657126 speedboat<br>0.0458605 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
resnet50_v2 |0.4814195 container ship, containership, container vessel<br>0.1134715 liner, ocean liner<br>0.0718216 drilling platform, offshore rig<br>0.0571725 dock, dockage, docking facility<br>0.0450075 lifeboat|
resnet50_v1b |0.3147515 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1076186 beacon, lighthouse, beacon light, pharos<br>0.0938480 liner, ocean liner<br>0.0601708 container ship, containership, container vessel<br>0.0513268 catamaran|
resnet50_v1b_custom |0.0048008 Madagascar cat, ring-tailed lemur, Lemur catta<br>0.0047634 rock python, rock snake, Python sebae<br>0.0046949 house finch, linnet, Carpodacus mexicanus<br>0.0046650 sea slug, nudibranch<br>0.0044506 Tibetan mastiff|
resnet50_v1b_gn|0.2332796 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1691528 liner, ocean liner<br>0.1512439 beacon, lighthouse, beacon light, pharos<br>0.0507854 dock, dockage, docking facility<br>0.0476710 wreck|
resnet50_v1c |0.1537983 liner, ocean liner<br>0.1531646 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1442180 catamaran<br>0.0900431 container ship, containership, container vessel<br>0.0479482 dock, dockage, docking facility|
resnet50_v1d |0.2062457 lifeboat<br>0.0950574 beacon, lighthouse, beacon light, pharos<br>0.0893152 liner, ocean liner<br>0.0759133 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0445664 submarine, pigboat, sub, U-boat|
resnet50_v1d_0.11|0.1494648 container ship, containership, container vessel<br>0.0635204 pirate, pirate ship<br>0.0557595 drilling platform, offshore rig<br>0.0280262 liner, ocean liner<br>0.0257161 lifeboat|
resnet50_v1d_0.37|0.1321165 liner, ocean liner<br>0.0722743 container ship, containership, container vessel<br>0.0718901 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0668206 dock, dockage, docking facility<br>0.0600580 catamaran|
resnet50_v1d_0.48|0.2222678 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0869509 beacon, lighthouse, beacon light, pharos<br>0.0669275 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0598991 liner, ocean liner<br>0.0556236 submarine, pigboat, sub, U-boat|
resnet50_v1d_0.86|0.1930386 liner, ocean liner<br>0.1047459 container ship, containership, container vessel<br>0.0845692 dock, dockage, docking facility<br>0.0839940 lifeboat<br>0.0681260 submarine, pigboat, sub, U-boat|
resnet50_v1s|0.2640891 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2070212 lifeboat<br>0.0966062 dock, dockage, docking facility<br>0.0908102 container ship, containership, container vessel<br>0.0581087 beacon, lighthouse, beacon light, pharos|
resnet101_v1 |0.2196445 beacon, lighthouse, beacon light, pharos<br>0.1348773 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0985300 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0834722 fireboat<br>0.0616940 drilling platform, offshore rig|
resnet101_v2 |0.2760630 pirate, pirate ship<br>0.1350921 wreck<br>0.0808766 liner, ocean liner<br>0.0636320 drilling platform, offshore rig<br>0.0605572 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
resnet101_v1b |0.0885735 beacon, lighthouse, beacon light, pharos<br>0.0653725 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0633635 catamaran<br>0.0506628 seashore, coast, seacoast, sea-coast<br>0.0471093 pirate, pirate ship|
resnet101_v1c |0.1898097 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1086092 beacon, lighthouse, beacon light, pharos<br>0.0697590 liner, ocean liner<br>0.0553854 catamaran<br>0.0528718 dock, dockage, docking facility|
resnet101_v1d |0.3125349 beacon, lighthouse, beacon light, pharos<br>0.0871910 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0688296 drilling platform, offshore rig<br>0.0468906 liner, ocean liner<br>0.0428201 container ship, containership, container vessel|
resnet101_v1d_0.73|0.2870496 beacon, lighthouse, beacon light, pharos<br>0.1222293 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0537432 liner, ocean liner<br>0.0345260 container ship, containership, container vessel<br>0.0309129 water bottle|
resnet101_v1d_0.76|0.2803617 lifeboat<br>0.0701866 beacon, lighthouse, beacon light, pharos<br>0.0653023 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0499815 container ship, containership, container vessel<br>0.0268924 liner, ocean liner|
resnet101_v1s|0.3312930 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0998191 dock, dockage, docking facility<br>0.0886510 beacon, lighthouse, beacon light, pharos<br>0.0830901 lifeboat<br>0.0584256 liner, ocean liner|
resnet152_v1 |0.5388135 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2476967 beacon, lighthouse, beacon light, pharos<br>0.0155439 drilling platform, offshore rig<br>0.0131202 fireboat<br>0.0130310 lifeboat|
resnet152_v2 |0.1715948 drilling platform, offshore rig<br>0.1319761 beacon, lighthouse, beacon light, pharos<br>0.0740682 dock, dockage, docking facility<br>0.0558942 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0398144 container ship, containership, container vessel|
resnet152_v1b |0.1880362 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1045246 dock, dockage, docking facility<br>0.0919990 liner, ocean liner<br>0.0881177 beacon, lighthouse, beacon light, pharos<br>0.0596821 container ship, containership, container vessel|
resnet152_v1c |0.6195551 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0571322 drilling platform, offshore rig<br>0.0511749 beacon, lighthouse, beacon light, pharos<br>0.0398432 dock, dockage, docking facility<br>0.0232956 liner, ocean liner|
resnet152_v1d |0.2989854 beacon, lighthouse, beacon light, pharos<br>0.0665542 lifeboat<br>0.0560873 catamaran<br>0.0472852 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0300369 drilling platform, offshore rig|
resnet152_v1s|0.6420261 lifeboat<br>0.0874910 dock, dockage, docking facility<br>0.0536488 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0530122 fireboat<br>0.0286627 beacon, lighthouse, beacon light, pharos|
resnext50_32x4d |0.2343378 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1751438 beacon, lighthouse, beacon light, pharos<br>0.0791734 dock, dockage, docking facility<br>0.0537418 liner, ocean liner<br>0.0213372 container ship, containership, container vessel|
resnext101_32x4d |0.4391710 drilling platform, offshore rig<br>0.0688623 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0503909 beacon, lighthouse, beacon light, pharos<br>0.0230537 liner, ocean liner<br>0.0186267 container ship, containership, container vessel|
resnext101_64x4d|0.1538679 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0682765 drilling platform, offshore rig<br>0.0661227 beacon, lighthouse, beacon light, pharos<br>0.0637413 fireboat<br>0.0429024 liner, ocean liner|
se_resnext50_32x4d |0.1261469 beacon, lighthouse, beacon light, pharos<br>0.1138437 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0567448 sandbar, sand bar<br>0.0548189 dock, dockage, docking facility<br>0.0368647 drilling platform, offshore rig|
se_resnext101_32x4d |0.4807236 drilling platform, offshore rig<br>0.0311037 beacon, lighthouse, beacon light, pharos<br>0.0283869 liner, ocean liner<br>0.0250085 lifeboat<br>0.0242792 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
se_resnext101_64x4d |0.4892049 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1304153 beacon, lighthouse, beacon light, pharos<br>0.0428700 lifeboat<br>0.0310130 drilling platform, offshore rig<br>0.0167582 container ship, containership, container vessel|
resnest14 |0.4676793 lifeboat<br>0.0637489 drilling platform, offshore rig<br>0.0437817 liner, ocean liner<br>0.0277586 container ship, containership, container vessel<br>0.0164626 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
resnest26 |0.2446134 lifeboat<br>0.1767577 liner, ocean liner<br>0.1365290 container ship, containership, container vessel<br>0.0678219 dock, dockage, docking facility<br>0.0492914 breakwater, groin, groyne, mole, bulwark, seawall, jetty|
resnest50 |0.5605062 lifeboat<br>0.1056664 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0542563 drilling platform, offshore rig<br>0.0259242 liner, ocean liner<br>0.0175263 dock, dockage, docking facility|
resnest101 |0.6135045 lifeboat<br>0.1416010 beacon, lighthouse, beacon light, pharos<br>0.0873754 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0122695 drilling platform, offshore rig<br>0.0065282 fireboat|
resnest200 |0.7472307 lifeboat<br>0.0687387 beacon, lighthouse, beacon light, pharos<br>0.0341304 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0075599 fireboat<br>0.0058176 container ship, containership, container vessel|
resnest269 |0.7652729 lifeboat<br>0.0210087 liner, ocean liner<br>0.0207347 drilling platform, offshore rig<br>0.0199058 dock, dockage, docking facility<br>0.0144701 fireboat|
squeezenet1.0 |0.8105509 liner, ocean liner<br>0.0785139 drilling platform, offshore rig<br>0.0295157 container ship, containership, container vessel<br>0.0153661 dock, dockage, docking facility<br>0.0115070 submarine, pigboat, sub, U-boat|
squeezenet1.1 |0.4413090 liner, ocean liner<br>0.1931009 container ship, containership, container vessel<br>0.1459102 pirate, pirate ship<br>0.0937755 fireboat<br>0.0198681 drilling platform, offshore rig|
vgg11 |0.3343858 container ship, containership, container vessel<br>0.3068859 liner, ocean liner<br>0.0492899 submarine, pigboat, sub, U-boat<br>0.0455569 fireboat<br>0.0391509 lifeboat|
vgg11_bn |0.7272950 container ship, containership, container vessel<br>0.1716907 liner, ocean liner<br>0.0226532 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0206520 dock, dockage, docking facility<br>0.0114507 lifeboat|
vgg13 |0.3224940 container ship, containership, container vessel<br>0.2891446 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1808189 liner, ocean liner<br>0.0591592 beacon, lighthouse, beacon light, pharos<br>0.0270378 dock, dockage, docking facility|
vgg13_bn |0.3478979 container ship, containership, container vessel<br>0.2664563 fireboat<br>0.0766567 lifeboat<br>0.0664667 liner, ocean liner<br>0.0515883 submarine, pigboat, sub, U-boat|
vgg16 |0.2839452 liner, ocean liner<br>0.2079167 fireboat<br>0.1477824 container ship, containership, container vessel<br>0.0909363 lifeboat<br>0.0704186 dock, dockage, docking facility|
vgg16_bn |0.3687423 container ship, containership, container vessel<br>0.3540938 liner, ocean liner<br>0.1349642 fireboat<br>0.0337694 speedboat<br>0.0263290 submarine, pigboat, sub, U-boat|
vgg19 |0.4434193 liner, ocean liner<br>0.1207933 container ship, containership, container vessel<br>0.0979090 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0852779 drilling platform, offshore rig<br>0.0730739 dock, dockage, docking facility|
vgg19_bn |0.5504531 fireboat<br>0.1722970 liner, ocean liner<br>0.0720538 container ship, containership, container vessel<br>0.0406804 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0388017 drilling platform, offshore rig|
xception |0.9181097 water bottle<br>0.0309580 sandbar, sand bar<br>0.0148073 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0098892 seashore, coast, seacoast, sea-coast<br>0.0050070 lifeboat|
senet_154 |0.4430478 beacon, lighthouse, beacon light, pharos<br>0.2592156 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0319326 lifeboat<br>0.0148673 seashore, coast, seacoast, sea-coast<br>0.0140872 submarine, pigboat, sub, U-boat|


<!-- LINKS -->
[imagenet]: http://www.image-net.org
[gluon_modelzoo_classification]: https://cv.gluon.ai/model_zoo/classification.html
