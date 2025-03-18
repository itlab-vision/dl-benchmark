# Validation results for the models inferring using Intel® Optimizations for TensorFlow

## Image classification
Файлы меток для параметра `--labels` расположены [здесь](../../src/inference/labels/).

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

Model | Parameters | Python API (without using XLA) | Python API (with using XLA)|
-|-|-|-|
densenet-121-tf |--input_shape 224 224 3<br>--input_name keras_tensor:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--output_names output_0|0.9906962 Granny Smith<br>0.0014767 lemon<br>0.0012409 orange<br>0.0009354 tennis ball<br>0.0007776 piggy bank, penny bank<br>0.0006042 water jug<br>0.0004794 banana<br>0.0004392 vase<br>0.0004066 pitcher, ewer<br>0.0002944 teapot|0.9906962 Granny Smith<br>0.0014767 lemon<br>0.0012409 orange<br>0.0009354 tennis ball<br>0.0007776 piggy bank, penny bank<br>0.0006042 water jug<br>0.0004794 banana<br>0.0004392 vase<br>0.0004066 pitcher, ewer<br>0.0002944 teapot|
efficientnet-b0 |--input_name sub:0<br>--input_shape 224 224 3<br>--output_names logits<br>--channel_swap 2 1 0<br>--mean 123.68 116.78 103.94<br>--labels image_net_synset.txt|10.7337656 Granny Smith<br>4.8936863 lemon<br>4.3447976 bell pepper<br>4.3027458 orange<br>4.2535648 piggy bank, penny bank<br>4.1575651 tennis ball<br>3.5578172 teapot<br>3.2271135 pomegranate<br>3.1768432 saltshaker, salt shaker<br>3.1720369 acorn|10.7337656 Granny Smith<br>4.8936863 lemon<br>4.3447976 bell pepper<br>4.3027458 orange<br>4.2535648 piggy bank, penny bank<br>4.1575651 tennis ball<br>3.5578172 teapot<br>3.2271135 pomegranate<br>3.1768432 saltshaker, salt shaker<br>3.1720369 acorn|
googlenet-v1-tf |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.6735917 Granny Smith<br>0.0737862 piggy bank, penny bank<br>0.0155381 vase<br>0.0154005 pitcher, ewer<br>0.0136553 saltshaker, salt shaker<br>0.0110440 bell pepper<br>0.0063354 pool table, billiard table, snooker table<br>0.0063268 soap dispenser<br>0.0057057 water jug<br>0.0056899 dumbbell|0.6735917 Granny Smith<br>0.0737862 piggy bank, penny bank<br>0.0155381 vase<br>0.0154005 pitcher, ewer<br>0.0136553 saltshaker, salt shaker<br>0.0110440 bell pepper<br>0.0063354 pool table, billiard table, snooker table<br>0.0063268 soap dispenser<br>0.0057057 water jug<br>0.0056899 dumbbell|
googlenet-v2-tf |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.9849941 Granny Smith<br>0.0010004 lemon<br>0.0009706 pomegranate<br>0.0006835 tennis ball<br>0.0006694 banana<br>0.0004955 orange<br>0.0003062 pitcher, ewer<br>0.0002888 piggy bank, penny bank<br>0.0001519 fig<br>0.0001152 bell pepper|0.9849941 Granny Smith<br>0.0010004 lemon<br>0.0009706 pomegranate<br>0.0006835 tennis ball<br>0.0006694 banana<br>0.0004955 orange<br>0.0003062 pitcher, ewer<br>0.0002888 piggy bank, penny bank<br>0.0001519 fig<br>0.0001152 bell pepper|
googlenet-v3 |--input_name input:0<br>--input_shape 299 299 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.9867677 Granny Smith<br>0.0008529 bikini, two-piece<br>0.0005354 piggy bank, penny bank<br>0.0003701 pomegranate<br>0.0001682 pool table, billiard table, snooker table<br>0.0001114 brassiere, bra, bandeau<br>0.0001009 orange<br>0.0000922 Band Aid<br>0.0000916 tennis ball<br>0.0000896 syringe|0.9867677 Granny Smith<br>0.0008529 bikini, two-piece<br>0.0005354 piggy bank, penny bank<br>0.0003701 pomegranate<br>0.0001682 pool table, billiard table, snooker table<br>0.0001114 brassiere, bra, bandeau<br>0.0001009 orange<br>0.0000922 Band Aid<br>0.0000916 tennis ball<br>0.0000896 syringe|
googlenet-v4-tf |--input_name input:0<br>--input_shape 299 299 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.9934987 Granny Smith<br>0.0002234 Rhodesian ridgeback<br>0.0000959 pineapple, ananas<br>0.0000871 hair slide<br>0.0000778 banana<br>0.0000679 orange<br>0.0000540 kuvasz<br>0.0000513 EntleBucher<br>0.0000490 bib<br>0.0000422 traffic light, traffic signal, stoplight|0.9934987 Granny Smith<br>0.0002234 Rhodesian ridgeback<br>0.0000959 pineapple, ananas<br>0.0000871 hair slide<br>0.0000778 banana<br>0.0000679 orange<br>0.0000540 kuvasz<br>0.0000513 EntleBucher<br>0.0000490 bib<br>0.0000422 traffic light, traffic signal, stoplight|
inception-resnet-v2-tf |--input_name input:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|9.1747866 Granny Smith<br>4.0729303 pomegranate<br>3.7423978 orange<br>3.7375512 bell pepper<br>3.6937847 piggy bank, penny bank|9.1747866 Granny Smith<br>4.0729303 pomegranate<br>3.7423978 orange<br>3.7375512 bell pepper<br>3.6937847 piggy bank, penny bank|
mixnet-l|--input_name IteratorGetNext:0<br>--output_names logits<br>--input_shape 224 224 3|9.1395369 Granny Smith<br>4.2666969 piggy bank, penny bank<br>3.4046013 saltshaker, salt shaker<br>2.9367111 tennis ball<br>2.5734735 soap dispenser<br>2.5491297 syringe<br>2.4780371 candle, taper, wax light<br>2.4671471 bakery, bakeshop, bakehouse<br>2.4141140 orange<br>2.2456863 pillow|9.1395369 Granny Smith<br>4.2666969 piggy bank, penny bank<br>3.4046013 saltshaker, salt shaker<br>2.9367111 tennis ball<br>2.5734735 soap dispenser<br>2.5491297 syringe<br>2.4780371 candle, taper, wax light<br>2.4671471 bakery, bakeshop, bakehouse<br>2.4141140 orange<br>2.2456863 pillow|
mobilenet-v1-1.0-224-tf |--input_name input:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.1775393 necklace<br>0.1625960 saltshaker, salt shaker<br>0.0680758 pitcher, ewer<br>0.0600448 syringe<br>0.0574061 Granny Smith|0.1775393 necklace<br>0.1625960 saltshaker, salt shaker<br>0.0680758 pitcher, ewer<br>0.0600448 syringe<br>0.0574061 Granny Smith|
mobilenet-v2-1.0-224 |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.8931151 Granny Smith<br>0.0335338 piggy bank, penny bank<br>0.0027360 saltshaker, salt shaker<br>0.0021255 vase<br>0.0016607 pitcher, ewer|0.8931151 Granny Smith<br>0.0335338 piggy bank, penny bank<br>0.0027360 saltshaker, salt shaker<br>0.0021255 vase<br>0.0016607 pitcher, ewer|
mobilenet-v2-1.4-224 |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.7240402 Granny Smith<br>0.0312107 vase<br>0.0237109 fig<br>0.0122461 piggy bank, penny bank<br>0.0118888 saltshaker, salt shaker|0.7240402 Granny Smith<br>0.0312107 vase<br>0.0237109 fig<br>0.0122461 piggy bank, penny bank<br>0.0118888 saltshaker, salt shaker|
mobilenet-v3-small-1.0-224-tf |-|-|-|
mobilenet-v3-large-1.0-224-tf |-|-|-|
resnet-50-tf |--input_name map/TensorArrayStack/TensorArrayGatherV3:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 123.68 116.78 103.94<br>--labels image_net_synset_first_class_base.txt|0.9553044 Granny Smith<br>0.0052123 lemon<br>0.0047184 piggy bank, penny bank<br>0.0045875 orange<br>0.0044232 necklace|0.9553044 Granny Smith<br>0.0052123 lemon<br>0.0047184 piggy bank, penny bank<br>0.0045875 orange<br>0.0044232 necklace|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
</div>

