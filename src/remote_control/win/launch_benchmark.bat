@echo off

call "C:\Intel\computer_vision_sdk_2018.4.420\bin\setupvars.bat"
set benchmark_py="C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\benchmark\inference_benchmark.py"
set "config=%C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\benchmark\benchmark_configuration.xml"
set "output_file=%C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\remote_control\win\result_table"
call python %benchmark_py% -c %config% -f %output_file% 