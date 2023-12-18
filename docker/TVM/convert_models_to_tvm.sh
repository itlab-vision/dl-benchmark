#!/bin/bash

WORK_DIR="/home/itmm/Documents/kustikova_v/origin-valentina"
cd "${WORK_DIR}"

OMZ_DIR="${WORK_DIR}/public"

TVM_CONVERTER_DIR="${WORK_DIR}/dl-benchmark/src/model_converters/tvm_converter"

OUTPUT_DIR="${WORK_DIR}/tvm_models"
echo "----------------------------------------"
echo "Working directory:       ${WORK_DIR}"
echo "OMZ directory:           ${OMZ_DIR}"
echo "TVM converter directory: ${TVM_CONVERTER_DIR}"
echo "Output directory:        ${OUTPUT_DIR}"
echo "----------------------------------------"
echo "Creating output directory..."
if [ ! -d "${OUTPUT_DIR}" ]; then
    mkdir -p "${OUTPUT_DIR}";
fi

model_names=(
"efficientnet-b0" "densenet-121-tf" "googlenet-v1"
"googlenet-v4-tf" "squeezenet1.1" "resnet-50-pytorch"
)
echo "Downloading OMZ models and creating output directory for each model..."
export PYTHON_PATH=${PYTHON_PATH}:"${OMZ_DIR}/googlenet-v4-tf/models/research/slim"
for model in ${model_names[@]}; do
    echo "Downloading model: ${model}"
    omz_downloader --name ${model}
    # omz_converter creates TensorFlow models in the intermediate format
    omz_converter --name ${model}
    echo "Creating directory ${OUTPUT_DIR}/${model}"
    if [ ! -d "${OUTPUT_DIR}/${model}" ]; then
        mkdir -p "${OUTPUT_DIR}/${model}";
    fi
done

batch_sizes=(
1 2 4 8
)
echo "Creating output directory for each batch size..."
for batch in ${batch_sizes[@]}; do
    echo "Creating directory ${OUTPUT_DIR}/${model}/batch_size${batch}"
    if [ ! -d "${OUTPUT_DIR}/${model}/batch_size${batch}" ]; then
        mkdir -p "${OUTPUT_DIR}/${model}/batch_size${batch}";
    fi
done

echo "Converting TensorFlow models to the ONNX format using tf2onnx"
echo -e "\tdensenet-121-tf"
cd ${OMZ_DIR}/densenet-121-tf
python -m tf2onnx.convert --saved-model densenet-121.savedmodel/ --output densenet-121-tf.onnx
echo -e "\tefficientnet-b0"
cd ${OMZ_DIR}/efficientnet-b0/efficientnet-b0
python -m tf2onnx.convert --saved-model saved_model/ --output efficientnet-b0.onnx
echo -e "\tgooglenet-v4-tf"
cd ${OMZ_DIR}/googlenet-v4-tf
python -m tf2onnx.convert --graphdef inception_v4.frozen.pb --output inception_v4.onnx \
                          --inputs input:0 --outputs InceptionV4/Logits/Predictions:0
cd ${WORK_DIR}

src_models=(
"${OMZ_DIR}/efficientnet-b0/efficientnet-b0/efficientnet-b0.onnx"
"${OMZ_DIR}/densenet-121-tf/densenet-121-tf.onnx"
"${OMZ_DIR}/googlenet-v1/googlenet-v1"
"${OMZ_DIR}/googlenet-v4-tf/inception_v4.onnx"
"${OMZ_DIR}/squeezenet1.1/densenet-121-tf.onnx"
"${OMZ_DIR}/resnet-50-pytorch/squeezenet1.1"
)

src_frameworks=(
"onnx" "onnx" "caffe"
"onnx" "caffe" "pytorch"
)

input_shapes=(
"224 224 3" "224 224 3" "299 299 3"
"299 299 3" "3 227 227" "3 224 224"
)
echo "Converting models to the TVM format..."
for model_idx in ${!model_names[@]}; do
    for batch in  ${batch_sizes[@]}; do
        command_line = ""
        if [ "${src_frameworks[${model_idx}]}" -eq "caffe" ]; then
            command_line = "${TVM_CONVERTER_DIR}/caffe_to_tvm_converter.py \
                           -mn ${model_names[${model_idx}]} \
                           -m ${src_models[${model_idx}]}.prototxt \
                           -w ${src_models[${model_idx}]}.caffemodel \
                           -is ${batch} ${input_shapes[${model_idx}]} \
                           -b ${batch} \
                           -op ${OUTPUT_DIR}/${model_names[${model_idx}]}"
        elif [ "${src_frameworks[${model_idx}]}" -eq "onnx" ]; then
            command_line = "${TVM_CONVERTER_DIR}/onnx_to_tvm_converter.py \
                           -mn ${model_names[${model_idx}]} \
                           -m ${src_models[${model_idx}]} \
                           -is ${batch} ${input_shapes[${model_idx}]} \
                           -b ${batch} \
                           -op ${OUTPUT_DIR}/${model_names[${model_idx}]}"
        elif [ "${src_frameworks[${model_idx}]}" -eq "pytorch" ]; then
            command_line = "${TVM_CONVERTER_DIR}/pytorch_to_tvm_converter.py \
                           -mn ${model_names[${model_idx}]} \
                           -m ${src_models[${model_idx}]} \
                           -is ${batch} ${input_shapes[${model_idx}]} \
                           -b ${batch} \
                           -op ${OUTPUT_DIR}/${model_names[${model_idx}]}"
        fi
        echo -e "\tpython ${command_line}"
#        python ${command_line}
    done
done
echo "----------------------------------------"