Model | Parameters | Python API (without using XLA) | Python API (with using XLA)|
-|-|-|-|
densenet-121-tf |--input_shape 224 224 3<br>--input_name keras_tensor:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--output_names output_0|0.9974865 junco, snowbird<br>0.0010784 brambling, Fringilla montifringilla<br>0.0006608 chickadee<br>0.0003314 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001343 water ouzel, dipper<br>0.0000895 hummingbird<br>0.0000695 goldfinch, Carduelis carduelis<br>0.0000309 magpie<br>0.0000182 jay<br>0.0000166 house finch, linnet, Carpodacus mexicanus|0.9974865 junco, snowbird<br>0.0010784 brambling, Fringilla montifringilla<br>0.0006608 chickadee<br>0.0003314 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0001343 water ouzel, dipper<br>0.0000895 hummingbird<br>0.0000695 goldfinch, Carduelis carduelis<br>0.0000309 magpie<br>0.0000182 jay<br>0.0000166 house finch, linnet, Carpodacus mexicanus|
efficientnet-b0 |--input_name sub:0<br>--input_shape 224 224 3<br>--output_names logits<br>--channel_swap 2 1 0<br>--mean 123.68 116.78 103.94<br>--labels image_net_synset.txt|7.7920899 junco, snowbird<br>5.7337275 chickadee<br>5.4845691 water ouzel, dipper<br>3.9789405 brambling, Fringilla montifringilla<br>3.1936705 bulbul<br>2.9660630 goldfinch, Carduelis carduelis<br>2.3687637 red-backed sandpiper, dunlin, Erolia alpina<br>2.3143539 house finch, linnet, Carpodacus mexicanus<br>2.0986230 magpie<br>2.0537992 jay|7.7920899 junco, snowbird<br>5.7337275 chickadee<br>5.4845691 water ouzel, dipper<br>3.9789405 brambling, Fringilla montifringilla<br>3.1936705 bulbul<br>2.9660630 goldfinch, Carduelis carduelis<br>2.3687637 red-backed sandpiper, dunlin, Erolia alpina<br>2.3143539 house finch, linnet, Carpodacus mexicanus<br>2.0986230 magpie<br>2.0537992 jay|
googlenet-v1-tf |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.7443175 junco, snowbird<br>0.0474521 brambling, Fringilla montifringilla<br>0.0457433 chickadee<br>0.0213393 goldfinch, Carduelis carduelis<br>0.0085103 house finch, linnet, Carpodacus mexicanus<br>0.0063562 water ouzel, dipper<br>0.0061872 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0021891 bulbul<br>0.0020557 jay<br>0.0009130 magpie|0.7443175 junco, snowbird<br>0.0474521 brambling, Fringilla montifringilla<br>0.0457433 chickadee<br>0.0213393 goldfinch, Carduelis carduelis<br>0.0085103 house finch, linnet, Carpodacus mexicanus<br>0.0063562 water ouzel, dipper<br>0.0061872 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0021891 bulbul<br>0.0020557 jay<br>0.0009130 magpie|
googlenet-v2-tf |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.9265916 junco, snowbird<br>0.0166746 brambling, Fringilla montifringilla<br>0.0058714 chickadee<br>0.0026126 water ouzel, dipper<br>0.0022344 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0022262 goldfinch, Carduelis carduelis<br>0.0015069 house finch, linnet, Carpodacus mexicanus<br>0.0006082 jay<br>0.0005987 loupe, jeweler's loupe<br>0.0003603 American coot, marsh hen, mud hen, water hen, Fulica americana|0.9265916 junco, snowbird<br>0.0166746 brambling, Fringilla montifringilla<br>0.0058714 chickadee<br>0.0026126 water ouzel, dipper<br>0.0022344 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0022262 goldfinch, Carduelis carduelis<br>0.0015069 house finch, linnet, Carpodacus mexicanus<br>0.0006082 jay<br>0.0005987 loupe, jeweler's loupe<br>0.0003603 American coot, marsh hen, mud hen, water hen, Fulica americana|
googlenet-v3 |--input_name input:0<br>--input_shape 299 299 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.9488295 junco, snowbird<br>0.0005887 water ouzel, dipper<br>0.0004797 iron, smoothing iron<br>0.0003071 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002692 cleaver, meat cleaver, chopper<br>0.0002677 ox<br>0.0002656 oxcart<br>0.0002526 photocopier<br>0.0002514 brambling, Fringilla montifringilla<br>0.0002449 cougar, puma, catamount, mountain lion, painter, panther, Felis concolor|0.9488295 junco, snowbird<br>0.0005887 water ouzel, dipper<br>0.0004797 iron, smoothing iron<br>0.0003071 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0002692 cleaver, meat cleaver, chopper<br>0.0002677 ox<br>0.0002656 oxcart<br>0.0002526 photocopier<br>0.0002514 brambling, Fringilla montifringilla<br>0.0002449 cougar, puma, catamount, mountain lion, painter, panther, Felis concolor|
googlenet-v4-tf |--input_name input:0<br>--input_shape 299 299 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.9399364 junco, snowbird<br>0.0005925 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005340 chickadee<br>0.0005273 brambling, Fringilla montifringilla<br>0.0004121 house finch, linnet, Carpodacus mexicanus<br>0.0004003 water ouzel, dipper<br>0.0003616 hamster<br>0.0002994 goldfinch, Carduelis carduelis<br>0.0002704 koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus<br>0.0002471 robin, American robin, Turdus migratorius|0.9399364 junco, snowbird<br>0.0005925 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>0.0005340 chickadee<br>0.0005273 brambling, Fringilla montifringilla<br>0.0004121 house finch, linnet, Carpodacus mexicanus<br>0.0004003 water ouzel, dipper<br>0.0003616 hamster<br>0.0002994 goldfinch, Carduelis carduelis<br>0.0002704 koala, koala bear, kangaroo bear, native bear, Phascolarctos cinereus<br>0.0002471 robin, American robin, Turdus migratorius|
inception-resnet-v2-tf |--input_name input:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|10.2994785 junco, snowbird<br>5.9667974 brambling, Fringilla montifringilla<br>3.8809638 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>3.7881403 house finch, linnet, Carpodacus mexicanus<br>3.4699843 goldfinch, Carduelis carduelis|10.2994785 junco, snowbird<br>5.9667974 brambling, Fringilla montifringilla<br>3.8809638 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>3.7881403 house finch, linnet, Carpodacus mexicanus<br>3.4699843 goldfinch, Carduelis carduelis|
mixnet-l|--input_name IteratorGetNext:0<br>--output_names logits<br>--input_shape 224 224 3|8.9584866 junco, snowbird<br>5.7800508 brambling, Fringilla montifringilla<br>4.1285877 water ouzel, dipper<br>3.8712854 goldfinch, Carduelis carduelis<br>3.6966913 chickadee<br>3.1218438 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>2.9483540 house finch, linnet, Carpodacus mexicanus<br>1.7852575 face powder<br>1.7800363 chain<br>1.6861986 hamster|8.9584866 junco, snowbird<br>5.7800508 brambling, Fringilla montifringilla<br>4.1285877 water ouzel, dipper<br>3.8712854 goldfinch, Carduelis carduelis<br>3.6966913 chickadee<br>3.1218438 indigo bunting, indigo finch, indigo bird, Passerina cyanea<br>2.9483540 house finch, linnet, Carpodacus mexicanus<br>1.7852575 face powder<br>1.7800363 chain<br>1.6861986 hamster|
mobilenet-v1-1.0-224-tf |--input_name input:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.9818491 junco, snowbird<br>0.0097170 house finch, linnet, Carpodacus mexicanus<br>0.0029993 brambling, Fringilla montifringilla<br>0.0022394 goldfinch, Carduelis carduelis<br>0.0022212 chickadee|0.9818491 junco, snowbird<br>0.0097170 house finch, linnet, Carpodacus mexicanus<br>0.0029993 brambling, Fringilla montifringilla<br>0.0022394 goldfinch, Carduelis carduelis<br>0.0022212 chickadee|
mobilenet-v2-1.0-224 |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.8770270 junco, snowbird<br>0.0143872 water ouzel, dipper<br>0.0103318 chickadee<br>0.0063065 brambling, Fringilla montifringilla<br>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|0.8770270 junco, snowbird<br>0.0143872 water ouzel, dipper<br>0.0103318 chickadee<br>0.0063065 brambling, Fringilla montifringilla<br>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|
mobilenet-v2-1.4-224 |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.6637316 junco, snowbird<br>0.0811651 chickadee<br>0.0119593 water ouzel, dipper<br>0.0038528 brambling, Fringilla montifringilla<br>0.0022498 goldfinch, Carduelis carduelis|0.6637316 junco, snowbird<br>0.0811651 chickadee<br>0.0119593 water ouzel, dipper<br>0.0038528 brambling, Fringilla montifringilla<br>0.0022498 goldfinch, Carduelis carduelis|
mobilenet-v3-small-1.0-224-tf |-|-|-|
mobilenet-v3-large-1.0-224-tf |-|-|-|
resnet-50-tf |--input_name map/TensorArrayStack/TensorArrayGatherV3:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 123.68 116.78 103.94<br>--labels image_net_synset_first_class_base.txt|0.9983400 junco, snowbird<br>0.0004680 brambling, Fringilla montifringilla<br>0.0003848 chickadee<br>0.0003656 water ouzel, dipper<br>0.0003383 goldfinch, Carduelis carduelis|0.9983400 junco, snowbird<br>0.0004680 brambling, Fringilla montifringilla<br>0.0003848 chickadee<br>0.0003656 water ouzel, dipper<br>0.0003383 goldfinch, Carduelis carduelis|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
</div>

