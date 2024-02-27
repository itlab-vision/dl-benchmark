#!/bin/bash

WORK_DIR="$1"
OUTPUT_DIR="${WORK_DIR}/tvm_models"
TVM_TUNING_DIR="${WORK_DIR}/dl-benchmark/src/tvm_autotuning"

MODEL_TUNING_OPTIONS="llvm -mcpu=core-avx2 --num-cores="
DIR_SUFFIX_NAME="so_x86_cores"
MAX_TRIALS_PER_TASK=2
N_TRIALS=32


model_names=(
"efficientnet-b0" "densenet-121-tf" "googlenet-v1"
"googlenet-v4-tf" "squeezenet1.1" "resnet-50-pytorch"
"ssd_512_resnet50_v1_coco" "ssd_512_vgg16_atrous_voc"
"ssd_300_vgg16_atrous_voc" "ssd_512_mobilenet1.0_coco"
)
batch_sizes=(
1 2 4 8
)
core_number_list=(4 6 40)


echo "Compiling models for the RISCV device..."
for model_name in ${model_names[@]}; do
    for batch in  ${batch_sizes[@]}; do
        for core_number in ${core_number_list[@]}; do
            current_model_output_dir="${OUTPUT_DIR}/${model_name}/batch_size${batch}/${DIR_SUFFIX_NAME}_op${core_number}/"
            mkdir -p ${current_model_output_dir}
            command_line=("python ${TVM_TUNING_DIR}/tvm_meta_schedule.py"
                      "--mod=${OUTPUT_DIR}/${model_name}/batch_size${batch}/${model_name}.json"
                      "--params=${OUTPUT_DIR}/${model_name}/batch_size${batch}/${model_name}.params"
                      "--output=${current_model_output_dir}/${model_name}.so"
                      "--target=\"${MODEL_TUNING_OPTIONS}${core_number}\""
                      "--n_trials=${N_TRIALS}"
                      "--max_trials_per_task=${MAX_TRIALS_PER_TASK}")
            echo -e "${command_line[@]}"
            eval ${command_line[@]}
        done
    done
done

