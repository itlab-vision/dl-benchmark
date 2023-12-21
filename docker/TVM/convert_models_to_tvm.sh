#!/bin/bash


WORK_DIR="/home/itmm/Documents/kustikova_v/origin-valentina"
cd "${WORK_DIR}"

OMZ_DIR="${WORK_DIR}/public"

TVM_CONVERTER_DIR="${WORK_DIR}/dl-benchmark/src/model_converters/tvm_converter"
TF_CONVERTER_DIR="${WORK_DIR}/dl-benchmark/src/model_converters/tf2tflite"
TF_CONVERTER="${TF_CONVERTER_DIR}/tf_converter.py"

OUTPUT_DIR="${WORK_DIR}/tvm_models"
echo "----------------------------------------"
echo "Working directory:       ${WORK_DIR}"
echo "OMZ directory:           ${OMZ_DIR}"
echo "TVM converter directory: ${TVM_CONVERTER_DIR}"
echo "Output directory:        ${OUTPUT_DIR}"
echo "----------------------------------------"

echo "Creating virtual environment for Caffe (Python 3.7)..."
conda create --name tvm_convert_python3.7 python=3.7 -y
echo "Activating virtual environment..."
conda activate tvm_convert_python3.7
echo "Installing packages..."
pip install openvino-dev
pip install apache-tvm
conda install -y caffe
echo "Deactivating virtual environment..."
conda deactivate

echo "Creating virtual environment for ONNX, PyTorch (Python 3.9)..."
conda create --name tvm_convert_python3.9 python=3.9 -y
echo "Activating virtual environment..."
conda activate tvm_convert_python3.9
echo "Installing packages..."
pip install openvino-dev
pip install openvino-dev[caffe,tensorflow2,pytorch]
pip install tensorflow==2.12.0
pip install onnx==1.14.0
pip install torch==2.1.0
pip install tf-keras
pip install apache-tvm==0.14.dev264
pip install tf2onnx
# dependencies for tf_converter.py
pip install onnx-tf
pip install tensorflow-addons
pip install tensorflow-probability
echo "Deactivating virtual environment..."
conda deactivate


model_names=(
"efficientnet-b0" "densenet-121-tf" "googlenet-v1"
"googlenet-v4-tf" "squeezenet1.1" "resnet-50-pytorch"
)
batch_sizes=(
1 2 4 8
)
src_models=(
"${OMZ_DIR}/efficientnet-b0/efficientnet-b0/efficientnet-b0.onnx"
"${OMZ_DIR}/densenet-121-tf/densenet-121-tf.onnx"
"${OMZ_DIR}/googlenet-v1/googlenet-v1"
"${OMZ_DIR}/googlenet-v4-tf/inception_v4.onnx"
"${OMZ_DIR}/squeezenet1.1/squeezenet1.1"
"${OMZ_DIR}/resnet-50-pytorch/resnet50-19c8e357.pth"
)
src_frameworks=(
"onnx" "onnx" "caffe"
"onnx" "caffe" "pytorch"
)
input_shapes=(
"224 224 3" "224 224 3" "299 299 3"
"299 299 3" "3 227 227" "3 224 224"
)

conda activate tvm_convert_python3.9

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

echo "Creating output directories for each model and batch size..."
for model in ${model_names[@]}; do
    echo "Creating directory ${OUTPUT_DIR}/${model}"
    if [ ! -d "${OUTPUT_DIR}/${model}" ]; then
        mkdir -p "${OUTPUT_DIR}/${model}";
    fi
    for batch in ${batch_sizes[@]}; do
        echo -e "\tCreating directory ${OUTPUT_DIR}/${model}/batch_size${batch}"
        if [ ! -d "${OUTPUT_DIR}/${model}/batch_size${batch}" ]; then
            mkdir -p "${OUTPUT_DIR}/${model}/batch_size${batch}";
        fi
    done
done

