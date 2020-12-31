# Шаблоны для файлов конфигурации

## Заполнение файла конфигурации для скрипта замера производительности

### Правила заполнения

Общая информация:

- Файл конфигурации описывается в формате XML.
- Шаблонная структура приведена в файле `benchmark_configuration_file_template.xml`.
- Порядок тегов важен и при изменении порядка тегов поведение скрипта не определено.
- Кодировка файла - `utf-8`.
- Корневой тег называется `Tests`.
- Каждый тест анализа производительности для конкретной модели с определенным набором
  параметров запуска описывается внутри тега `Test` (внутри тега `Tests`).
- Информация о модели описывается внутри тега `Model` (внутри тега `Test`).
- Информация о наборе данных описывается внутри тега `Dataset` (внутри тега `Test`).
- Информация о параметрах теста, независящих от используемого для вывода фреймворка,
  описывается внутри тега `FrameworkIndependent` (внутри тега `Test`).
- Информация о параметрах теста, зависящих от используемого для вывода фреймворка,
  описывается внутри тега `FrameworkDependent` (внутри тега `Test`).

Заполнение информации о модели:

- Все теги, пренадлежащие тегу `Model`, являются обязательными для заполнения.
- Название задачи, которую решает модель, описывается внутри тега `Task`.
- Имя модели описывается внутри тега `Name`.
- Тип данных весов описывется внутри тега `Precision`.
- Фреймворк, с использованием которого обучена модель, описывается внутри
  тега `SourceFramework` (используется для формирования финальной таблицы результатов).
- Абсолютный путь до файла, который содержит описание модели, описывается внутри тега `ModelPath`.
- Абсолютный путь до файла, который содержит веса модели, описывается внутри тега `WeightsPath`.

Заполнение информации о выборке:

- Все теги, пренадлежащие тегу `Dataset`, являются обязательными для заполнения.
- Название наора данных описывается внутри тега `Name`.
- Абсолютный путь до директории, где лежат данные, описывается внутри тега `Path`.

Заполнение информации о параметрах теста, не зависящих от используемого
для вывода фреймворка:

- Все теги, пренадлежащие тегу `FrameworkIndependent`, являются обязательными
  для заполнения.
- Название фреймворка, используемого для вывода, описывается внутри
  тега `InferenceFramework`.
- Размер пачки данных, обрабатываемых за один прямой проход сети, описывается
  внутри тега `BatchSize`.
- Устройство, на котором будет запущен вывод, описывается внутри тега `Device`.
- Количество итераций цикла тестирования описывается внутри тега `IterationCount`.
- Максимальное время выполнения теста в минутах описывается внутри тега `TestTimeLimit`.

Заполнение информации о параметрах теста, зависящих от используемого
для вывода фреймворка:

- Набор тегов для тестирования вывода средствами Intel Distribution
  of OpenVINO Toolkit:

  - `Mode` - тег, обязательный для заполнения. Описывает программный интерфейс вывода.
    Допустимые значения `Sync` (используется для реализации latency-режима) и `Async`
    (используется для реализации latency-режима при создании очереди из одного запроса
    и throughput-режима при создании очереди из большего числа запросов).
  - `Extension` - тег, необязательный для заполнения. Описывает абсолютный путь
    до реализации слоев, неподдерживаемых OpenVINO.
  - `AsyncRequestCount` - опциональный тег. Может быть заполнен для асинхронноого
    интерфейса. Описывает количество запросов на одновременное исполнение вывода.
  - `ThreadCount` - опциональный тег. Описывает максимальное количество физических
    потоков для выполнения вывода. По умолчанию будет выставлено число потоков, равное
    физическому количеству ядер в системе.
  - `StreamCount` - опциональный тег. Может быть заполнен для асинхронного интерфейса.
    Описывает максимальное количество одновременно выполняющихся запросов на вывод.

- Набор тегов для тестирования вывода средствами Intel Optimization for Caffe:

  - `ChannelSwap` - тег, необязательный для заполнения. Описывает изменение порядка каналов на
    входном изображении. По умолчанию будет установлен порядок (2, 0, 1), что соответствует BGR.
  - `Mean` - тег, необязательный для заполнения. Определяет средние значения, которые будут вычитаться
    по каждому из каналов входного изображения. По умолчанию (0, 0, 0).
  - `InputScale` - тег, необязательный для заполнения. Определяет коэффициент масштабирования входного
    изображения. По умолчению равен 1.

