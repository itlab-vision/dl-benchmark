# Validation results for the models inferring using PyTorch

## Image classification

Complete information about the supported classification
models is available [here][torchvision_classification].

Notes:

- For all classification models input shape BxCxHxW, where
  B is a batch size, C is an image number of channels,
  H is an image height, W is an image width.
  W=H=224 except inception_v3, for this model W=H=299.
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

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.4499779 Granny Smith<br>0.0933098 dumbbell<br>0.0876729 ocarina, sweet potato<br>0.0628701 hair slide<br>0.0484683 bottlecap<br>|
densenet121              |0.9523344 Granny Smith<br>0.0132273 orange<br>0.0125171 lemon<br>0.0027910 banana<br>0.0020333 piggy bank, penny bank<br>|
densenet161              |0.9372966 Granny Smith<br>0.0082274 dumbbell<br>0.0056475 piggy bank, penny bank<br>0.0055374 ping-pong ball<br>0.0041915 pitcher, ewer<br>|
densenet169              |0.9523344 Granny Smith<br>0.0132273 orange<br>0.0125171 lemon<br>0.0027910 banana<br>0.0020333 piggy bank, penny bank<br>|
densenet201              |0.9119796 Granny Smith<br>0.0533455 piggy bank, penny bank<br>0.0056832 lemon<br>0.0017810 pool table, billiard table, snooker table<br>0.0015689 tennis ball<br>|
googlenet              |0.5432544 Granny Smith<br>0.1103975 piggy bank, penny bank<br>0.0232569 vase<br>0.0213901 pitcher, ewer<br>0.0196196 bell pepper<br>|
inception_v3              |0.9999496 Granny Smith<br>0.0000175 piggy bank, penny bank<br>0.0000171 pomegranate<br>0.0000016 whiskey jug<br>0.0000011 water jug<br>|
mnasnet0_5              |0.0728453 Granny Smith<br>0.0632434 piggy bank, penny bank<br>0.0314232 pitcher, ewer<br>0.0235659 safety pin<br>0.0232115 saltshaker, salt shaker<br>|
mnasnet0_75              |0.1419373 Granny Smith<br>0.0228578 lemon<br>0.0172555 piggy bank, penny bank<br>0.0164039 orange<br>0.0098360 dumbbell<br>|
mnasnet1_0              |0.1931600 Granny Smith<br>0.1841204 lemon<br>0.1414814 piggy bank, penny bank<br>0.0808636 teapot<br>0.0785343 orange<br>|
mnasnet1_3              |0.2819200 Granny Smith<br>0.0192138 piggy bank, penny bank<br>0.0092013 lemon<br>0.0071209 tennis ball<br>0.0066861 orange<br>|
mobilenet_v2              |0.5066760 Granny Smith<br>0.0543401 pitcher, ewer<br>0.0461567 saltshaker, salt shaker<br>0.0433900 lemon<br>0.0314979 vase<br>|
resnext50_32x4d              |0.9059284 Granny Smith<br>0.0208117 lemon<br>0.0138094 orange<br>0.0067536 banana<br>0.0038122 piggy bank, penny bank<br>|
resnext101_32x8d              |0.4214238 Granny Smith<br>0.1213467 piggy bank, penny bank<br>0.0461432 lemon<br>0.0443953 orange<br>0.0392590 vase<br>|
resnet18              |0.1507515 safety pin<br>0.1102253 piggy bank, penny bank<br>0.0657376 purse<br>0.0558254 teapot<br>0.0341885 hair slide<br>|
resnet34              |0.9595408 Granny Smith<br>0.0054884 banana<br>0.0043731 orange<br>0.0035087 piggy bank, penny bank<br>0.0025556 lemon<br>|
resnet50              |0.9278085 Granny Smith<br>0.0129410 orange<br>0.0059573 lemon<br>0.0042141 necklace<br>0.0025712 banana<br>|
resnet101              |0.9483170 Granny Smith<br>0.0055002 hay<br>0.0050311 orange<br>0.0020548 syringe<br>0.0018223 pitcher, ewer<br>|
resnet152              |0.8913258 Granny Smith<br>0.0149238 piggy bank, penny bank<br>0.0058584 hook, claw<br>0.0057759 saltshaker, salt shaker<br>0.0044805 analog clock<br>|
shufflenet_v2_x0_5              |0.1090845 vase<br>0.1067461 piggy bank, penny bank<br>0.1048482 saltshaker, salt shaker<br>0.0685889 lemon<br>0.0643356 pitcher, ewer<br>|
shufflenet_v2_x1_0              |0.2771632 Granny Smith<br>0.1798794 safety pin<br>0.0308319 warplane, military plane<br>0.0300632 hair slide<br>0.0290498 piggy bank, penny bank<br>|
shufflenet_v2_x1_5              |0.3420659 Granny Smith<br>0.0544274 lemon<br>0.0335732 orange<br>0.0223579 piggy bank, penny bank<br>0.0180992 pomegranate<br>|
shufflenet_v2_x2_0              |0.7161155 Granny Smith<br>0.0284324 orange<br>0.0277892 lemon<br>0.0249504 piggy bank, penny bank<br>0.0099330 saltshaker, salt shaker<br>|
squeezenet1_0              |0.3275049 piggy bank, penny bank<br>0.1791330 dumbbell<br>0.1542633 Granny Smith<br>0.0912989 water bottle<br>0.0385818 rubber eraser, rubber, pencil eraser<br>|
squeezenet1_1              |0.5895362 piggy bank, penny bank<br>0.0677936 Granny Smith<br>0.0610653 necklace<br>0.0610450 lemon<br>0.0490913 bucket, pail<br>|
vgg11              |0.3721458 piggy bank, penny bank<br>0.2952032 Granny Smith<br>0.1076759 tennis ball<br>0.0314685 soap dispenser<br>0.0285692 dumbbell<br>|
vgg11_bn              |0.5464042 Granny Smith<br>0.2313125 dumbbell<br>0.0658235 piggy bank, penny bank<br>0.0269569 tennis ball<br>0.0218533 teapot<br>|
vgg13              |0.4068233 Granny Smith<br>0.2272189 dumbbell<br>0.0475026 necklace<br>0.0303710 maraca<br>0.0250665 teapot<br>|
vgg13_bn              |0.9389400 Granny Smith<br>0.0383619 tennis ball<br>0.0069443 lemon<br>0.0039320 orange<br>0.0013574 banana<br>|
vgg16              |0.2294290 Granny Smith<br>0.2084264 tennis ball<br>0.0561063 necklace<br>0.0523627 piggy bank, penny bank<br>0.0300660 pencil box, pencil case<br>|
vgg16_bn              |0.3850222 Granny Smith<br>0.0595219 dumbbell<br>0.0565265 pencil box, pencil case<br>0.0528648 tennis ball<br>0.0333556 piggy bank, penny bank<br>|
vgg19              |0.4694367 Granny Smith<br>0.1882819 tennis ball<br>0.0588473 acorn<br>0.0566673 lemon<br>0.0416055 piggy bank, penny bank<br>|
vgg19_bn              |0.8778616 Granny Smith<br>0.0404896 lemon<br>0.0315287 orange<br>0.0050720 soap dispenser<br>0.0047691 piggy bank, penny bank<br>|
wide_resnet50_2              |0.8607227 Granny Smith<br>0.0346713 piggy bank, penny bank<br>0.0130316 abacus<br>0.0083917 necklace<br>0.0075835 spindle<br>|
wide_resnet101_2              |0.5728682 Granny Smith<br>0.0822066 piggy bank, penny bank<br>0.0709140 tennis ball<br>0.0597228 golf ball<br>0.0115059 goblet<br>|



### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500

Mean: [0.485, 0.456, 0.406]

Standard deviation: [0.229, 0.224, 0.225]

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.9947648 junco, snowbird<br>0.0043087 chickadee<br>0.0002780 water ouzel, dipper<br>0.0002770 bulbul<br>0.0001244 brambling, Fringilla montifringilla<br>|
densenet121              |0.9841599 junco, snowbird<br>0.0072199 chickadee<br>0.0034963 brambling, Fringilla montifringilla<br>0.0016226 water ouzel, dipper<br>0.0012858 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
densenet161              |0.9932058 junco, snowbird<br>0.0015922 chickadee<br>0.0012295 brambling, Fringilla montifringilla<br>0.0011838 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0008891 goldfinch, Carduelis carduelis<br>|
densenet169              |0.9640695 junco, snowbird<br>0.0201315 brambling, Fringilla montifringilla<br>0.0044098 chickadee<br>0.0032345 goldfinch, Carduelis carduelis<br>0.0026739 water ouzel, dipper<br>|
densenet201              |0.9515251 junco, snowbird<br>0.0178251 water ouzel, dipper<br>0.0109119 brambling, Fringilla montifringilla<br>0.0077980 house finch, linnet, Carpodacus mexicanus<br>0.0044695 chickadee<br>|
googlenet              |0.6461046 junco, snowbird<br>0.0772564 chickadee<br>0.0468783 brambling, Fringilla montifringilla<br>0.0295898 goldfinch, Carduelis carduelis<br>0.0123323 house finch, linnet, Carpodacus mexicanus<br>|
inception_v3              |0.9999989 junco, snowbird<br>0.0000001 iron, smoothing iron<br>0.0000001 cleaver, meat cleaver, chopper<br>0.0000000 water ouzel, dipper<br>0.0000000 chickadee<br>|
mnasnet0_5              |0.9237853 junco, snowbird<br>0.0206866 chickadee<br>0.0049339 brambling, Fringilla montifringilla<br>0.0039299 water ouzel, dipper<br>0.0029348 jay<br>|
mnasnet0_75              |0.1342174 junco, snowbird<br>0.0332264 goldfinch, Carduelis carduelis<br>0.0287836 brambling, Fringilla montifringilla<br>0.0138830 chickadee<br>0.0116728 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
mnasnet1_0              |0.9980335 junco, snowbird<br>0.0013290 brambling, Fringilla montifringilla<br>0.0004499 water ouzel, dipper<br>0.0001339 chickadee<br>0.0000133 goldfinch, Carduelis carduelis<br>|
mnasnet1_3              |0.3347574 junco, snowbird<br>0.0074588 chickadee<br>0.0058638 brambling, Fringilla montifringilla<br>0.0055867 water ouzel, dipper<br>0.0047144 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
mobilenet_v2              |0.9989253 junco, snowbird<br>0.0004260 water ouzel, dipper<br>0.0004213 chickadee<br>0.0001264 brambling, Fringilla montifringilla<br>0.0000537 goldfinch, Carduelis carduelis<br>|
resnext50_32x4d              |0.9919545 junco, snowbird<br>0.0036273 brambling, Fringilla montifringilla<br>0.0016091 goldfinch, Carduelis carduelis<br>0.0015197 chickadee<br>0.0004831 water ouzel, dipper<br>|
resnext101_32x8d              |0.9755010 junco, snowbird<br>0.0071145 water ouzel, dipper<br>0.0047595 brambling, Fringilla montifringilla<br>0.0021230 chickadee<br>0.0009639 red-backed sandpiper, dunlin, Erolia alpina<br>|
resnet18              |0.9991090 junco, snowbird<br>0.0005329 chickadee<br>0.0002098 water ouzel, dipper<br>0.0000690 bulbul<br>0.0000579 brambling, Fringilla montifringilla<br>|
resnet34              |0.9923642 junco, snowbird<br>0.0043307 chickadee<br>0.0011341 water ouzel, dipper<br>0.0005041 brambling, Fringilla montifringilla<br>0.0004572 goldfinch, Carduelis carduelis<br>|
resnet50              |0.9805019 junco, snowbird<br>0.0049154 goldfinch, Carduelis carduelis<br>0.0039196 chickadee<br>0.0038097 water ouzel, dipper<br>0.0028983 brambling, Fringilla montifringilla<br>|
resnet101              |0.9986678 junco, snowbird<br>0.0004156 chickadee<br>0.0002674 goldfinch, Carduelis carduelis<br>0.0001532 brambling, Fringilla montifringilla<br>0.0001518 water ouzel, dipper<br>|
resnet152              |0.9983380 junco, snowbird<br>0.0009362 water ouzel, dipper<br>0.0003330 brambling, Fringilla montifringilla<br>0.0001030 goldfinch, Carduelis carduelis<br>0.0000701 house finch, linnet, Carpodacus mexicanus<br>|
shufflenet_v2_x0_5              |0.9972883 junco, snowbird<br>0.0010430 goldfinch, Carduelis carduelis<br>0.0004120 brambling, Fringilla montifringilla<br>0.0003422 jay<br>0.0001990 chickadee<br>|
shufflenet_v2_x1_0              |0.9997568 junco, snowbird<br>0.0001209 damselfly<br>0.0000400 chickadee<br>0.0000233 water ouzel, dipper<br>0.0000091 dragonfly, darning needle, devil's darning needle, sewing needle, snake feeder, snake doctor, mosquito hawk, skeeter hawk<br>|
shufflenet_v2_x1_5              |0.3117434 junco, snowbird<br>0.0404440 brambling, Fringilla montifringilla<br>0.0254127 chickadee<br>0.0110461 water ouzel, dipper<br>0.0090534 goldfinch, Carduelis carduelis<br>|
shufflenet_v2_x2_0              |0.3471888 junco, snowbird<br>0.0091527 chickadee<br>0.0086562 bulbul<br>0.0055233 brambling, Fringilla montifringilla<br>0.0050128 water ouzel, dipper<br>|
squeezenet1_0              |0.9904412 junco, snowbird<br>0.0045286 chickadee<br>0.0040343 brambling, Fringilla montifringilla<br>0.0003414 water ouzel, dipper<br>0.0002521 house finch, linnet, Carpodacus mexicanus<br>|
squeezenet1_1              |0.9614578 junco, snowbird<br>0.0250983 chickadee<br>0.0040701 brambling, Fringilla montifringilla<br>0.0035156 goldfinch, Carduelis carduelis<br>0.0030858 ruffed grouse, partridge, Bonasa umbellus<br>|
vgg11              |0.9998955 junco, snowbird<br>0.0000967 chickadee<br>0.0000043 brambling, Fringilla montifringilla<br>0.0000023 water ouzel, dipper<br>0.0000006 bulbul<br>|
vgg11_bn              |0.9994940 junco, snowbird<br>0.0002460 brambling, Fringilla montifringilla<br>0.0002328 chickadee<br>0.0000130 water ouzel, dipper<br>0.0000100 goldfinch, Carduelis carduelis<br>|
vgg13              |0.9359031 junco, snowbird<br>0.0610291 chickadee<br>0.0012531 brambling, Fringilla montifringilla<br>0.0012155 water ouzel, dipper<br>0.0002740 bulbul<br>|
vgg13_bn              |0.9927478 junco, snowbird<br>0.0041162 chickadee<br>0.0028725 brambling, Fringilla montifringilla<br>0.0000676 goldfinch, Carduelis carduelis<br>0.0000641 house finch, linnet, Carpodacus mexicanus<br>|
vgg16              |0.9991580 junco, snowbird<br>0.0007120 chickadee<br>0.0000800 water ouzel, dipper<br>0.0000323 brambling, Fringilla montifringilla<br>0.0000049 house finch, linnet, Carpodacus mexicanus<br>|
vgg16_bn              |0.9920998 junco, snowbird<br>0.0066640 chickadee<br>0.0004240 jay<br>0.0003181 water ouzel, dipper<br>0.0001396 brambling, Fringilla montifringilla<br>|
vgg19              |0.9994042 junco, snowbird<br>0.0003172 brambling, Fringilla montifringilla<br>0.0001609 chickadee<br>0.0000671 water ouzel, dipper<br>0.0000236 goldfinch, Carduelis carduelis<br>|
vgg19_bn              |0.9999533 junco, snowbird<br>0.0000318 chickadee<br>0.0000074 brambling, Fringilla montifringilla<br>0.0000030 water ouzel, dipper<br>0.0000021 house finch, linnet, Carpodacus mexicanus<br>|
wide_resnet50_2              |0.9617861 junco, snowbird<br>0.0119062 water ouzel, dipper<br>0.0064385 chickadee<br>0.0044642 brambling, Fringilla montifringilla<br>0.0019096 bulbul<br>|
wide_resnet101_2              |0.9748272 junco, snowbird<br>0.0074479 water ouzel, dipper<br>0.0047218 chickadee<br>0.0023339 brambling, Fringilla montifringilla<br>0.0022661 goldfinch, Carduelis carduelis<br>|


### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500

Mean: [0.485, 0.456, 0.406]

Standard deviation: [0.229, 0.224, 0.225]

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.3216888 container ship, containership, container vessel<br>0.1360615 drilling platform, offshore rig<br>0.1140690 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1057476 beacon, lighthouse, beacon light, pharos<br>0.0471225 liner, ocean liner<br>|
densenet121              |0.3022412 liner, ocean liner<br>0.1322481 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1194608 container ship, containership, container vessel<br>0.0795042 drilling platform, offshore rig<br>0.0723068 dock, dockage, docking facility<br>|
densenet161              |0.4418393 lifeboat<br>0.1824290 liner, ocean liner<br>0.0596464 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0325273 submarine, pigboat, sub, U-boat<br>0.0298845 dock, dockage, docking facility<br>|
densenet169              |0.2955876 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2342377 drilling platform, offshore rig<br>0.0940930 liner, ocean liner<br>0.0876009 container ship, containership, container vessel<br>0.0717737 dock, dockage, docking facility<br>|
densenet201              |0.5008168 fireboat<br>0.0950198 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0701648 lifeboat<br>0.0622605 liner, ocean liner<br>0.0582345 container ship, containership, container vessel<br>|
googlenet              |0.1323652 liner, ocean liner<br>0.0796395 drilling platform, offshore rig<br>0.0678082 container ship, containership, container vessel<br>0.0585721 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0366881 fireboat<br>|
inception_v3              |0.3510072 drilling platform, offshore rig<br>0.3065925 beacon, lighthouse, beacon light, pharos<br>0.1853052 submarine, pigboat, sub, U-boat<br>0.0660644 wreck<br>0.0121473 space shuttle<br>|
mnasnet0_5              |0.0854459 drilling platform, offshore rig<br>0.0850178 liner, ocean liner<br>0.0445188 container ship, containership, container vessel<br>0.0357058 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0247475 aircraft carrier, carrier, flattop, attack aircraft carrier<br>|
mnasnet0_75              |0.0212122 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0189475 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0135526 beacon, lighthouse, beacon light, pharos<br>0.0114984 submarine, pigboat, sub, U-boat<br>0.0114306 liner, ocean liner<br>|
mnasnet1_0              |0.2078572 container ship, containership, container vessel<br>0.1769478 dock, dockage, docking facility<br>0.1064179 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0966766 liner, ocean liner<br>0.0637138 lifeboat<br>|
mnasnet1_3              |0.0924414 lifeboat<br>0.0341632 container ship, containership, container vessel<br>0.0281921 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0210488 liner, ocean liner<br>0.0208530 beacon, lighthouse, beacon light, pharos<br>|
mobilenet_v2              |0.3933903 container ship, containership, container vessel<br>0.2136005 liner, ocean liner<br>0.0991812 beacon, lighthouse, beacon light, pharos<br>0.0715421 drilling platform, offshore rig<br>0.0498366 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>|
resnext50_32x4d              |0.3138136 liner, ocean liner<br>0.1791683 catamaran<br>0.0695947 drilling platform, offshore rig<br>0.0535790 dock, dockage, docking facility<br>0.0486278 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>|
resnext101_32x8d              |0.2383151 beacon, lighthouse, beacon light, pharos<br>0.2232965 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1179476 water bottle<br>0.0526662 drilling platform, offshore rig<br>0.0363510 liner, ocean liner<br>|
resnet18              |0.1980100 liner, ocean liner<br>0.1092247 submarine, pigboat, sub, U-boat<br>0.1024882 container ship, containership, container vessel<br>0.1021967 drilling platform, offshore rig<br>0.0800809 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>|
resnet34              |0.2605784 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1120401 fireboat<br>0.1080514 liner, ocean liner<br>0.0992261 pirate, pirate ship<br>0.0759654 container ship, containership, container vessel<br>|
resnet50              |0.4759621 liner, ocean liner<br>0.1025401 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0690000 container ship, containership, container vessel<br>0.0524496 dock, dockage, docking facility<br>0.0473781 pirate, pirate ship<br>|
resnet101              |0.8149654 drilling platform, offshore rig<br>0.0403631 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0207643 beacon, lighthouse, beacon light, pharos<br>0.0188019 container ship, containership, container vessel<br>0.0160020 liner, ocean liner<br>|
resnet152              |0.3274736 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.2284682 liner, ocean liner<br>0.0779443 lifeboat<br>0.0710691 beacon, lighthouse, beacon light, pharos<br>0.0688560 container ship, containership, container vessel<br>|
shufflenet_v2_x0_5              |0.2142884 agama<br>0.0945462 water bottle<br>0.0885760 jay<br>0.0579272 liner, ocean liner<br>0.0566052 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>|
shufflenet_v2_x1_0              |0.3391730 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1130056 beacon, lighthouse, beacon light, pharos<br>0.0324217 liner, ocean liner<br>0.0203185 terrapin<br>0.0181812 drilling platform, offshore rig<br>|
shufflenet_v2_x1_5              |0.0450035 pirate, pirate ship<br>0.0366058 lifeboat<br>0.0158971 liner, ocean liner<br>0.0139720 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0139460 dock, dockage, docking facility<br>|
shufflenet_v2_x2_0              |0.0682886 beacon, lighthouse, beacon light, pharos<br>0.0495765 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0448658 container ship, containership, container vessel<br>0.0410116 liner, ocean liner<br>0.0403494 lifeboat<br>|
squeezenet1_0              |0.8105499 liner, ocean liner<br>0.0785143 drilling platform, offshore rig<br>0.0295160 container ship, containership, container vessel<br>0.0153662 dock, dockage, docking facility<br>0.0115069 submarine, pigboat, sub, U-boat<br>|
squeezenet1_1              |0.4413064 liner, ocean liner<br>0.1931020 container ship, containership, container vessel<br>0.1459110 pirate, pirate ship<br>0.0937753 fireboat<br>0.0198683 drilling platform, offshore rig<br>|
vgg11              |0.3343855 container ship, containership, container vessel<br>0.3068857 liner, ocean liner<br>0.0492899 submarine, pigboat, sub, U-boat<br>0.0455569 fireboat<br>0.0391509 lifeboat<br>|
vgg11_bn              |0.7272952 container ship, containership, container vessel<br>0.1716904 liner, ocean liner<br>0.0226532 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0206520 dock, dockage, docking facility<br>0.0114507 lifeboat<br>|
vgg13              |0.3224932 container ship, containership, container vessel<br>0.2891453 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1808192 liner, ocean liner<br>0.0591593 beacon, lighthouse, beacon light, pharos<br>0.0270378 dock, dockage, docking facility<br>|
vgg13_bn              |0.3478982 container ship, containership, container vessel<br>0.2664560 fireboat<br>0.0766569 lifeboat<br>0.0664668 liner, ocean liner<br>0.0515882 submarine, pigboat, sub, U-boat<br>|
vgg16              |0.4804810 container ship, containership, container vessel<br>0.1304805 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0867475 liner, ocean liner<br>0.0751447 drilling platform, offshore rig<br>0.0444228 lifeboat<br>|
vgg16_bn              |0.5045572 container ship, containership, container vessel<br>0.1368753 liner, ocean liner<br>0.1096228 lifeboat<br>0.0501405 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0392852 dock, dockage, docking facility<br>|
vgg19              |0.4432594 container ship, containership, container vessel<br>0.1617560 liner, ocean liner<br>0.1536936 fireboat<br>0.0549521 drilling platform, offshore rig<br>0.0304159 lifeboat<br>|
vgg19_bn              |0.2604308 fireboat<br>0.1715146 container ship, containership, container vessel<br>0.0810636 submarine, pigboat, sub, U-boat<br>0.0738690 dock, dockage, docking facility<br>0.0685641 lifeboat<br>|
wide_resnet50_2              |0.1823847 liner, ocean liner<br>0.1433828 dock, dockage, docking facility<br>0.1098627 container ship, containership, container vessel<br>0.0992484 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0717444 catamaran<br>|
wide_resnet101_2              |0.4919022 drilling platform, offshore rig<br>0.0996324 liner, ocean liner<br>0.0898810 beacon, lighthouse, beacon light, pharos<br>0.0402922 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0381101 catamaran<br>|

<!-- LINKS -->
[imagenet]: http://www.image-net.org
[torchvision_classification]: https://pytorch.org/vision/0.8/models.html