Model | Parameters | Python API (without using XLA) | Python API (with using XLA)|
-|-|-|-|
densenet-121-tf |--input_shape 224 224 3<br>--input_name keras_tensor:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--output_names output_0|0.4439965 liner, ocean liner<br>0.1304450 drilling platform, offshore rig<br>0.0822599 container ship, containership, container vessel<br>0.0457604 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0422195 dock, dockage, docking facility<br>0.0352443 fireboat<br>0.0330128 submarine, pigboat, sub, U-boat<br>0.0322974 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0270287 lifeboat<br>0.0120249 beacon, lighthouse, beacon light, pharos|0.4439965 liner, ocean liner<br>0.1304450 drilling platform, offshore rig<br>0.0822599 container ship, containership, container vessel<br>0.0457604 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0422195 dock, dockage, docking facility<br>0.0352443 fireboat<br>0.0330128 submarine, pigboat, sub, U-boat<br>0.0322974 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0270287 lifeboat<br>0.0120249 beacon, lighthouse, beacon light, pharos|
efficientnet-b0 |--input_name sub:0<br>--input_shape 224 224 3<br>--output_names logits<br>--channel_swap 2 1 0<br>--mean 123.68 116.78 103.94<br>--labels image_net_synset.txt|6.3308706 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>5.6206555 beacon, lighthouse, beacon light, pharos<br>5.5816450 liner, ocean liner<br>5.2046542 submarine, pigboat, sub, U-boat<br>5.1616158 lifeboat<br>4.8865576 drilling platform, offshore rig<br>4.8124046 seashore, coast, seacoast, sea-coast<br>4.6078129 wreck<br>4.2392783 fireboat<br>4.1382837 container ship, containership, container vessel|6.3308706 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>5.6206555 beacon, lighthouse, beacon light, pharos<br>5.5816450 liner, ocean liner<br>5.2046542 submarine, pigboat, sub, U-boat<br>5.1616158 lifeboat<br>4.8865576 drilling platform, offshore rig<br>4.8124046 seashore, coast, seacoast, sea-coast<br>4.6078129 wreck<br>4.2392783 fireboat<br>4.1382837 container ship, containership, container vessel|
googlenet-v1-tf |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.1235983 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1017589 liner, ocean liner<br>0.0949445 drilling platform, offshore rig<br>0.0817945 container ship, containership, container vessel<br>0.0486889 fireboat<br>0.0372103 lifeboat<br>0.0222339 submarine, pigboat, sub, U-boat<br>0.0194757 beacon, lighthouse, beacon light, pharos<br>0.0187142 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0149769 dock, dockage, docking facility|0.1235983 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1017589 liner, ocean liner<br>0.0949445 drilling platform, offshore rig<br>0.0817945 container ship, containership, container vessel<br>0.0486889 fireboat<br>0.0372103 lifeboat<br>0.0222339 submarine, pigboat, sub, U-boat<br>0.0194757 beacon, lighthouse, beacon light, pharos<br>0.0187142 aircraft carrier, carrier, flattop, attack aircraft carrier<br>0.0149769 dock, dockage, docking facility|
googlenet-v2-tf |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.2662658 container ship, containership, container vessel<br>0.0966039 dock, dockage, docking facility<br>0.0876836 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0488675 beacon, lighthouse, beacon light, pharos<br>0.0343598 drilling platform, offshore rig<br>0.0228717 lifeboat<br>0.0226615 liner, ocean liner<br>0.0193398 fireboat<br>0.0147396 water bottle<br>0.0085407 submarine, pigboat, sub, U-boat|0.2662658 container ship, containership, container vessel<br>0.0966039 dock, dockage, docking facility<br>0.0876836 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0488675 beacon, lighthouse, beacon light, pharos<br>0.0343598 drilling platform, offshore rig<br>0.0228717 lifeboat<br>0.0226615 liner, ocean liner<br>0.0193398 fireboat<br>0.0147396 water bottle<br>0.0085407 submarine, pigboat, sub, U-boat|
googlenet-v3 |--input_name input:0<br>--input_shape 299 299 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.4653859 beacon, lighthouse, beacon light, pharos<br>0.3437518 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0512174 submarine, pigboat, sub, U-boat<br>0.0174646 liner, ocean liner<br>0.0134647 lifeboat<br>0.0114189 container ship, containership, container vessel<br>0.0101290 fireboat<br>0.0070726 wreck<br>0.0037166 drilling platform, offshore rig<br>0.0036825 promontory, headland, head, foreland|0.4653859 beacon, lighthouse, beacon light, pharos<br>0.3437518 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0512174 submarine, pigboat, sub, U-boat<br>0.0174646 liner, ocean liner<br>0.0134647 lifeboat<br>0.0114189 container ship, containership, container vessel<br>0.0101290 fireboat<br>0.0070726 wreck<br>0.0037166 drilling platform, offshore rig<br>0.0036825 promontory, headland, head, foreland|
googlenet-v4-tf |--input_name input:0<br>--input_shape 299 299 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.4704932 beacon, lighthouse, beacon light, pharos<br>0.1695956 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0431101 lifeboat<br>0.0307511 fireboat<br>0.0149649 dock, dockage, docking facility<br>0.0143449 pier<br>0.0133830 drilling platform, offshore rig<br>0.0108169 submarine, pigboat, sub, U-boat<br>0.0082825 wreck<br>0.0072376 container ship, containership, container vessel|0.4704932 beacon, lighthouse, beacon light, pharos<br>0.1695956 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0431101 lifeboat<br>0.0307511 fireboat<br>0.0149649 dock, dockage, docking facility<br>0.0143449 pier<br>0.0133830 drilling platform, offshore rig<br>0.0108169 submarine, pigboat, sub, U-boat<br>0.0082825 wreck<br>0.0072376 container ship, containership, container vessel|
inception-resnet-v2-tf |--input_name input:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|6.6930799 fireboat<br>6.1025167 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.0896273 lifeboat<br>5.7389712 container ship, containership, container vessel<br>5.4940562 dock, dockage, docking facility|6.6930799 fireboat<br>6.1025167 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>6.0896273 lifeboat<br>5.7389712 container ship, containership, container vessel<br>5.4940562 dock, dockage, docking facility|
mixnet-l|--input_name IteratorGetNext:0<br>--output_names logits<br>--input_shape 224 224 3|8.3550520 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>7.1289797 container ship, containership, container vessel<br>6.9460378 beacon, lighthouse, beacon light, pharos<br>6.7993770 lifeboat<br>6.4594803 fireboat<br>6.4359784 catamaran<br>6.4354229 wreck<br>6.3726940 drilling platform, offshore rig<br>6.2994452 amphibian, amphibious vehicle<br>5.8687139 submarine, pigboat, sub, U-boat|8.3550520 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>7.1289797 container ship, containership, container vessel<br>6.9460378 beacon, lighthouse, beacon light, pharos<br>6.7993770 lifeboat<br>6.4594803 fireboat<br>6.4359784 catamaran<br>6.4354229 wreck<br>6.3726940 drilling platform, offshore rig<br>6.2994452 amphibian, amphibious vehicle<br>5.8687139 submarine, pigboat, sub, U-boat|
mobilenet-v1-1.0-224-tf |--input_name input:0<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.3759801 liner, ocean liner<br>0.1252522 lifeboat<br>0.1200093 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0882490 beacon, lighthouse, beacon light, pharos<br>0.0568063 fireboat|0.3759801 liner, ocean liner<br>0.1252522 lifeboat<br>0.1200093 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0882490 beacon, lighthouse, beacon light, pharos<br>0.0568063 fireboat|
mobilenet-v2-1.0-224 |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.1885883 beacon, lighthouse, beacon light, pharos<br>0.1434043 liner, ocean liner<br>0.0768170 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0497303 drilling platform, offshore rig<br>0.0225758 container ship, containership, container vessel|0.1885883 beacon, lighthouse, beacon light, pharos<br>0.1434043 liner, ocean liner<br>0.0768170 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.0497303 drilling platform, offshore rig<br>0.0225758 container ship, containership, container vessel|
mobilenet-v2-1.4-224 |--input_name input:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 127.5 127.5 127.5<br>--input_scale 127.5 127.5 127.5<br>--labels image_net_synset_first_class_base.txt|0.1300134 container ship, containership, container vessel<br>0.0765783 lifeboat<br>0.0406071 dock, dockage, docking facility<br>0.0393021 drilling platform, offshore rig<br>0.0381023 liner, ocean liner|0.1300134 container ship, containership, container vessel<br>0.0765783 lifeboat<br>0.0406071 dock, dockage, docking facility<br>0.0393021 drilling platform, offshore rig<br>0.0381023 liner, ocean liner|
mobilenet-v3-small-1.0-224-tf |-|-|-|
mobilenet-v3-large-1.0-224-tf |-|-|-|
resnet-50-tf |--input_name map/TensorArrayStack/TensorArrayGatherV3:0<br>--input_shape 224 224 3<br>--channel_swap 2 1 0<br>--mean 123.68 116.78 103.94<br>--labels image_net_synset_first_class_base.txt|0.2357705 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1480758 liner, ocean liner<br>0.1104694 container ship, containership, container vessel<br>0.1095414 drilling platform, offshore rig<br>0.0915567 beacon, lighthouse, beacon light, pharos|0.2357705 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br>0.1480758 liner, ocean liner<br>0.1104694 container ship, containership, container vessel<br>0.1095414 drilling platform, offshore rig<br>0.0915567 beacon, lighthouse, beacon light, pharos|

