# Validation results for the models inferring using OpenCV (IE backend)

## Image classification

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.9896094 Granny Smith<br>0.0037969 bell pepper<br>0.0013717 piggy bank, penny bank<br>0.0011059 acorn<br>0.0009710 fig<br>|
caffenet             |0.8602298 Granny Smith<br>0.0503849 teapot<br>0.0141508 piggy bank, penny bank<br>0.0113873 saltshaker, salt shaker<br>0.0104464 bell pepper<br>|
convnext-tiny        |8.9958363 Granny Smith<br>1.5541909 orange<br>1.3344822 crate<br>1.3133279 military uniform<br>1.3033230 lemon<br>|
densenet-121         |15.7979145 Granny Smith<br>9.9429483 lemon<br>9.3676071 orange<br>8.6181574 banana<br>7.1164074 tennis ball<br>|
densenet-121-tf      |0.9939485 Granny Smith<br>0.0029237 lemon<br>0.0014410 orange<br>0.0006841 banana<br>0.0001481 fig<br>|
dla-34               |11.2761707 Granny Smith<br>6.9377527 fig<br>6.4480419 tennis ball<br>5.9033742 lemon<br>5.6257262 dumbbell<br>|
efficientnet-b0-pytorch |10.4229183 Granny Smith<br>3.4506552 fig<br>3.4175596 tennis ball<br>3.2212656 piggy bank, penny bank<br>2.9930823 teapot<br>|
efficientnet-v2-b0   |9.9698296 Granny Smith<br>3.0172594 tennis ball<br>2.7638943 lemon<br>2.5047600 bell pepper<br>2.4356534 orange<br>|
efficientnet-v2-s    |9.7563076 Granny Smith<br>2.2714353 green mamba<br>2.1594198 croquet ball<br>1.9994626 Siamese cat, Siamese<br>1.9378304 orange<br>|
googlenet-v1         |0.9982972 Granny Smith<br>0.0005613 bell pepper<br>0.0003487 candle, taper, wax light<br>0.0000679 tennis ball<br>0.0000656 piggy bank, penny bank<br>|
googlenet-v1-tf      |0.8873318 Granny Smith<br>0.0083221 lemon<br>0.0073108 piggy bank, penny bank<br>0.0063511 pomegranate<br>0.0033214 banana<br>|
googlenet-v2-tf      |0.9925030 Granny Smith<br>0.0003358 lemon<br>0.0002452 pomegranate<br>0.0002079 tennis ball<br>0.0001853 banana<br>|
googlenet-v3         |0.9951954 Granny Smith<br>0.0004196 bikini, two-piece<br>0.0000741 Band Aid<br>0.0000674 piggy bank, penny bank<br>0.0000554 brassiere, bra, bandeau<br>|
googlenet-v4-tf      |0.9900998 Granny Smith<br>0.0003072 Rhodesian ridgeback<br>0.0001467 hair slide<br>0.0001104 pineapple, ananas<br>0.0000988 banana<br>|
hbonet-0.25          |17.2663136 Granny Smith<br>14.2053719 tennis ball<br>12.7874222 green snake, grass snake<br>12.4133892 bell pepper<br>12.2039146 fig<br>|
hbonet-1.0           |14.2947559 Granny Smith<br>9.1487637 lemon<br>9.0358086 fig<br>8.9222002 cup<br>8.8918133 vase<br>|
inception-resnet-v2-tf |9.1892223 Granny Smith<br>4.2343912 pomegranate<br>3.3494289 lemon<br>3.2723539 crate<br>3.2125192 orange<br>|
mobilenet-v1-0.25-128 |0.5188020 bell pepper<br>0.1175016 Granny Smith<br>0.0549230 cucumber, cuke<br>0.0392878 strawberry<br>0.0295592 broccoli<br>|
mobilenet-v1-1.0-224 |0.9441363 Granny Smith<br>0.0080111 fig<br>0.0042947 lemon<br>0.0042536 custard apple<br>0.0036513 orange<br>|
mobilenet-v1-1.0-224-tf |0.7547259 Granny Smith<br>0.0404322 saltshaker, salt shaker<br>0.0232461 lemon<br>0.0218173 fig<br>0.0153217 rubber eraser, rubber, pencil eraser<br>|
mobilenet-v2         |0.9951226 Granny Smith<br>0.0009853 fig<br>0.0007886 lemon<br>0.0006782 pomegranate<br>0.0006098 piggy bank, penny bank<br>|
mobilenet-v2-1.0-224 |0.9844690 Granny Smith<br>0.0003918 piggy bank, penny bank<br>0.0002854 green snake, grass snake<br>0.0002140 bell pepper<br>0.0001963 acorn<br>|
mobilenet-v2-1.4-224 |0.8810015 Granny Smith<br>0.0252362 fig<br>0.0074155 jackfruit, jak, jack<br>0.0054691 custard apple<br>0.0037350 lemon<br>|
mobilenet-v3-large-1.0-224-tf |0.9964420 Granny Smith<br>0.0002401 bell pepper<br>0.0001802 lemon<br>0.0001636 tennis ball<br>0.0001620 fig<br>|
mobilenet-v3-small-1.0-224-tf |0.8053148 Granny Smith<br>0.0281765 fig<br>0.0171755 lemon<br>0.0161600 bell pepper<br>0.0090295 strawberry<br>|
nfnet-f0             |8.2904587 Granny Smith<br>1.7036148 orange<br>1.4136231 lemon<br>1.3692873 tennis ball<br>1.3179532 tray<br>|
regnetx-3.2gf        |17.9561234 Granny Smith<br>8.9531670 piggy bank, penny bank<br>7.8655953 tennis ball<br>6.9753861 screw<br>6.9729953 orange<br>|
repvgg-a0            |18.5661106 Granny Smith<br>9.8166199 acorn<br>9.7410145 teapot<br>9.5852728 fig<br>9.4273586 piggy bank, penny bank<br>|
repvgg-b1            |16.7964344 Granny Smith<br>7.4920535 candle, taper, wax light<br>7.3861327 lemon<br>7.3710642 purse<br>7.2753754 cup<br>|
repvgg-b3            |13.2293549 Granny Smith<br>3.1549642 lemon<br>3.0749834 banana<br>2.7251165 fig<br>2.6711121 syringe<br>|
resnet-50-tf         |0.9986790 Granny Smith<br>0.0001879 banana<br>0.0001561 acorn<br>0.0001348 lemon<br>0.0000943 fig<br>|
shufflenet-v2-x0.5   |14.8072624 Granny Smith<br>13.4187317 bell pepper<br>12.5896816 lemon<br>12.3368931 cucumber, cuke<br>11.8330803 fig<br>|
shufflenet-v2-x1.0   |13.5337648 Granny Smith<br>7.2673421 piggy bank, penny bank<br>6.3470674 teapot<br>6.0261302 warplane, military plane<br>5.9806600 safety pin<br>|
squeezenet1.0        |0.9988523 Granny Smith<br>0.0004736 fig<br>0.0001965 bell pepper<br>0.0000892 piggy bank, penny bank<br>0.0000732 tennis ball<br>|
squeezenet1.1        |0.9937355 Granny Smith<br>0.0014752 lemon<br>0.0013913 fig<br>0.0008874 tennis ball<br>0.0006791 piggy bank, penny bank<br>|
t2t-vit-14           |9.1455536 Granny Smith<br>1.9544238 tennis ball<br>1.6415716 lemon<br>1.5808551 syringe<br>1.4673669 piggy bank, penny bank<br>|
vgg16                |0.7317344 Granny Smith<br>0.0350750 bell pepper<br>0.0209236 grocery store, grocery, food market, market<br>0.0137958 saltshaker, salt shaker<br>0.0127183 fig<br>|
vgg19                |0.7072729 Granny Smith<br>0.0805917 acorn<br>0.0473263 fig<br>0.0367724 necklace<br>0.0180316 lemon<br>|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.9979280 junco, snowbird<br>0.0020288 chickadee<br>0.0000137 jay<br>0.0000119 brambling, Fringilla montifringilla<br>0.0000104 bulbul<br>|
caffenet             |0.9997593 junco, snowbird<br>0.0002351 chickadee<br>0.0000033 brambling, Fringilla montifringilla<br>0.0000010 bulbul<br>0.0000007 jay<br>|
convnext-tiny        |9.1146832 junco, snowbird<br>1.5958253 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>1.4651724 brambling, Fringilla montifringilla<br>1.3361552 lacewing, lacewing fly<br>1.1702032 cricket<br>|
densenet-121         |17.8269691 junco, snowbird<br>11.4734726 brambling, Fringilla montifringilla<br>11.3202248 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>10.3598862 chickadee<br>8.2504816 magpie<br>|
densenet-121-tf      |0.9960338 junco, snowbird<br>0.0016738 brambling, Fringilla montifringilla<br>0.0014138 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0004691 chickadee<br>0.0000661 magpie<br>|
dla-34               |18.2753429 junco, snowbird<br>9.4783382 brambling, Fringilla montifringilla<br>8.8363400 chickadee<br>7.9899230 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>7.9558954 water ouzel, dipper<br>|
efficientnet-b0-pytorch |11.0220919 junco, snowbird<br>4.6539059 chickadee<br>3.3183093 brambling, Fringilla montifringilla<br>2.9133186 water ouzel, dipper<br>2.5835512 goldfinch, Carduelis carduelis<br>|
efficientnet-v2-b0   |9.8332729 junco, snowbird<br>3.2819800 chickadee<br>2.5940940 brambling, Fringilla montifringilla<br>2.5063193 American coot, marsh hen, mud hen, water hen, Fulica americana<br>2.4632654 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
efficientnet-v2-s    |9.3140516 junco, snowbird<br>2.2458248 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>1.9766805 hamster<br>1.7983806 oystercatcher, oyster catcher<br>1.7608243 goldfinch, Carduelis carduelis<br>|
googlenet-v1         |0.9999954 junco, snowbird<br>0.0000043 chickadee<br>0.0000003 brambling, Fringilla montifringilla<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000000 water ouzel, dipper<br>|
googlenet-v1-tf      |0.8905122 junco, snowbird<br>0.0376492 brambling, Fringilla montifringilla<br>0.0115119 chickadee<br>0.0029901 goldfinch, Carduelis carduelis<br>0.0027506 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
googlenet-v2-tf      |0.9514890 junco, snowbird<br>0.0017660 chickadee<br>0.0015834 brambling, Fringilla montifringilla<br>0.0009348 loupe, jeweler's loupe<br>0.0007034 American coot, marsh hen, mud hen, water hen, Fulica americana<br>|
googlenet-v3         |0.9069702 junco, snowbird<br>0.0006983 water ouzel, dipper<br>0.0006681 American coot, marsh hen, mud hen, water hen, Fulica americana<br>0.0006445 cleaver, meat cleaver, chopper<br>0.0006050 iron, smoothing iron<br>|
googlenet-v4-tf      |0.9426625 junco, snowbird<br>0.0005340 chickadee<br>0.0004552 hamster<br>0.0004131 brambling, Fringilla montifringilla<br>0.0003347 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
hbonet-0.25          |20.5088139 junco, snowbird<br>17.8573513 chickadee<br>16.4232254 brambling, Fringilla montifringilla<br>13.0919437 jay<br>12.8791981 goldfinch, Carduelis carduelis<br>|
hbonet-1.0           |25.9305286 junco, snowbird<br>18.4999161 chickadee<br>16.3906898 brambling, Fringilla montifringilla<br>14.7982817 goldfinch, Carduelis carduelis<br>13.1259842 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
inception-resnet-v2-tf |10.2546673 junco, snowbird<br>5.3206620 brambling, Fringilla montifringilla<br>3.7312555 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>2.8738842 hamster<br>2.7935836 chickadee<br>|
mobilenet-v1-0.25-128 |0.9801750 junco, snowbird<br>0.0190140 chickadee<br>0.0003644 brambling, Fringilla montifringilla<br>0.0002570 jay<br>0.0000603 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
mobilenet-v1-1.0-224 |0.9988418 junco, snowbird<br>0.0007267 chickadee<br>0.0002552 brambling, Fringilla montifringilla<br>0.0000451 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000312 bulbul<br>|
mobilenet-v1-1.0-224-tf |0.9979226 junco, snowbird<br>0.0014879 chickadee<br>0.0005082 brambling, Fringilla montifringilla<br>0.0000585 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000071 jay<br>|
mobilenet-v2         |0.9998599 junco, snowbird<br>0.0000698 brambling, Fringilla montifringilla<br>0.0000668 chickadee<br>0.0000014 water ouzel, dipper<br>0.0000011 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
mobilenet-v2-1.0-224 |0.9005619 junco, snowbird<br>0.0027264 chickadee<br>0.0021331 water ouzel, dipper<br>0.0018665 brambling, Fringilla montifringilla<br>0.0008477 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
mobilenet-v2-1.4-224 |0.8708087 junco, snowbird<br>0.0020907 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0017842 water ouzel, dipper<br>0.0014236 brambling, Fringilla montifringilla<br>0.0013358 chickadee<br>|
mobilenet-v3-large-1.0-224-tf |0.8872589 junco, snowbird<br>0.0007308 American coot, marsh hen, mud hen, water hen, Fulica americana<br>0.0007247 brambling, Fringilla montifringilla<br>0.0006315 water ouzel, dipper<br>0.0005308 wood rabbit, cottontail, cottontail rabbit<br>|
mobilenet-v3-small-1.0-224-tf |0.9578514 junco, snowbird<br>0.0016599 chickadee<br>0.0016166 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0009595 jay<br>0.0006696 brambling, Fringilla montifringilla<br>|
nfnet-f0             |8.8884630 junco, snowbird<br>1.9537926 brambling, Fringilla montifringilla<br>1.6793123 water ouzel, dipper<br>1.6440620 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>1.5960771 American coot, marsh hen, mud hen, water hen, Fulica americana<br>|
regnetx-3.2gf        |15.8536396 junco, snowbird<br>7.8364000 chickadee<br>7.1086564 goldfinch, Carduelis carduelis<br>7.0338268 brambling, Fringilla montifringilla<br>6.8863440 water ouzel, dipper<br>|
repvgg-a0            |26.3615952 junco, snowbird<br>19.2394314 chickadee<br>17.6558857 brambling, Fringilla montifringilla<br>14.7114849 goldfinch, Carduelis carduelis<br>14.4735651 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
repvgg-b1            |19.3077412 junco, snowbird<br>11.3808165 brambling, Fringilla montifringilla<br>10.3980303 chickadee<br>9.7500534 water ouzel, dipper<br>9.3564224 goldfinch, Carduelis carduelis<br>|
repvgg-b3            |14.0971813 junco, snowbird<br>3.1309497 water ouzel, dipper<br>2.6912334 chickadee<br>2.2140563 oystercatcher, oyster catcher<br>1.9939196 quail<br>|
resnet-50-tf         |0.9999458 junco, snowbird<br>0.0000307 chickadee<br>0.0000170 brambling, Fringilla montifringilla<br>0.0000028 goldfinch, Carduelis carduelis<br>0.0000013 water ouzel, dipper<br>|
shufflenet-v2-x0.5   |27.7634544 junco, snowbird<br>20.2297573 chickadee<br>19.7337132 jay<br>18.1307297 brambling, Fringilla montifringilla<br>16.9049988 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
shufflenet-v2-x1.0   |25.2157574 junco, snowbird<br>10.2119236 American coot, marsh hen, mud hen, water hen, Fulica americana<br>10.1851845 damselfly<br>10.1463785 chickadee<br>9.6026402 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
squeezenet1.0        |0.9931426 junco, snowbird<br>0.0064122 chickadee<br>0.0003084 brambling, Fringilla montifringilla<br>0.0000394 bulbul<br>0.0000340 magpie<br>|
squeezenet1.1        |0.9949969 junco, snowbird<br>0.0048572 chickadee<br>0.0000578 jay<br>0.0000297 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0000271 brambling, Fringilla montifringilla<br>|
t2t-vit-14           |9.0317535 junco, snowbird<br>1.9845200 brambling, Fringilla montifringilla<br>1.8275673 oystercatcher, oyster catcher<br>1.7650952 American coot, marsh hen, mud hen, water hen, Fulica americana<br>1.5909541 chickadee<br>|
vgg16                |0.9999772 junco, snowbird<br>0.0000132 brambling, Fringilla montifringilla<br>0.0000089 chickadee<br>0.0000006 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|
vgg19                |0.9999394 junco, snowbird<br>0.0000580 brambling, Fringilla montifringilla<br>0.0000023 chickadee<br>0.0000002 water ouzel, dipper<br>0.0000000 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500
﻿

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

   Model             |  Python (implementation)  |
