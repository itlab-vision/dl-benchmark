# Оценка точности вывода глубоких моделей

## Описание скрипта

### Основная информация

Скрипт позволяет оценивать точность вывода глубоких моделей с использованием
инструмента [AccuracyChecker][accuracy_checker] в составе пакета [Intel® Distribution of OpenVINO™ Toolkit][openvino-toolkit].
На данный момент скрипт поддерживает полный список фреймворков,
которые поддерживаются AccuracyChecker.

Наряду с этим, для поддержки валидации моделей, запускаемых средствами TVM, можно использовать стороннее расширение AccuracyChecker, которое доступно по [ссылке][open-model-zoo-tvm]. Для запуска необходимо сначала установить python пакет `openvino-dev`, затем собрать приложение `accuracy_check` из репозитория командой `pip install <open_model_zoo_tvm_path>/tools/accuracy_checker/`.

### Алгоритм работы скрипта

Скрипт принимает на вход конфигурации тестов. Описание конфигурации 
тестов можно посмотреть [здесь](../configs/README.md).

Тест представляет собой запуск инструмента AccuracyChecker для одной модели с параметрами,
переданными в конфигурации.

Тесты проводятся последовательно. Каждый тест запускается в отдельном процессе.

### Результаты работы скрипта

Результатом теста являются набор точностей вывода для параметров,
переданных в конфигурации. Результаты записываются в результирующий файл,
представленный csv-таблицей.

## Показатели точности

Показатели точности описаны [здесь][omz-ac-metrics].

## Использование скрипта

Общий вид командной строки:

```bash
python3 accuracy_checker.py <arguments>
```

Аргументы командной строки:

- `-с / --config <accuracy_checker_configuration.xml>` - путь до файла конфигурации,
  содержащего информацию о проводимых тестах.
- `-s / --source <path>` - путь до директории с наборами данных.
- `-r / --result <results.csv>` - имя результирующего файла.
- `-d / --definitions <dataset_definitions.yml>` - путь до файла с описанием наборов данных. Данный файл
  хранится в репозитории [OpenVINO™ Toolkit - Open Model Zoo][omz-ac-definitions].
- `--executor_type` - окружение для запуска скрипта тестирования проверки качества моделей.
  Доступные значения `host_machine` и `docker_container`, `host_machine`
  предполагает запуск в текущем окружении, `docker_container` - запуск в соответсвующем
  docker-контейнере.
- `-a / --annotations <path>` - путь до директории с аннотациями к наборам данным. Параметр необязательный.
- `-e / --extensions <path>` - путь до библиотеки с реализацией нестандартных слоев для устройств. Параметр необязательный.

Пример запуска в текущем окружении:

```bash
python3 accuracy_checker.py \
    -r results.csv -c accuracy_checker.xml \
    -s /mnt/datasets -d dataset_definitions.yml \
    --executor_type host_machine
```

Пример запуска в docker-контейнере:

```bash
python3 accuracy_checker.py \
    -r results.csv -c accuracy_checker.xml \
    -s /mnt/datasets -d dataset_definitions.yml \
    --executor_type docker_container
```

<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[accuracy-checker]: https://docs.openvino.ai/latest/omz_tools_accuracy_checker.html
[omz-ac-metrics]: https://github.com/openvinotoolkit/open_model_zoo/blob/2022.2.0/tools/accuracy_checker/openvino/tools/accuracy_checker/metrics/README.md
[omz-ac-definitions]: https://github.com/openvinotoolkit/open_model_zoo/blob/2022.2.0/tools/accuracy_checker/dataset_definitions.yml
[open-model-zoo-tvm]: https://github.com/FenixFly/open_model_zoo_tvm