## Object detection

### Test image #1

Data source: [ImageNet][imagenet]

Image resolution: 709 x 510

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000023.JPEG"></img>
<img width="150" src="detection\ILSVRC2012_val_00000023.JPEG"></img>
</div>
Bounding boxes (upper left and bottom right corners):<br>
(55, 155), (236, 375)<br>
(190, 190), (380, 400)<br>
(374, 209), (588, 422)<br>
(289, 111), (440, 255)<br>
(435, 160), (615, 310)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #2

Data source: [ImageNet][imagenet]

Image resolution: 500 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00000247.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00000247.JPEG">
</div>
Bounding box (upper left and bottom right corners):<br>
(117, 86), (365, 465)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #3

Data source: [ImageNet][imagenet]

Image resolution: 333 x 500

<div style='float: center'>
<img width="150" src="images\ILSVRC2012_val_00018592.JPEG">
<img width="150" src="detection\ILSVRC2012_val_00018592.JPEG">
</div>
Bounding box (upper left and bottom right corners):<br>
(82, 262), (269, 376)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #4

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 480

<div style='float: center'>
<img width="300" src="images\9.jpg">
<img width="300" src="detection\faster_rcnn_out.bmp">
</div>
Bounding boxes (upper left and bottom right corners):<br>
TV (110, 41), (397, 304)<br>
MOUSE (508, 337), (559, 374)<br>
KEYBOARD (241, 342), (496, 461)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #5

