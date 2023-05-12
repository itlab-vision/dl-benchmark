# Измерение производительности вывода глубоких моделей

## Описание скрипта

### Основная информация

Скрипт позволяет измерять производительность вывода глубоких моделей
с использованием разных фреймворков. На данный момент поддерживается
вывод с использованием следующих фреймворков:

- Inference Engine в составе
  [Intel® Distribution of OpenVINO™ Toolkit][openvino-toolkit].
- [Intel® Optimization for Caffe][intel-caffe].
- [Intel® Optimization for TensorFlow][intel-tensorflow].
- [TensorFlow Lite][tensorflow-lite].
- [ONNX Runtime][onnx-runtime].
- [OpenCV][opencv].
- [MXNet][mxnet].
- [PyTorch][pytorch].

### Алгоритм работы скрипта

Скрипт принимает на вход конфигурации тестов. Описание конфигурации 
тестов можно посмотреть [здесь](../configs/README.md).

Тест представляет собой запуск вывода одной модели с параметрами,
переданными в конфигурации.

Тесты проводятся последовательно. Каждый тест запускается в отдельном процессе.

### Результаты работы скрипта тестирования

Результатом теста являются метрики производительности вывода для параметров,
переданных в конфигурации. Результаты записываются в результирующий файл,
представленный csv-таблицей.

## Показатели производительности

### Показатели производительности вывода для Intel® Distribution of OpenVINO™ Toolkit

Разработанная система для вывода нейронных сетей использует компонент
Inference Engine в составе пакета Intel® Distribution of OpenVINO™ Toolkit.
Intel® Distribution of OpenVINO™ Toolkit поддерживает два режима вывода.

1. **Режим минимизации времени выполнения одного запроса (latency mode)**.
   Предполагает создание и выполнение одного запроса для вывода модели
   на выбранном устройстве. Следующий запрос на вывод создается
   по завершении предыдущего. Во время анализа производительности количество
   сгенерированных запросов определяется числом итераций цикла тестирования модели.
1. **Режим минимизации времени выполнения набора запросов (throughtput mode)**.
   Предполагает создание набора запросов для вывода нейронной сети на выбранном
   устройстве. Порядок выполнения запросов может быть произвольным. Количество
   наборов запросов определяется количеством итераций цикла тестирования модели.

Inference Engine предоставляет 2 программных интерфейса для вывода глубоких моделей.

1. **Синхронный интерфейс (Sync API)**. Используется для реализации вывода
   в режиме минимизации времени выполнения одного запроса (latency mode).
1. **Асинхронный интерфейс (Async API)**.  Используется для реализации вывода
   в режиме минимизации времени выполнения одного запроса (latency mode),
   если создан один запрос, и вывода в режиме минимизации времени выполнения
   набора запросов (throughput mode), если создано более одного запроса.

Один запрос на вывод соответствует прямому проходу нейронной сети для пачки изображений.
Обязательные параметры выполнения:

- размер пачки (batch size);
- количество итераций;
- количество запросов, созданных в асинхронном режиме.

Вывод может быть выполнен в многопоточном режиме. Количество потоков (threads)
может быть установлено в качестве параметра выполнения модели.

Для асинхронного интерфейса есть возможность выполнять запросы параллельно,
используя логические потоки - стримы (streams). Стрим — это группа
физических потоков. Число стримов является параметром асинхронного режима.
По умолчанию количество стримов совпадает с количеством запросов.

Поскольку OpenVINO обеспечивает два режима вывода, то выделяется
два набора показателей производительности. При оценке производительности
вывода для **режима минимизации времени выполнения одного запроса (latency mode)**
запросы выполняются последовательно. Следующий запрос выполняется после
завершения предыдущего. Для каждого запроса измеряется продолжительность
его выполнения. Стандартное отклонение рассчитывается на основе набора
полученных длительностей, а те, которые выходят за пределы трех стандартных
отклонений относительно среднего времени вывода, отбрасываются. Результирующий
набор времен используется для вычисления метрик производительности
для синхронного режима.

- **Латентность (latency)** - медиана множества времен выполнения вывода.
- **Среднее время одного прохода (average time of single pass)** - отношение
  общего времени выполнения всех запросов к числу запросов.
- **Количество кадров, обрабатываемых за секунду (frames per second, FPS)** -
  отношение размера обрабатываемой "пачки" изображений к среднему времени
  одного прохода.

Для **режима минимизации времени выполнения набора запросов (throughput mode)**
вычисляется следующий набор показателей.

- **Среднее время одного прохода (average time of single pass)** -
  отношение времени выполнения всех наборов запросов к числу
  итераций цикла тестирования. Характеризует время выполнения набора
  одновременно созданных запросов на устройстве.
- **Количество кадров, обрабатываемых за секунду (frames per second, FPS)** -
  отношение произведения размера обрабатываемой "пачки" и числа итераций
  к общему времени выполнения всех запросов.

**Примечание:** в публикуемой html-таблице содержатся только показатели FPS.

### Показатели производительности вывода для Intel® Optimization for Caffe, Intel® Optimization for TensorFlow, TensorFlow Lite, OpenCV, MXNet и PyTorch

