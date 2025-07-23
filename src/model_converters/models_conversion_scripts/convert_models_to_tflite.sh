#!/bin/bash
export TF_CPP_MIN_LOG_LEVEL="2"

WORK_DIR="$1"
echo "WORK_DIR: $WORK_DIR"
cd "${WORK_DIR}"

OMZ_DIR="${WORK_DIR}/public"
TF_CONVERTER_DIR="${WORK_DIR}/dl-benchmark/src/model_converters/tf2tflite"
TF_CONVERTER="${TF_CONVERTER_DIR}/tf_converter.py"
TFLITE_CONVERTER="${TF_CONVERTER_DIR}/tflite_converter.py"
CAFFE_ONNX_CONVERTER="${WORK_DIR}/caffe2onnx/caffe2onnx/convert.py"
OUTPUT_DIR="${WORK_DIR}/tflite_models"

echo "----------------------------------------"
echo "Working directory:       ${WORK_DIR}"
echo "OMZ directory:           ${OMZ_DIR}"
echo "TFLite converter directory: ${TF_CONVERTER_DIR}"
echo "Output directory:        ${OUTPUT_DIR}"
echo "----------------------------------------"

echo "Creating virtual environment for Caffe (Python 3.7)..."
conda create --name tflite_convert_python3.7 python=3.7 -y
echo "Activating virtual environment..."
conda activate tflite_convert_python3.7
echo "Installing packages..."
pip install openvino-dev==2022.3.0
conda install -y caffe
pip install onnx==1.6.0
git clone https://github.com/asiryan/caffe2onnx caffe2onnx
python caffe2onnx/setup.py install
echo "Deactivating virtual environment..."
conda deactivate

echo "Creating virtual environment for MXNet, ONNX, PyTorch (Python 3.9)..."
conda create --name tflite_convert_python3.9 python=3.9 -y
echo "Activating virtual environment..."
conda activate tflite_convert_python3.9
echo "Installing packages..."
pip install openvino-dev==2023.3.0
pip install tensorflow==2.14.0
pip install tf-keras==2.15.0
pip install tf2onnx==1.16.0
# dependencies for tf_converter.py
pip install onnx-tf==1.10.0
pip install tensorflow-addons==0.22.0
pip install tensorflow-probability==0.22.0
pip install torch==1.13.1 torchvisio==0.14.1
pip install mxnet==1.9.1
pip install gluoncv==0.10.5.post0
pip install numpy==1.23.5
echo "Deactivating virtual environment..."
conda deactivate

batch_sizes=(
1 8
)

model_names=(
"densenet-121-tf"
"googlenet-v1"
"googlenet-v4-tf"
"squeezenet1.1"
"resnet-50-pytorch"
"ssd_512_resnet50_v1_coco"
"ssd_512_vgg16_atrous_voc"
"ssd_300_vgg16_atrous_voc"
"ssd_512_mobilenet1.0_coco"
)

src_models=(
"${OMZ_DIR}/densenet-121-tf/densenet-121.savedmodel/"
"${OMZ_DIR}/googlenet-v1/googlenet-v1"
"${OMZ_DIR}/googlenet-v4-tf/inception_v4.frozen.pb"
"${OMZ_DIR}/squeezenet1.1/squeezenet1.1"
"${OMZ_DIR}/resnet-50-pytorch/resnet-v1-50.onnx"
"${OUTPUT_DIR}/ssd_512_resnet50_v1_coco/ssd_512_resnet50_v1_coco.onnx"
"${OUTPUT_DIR}/ssd_512_vgg16_atrous_voc/ssd_512_vgg16_atrous_voc.onnx"
"${OUTPUT_DIR}/ssd_300_vgg16_atrous_voc/ssd_300_vgg16_atrous_voc.onnx"
"${OUTPUT_DIR}/ssd_512_mobilenet1.0_coco/ssd_512_mobilenet1.0_coco.onnx"
)

src_frameworks=(
"tf"
"caffe"
"tf"
"caffe" 
"onnx"
"mxnet"
"mxnet"
"mxnet"
"mxnet"
)

input_shapes=(
"224 224 3"
"3 224 224"
"299 299 3"
"3 227 227"
"3 224 224"
"1 3 512 512"
"1 3 512 512"
"1 3 300 300"
"1 3 512 512"
)

conversation_params=(
""
""
"--input-names input --output-names InceptionV4/Logits/Predictions"
""
""
""
""
""
""
)

tflite_model_names=(
"densenet-121.tflite"
"googlenet-v1.tflite"
"inception_v4.frozen.tflite"
"squeezenet1.1.tflite"
"resnet-v1-50.tflite"
"ssd_512_resnet50_v1_coco.tflite"
"ssd_512_vgg16_atrous_voc.tflite"
"ssd_300_vgg16_atrous_voc.tflite"
"ssd_512_mobilenet1.0_coco.tflite"
)

conda activate tflite_convert_python3.9

echo "Creating output directory..."
if [ ! -d "${OUTPUT_DIR}" ]; then
    mkdir -p "${OUTPUT_DIR}";