Data source: [Pascal VOC][PASCAL_VOC_2012]

Image resolution: 500 x 375

<div style='float: center'>
<img width="300" src="images\2011_002352.jpg">
<img width="300" src="detection\python_yolo_voc_2011_002352.bmp">
</div>
Bounding box (upper left and bottom right corners):<br>
AEROPLANE (131, 21), (248, 414)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

### Test image #6

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 427

<div style='float: center'>
<img width="300" src="images\000000367818.jpg">
<img width="300" src="detection\python_yolo_coco_000000367818.bmp">
</div>

Bounding boxes (upper left and bottom right corners):<br>
PERSON (86, 84), (394, 188)<br>
HORSE (44, 108), (397, 565)<br>

 Model | Python API |
-------|-------------------------|
ctpn|-|
efficientdet-d0|-|
efficientdet-d1|-|
faster_rcnn_inception_resnet_v2_atrous_coco|-|
faster_rcnn_resnet50_coco|-|
retinanet|-|
rfcn-resnet101-coco|-|
ssd_mobilenet_v1_coco|-|
ssd_mobilenet_v1_fpn_coco|-|
ssdlite_mobilenet_v2|-|

## Semantic segmentation

### Test image #1

Data source: -

Image resolution: -

Image: -

Segmented images are identical.

 Model | Python API |
-------|-------------------------|
deeplabv3|-|

## Instance segmentation

### Test image #1

Data source: [MS COCO][ms_coco]

Image resolution: 640 x 480

Image:
<div style='float: center'>
<img width="300" src="images\22.jpg"></img>
</div>

Segmented images are identical.

 Model | Python API |
-------|-------------------------|
mask_rcnn_resnet50_atrous_coco|-|
mask_rcnn_inception_resnet_v2_atrous_coco|-|


Color map:

<div style='float: center'>
<img width="300" src="instance_segmentation\mscoco90_colormap.jpg">
</div>


<!-- LINKS -->
[imagenet]: http://www.image-net.org
[ms_coco]: http://cocodataset.org
[PASCAL_VOC_2012]: http://host.robots.ox.ac.uk/pascal/VOC/voc2012
