# Скрипт тестирования производительности Inference Engine

## Использование скрипта тестирования производительности

Скрипт запускается из командной строки и принимает
на вход 2 аргумента:

- `-f / --filename` - имя результирующего файла с форматом.
- `-с / --config` - путь до файла конфигурации,
  содержащего информацию о тестах.

Пример запуска:  
```bash
python inference_benchmark.py \
    -f results.csv -c C:/benchmark_configuration.xml
python inference_benchmark.py \
    --filename results.csv --config C:/benchmark_configuration.xml
```

Примечание: если агрументы не переданы или переданы
некорректно, скрипт сообщит об ошибке и закончит свою работу.

## Работа скрипта тестирования производительности

Для каждой модели из списка производится тестирование в синхронном и
асинхронном режимах с одинаковыми параметрами тестирования.

## Результаты работы скрипта тестирования производительности

Скрипт произведет тестирование производительности моделей,
после чего создаст результирующий файл и сохранит в него полученные данные.

## Показатели производительности

**Показатели производительности для синхронного режима**

- Времена работы всех запросов. Выполняются замеры времени работы каждого
  запроса. Вычисляется срандартное среднеквадратичное отклонение всех
  времен, и отбрасываются времена, выходящие за пределы трех стандартных
  отклонений.
- Латентность (`Latency`). Построенный перечень времен сортируется
  и вычисляется медиана полученного массива времен.
- Среднее время одного прохода (`Average time of single pass`) -
  отношение времени выполнения всех циклов запросов к числу итераций.
- Количество кадров, обрабатываемых за секунду с учетом параметра
  `batch size`(`Frame Per Seconds, FPS`):
  `FPS = Batch size / Average time of single pass`.

**Показатели производительности для асинхронного режима**

- Среднее время одного прохода (`Average time of single pass`) -
  отношение времени выполнения всего цикла запросов к числу итераций.
- Количество кадров, обрабатываемых за секунду с учетом параметра
  `batch size` (`Frame Per Seconds, FPS`):
  `FPS = (Batch size * Iteration count) / Inference time`.

## Список моделей для теста

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
    resnet-50
    resnet-101
    resnet-152
    googlenet-v3
```

OpenVINO R5:
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
    resnet-50
    resnet-101
    resnet-152
    googlenet-v3
```