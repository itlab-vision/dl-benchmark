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