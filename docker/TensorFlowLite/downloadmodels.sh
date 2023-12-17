#!/bin/bash

converter_path='./src/model_converters/tflite_converter.py'
models_path='public/'
model_paths=('./mobilenet-v3-small-1.0-224-tf/mobilenet_v3_small_224_1.0_float.savedmodel' './mobilenet-v3-large-1.0-224-tf/mobilenet_v3_large_224_1.0_float.savedmodel' './resnet-50-tf/resnet_v1-50.pb' './densenet-121-tf/densenet-121.savedmodel' './googlenet-v1-tf/inception_v1.frozen.pb' './googlenet-v2-tf/inception_v2.frozen.pb' './googlenet-v3/inception_v3_2016_08_28_frozen.pb' './googlenet-v4-tf/inception_v4.frozen.pb')
input_names=('input_1' 'input_1' 'map/TensorArrayStack/TensorArrayGatherV3' 'input_1' 'input' 'input' 'input' 'input')
input_shapes=('[1,224,224,3]' '[1,224,224,3]' '[1,224,224,3]' '[1,224,224,3]' '[1,224,224,3]' '[1,224,224,3]' '[1,299,299,3]' '[1,299,299,3]')
output_names=('StatefulPartitionedCall/MobilenetV3small/Predictions/Softmax' 'StatefulPartitionedCall/MobilenetV3large/Predictions/Softmax' 'softmax_tensor' 'Inception3/Predictions/Softmax' 'InceptionV1/Logits/Predictions/Softmax' 'InceptionV2/Predictions/Softmax' 'InceptionV3/Predictions/Softmax' 'InceptionV4/Logits/Predictions')
src_frameworks=('tf' 'tf' 'tf' 'tf' 'tf' 'tf' 'tf' 'tf')


cd dl-benchmark/

omz_downloader --list ./../models.lst
omz_converter --list ./../models.lst

for i in ${!model_paths[*]}; do
  python3 $converter_path --model-path ${models_path}${model_paths[$i]} --input-names ${input_names[$i]} --input-shapes ${input_shapes[$i]} --output-names ${output_names[$i]} --source-framework ${src_frameworks[$i]}
done


