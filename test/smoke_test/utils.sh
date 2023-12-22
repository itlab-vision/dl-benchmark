#!/bin/bash

function check_exit_code {
    return_value=$?
    if [ $return_value -ne 0 ]; then
        echo "$1 exited with non-zero code: ${return_value}"
    fi
}

function check_results_file {
    if [ ! -f "$1" ]; then
        echo "File $1 not exist!"
        return_value=128
    else
        success_tests_count=$(grep -io 'Success' "$1" | wc -l)
        failed_tests=$(grep -i Failed "$1")
        if [ "$success_tests_count" -ne "$2" ]; then
            echo "There are should be $2 tests in $1 and all the tests should be passed"
            echo "Failed tests:"
            echo "$failed_tests"
            return_value=255
        else
            echo "Done, $success_tests_count tests passed"
        fi
    fi
}

function check_classification() {
    local output="$1"
    local class_name="$2"
    local model_name="$3"

    local start_line=$(echo "$output" | grep -n "Start inference test on model: $model_name" | cut -d : -f 1)
    local end_line=$(echo "$output" | grep -n "End inference test on model : $model_name" | cut -d : -f 1)

    if [[ ! -z "$start_line" && ! -z "$end_line" ]]; then
        local target_text=$(sed -n "${start_line},${end_line}p" <<< "$output")

        if echo "$target_text" | grep -q "Result for image 1"; then
            local top_result=$(echo "$target_text" | grep -A1 '\[ INFO \] Result for image 1' | tail -n 1)
            
            if echo "$top_result" | grep -q "$class_name"; then
                echo "[$model_name] Classification passed"
            else
                echo "[$model_name] Classification failed. Predicted: $(echo $top_result | cut -d' ' -f4- | cut -d' ' -f2-); Actual: $class_name"
                return_value=1
            fi
        else
            echo "[$model_name] Failed: could not find classification results. Please, check if you set RawOutput to False in configuration."
            return_value=1
        fi
    else
        echo "Failed: could not find any runs for '$model_name'."
        return_value=1
    fi
    
    return $return_value
}