- Набор тегов для тестирования вывода средствами Intel Optimization for TensorFlow:

  - `ChannelSwap` - тег, необязательный для заполнения. Описывает изменение порядка каналов на
    входном изображении. По умолчанию будет установлен порядок (2, 0, 1), что соответствует BGR.
  - `Mean` - тег, необязательный для заполнения. Определяет средние значения, которые будут вычитаться
    по каждому из каналов входного изображения. По умолчанию (0, 0, 0).
  - `InputScale` - тег, необязательный для заполнения. Определяет коэффициент масштабирования входного
    изображения. По умолчению равен 1.
  - `InputShape` - тег, необязательный для заполнения. Определяет размеры входного тензора в формате HWC
    (высота, ширина, число каналов). По умолчанию не установлен.
  - `OutputNames` - тег, необязательный для заполнения. Определяет имена выходных узлов модели. 
    По умолчанию не установлен.

### Примеры заполнения

#### Пример заполнения конфигурации для измерения производительности вывода средствами Intel Distribution of OpenVINO Toolkit

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Tests>
    <Test>
        <Model>
            <Task>Classification</Task>
            <Name>densenet-121</Name>
            <Precision>FP32</Precision>
            <SourceFramework>Caffe</SourceFramework>
            <ModelPath>/home/alexander/models/classification/densenet/121/IR/FP32/densenet-121.xml</ModelPath>
            <WeightsPath>/home/alexander/models/classification/densenet/121/IR/FP32/densenet-121.bin</WeightsPath>
        </Model>
        <Dataset>
            <Name>ImageNET</Name>
            <Path>/home/alexander/data/ImageNET</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <BatchSize>4</BatchSize>
            <Device>CPU</Device>
            <IterationCount>1000</IterationCount>
            <TestTimeLimit>180</TestTimeLimit>
        </FrameworkIndependent>
        <FrameworkDependent>
            <Mode>Sync</Mode>
            <Extension></Extension>
            <AsyncRequestCount></AsyncRequestCount>
            <ThreadCount></ThreadCount>
            <StreamCount></StreamCount>
        </FrameworkDependent>
    </Test>
    <Test>
        <Model>
            <Task>Classification</Task>
            <Name>densenet-121</Name>
            <Precision>FP32</Precision>
            <SourceFramework>Caffe</SourceFramework>
            <ModelPath>/home/alexander/models/classification/densenet/121/IR/FP32/densenet-121.xml</ModelPath>
            <WeightsPath>/home/alexander/models/classification/densenet/121/IR/FP32/densenet-121.bin</WeightsPath>
        </Model>
        <Dataset>
            <Name>ImageNET</Name>
            <Path>/home/alexander/data/ImageNET</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <BatchSize>4</BatchSize>
            <Device>CPU</Device>
            <IterationCount>1000</IterationCount>
            <TestTimeLimit>180</TestTimeLimit>
        </FrameworkIndependent>
        <FrameworkDependent>
            <Mode>Async</Mode>
            <Extension></Extension>
            <AsyncRequestCount></AsyncRequestCount>
            <ThreadCount></ThreadCount>
            <StreamCount></StreamCount>
        </FrameworkDependent>
    </Test>
</Tests>
```

#### Пример заполнения конфигурации для измерения производительности вывода средствами Intel Optimization for Caffe

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Tests>
    <Test>
        <Model>
            <Task>Classification</Task>
            <Name>mobilenet-v1-1.0-224</Name>
            <Precision>FP32</Precision>
            <SourceFramework>Caffe</SourceFramework>
            <ModelPath>/home/roix/models/public/mobilenet-v1-1.0-224/mobilenet-v1-1.0-224.prototxt</ModelPath>
            <WeightsPath>/home/roix/models/public/mobilenet-v1-1.0-224/mobilenet-v1-1.0-224.caffemodel</WeightsPath>
        </Model>
        <Dataset>
            <Name>ImageNET</Name>
            <Path>/home/roix/data/ImageNET</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>Caffe</InferenceFramework>
            <BatchSize>4</BatchSize>
            <Device>CPU</Device>
            <IterationCount>1000</IterationCount>
            <TestTimeLimit>180</TestTimeLimit>
        </FrameworkIndependent>
        <FrameworkDependent>
            <ChannelSwap>2 1 0</ChannelSwap>
            <Mean>103.94 116.78 123.68</Mean>
            <InputScale>0.017</InputScale>
        </FrameworkDependent>
    </Test>
</Tests>
```