fi

echo "Downloading and converting OMZ models..."
export PYTHON_PATH=${PYTHON_PATH}:"${OMZ_DIR}/googlenet-v4-tf/models/research/slim"
for model in ${model_names[@]}; do
    echo "Downloading model: ${model}"
    omz_downloader --name ${model}
    # omz_converter creates TensorFlow models in the intermediate format (.pb)
    omz_converter --name ${model}
done
conda deactivate

echo "Converting models to the TFLite format..."
for model_idx in ${!model_names[@]}; do
    model_name=( "${model_names[$model_idx]}" )
    command_line=()
    if [ "${src_frameworks[$model_idx]}" = "tf" ]; then
        command_line=("python ${TFLITE_CONVERTER}"
                      "--model-path ${src_models[$model_idx]}"
                      "--source-framework tf"
                      "${conversation_params[$model_idx]}")
        echo -e "Conversation command: ${command_line[@]}"
        conda activate tflite_convert_python3.9
        ${command_line[@]}
        conda deactivate

        if [ ! -d "${OUTPUT_DIR}/${model_name}" ]; then
            mkdir -p "${OUTPUT_DIR}/${model_name}";
        fi
        cp "${OMZ_DIR}/${model_name}/${tflite_model_names[$model_idx]}" "${OUTPUT_DIR}/${model_name}/"
        
    elif [ "${src_frameworks[$model_idx]}" = "caffe" ]; then
        command_line=("python ${CAFFE_ONNX_CONVERTER}"
                      "--prototxt ${src_models[$model_idx]}.prototxt"
                      "--caffemodel ${src_models[$model_idx]}.caffemodel"
                      "--onnx ${src_models[$model_idx]}.onnx")
        echo -e "Conversation command: ${command_line[@]}"
        conda activate tflite_convert_python3.7
        ${command_line[@]}
        conda deactivate

        command_line=("python ${TFLITE_CONVERTER}"
                      "--model-path ${src_models[$model_idx]}.onnx"
                      "--source-framework onnx"
                      "${conversation_params[$model_idx]}")
        echo -e "Conversation command: ${command_line[@]}"                      
        conda activate tflite_convert_python3.9
        ${command_line[@]}
        conda deactivate

        if [ ! -d "${OUTPUT_DIR}/${model_name}" ]; then
            mkdir -p "${OUTPUT_DIR}/${model_name}";
        fi
        cp "${OMZ_DIR}/${model_name}/${tflite_model_names[$model_idx]}" "${OUTPUT_DIR}/${model_name}/"

    elif [ "${src_frameworks[$model_idx]}" = "onnx" ]; then
        command_line=("python ${TFLITE_CONVERTER}"
                      "--model-path ${src_models[$model_idx]}"
                      "--source-framework onnx"
                      "${conversation_params[$model_idx]}")
        echo -e "Conversation command: ${command_line[@]}"
        conda activate tflite_convert_python3.9
        ${command_line[@]}
        conda deactivate

        if [ ! -d "${OUTPUT_DIR}/${model_name}" ]; then
            mkdir -p "${OUTPUT_DIR}/${model_name}";
        fi
        cp "${OMZ_DIR}/${model_name}/${tflite_model_names[$model_idx]}" "${OUTPUT_DIR}/${model_name}/"        

    elif [ "${src_frameworks[$model_idx]}" = "mxnet" ]; then
        if [ ! -d "${OUTPUT_DIR}/${model_name}" ]; then
            mkdir -p "${OUTPUT_DIR}/${model_name}";
        fi

        command_line=("python -c 'import mxnet; import gluoncv; from gluoncv.model_zoo import get_model; net = get_model(\"${model_name}\", pretrained=True); gluoncv.utils.export_block(\"${OUTPUT_DIR}/${model_name}/${model_name}\", net, preprocess=None, layout=\"CHW\", ctx=mxnet.cpu())'")
        echo -e "Model downloading command: ${command_line[@]}"
        conda activate tflite_convert_python3.9
        eval ${command_line[@]}       
        conda deactivate

        command_line=("python ${MXNET_ONNX_CONVERTER}"
                      "-m ${OUTPUT_DIR}/${model_name}/${model_name}-symbol.json"
                      "-w ${OUTPUT_DIR}/${model_name}/${model_name}-0000.params"
                      "-is ${input_shapes[$model_idx]}"
                      "-p ${src_models[$model_idx]}")       
        echo -e "Conversation command: ${command_line[@]}"
        conda activate tflite_convert_python3.9
        ${command_line[@]}
        conda deactivate

        command_line=("python ${TFLITE_CONVERTER}"
                      "--model-path ${src_models[$model_idx]}"
                      "--source-framework onnx"
                      "${conversation_params[$model_idx]}")
        echo -e "Conversation command: ${command_line[@]}"
        conda activate tflite_convert_python3.9
        ${command_line[@]}
        conda deactivate        
    fi
done

echo "Removing virtual environments..."
conda env remove --name tflite_convert_python3.7
conda env remove --name tflite_convert_python3.9
echo "----------------------------------------"