При оценке производительности вывода для Intel® Optimization for Caffe,
Intel® Optimization for TensorFlow, TensorFlow Lite, OpenCV, MXNet и PyTorch
осуществляется последовательный и независимый запуск запросов.
Запуск очередного запроса выполняется после завершения предыдущего.
Для каждого запроса осуществляется замер времени его выполнения.
Для множества полученных времен определяется стандартное среднеквадратичное 
отклонение, и отбрасываются времена, выходящие за пределы трех стандартных 
отклонений от среднего времени вывода. Результирующий набор времен 
используется для вычисления показателя латентности.
Остальные показатели вычисляются для всего множества времен.

- **Латентность (latency)** - медиана множества времен выполнения вывода.
- **Среднее время одного прохода (average time of single pass)** - отношение
  общего времени выполнения всех запросов к числу запросов.
- **Количество кадров, обрабатываемых за секунду (frames per second, FPS)** -
  отношение размера обрабатываемой “пачки” изображений к среднему времени
  одного прохода.

### Показатели производительности вывода при использовании benchmark_app

На данный момент для измерения производительности вывода библиотек
можно использовать инструмент `benchmark_app`, входящий в состав
[Intel® Distribution of OpenVINO™ Toolkit][openvino-toolkit].
Алгоритм вычисления показателей производительности доступен в документации.

## Использование скрипта

Общий вид командной строки:

```bash
python3 inference_benchmark.py <arguments>
```

Аргументы командной строки:

- `-с / --config <benchmark_configuration.xml>` - путь до файла конфигурации,
  содержащего информацию о проводимых тестах.
- `-r / --result <results.csv>` - имя результирующего файла.
- `--executor_type` - окружение для запуска скрипта тестирования производительности.
  Доступные значения `host_machine` и `docker_container`, `host_machine`
  предполагает запуск в текущем окружении, `docker_container` запуск в соответсвующем
  docker-контейнере.

Пример запуска в текущем окружении:

```bash
python3 inference_benchmark.py \
    -r results.csv -c benchmark_configuration.xml \
    --executor_type host_machine
```

Пример запуска в docker-контейнере:

```bash
python3 inference_benchmark.py \
    -r results.csv -c benchmark_configuration.xml \
    --executor_type docker_container
```

## Использование OpenVINO Benchmark C++ tool в качестве инструмента для замеров

### Сборка (linux)

1. Клонировать репозиторий. Рекомендуется использовать стабильную версию из списка 
   https://github.com/openvinotoolkit/openvino/releases.

   ```bash
   git clone https://github.com/openvinotoolkit/openvino.git
   git checkout <release_tag>
   cd openvino
   git submodule update --init --recursive
   ```

1. Собрать OpenVINO, следуя официальной инструкции 
   https://github.com/openvinotoolkit/openvino/wiki/BuildingForLinux.

1. В случае использования стабильной версии установить python wheels
   из PyPI-хранилища.

   ```bash
   pip install --upgrade pip 
   pip install openvino==<your version, ex 2022.1.0>
   pip install openvino_dev
   pip install openvino_dev[mxnet,caffe,caffe2,onnx,pytorch,tensorflow2]==<your version, ex 2022.1.0>
   ```

1. Запустить `setupvars.sh`:

   ```bash
   source INSTALL_DIR/setupvars.sh 
   ```

1. В директории `INSTALL_DIR/samples/cpp` запустить `./build_samples.sh`.

### Использование

1. В конфигурационном файле (секция `FrameworkDependent`)
   укажите `Mode`: `ovbenchmark_cpp_latency` или `ovbenchmark_cpp_throughput`.

1. Найдите исполняемый файл `benchmark_app` по адресу, приведенному ниже.

   ```
   /home/<user>/inference_engine_cpp_samples_build/intel64/Release/benchmark_app
   ```

1. Используйте его в качестве параметра для `inference_benchmark.py`:

   ```bash
   python3 inference_benchmark.py -c <path_to_benchmark_configuration_file.xml> -r result.csv -b /home/<user>/inference_engine_cpp_samples_build/intel64/Release/benchmark_app
   ```

## Использование OpenVINO Benchmark Python tool в качестве инструмента для замеров

### Установка

В случае использования стабильной версии, установить python wheels из PyPI-хранилища.

```bash
pip install --upgrade pip 
pip install openvino==<your version, ex 2022.1.0>
pip install openvino_dev
pip install openvino_dev[mxnet,caffe,caffe2,onnx,pytorch,tensorflow2]==<your version, ex 2022.1.0>
```

### Использование

1. В конфигурационном файле (секция `FrameworkDependent`)
   укажите `Mode`: `ovbenchmark_python_latency` или `ovbenchmark_python_throughput`.

1. Запустите скрипт `inference_benchmark.py`.

   ```bash
   python3 inference_benchmark.py -c <path_to_benchmark_configuration_file.xml> -r result.csv
   ```


<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[intel-caffe]: https://github.com/intel/caffe
[intel-tensorflow]: https://www.intel.com/content/www/us/en/developer/articles/guide/optimization-for-tensorflow-installation-guide.html
[tensorflow-lite]: https://www.tensorflow.org/lite
[onnx-runtime]: https://onnxruntime.ai
[mxnet]: https://mxnet.apache.org
[opencv]: https://opencv.org
[pytorch]: https://pytorch.org
