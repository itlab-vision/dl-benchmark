pylint_status=0;

while read file; do
    pylint ${file} --errors-only \
        -j0 \
        --max-line-length=200 \
        --ignore-patterns="__init__" \
        --extension-pkg-whitelist=cv2,PyQt5,numpy \
        --generated-members=cv2.*,PyQt5.*,numpy.*;
    if test $? -ne 0; then
        pylint_status=1;
    fi;

done < <(find . | grep "\.py$" | sort);

if [ ${pylint_status} -ne 0 ]; then
        false;
fi