#### Пример заполнения конфигурации для измерения производительности вывода средствами Intel Optimization for TensorFlow

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Tests>
    <Test>
        <Model>
            <Task>Classification</Task>
            <Name>densenet-121-tf</Name>
            <Precision>FP32</Precision>
            <SourceFramework>TensorFlow</SourceFramework>
            <ModelPath>/home/roix/models/public/densenet-121-tf/tf-densenet121.ckpt.meta</ModelPath>
            <WeightsPath>/home/roix/models/public/densenet-121-tf/tf-densenet121.ckpt.meta</WeightsPath>
        </Model>
        <Dataset>
            <Name>ImageNET</Name>
            <Path>/home/roix/data/ImageNET</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>TensorFlow</InferenceFramework>
            <BatchSize>4</BatchSize>
            <Device>CPU</Device>
            <IterationCount>1000</IterationCount>
            <TestTimeLimit>180</TestTimeLimit>
        </FrameworkIndependent>
        <FrameworkDependent>
            <ChannelSwap>2 1 0</ChannelSwap>
            <Mean>123.68 116.78 103.94</Mean>
            <InputScale>58.8235294</InputScale>
            <InputShape>224 224 3</InputShape>
            <OutputNames>densenet121/predictions/Reshape_1</OutputNames>
        </FrameworkDependent>
    </Test>
</Tests>
```

## Заполнение файла конфигурации для скрипта удаленного запуска

### Правила заполнения

- Файл конфигурации описывается в формате XML.
- Шаблонная структура приведена в файле `remote_configuration_file_template.xml`.
- Кодировка файла - `utf-8`.
- Корневой тег называется `Computers`.
- Каждый компьютер, на котором производится запуск бенчмарка, описывается 
  внутри тега `Computer`.
- Первый параметр представляет собой IP-адрес компьютера, на котором планируется
  запуск. Параметр описывается внутри тега `IP`.
- `Login` - логин пользователя компьютера, на котором планируется
  запуск.
- `Password` - пароль пользователя компьютера,
  на котором планируется запуск.
- OS - операционная система, установленная на компьютер,
  на котором планируется запуск.
- Путь до скрипта `ftp_client.py` в папке `remote_start`
  (на компьютер предварительно нужно склонировать наш репозиторий)
  описывается внутри тегов `FTPClientPath`.
- Путь до конфигурации бенчмарка описывается внутри тега `BenchmarkConfig`.
- Тип исполнителя вывода при бенчмаркинге описывается внутри тега `BenchmarkExecutor`.
  Допустимые значения `host_machine ` (запуск вывода производится в окружении пользователя) и
  `docker_container` (запуск вывода производится в предварительно настроенном docker контейнере)
- Имя файла, в который запишется лог работы программы, описывается внутри
  тега `LogFile`.
- Имя таблицы, в которую записывается результат работы программы, описывается
  внутри тега `ResultFile`.

### Пример заполнения

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Computers>
    <Computer>
        <IP>4.4.4.4</IP>
        <Login>Admin</Login>
        <Password>Admin</Password>
        <OS>Windows</OS>
        <FTPClientPath>C:/dl-benchmark/src/remote_control/ftp_client.py</FTPClientPath>
        <BenchmarkConfig>C:/dl-benchmark/src/configs/benchmark_configuration.xml</BenchmarkConfig>
        <BenchmarkExecutor>host_machine</BenchmarkExecutor>
        <LogFile>program_log.txt</LogFile>
        <ResultFile>result_table.csv</ResultFile>
    </Computer>
</Computers>
```

## Заполнение файла конфигурации для скрипта развертывания инфраструктуры для системы бенчмаркинга

### Правила заполнения

- Файл конфигурации описывается в формате XML.
- Шаблонная структура описана в файле `deploy_configuration_file_template.xml`.
- Кодировка файла - `utf-8`.
- Корневой тег называется `Computers`.
- Каждый компьютер, на котором производится развертывание инфраструктуры,
  описывается внутри тега `Computer`.
- Первый параметр представляет собой IP-адрес компьютера, на котором планируется
  запуск. Параметр описывается внутри тега `IP`.
- `Login` - логин пользователя компьютера, на котором планируется выполнить
  развертывание.
- `Password` - пароль пользователя компьютера, на котором планируется
  выполнить развертывание.
- OS - операционная система, установленная на компьютер,
  на котором планируется запуск.
- Путь до директории, куда будет сохранен Docker-образ, описывается
  внутри тега `DownloadFolder`.

### Пример заполнения

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Computers>
    <Computer>
        <IP>2.2.2.2</IP>
        <Login>admin</Login>
        <Password>admin</Password>
        <OS>Linux</OS>
        <DownloadFolder>/tmp/docker_folder</DownloadFolder>
    </Computer>
</Computers>
```