echo "Converting TensorFlow models to the ONNX format using tf2onnx"
echo -e "\tdensenet-121-tf"
cd ${OMZ_DIR}/densenet-121-tf
echo -e "\tWorking directory: ${PWD}"
python -m tf2onnx.convert --saved-model densenet-121.savedmodel/ --output densenet-121-tf.onnx
echo -e "\tefficientnet-b0"
cd ${TF_CONVERTER_DIR}
python tf_converter.py --model_path "${OMZ_DIR}/efficientnet-b0/efficientnet-b0/model.ckpt.meta" \
                       --input_name sub --output_names logits
cd ${OMZ_DIR}/efficientnet-b0/efficientnet-b0
echo -e "\tWorking directory: ${PWD}"
python -m tf2onnx.convert --saved-model saved_model/ --output efficientnet-b0.onnx
echo -e "\tgooglenet-v4-tf"
cd ${OMZ_DIR}/googlenet-v4-tf
echo -e "\tWorking directory: ${PWD}"
python -m tf2onnx.convert --graphdef inception_v4.frozen.pb --output inception_v4.onnx \
                          --inputs input:0 --outputs InceptionV4/Logits/Predictions:0

conda deactivate


cd ${WORK_DIR}

echo "Converting models to the TVM format..."
for model_idx in ${!model_names[@]}; do
    for batch in  ${batch_sizes[@]}; do
        command_line=()
        if [ "${src_frameworks[$model_idx]}" = "caffe" ]; then
            command_line=("python ${TVM_CONVERTER_DIR}/caffe_to_tvm_converter.py"
                          "-mn ${model_names[$model_idx]}"
                          "-m ${src_models[$model_idx]}.prototxt"
                          "-w ${src_models[$model_idx]}.caffemodel"
                          "-is ${batch} ${input_shapes[$model_idx]}"
                          "-b ${batch}"
                          "-op ${OUTPUT_DIR}/${model_names[$model_idx]}/batch_size${batch}")
            echo -e "\t${command_line[@]}"
            conda activate tvm_convert_python3.7
            ${command_line[@]}
            conda deactivate
        elif [ "${src_frameworks[$model_idx]}" = "onnx" ]; then
            command_line=("python ${TVM_CONVERTER_DIR}/onnx_to_tvm_converter.py"
                          "-mn ${model_names[$model_idx]}"
                          "-m ${src_models[$model_idx]}"
                          "-is ${batch} ${input_shapes[$model_idx]}"
                          "-b ${batch}"
                          "-op ${OUTPUT_DIR}/${model_names[$model_idx]}/batch_size${batch}")
            echo -e "\t${command_line[@]}"
            conda activate tvm_convert_python3.9
            ${command_line[@]}
            conda deactivate
        elif [ "${src_frameworks[$model_idx]}" = "pytorch" ]; then
            if [ "${model_names[$model_idx]}" = "resnet-50-pytorch" ]; then
                command_line=("python ${TVM_CONVERTER_DIR}/pytorch_to_tvm_converter.py"
                              "-mn resnet50"
                              "-w ${src_models[$model_idx]}"
                              "-is ${batch} ${input_shapes[$model_idx]}"
                              "-b ${batch}"
                              "-op ${OUTPUT_DIR}/${model_names[$model_idx]}/batch_size${batch}")
            else
                command_line=("python ${TVM_CONVERTER_DIR}/pytorch_to_tvm_converter.py"
                              "-mn ${model_names[$model_idx]}"
                              "-m ${src_models[$model_idx]}"
                              "-is ${batch} ${input_shapes[$model_idx]}"
                              "-b ${batch}"
                              "-op ${OUTPUT_DIR}/${model_names[$model_idx]}/batch_size${batch}")
            fi
            echo -e "\t${command_line[@]}"
            conda activate tvm_convert_python3.9
            ${command_line[@]}
            conda deactivate
        fi
    done
done

echo "Removing virtual environments..."
conda env remove --name tvm_convert_python3.7
conda env remove --name tvm_convert_python3.9
echo "----------------------------------------"