# Конвертер моделей из формата инструментов в промежуточный формат OpenVINO

**Использование конвертера**  

Конвертер запускается из коммандной строки и принимает
на вход 3 аргумента:

- `-m / --mo_dir` - путь до директории,
  где лежит Model Optimizer.
- `-i / --input_dir` - путь до директории,
  где лежат загруженные модели.
- `-d / --data_type` - тип данных весов
  (допустимые значения: `FP16`/`FP32`/`float`/`half`).

Пример запуска:  
```
converter.py -m C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_optimizer \
             -i C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_downloader -d FP32
converter.py --mo_dir C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_optimizer \
             --input_dir C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_downloader \
             --data_type FP32
```

В случае, когда агрументы не переданы или переданы
некорректно, конвертер сообщит об ошибке и закончит свою работу.

**Сохранение результатов**  
Конвертер преобразует модели в промежуточное значение. Результаты работы
конвертера находятся в директории `<Путь до модели>/ir/<Точность, с которой модель была преобразована>`.

Пример:
`<...>\deployment_tools\model_downloader\object_detection\common\ssd_mobilenet_v2_coco\tf\ssd_mobilenet_v2_coco_2018_03_29\ir\FP32`
В этой директории лежит модель `ssd_mobilenet_v2_coco`
в своем промежуточном состоянии с точностью `FP32`.
