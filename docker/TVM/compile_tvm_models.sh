#!/bin/bash

WORK_DIR="$1"
OUTPUT_DIR="${WORK_DIR}/tvm_models"
TVM_COMPILER_DIR="${WORK_DIR}/dl-benchmark/src/model_converters/tvm_converter"

MODEL_COMPILER_OPTIONS="llvm -mtriple=riscv64-unknown-linux-gnu -mcpu=generic-rv64 -mabi=lp64d -mattr=+64bit,+m,+a,+f,+d,+c"
DIR_SUFFIX_NAME="tar_riscv"


model_names=(
"efficientnet-b0" "densenet-121-tf" "googlenet-v1"
"googlenet-v4-tf" "squeezenet1.1" "resnet-50-pytorch"
"ssd_512_resnet50_v1_coco" "ssd_512_vgg16_atrous_voc"
"ssd_300_vgg16_atrous_voc" "ssd_512_mobilenet1.0_coco"
)
batch_sizes=(
1 2 4 8
)
opt_levels=(0 2 3)

echo "Compiling models for the RISCV device..."
for model_name in ${model_names[@]}; do
    for batch in  ${batch_sizes[@]}; do
        for opt_level in ${opt_levels[@]}; do
            current_model_output_dir="${OUTPUT_DIR}/${model_name}/batch_size${batch}/${DIR_SUFFIX_NAME}_op${opt_level}/"
            mkdir -p ${current_model_output_dir}
            command_line=("python ${TVM_COMPILER_DIR}/tvm_compiler.py"
                      "--mod=${OUTPUT_DIR}/${model_name}/batch_size${batch}/${model_name}.json"
                      "--params=${OUTPUT_DIR}/${model_name}/batch_size${batch}/${model_name}.params"
                      "--opt_level=${opt_level}"
                      "--lib_name=${model_name}.tar"
                      "--output_dir=${current_model_output_dir}"
                      "--target=\"${MODEL_COMPILER_OPTIONS}\"")
            echo -e "${command_line[@]}"
            eval ${command_line[@]}
        done
    done
done

