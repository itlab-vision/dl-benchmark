# Шаблоны для файлов конфигурации

## Заполнение файла конфигурации для скрипта замера производительности

### Правила заполнения файла конфигурации для скрипта замера производительности

Общая информация:

- Файл конфигурации описывается в формате XML.
- Шаблон тегов находится в файле `benchmark_configuration_file_template.xml`.
- Порядок тегов важен и при изменении порядка тегов поведение скрипта не определено.
- Кодирование файла осуществляется в формате `utf-8`.
- Корневой тег `Tests`.
- Каждый тест описывается внутри тегов `Test`.
- Информация о модели описывается внутри тегов `Model`.
- Информация о выборке описывается внутри тегов `Dataset`.
- Информация о параметрах теста, независящих от фреймверка, описывается внутри тегов `FrameworkIndependent`.
- Информация о параметрах теста, зависящих от фреймверка, описывается внутри тегов `FrameworkDependent`.

Заполнение информации о модели:

- Все теги, пренадлежащие тегу `Model`, являются обязательными для заполнения.
- Название задачи, которую решает модель, описывается внутри тега `Task`.
- Имя модели описывается внутри тега `Name`.
- Тип данных весов описывется внутри тега `Precision`.
- Исходный фреймверк модели описывается внутри тега `SourceFramework`.
- Абсолютный путь до директории, где расположена модель, описывается внутри тега `Path`.

Заполнение информации о выборке:
- Все теги, пренадлежащие тегу `Dataset`, являются обязательными для заполнения.
- Имя выборки описывается внутри тега `Name`.
- Абсолютный путь до директории, где лежат данные из выборки, описывается внутри тега `Path`.

Заполнение информации о параметрах теста, не зависящих от фреймверка:

- Все теги, пренадлежащие тегу `FrameworkIndependent`, являются обязательными для заполнения.
- Имя фреймверка, производительность вывода которого будет измерятся, описывается внутри тега `InferenceFramework`.
- Размер пачки данных, обрабатываемых за один прямой проход сети, описывается внутри тега `BatchSize`.
- Устройство, на котором будет запущен вывод, описывается внутри тега `Device`.
- Количество итераций цикла тестирования описывается внутри тега `IterationCount`.
- Максимальное время выполнения теста в минутах описывается внутри тега `TestTimeLimit`.

Заполнение информации о параметрах теста, зависящих от фреймверка:

- Набор тегов для тестирования вывода OpenVINO:

  - `Mode` - Обязательный для заполнения. Описывает режим исполнения вывода. Допустимые значения `Sync` и `Async`. 
  - `Extension` - Необязательный для заполнения. Описывает абсолютный путь до реализации слоёв, неподдерживаемых OpenVINO.
  - `AsyncRequestCount` - Необязательный для заполнения. Может быть заполнен при асинхронном режиме вывода. Описывает количество запросов на одновременное исполнение вывода.
  - `ThreadCount` - Необязательный для заполнения. Описывает максимальное количество потоков для выполнения вывода.
  - `StreamCount` - Необязательный для заполнения. Может быть заполнен при асинхронном режиме вывода. Описывает максимальное количество одновременно выполняющихся запросов на вывод.

### Примеры заполнения файла конфигурации для скрипта замера производительности

#### Пример заполнения файла конфигурации для замера производительности вывода OpenVINO

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

### Правила заполнения файла конфигурации для скрипта удаленного запуска

- Файл конфигурации описывается в формате XML.
- Шаблон тегов находится в файле `remote_configuration_file_template.xml`.
- Кодирование файла осуществляется в формате `utf-8`.
- Корневой тег `Computers`.
- Каждый компьютер, на котором производится запуск бэнчмарка описывается 
  внутри тегов `Computer`.
- Первый параметр представляет собой IP-адрес компьютера, на котором планируется
  запуск. Параметр описывается внутри тегов `IP`.
- Второй параметр - Login - логин пользователя компьютера, на котором планируется
  запуск. Параметр описывается внутри тегов `Login`.
- Третий параметр - Password - пароль пользователя компьютера,
  на котором планируется запуск. Параметр описывается внутри тегов `Password`.
- Четвертый параметр - OS - операционная система, установленная на компьютер,
  на котором планируется запуск. Параметр описывается внутри тегов `OS`.
- Пятый параметр - путь до скрипта `ftp_client.py` в папке `remote_start`,
  на компьютер предварительно нужно склонировать наш репозиторий.
  Параметр описывается внутри тегов `FTPClientPath`.
- Шестой параметр - путь до файла, устанавливающего окружение OpenVINO.
  Параметр описывается внутри тегов `OpenVINOEnvironmentPath`.
- Седьмой параметр - путь до конфигурации бэнчмарка.
  Параметр описывается внутри тегов `BenchmarkConfig`.
- Восьмой параметр - имя файла, в который запишется лог работы программы.
  Параметр описывается внутри тегов `LogFile`.
- Седьмой параметр - имя таблицы, в которую
  записывается результат работы программы.
  Параметр описывается внутри тегов `ResultFile`.

### Пример заполнения файла конфигурации для скрипта удаленного запуска

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
