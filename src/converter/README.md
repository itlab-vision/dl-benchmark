# Конвертер моделей из формата инструментов в промежуточный формат OpenVINO

## Использование конвертера

Конвертер запускается из коммандной строки и принимает
на вход 2 аргумента:

- `-m / --mo` - путь до компонента Model Optimizer.
- `-с / --config` - путь до файла конфигурации,
  содержащего информацию о конвертируемых моделях.

Пример запуска:  
```bash
python converter.py \
    -m C:/Intel/computer_vision_sdk_2018.3.343/deployment_tools/model_optimizer/mo.py \
    -c C:/Intel/computer_vision_sdk_2018.3.343/deployment_tools/config.xml
python converter.py \
    --mo C:/Intel/computer_vision_sdk_2018.3.343/deployment_tools/model_optimizer/mo.py \
    --config C:/Intel/computer_vision_sdk_2018.3.343/deployment_tools/config.xml
```

Примечание: если агрументы не переданы или переданы
некорректно, конвертер сообщит об ошибке и закончит свою работу.

## Результаты работы конвертера

Конвертер преобразует модели в промежуточное значение, с теми параметрами,
которые были описаны в переданном файле конфигурации. Результаты работы
конвертера находятся в директориях, указанных в описании конкретной модели
в файле кофигурации.

## Список моделей для конвертации 

OpenVINO R4:
```bash
    densenet-121
    densenet-161
    densenet-169
    densenet-201
    squeezenet1.0
    squeezenet1.1
    mtcnn-p
    mtcnn-r
    mtcnn-o
    mobilenet-ssd
    vgg19
    vgg16
    ssd512
    ssd300
    inception-resnet-v2
    dilation
    googlenet-v1
    googlenet-v2
    googlenet-v4
    alexnet
    ssd_mobilenet_v2_coco
    age-gender-recognition-retail-0013
    age-gender-recognition-retail-0013-fp16
    emotions-recognition-retail-0003
    emotions-recognition-retail-0003-fp16
    face-detection-adas-0001
    face-detection-adas-0001-fp16
    face-detection-retail-0004
    face-detection-retail-0004-fp16
    face-person-detection-retail-0002
    face-person-detection-retail-0002-fp16
    face-reidentification-retail-0001
    face-reidentification-retail-0001-fp16
    head-pose-estimation-adas-0001
    head-pose-estimation-adas-0001-fp16
    landmarks-regression-retail-0001
    landmarks-regression-retail-0001-fp16
    license-plate-recognition-barrier-0001
    license-plate-recognition-barrier-0001-fp16
    pedestrian-and-vehicle-detector-adas-0001
    pedestrian-and-vehicle-detector-adas-0001-fp16
    pedestrian-detection-adas-0002
    pedestrian-detection-adas-0002-fp16
    person-attributes-recognition-crossroad-0031
    person-attributes-recognition-crossroad-0031-fp16
    person-detection-action-recognition-0001
    person-detection-action-recognition-0001-fp16
    person-detection-retail-0001
    person-detection-retail-0001-fp16
    person-detection-retail-0013
    person-detection-retail-0013-fp16
    person-reidentification-retail-0031
    person-reidentification-retail-0031-fp16
    person-reidentification-retail-0076
    person-reidentification-retail-0076-fp16
    person-reidentification-retail-0079
    person-reidentification-retail-0079-fp16
    person-vehicle-bike-detection-crossroad-0078
    person-vehicle-bike-detection-crossroad-0078-fp16
    road-segmentation-adas-0001
    road-segmentation-adas-0001-fp16
    semantic-segmentation-adas-0001
    semantic-segmentation-adas-0001-fp16
    vehicle-attributes-recognition-barrier-0039
    vehicle-attributes-recognition-barrier-0039-fp16
    vehicle-detection-adas-0002
    vehicle-detection-adas-0002-fp16
    vehicle-license-plate-detection-barrier-0106
    vehicle-license-plate-detection-barrier-0106-fp16
```

OpenVINO R5:
```bash
    [TBD]
```