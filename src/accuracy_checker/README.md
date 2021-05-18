# Проверка точности глубоких моделей

## Описание скрипта

### Основная информация

Скрипт позволяет проверять точность глубоких моделей
с использованием разных фреймворков для вывода.

### Алгоритм работы скрипта

Скрипт принимает на вход конфигурацую тестов. Описание конфигурации 
тестов можно посмотреть [здесь][configs].

Тест представляет собой запуск `accuracy check`,
предоставляемый [Intel® Distribution of OpenVINO™ Toolkit Open Model Zoo][openvino-toolkit-omz],
с подачей необходимых ему параметров.

### Результаты работы скрипта тестирования

Результаты, полученные в процессе `accuracy check`,
записываются в результирующий файл, представленный csv-таблицей.

## Использование скрипта

Аргументы командной строки:

- `-с / --config <configuration_file.yml>` - путь до файла конфигурации,
  содержащего информацию о моделях.
- `-m / --models <path_to_models>` - путь до директории, в которой хранятся модели.
- `-s / --source <path_to_source>` - путь до директории, в которой хранятся датасеты.
- `-r / --result <results.csv>` - имя результирующего файла.
- `-a / --annotations <path_to_annotations>` - путь до директории с аннотациями.
- `-d / --definitions <path_to_definition>` - путь до глобальной конфигурации датасетов.
- `-e / --extensions <path_to_extensions>` - путь до реализации слоев, неподдерживаемых
  OpenVINO.
- `--executor_type` - окружение для запуска скрипта тестирования производительности.
  Доступные значения `host_machine` и `docker_container`, `host_machine`
  предполагает запуск в текущем окружении, `docker_container` запуск в соответсвующем
  docker-контейнере.

Пример запуска в текущем окружении:

```bash
python3 accuracy_checker.py \
    -r results.csv -c accuracy_checker_configuration.yml -m models -s source \
    --executor_type host_machine
```

Пример запуска в docker-контейнере:

```bash
python3 accuracy_checker.py \
    -r results.csv -c accuracy_checker_configuration.yml -m models -s source \
    --executor_type docker_container
```

<!-- LINKS -->
[configs]: https://software.intel.com/en-us/openvino-toolkit
[openvino-toolkit-omz]: https://github.com/openvinotoolkit/open_model_zoo
