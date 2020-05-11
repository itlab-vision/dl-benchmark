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
- Абсолютный путь до директории, где расположена модель, описывается внутри тега `Path`.

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
            <Path>/home/alexander/models/classification/densenet/121/IR/FP32</Path>
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
            <Path>/home/alexander/models/classification/densenet/121/IR/FP32</Path>
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
  на котором планируется запуск. Параметр описывается внутри тегов `OS`.
- Путь до скрипта `ftp_client.py` в папке `remote_start`
  (на компьютер предварительно нужно склонировать наш репозиторий)
  описывается внутри тегов `FTPClientPath`.
- Путь до файла, устанавливающего окружение OpenVINO описывается
  внутри тега `OpenVINOEnvironmentPath`.
- Путь до конфигурации бенчмарка описывается внутри тега `BenchmarkConfig`.
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
        <FTPClientPath>C:/openvino-dl-benchmark/src/remote_control/ftp_client.py</FTPClientPath>
        <OpenVINOEnvironmentPath>C:/Intel/computer_vision_sdk_2018.4.420/bin/setupvars.bat</OpenVINOEnvironmentPath>
        <BenchmarkConfig>C:/openvino-dl-benchmark/src/configs/benchmark_configuration.xml</BenchmarkConfig>
        <LogFile>program_log.txt</LogFile>
        <ResultFile>result_table.csv</ResultFile>
    </Computer>
</Computers>
```