---------------------|---------------------------|
alexnet              |0.9991654 lifeboat<br>0.0003741 container ship, containership, container vessel<br>0.0001206 pirate, pirate ship<br>0.0000820 drilling platform, offshore rig<br>0.0000784 wreck<br>|
caffenet             |0.9839840 lifeboat<br>0.0109296 container ship, containership, container vessel<br>0.0018576 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0007185 wreck<br>0.0007133 pirate, pirate ship<br>|
convnext-tiny        |10.0250521 lifeboat<br>2.9457700 beacon, lighthouse, beacon light, pharos<br>2.3076172 drilling platform, offshore rig<br>2.3043602 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.1287599 pirate, pirate ship|
densenet-121         |13.9662323 lifeboat<br>7.8177366 drilling platform, offshore rig<br>7.7323356 liner, ocean liner<br>7.5702772 wreck<br>7.5621595 pirate, pirate ship<br>|
densenet-121-tf      |0.9841739 lifeboat<br>0.0021340 drilling platform, offshore rig<br>0.0018787 liner, ocean liner<br>0.0017149 wreck<br>0.0016311 pirate, pirate ship<br>|
dla-34               |12.3063564 lifeboat<br>8.2191267 pirate, pirate ship<br>8.1342840 liner, ocean liner<br>7.8728123 wreck<br>7.7409649 container ship, containership, container vessel<br>|
efficientnet-b0-pytorch |8.5946884 lifeboat<br>4.9071603 container ship, containership, container vessel<br>4.8022614 drilling platform, offshore rig<br>4.5650768 liner, ocean liner<br>4.4569731 beacon, lighthouse, beacon light, pharos<br>|
efficientnet-v2-b0   |9.3472309 lifeboat<br>4.5113249 fireboat<br>3.5942109 drilling platform, offshore rig<br>3.0452106 liner, ocean liner<br>2.9931762 submarine, pigboat, sub, U-boat<br>|
efficientnet-v2-s    |8.7878838 lifeboat<br>4.2255139 beacon, lighthouse, beacon light, pharos<br>2.8448100 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.3274198 drilling platform, offshore rig<br>2.1449640 container ship, containership, container vessel<br>|
googlenet-v1         |0.8990629 lifeboat<br>0.0275983 drilling platform, offshore rig<br>0.0209237 beacon, lighthouse, beacon light, pharos<br>0.0196472 container ship, containership, container vessel<br>0.0062734 liner, ocean liner<br>|
googlenet-v1-tf      |0.5706088 lifeboat<br>0.0325632 fireboat<br>0.0318643 drilling platform, offshore rig<br>0.0204104 container ship, containership, container vessel<br>0.0166425 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>|
googlenet-v2-tf      |0.6405345 lifeboat<br>0.0454823 fireboat<br>0.0320881 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0218709 beacon, lighthouse, beacon light, pharos<br>0.0132588 dock, dockage, docking facility<br>|
googlenet-v3         |0.9512258 lifeboat<br>0.0023981 backpack, back pack, knapsack, packsack, rucksack, haversack<br>0.0005372 beacon, lighthouse, beacon light, pharos<br>0.0005263 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0003984 hook, claw<br>|
googlenet-v4-tf      |0.9516075 lifeboat<br>0.0006138 fireboat<br>0.0005795 submarine, pigboat, sub, U-boat<br>0.0003894 ambulance<br>0.0003887 drilling platform, offshore rig<br>|
hbonet-0.25          |14.6844559 liner, ocean liner<br>14.2568951 lifeboat<br>13.5083447 pirate, pirate ship<br>13.3783140 drilling platform, offshore rig<br>13.0703144 wreck<br>|
hbonet-1.0           |14.2455578 lifeboat<br>10.1138697 beacon, lighthouse, beacon light, pharos<br>10.0616055 pirate, pirate ship<br>9.7654886 drilling platform, offshore rig<br>9.4924793 container ship, containership, container vessel<br>|
inception-resnet-v2-tf |8.9238825 lifeboat<br>5.3607125 fireboat<br>4.2531109 beacon, lighthouse, beacon light, pharos<br>3.9253383 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>3.2657933 ambulance<br>|
mobilenet-v1-0.25-128 |0.8000432 lifeboat<br>0.0681746 container ship, containership, container vessel<br>0.0423646 pirate, pirate ship<br>0.0320395 liner, ocean liner<br>0.0205679 fireboat<br>|
mobilenet-v1-1.0-224 |0.8883280 lifeboat<br>0.0358161 pirate, pirate ship<br>0.0247643 container ship, containership, container vessel<br>0.0106019 drilling platform, offshore rig<br>0.0084067 liner, ocean liner<br>|
mobilenet-v1-1.0-224-tf |0.9885069 lifeboat<br>0.0053200 fireboat<br>0.0021363 liner, ocean liner<br>0.0006076 pirate, pirate ship<br>0.0005722 submarine, pigboat, sub, U-boat<br>|
mobilenet-v2         |0.9638824 lifeboat<br>0.0142666 pirate, pirate ship<br>0.0047917 submarine, pigboat, sub, U-boat<br>0.0040148 container ship, containership, container vessel<br>0.0019009 space shuttle<br>|
mobilenet-v2-1.0-224 |0.2958092 lifeboat<br>0.1187279 wreck<br>0.0404660 beacon, lighthouse, beacon light, pharos<br>0.0361662 liner, ocean liner<br>0.0325511 pirate, pirate ship<br>|
mobilenet-v2-1.4-224 |0.8931445 lifeboat<br>0.0078881 container ship, containership, container vessel<br>0.0038566 liner, ocean liner<br>0.0020695 dock, dockage, docking facility<br>0.0017923 pirate, pirate ship<br>|
mobilenet-v3-large-1.0-224-tf |0.8503661 lifeboat<br>0.0020597 drilling platform, offshore rig<br>0.0014562 fireboat<br>0.0014101 freight car<br>0.0013729 yellow lady's slipper, yellow lady-slipper, Cypripedium calceolus, Cypripedium parviflorum<br>|
mobilenet-v3-small-1.0-224-tf |0.7335873 lifeboat<br>0.0158998 liner, ocean liner<br>0.0122766 pirate, pirate ship<br>0.0066294 fireboat<br>0.0059244 beacon, lighthouse, beacon light, pharos<br>|
nfnet-f0             |9.3943815 lifeboat<br>3.9287939 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>3.4282088 beacon, lighthouse, beacon light, pharos<br>2.3570781 submarine, pigboat, sub, U-boat<br>2.3469169 speedboat<br>|
regnetx-3.2gf        |12.8932285 lifeboat<br>7.4015584 liner, ocean liner<br>7.2869158 pirate, pirate ship<br>7.0655079 wreck<br>6.2971840 drilling platform, offshore rig<br>|
repvgg-a0            |17.1645432 lifeboat<br>14.7260256 container ship, containership, container vessel<br>13.8417215 drilling platform, offshore rig<br>13.1186962 liner, ocean liner<br>12.8922052 dock, dockage, docking facility<br>|
repvgg-b1            |15.2668896 lifeboat<br>7.8373547 drilling platform, offshore rig<br>7.8056054 liner, ocean liner<br>7.7971869 pirate, pirate ship<br>7.6713929 container ship, containership, container vessel<br>|
repvgg-b3            |11.1052322 lifeboat<br>4.6516232 beacon, lighthouse, beacon light, pharos<br>4.1327052 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.4998040 liner, ocean liner<br>2.3353925 fireboat<br>|
resnet-50-tf         |0.9849118 lifeboat<br>0.0031135 drilling platform, offshore rig<br>0.0026399 pirate, pirate ship<br>0.0016441 submarine, pigboat, sub, U-boat<br>0.0013418 liner, ocean liner<br>|
shufflenet-v2-x0.5   |16.4951305 lifeboat<br>13.4137926 drilling platform, offshore rig<br>12.9157162 pirate, pirate ship<br>11.6706381 fireboat<br>11.2358427 aircraft carrier, carrier, flattop, attack aircraft carrier<br>|
shufflenet-v2-x1.0   |12.9555531 lifeboat<br>8.1005497 meerkat, mierkat<br>7.9074183 drilling platform, offshore rig<br>7.6318173 lacewing, lacewing fly<br>6.9140663 box turtle, box tortoise<br>|
squeezenet1.0        |0.9870794 lifeboat<br>0.0061878 container ship, containership, container vessel<br>0.0025447 fireboat<br>0.0024638 liner, ocean liner<br>0.0004083 beacon, lighthouse, beacon light, pharos<br>|
squeezenet1.1        |0.9570300 lifeboat<br>0.0211556 container ship, containership, container vessel<br>0.0102893 drilling platform, offshore rig<br>0.0034316 pirate, pirate ship<br>0.0029377 dock, dockage, docking facility<br>|
t2t-vit-14           |8.5352468 lifeboat<br>3.5179203 beacon, lighthouse, beacon light, pharos<br>2.8752832 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>2.2658072 drilling platform, offshore rig<br>2.0035105 promontory, headland, head, foreland<br>|
vgg16                |0.9821915 lifeboat<br>0.0082832 container ship, containership, container vessel<br>0.0014539 drilling platform, offshore rig<br>0.0014494 pirate, pirate ship<br>0.0009578 liner, ocean liner<br>|
vgg19                |0.9965214 lifeboat<br>0.0008823 container ship, containership, container vessel<br>0.0004778 drilling platform, offshore rig<br>0.0003970 dock, dockage, docking facility<br>0.0003622 fireboat<br>|


<!-- LINKS -->
[imagenet]: http://www.image-net.org
