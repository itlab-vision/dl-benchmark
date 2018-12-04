# Конвертер моделей из формата инструментов в промежуточный формат OpenVINO

**Использование конвертера**  

Конвертер запускается из коммандной строки и принимает
на вход 2 аргумента:

- `-m / --mo` - путь Model Optimizer.
- `-с / --config` - путь до файла конфигурации,
  в котором находятся список моделей с набором параметров,
  необходимые для конвертации.

Пример запуска:  
```
python converter.py -m C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_optimizer\mo.py
                    -c C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\config.xml
python converter.py --mo C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_optimizer\mo.py
                    --config C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\config.xml
```

В случае, когда агрументы не переданы или переданы
некорректно, конвертер сообщит об ошибке и закончит свою работу.

**Результаты работы**  
Конвертер преобразует модели в промежуточное значение, с теми параметрами,
которые были описаны в переданном файле конфигурации. Результаты работы
конвертера находятся в директории, указанные в параметрах конфига.

Пример:
`<...>\deployment_tools\model_downloader\object_detection\common\ssd_mobilenet_v2_coco\tf\ssd_mobilenet_v2_coco_2018_03_29\ir\FP32`.
В этой директории лежит модель `ssd_mobilenet_v2_coco`
в своем промежуточном состоянии с точностью `FP32`.
