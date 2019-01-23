@echo off

call "C:\Intel\computer_vision_sdk_2018.4.420\bin\setupvars.bat"
call cd C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\benchmark\
set benchmark_py="inference_benchmark.py"
set "config=%C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\benchmark\benchmark_configuration.xml"
set "output_file=%C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\remote_control\win\result_table.csv"
call python %benchmark_py% -c %config% -f %output_file% 