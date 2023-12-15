#!/bin/bash

cd dl-benchmark/

omz_downloader --list models.lst
omz_converter --list models.lst

python3 ./src/model_converters/tflite_converter.py --model-path ./public/mobilenet-v3-small-1.0-224-tf/mobilenet_v3_small_224_1.0_float.savedmodel --input-names input_1 --input-shapes [1,224,224,3] --output-names StatefulPartitionedCall/MobilenetV3small/Predictions/Softmax --source-framework tf
python3 ./src/model_converters/tflite_converter.py --model-path ./public/mobilenet-v3-large-1.0-224-tf/mobilenet_v3_large_224_1.0_float.savedmodel --input-names input_1 --input-shapes [1,224,224,3] --output-names StatefulPartitionedCall/MobilenetV3large/Predictions/Softmax --source-framework tf
python3 ./src/model_converters/tflite_converter.py --model-path ./public/resnet-50-tf/resnet_v1-50.pb --input-names map/TensorArrayStack/TensorArrayGatherV3 --input-shapes [1,224,224,3] --output-names softmax_tensor --source-framework tf
python3 ./src/model_converters/tflite_converter.py --model-path ./public/densenet-121-tf/densenet-121.savedmodel --input-names input_1 --input-shapes [1,224,224,3] --output-names Inception3/Predictions/Softmax --source-framework tf
python3 ./src/model_converters/tflite_converter.py --model-path ./public/googlenet-v1-tf/inception_v1.frozen.pb --input-names input --input-shapes [1,224,224,3] --output-names InceptionV1/Logits/Predictions/Softmax --source-framework tf
python3 ./src/model_converters/tflite_converter.py --model-path ./public/googlenet-v2-tf/inception_v2.frozen.pb --input-names input --input-shapes [1,224,224,3] --output-names InceptionV2/Predictions/Softmax --source-framework tf
python3 ./src/model_converters/tflite_converter.py --model-path ./public/googlenet-v3/inception_v3_2016_08_28_frozen.pb --input-names input --input-shapes [1,299,299,3] --output-names InceptionV3/Predictions/Softmax --source-framework tf
python3 ./src/model_converters/tflite_converter.py --model-path ./public/googlenet-v4-tf/inception_v4.frozen.pb --input-names input --input-shapes [1,299,299,3] --output-names InceptionV4/Logits/Predictions --source-framework tf

