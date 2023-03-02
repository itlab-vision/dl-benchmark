# Copyright (C) 2023 KNS Group LLC (YADRO)
# All Rights Reserved.

# This software contains the intellectual property of YADRO
# or is licensed to YADRO from third parties. Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by YADRO.
#

function(apply_code_style_fixes INPUT_FILE)
    execute_process(COMMAND ${CLANG_FORMAT} -style=file -i ${INPUT_FILE}
        OUTPUT_VARIABLE STYLE_CHECK_RESULT)
endfunction()

foreach(source_file IN LISTS INPUT_FILES)
    set(exclude FALSE)
    foreach(pattern IN LISTS EXCLUDE_PATTERNS)
        if(source_file MATCHES "${pattern}")
            set(exclude ON)
            break()
        endif()
    endforeach()

    if(exclude)
        continue()
    endif()

    apply_code_style_fixes(${source_file})
endforeach()