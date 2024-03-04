# table of content

* [exists](#exists)
    * [requirements](#requirements)
    * [images](#images)
    * [conversion](#conversion)
* [setup](#setup)
    * [directories](#directories)
    * [envs](#envs)
        * [inference-mxnet-3.9.13](#inference-mxnet-3913)
        * [inference-onnx-3.9.13](#inference-onnx-3913)
        * [conversion-mxnet2onnx-3.9.13](#conversion-mxnet2onnx-3913)
* [inference](#inference)
    * [MXNet](#mxnet)
        * [mobilenetv2_1.0](#mobilenetv2_10)
        * [resnet50_v1](#resnet50_v1)
    * [ONNX](#onnx)
        * [mobilenetv2_1.0](#mobilenetv2_10-1)
        * [resnet50_v1](#resnet50_v1-1)
* [conversion](#conversion-1)
    * [mobilenetv2_1.0](#mobilenetv2_10-2)
    * [resnet50_v1](#resnet50_v1-2)

# exists

### requirements

required packages

```text
requirements
├── conversion-mxnet2onnx-3.9.13.txt
├── inference-mxnet-3.9.13.txt
└── inference-onnx-3.9.13.txt
```

### images

images for validation

```text
images
├── ILSVRC2012_val_00000023.JPEG
├── ILSVRC2012_val_00000247.JPEG
└── ILSVRC2012_val_00018592.JPEG
```

### conversion

scripts for conversion

```text
conversion
├── mobilenetv2_1.0.py
└── resnet50_v1.py
```

# setup

```shell
cd src/inference
```

## directories

```shell
mkdir public
mkdir results
```

## envs

### inference-mxnet-3.9.13

```shell [OK]
conda create --name inference-mxnet-3.9.13 python=3.9.13 --yes
conda activate inference-mxnet-3.9.13
pip install --upgrade pip setuptools wheel
pip install -r ./requirements/inference-mxnet-3.9.13.txt
conda deactivate
```

### inference-onnx-3.9.13

```shell [OK]
conda create --name inference-onnx-3.9.13 python=3.9.13 --yes
conda activate inference-onnx-3.9.13
pip install --upgrade pip setuptools wheel
pip install -r ./requirements/inference-onnx-3.9.13.txt
conda deactivate
```

### conversion-mxnet2onnx-3.9.13

```shell [OK]
conda create --name conversion-mxnet2onnx-3.9.13 python=3.9.13 --yes
conda activate conversion-mxnet2onnx-3.9.13
pip install --upgrade pip setuptools wheel
pip install -r ./requirements/conversion-mxnet2onnx-3.9.13.txt
conda deactivate
```

# inference

## MXNet

### mobilenetv2_1.0

```shell [OK]
conda activate inference-mxnet-3.9.13
python3 inference_mxnet_sync_mode.py \
  --model_name mobilenetv2_1.0 \
  --task classification \
  --input ./images \
  --labels ./labels/image_net_labels.json \
  --input_name data \
  --output_names mobilenetv20_output_flatten0_flatten0 \
  --input_shape 3 3 224 224 \
  --norm \
  --mean 0.485 0.456 0.406 \
  --std 0.229 0.224 0.225 \
  --batch_size 3 \
  --save_model \
  --path_save_model ./public
conda deactivate
```

```text
[ INFO ] Inference results
[ INFO ] Top 5 results:
[ INFO ] Result for image 1
[ INFO ]        0.1127411 liner, ocean liner
[ INFO ]        0.1014166 container ship, containership, container vessel
[ INFO ]        0.0582132 submarine, pigboat, sub, U-boat
[ INFO ]        0.0552070 lifeboat
[ INFO ]        0.0221046 breakwater, groin, groyne, mole, bulwark, seawall, jetty
[ INFO ] Result for image 2
[ INFO ]        0.6325442 Granny Smith
[ INFO ]        0.0556754 piggy bank, penny bank
[ INFO ]        0.0443766 lemon
[ INFO ]        0.0086360 teapot
[ INFO ]        0.0071484 vase
[ INFO ] Result for image 3
[ INFO ]        0.8265611 junco, snowbird
[ INFO ]        0.0339170 chickadee
[ INFO ]        0.0146587 brambling, Fringilla montifringilla
[ INFO ]        0.0095486 water ouzel, dipper
[ INFO ]        0.0065168 hummingbird
[ INFO ] Performance results
[ INFO ] Performance results:
{
    "iterations_num": 1,
    "execution_time": 0.217,
    "first_inference_time": 0.21732,
    "latency_avg": 0.21732,
    "latency_median": 0.21732,
    "latency_std": 0.0,
    "latency_max": 0.21732,
    "latency_min": 0.21732,
    "latency_per_token": null,
    "num_tokens": null,
    "min_num_tokens": null,
    "max_num_tokens": null,
    "audio_len_avg": null,
    "audio_sampling_rate": null,
    "latency_per_second": null,
    "batch_throughput": 13.805,
    "throughput": 13.805
}
```

### resnet50_v1

```shell [OK]
conda activate inference-mxnet-3.9.13
python3 inference_mxnet_sync_mode.py \
  --model_name resnet50_v1 \
  --task classification \
  --input ./images \
  --labels ./labels/image_net_labels.json \
  --input_name data \
  --output_names resnetv10_dense0_fwd \
  --input_shape 3 3 224 224 \
  --norm \
  --mean 0.485 0.456 0.406 \
  --std 0.229 0.224 0.225 \
  --batch_size 3 \
  --save_model \
  --path_save_model ./public
conda deactivate
```

```text
[ INFO ] Inference results
[ INFO ] Top 5 results:
[ INFO ] Result for image 1
[ INFO ]        0.4411839 liner, ocean liner
[ INFO ]        0.0861827 container ship, containership, container vessel
[ INFO ]        0.0609572 speedboat
[ INFO ]        0.0587049 dock, dockage, docking facility
[ INFO ]        0.0369093 breakwater, groin, groyne, mole, bulwark, seawall, jetty
[ INFO ] Result for image 2
[ INFO ]        0.7377543 Granny Smith
[ INFO ]        0.0241721 piggy bank, penny bank
[ INFO ]        0.0123405 lemon
[ INFO ]        0.0061283 candle, taper, wax light
[ INFO ]        0.0051573 orange
[ INFO ] Result for image 3
[ INFO ]        0.8778600 junco, snowbird
[ INFO ]        0.0045333 water ouzel, dipper
[ INFO ]        0.0018932 brambling, Fringilla montifringilla
[ INFO ]        0.0016121 chickadee
[ INFO ]        0.0005472 magpie
[ INFO ] Performance results
[ INFO ] Performance results:
{
    "iterations_num": 1,
    "execution_time": 0.441,
    "first_inference_time": 0.44081,
    "latency_avg": 0.44081,
    "latency_median": 0.44081,
    "latency_std": 0.0,
    "latency_max": 0.44081,
    "latency_min": 0.44081,
    "latency_per_token": null,
    "num_tokens": null,
    "min_num_tokens": null,
    "max_num_tokens": null,
    "audio_len_avg": null,
    "audio_sampling_rate": null,
    "latency_per_second": null,
    "batch_throughput": 6.806,
    "throughput": 6.806
}
```

## ONNX

### mobilenetv2_1.0

```shell [WA]
conda activate inference-onnx-3.9.13
python3 inference_onnx_runtime.py \
  --model ./results/mobilenetv2_1.0.onnx \
  --task classification \
  --input ./images \
  --labels ./labels/image_net_labels.json \
  --input_name data \
  --output_names mobilenetv20_output_flatten0_flatten0 \
  --input_shape data\[3,3,224,224\] \
  --mean \[0.485,0.456,0.406\] \
  --batch_size 3
conda deactivate
```

```text
[ INFO ] Inference results
[ INFO ] Top 5 results:
[ INFO ] Result for image 1
[ INFO ]        8.7614803 window screen
[ INFO ]        5.5926709 perfume, essence
[ INFO ]        5.5896101 crane
[ INFO ]        5.2040415 screen, CRT screen
[ INFO ]        4.9710312 water bottle
[ INFO ] Result for image 2
[ INFO ]        6.0578766 tennis ball
[ INFO ]        6.0427632 Granny Smith
[ INFO ]        5.4407711 lemon
[ INFO ]        5.2290316 custard apple
[ INFO ]        4.5216541 jackfruit, jak, jack
[ INFO ] Result for image 3
[ INFO ]        6.1032429 Windsor tie
[ INFO ]        6.0583029 mosquito net
[ INFO ]        5.8213186 fire screen, fireguard
[ INFO ]        5.5263319 strainer
[ INFO ]        5.5130372 poncho
[ INFO ] Performance results:
{
    "iterations_num": 1,
    "execution_time": 0.119,
    "first_inference_time": 0.11918,
    "latency_avg": 0.11918,
    "latency_median": 0.11918,
    "latency_std": 0.0,
    "latency_max": 0.11918,
    "latency_min": 0.11918,
    "latency_per_token": null,
    "num_tokens": null,
    "min_num_tokens": null,
    "max_num_tokens": null,
    "audio_len_avg": null,
    "audio_sampling_rate": null,
    "latency_per_second": null,
    "batch_throughput": 25.172,
    "throughput": 25.172
}
```

### resnet50_v1

```shell [WA]
conda activate inference-onnx-3.9.13
python3 inference_onnx_runtime.py \
  --model ./results/resnet50_v1.onnx \
  --task classification \
  --input ./images \
  --labels ./labels/image_net_labels.json \
  --input_name data \
  --output_names resnetv10_dense0_fwd \
  --input_shape data\[3,3,224,224\] \
  --mean \[0.485,0.456,0.406\] \
  --batch_size 3
conda deactivate
```

```text
[ INFO ] Inference results
[ INFO ] Top 5 results:
[ INFO ] Result for image 1
[ INFO ]        568.8291016 strainer
[ INFO ]        561.8710327 beaver
[ INFO ]        494.1133423 titi, titi monkey
[ INFO ]        470.9338684 rhinoceros beetle
[ INFO ]        453.4077148 mixing bowl
[ INFO ] Result for image 2
[ INFO ]        747.7167969 strainer
[ INFO ]        675.6780396 beaver
[ INFO ]        590.6392212 rhinoceros beetle
[ INFO ]        584.9071655 titi, titi monkey
[ INFO ]        568.9278564 mixing bowl
[ INFO ] Result for image 3
[ INFO ]        345.7590942 strainer
[ INFO ]        338.1053162 beaver
[ INFO ]        305.1996460 titi, titi monkey
[ INFO ]        288.4573975 rhinoceros beetle
[ INFO ]        286.2150879 kit fox, Vulpes macrotis
[ INFO ] Performance results:
{
    "iterations_num": 1,
    "execution_time": 0.35,
    "first_inference_time": 0.35004,
    "latency_avg": 0.35004,
    "latency_median": 0.35004,
    "latency_std": 0.0,
    "latency_max": 0.35004,
    "latency_min": 0.35004,
    "latency_per_token": null,
    "num_tokens": null,
    "min_num_tokens": null,
    "max_num_tokens": null,
    "audio_len_avg": null,
    "audio_sampling_rate": null,
    "latency_per_second": null,
    "batch_throughput": 8.57,
    "throughput": 8.57
}
```

# conversion

### mobilenetv2_1.0

```shell [OK]
conda activate conversion-mxnet2onnx-3.9.13
python3 ./conversion/mobilenetv2_1.0.py
conda deactivate
```

### resnet50_v1

```shell [OK]
conda activate conversion-mxnet2onnx-3.9.13
python3 ./conversion/resnet50_v1.py
conda deactivate
```