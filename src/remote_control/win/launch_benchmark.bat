@echo off
call "C:\Intel\computer_vision_sdk_2018.4.420\bin\setupvars.bat"
set async_py="C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\inference\inference_async_mode.py"
set "model=%C:\Intel\computer_vision_sdk_2018.4.420\deployment_tools\model_downloader\classification\alexnet\IR\alexnet.xml"
set "weights=%C:\Intel\computer_vision_sdk_2018.4.420\deployment_tools\model_downloader\classification\alexnet\IR\alexnet.bin"
set "images=%C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\data\ImageNET\"
set "labels =%C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\inference\image_net_synset.txt"
call python %async_py% -m %model% -w %weights% -i %images% -t classification -r 1 -b 1 -ni 10 -nt 5 >> C:\Users\kumbrasev.p\Documents\GitHub\openvino-dl-benchmark\src\remote_control\win\result.txt