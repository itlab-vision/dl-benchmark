# Руководство для удаленного запуска массовых экспериментов

## Предисловие

Руководство содержит пример удаленного запуска тестов для получения
показателей производительности вывода глубоких нейросетевых моделей,
используя готовую инфраструктуру.

Примечание: фаза развертывания опущена, поскольку для OpenVINO 21.4 уже
все развернуто, также процесс развертывания должен измениться,
поскольку модели должны переехать в расшаренную директорию к наборам данных,
используемым компонентом оценки качества работы глубоких моделей (AccuracyChecker).

## Подготовка конфигурационного файла для бенчмаркинга

Для каждой машины следует создать свой конфигурационный файл для запуска
экспериментов по оценке производительности, поскольку на разных узлах
может быть разная аппаратная конфигурация (наличие/отсутствие GPU
и/или Movidius).

1. В текущей директории для хранения конфигурации запускаемых экспериментов
   создать набор директорий для хранения конфигурационных файлов
   для каждой отдельной машине. Например, `i3`, `i7` и `tower`.
1. Запустить ConfigMaker (GUI) и загрузить шаблонные конфигурации
   с данными по моделям и датасетам. Для этого необходимо выбрать пункт меню
   Data information -> Models/Data -> Load data -> Searching.

![ConfigMaker](./images/image1.png)

1. Сформировать конфигурации для бенчмаркинга и компонента оценки
   качества работы моделей (AccuracyChecker) для каждого отдельного узлах.
   Для этого необходимо выбрать пункт меню
   Creating Configuration -> Benchmark configuration.

![ConfigMaker](./images/image2.png)

   1. В качестве примера рассмотрим формирование конфигурации тестов
      производительности вывода для модели yolo-v2-ava-0001. Для этого необходимо
      выбрать пункт меню Add data.

![ConfigMaker](./images/image3.png)

      Согласно параметрам, указанным на скриншоте выше, будет сформировано
      4 теста производительности с следующими параметрами: размер пачки
      входных данных 1 и 8, режимы вывода OpenVINO - latency (sync)
      и throughput (async). После нажатия на кнопку ОК появится строка конфигурации.

![ConfigMaker](./images/image4.png)

1. Сохранить файлы конфигурации в директорию, соответствующую текущему узлу.

![ConfigMaker](./images/image5.png)


## Подготовка конфигурационного файла для удаленного запуска экспериментов

1. Запустить ConfigMaker.

1. Выбрать пункт меню Creating Configuration -> Remote configuration.

1. Для каждого вычислительного узла заполнить перечисленную информацию.
![ConfigMaker](./images/image6.png)

1. Сохранить конфигурационный файл для удаленного запуска экспериментов
   в текущую директорию со всеми файлами конфигурации, нажав кнопку `OK`.

![ConfigMaker](./images/image6.png)


## Запуск экспериментов

1. Скопировать набор конфигурационных файлов на FTP-сервер. Если на вашей
   рабочей машине установлена ОС Windows, то для этого можно воспользоваться
   утилитой WinSCP

![WinSCP](./images/images7.png)

1. Подключиться из консоли к FTP-серверу. Если на вашей
   рабочей машине установлена ОС Windows, то для этого можно воспользоваться
   утилитой x2go.
   
![X2GO](./images/images8.png)

1. Открыть терминал.

1. Перейти в директорию `/home/itmm/ftp` и ввести команду для удаленного
   запуска экспериментов. Указанная команда скопирует конфигурационные
   файлы на удаленные вычислительные узлы, запустит эксперименты и соберет
   результаты в единый файл на FTP-сервере.

```bash
python3 <путь до исходных кодов>/dl-benchmark/src/remote_control/remote_start.py \
        -c <путь до созданного файла конфигурации>/config.xml \
        -s <IP-адрес FTP-сервера> \
        -l <логин к FTP-серверу> \
        -p <пароль к FTP-серверу> \
        -br <название csv-файла для сохранения результатов производительности> \
        -acr <название csv-файла для сохранения результатов качества> \
        --ftp_dir <директория на FTP-сервере для сохранения результатов>
```

    Результат выполнения приведенной команды:

![RemoteStart](./images/images9.png)

    По окончании выполнения экспериментов должен появиться следующий вывод:

![RemoteStart](./images/images10.png)

    В `<директории на FTP-сервере для сохранения результатов>` должны появиться
    приведенные ниже файлы. Файлы, имеющие в качестве префикса в названии
    имя вычислительного узла,содержат результаты производительности и качества
    для каждой отдельной тестовой машины. Файлы `benchmark_results.csv`
    и `ac_results.csv` содержат объединенные таблицы результатов. Их можно
    перенести на свою машину и сконвертировать в формат HTML или XLSX
    с помощью имеющихся конвертеров (`csv2html` или `csv2xlsx` соответственно).
    Для этого можно использовать команды, приведенные ниже.

```bash
python3 <путь до исходных кодов>/dl-benchmark/src/csv2html/converter.py ...
```

```bash
python3 <путь до исходных кодов>/dl-benchmark/src/csv2xlsx/converter.py ...
```


## Примеры конфигурационных файлов

### Пример конфигурационного файла для оценки качества работы моделей

```xml
<?xml version="1.0" encoding="utf-8"?>
<Tests>
    <Test>
        <Model>
            <Task>object detection</Task>
            <Name>yolo-v2-tiny-ava-0001</Name>
            <Precision>FP32</Precision>
            <SourceFramework>OpenVINO DLDT</SourceFramework>
            <Directory>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-tiny-ava-0001/FP32</Directory>
        </Model>
        <Parameters>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <Device>CPU</Device>
            <Config>/home/itmm/sidorova/open_model_zoo/tools/accuracy_checker/configs/yolo-v2-ava-0001.yml</Config>
        </Parameters>
    </Test>
</Tests>

```

### Пример конфигурационного файла для оценки производительности

```xml
<?xml version="1.0" encoding="utf-8"?>
<Tests>
    <Test>
        <Model>
            <Task>object detection</Task>
            <Name>yolo-v2-ava-0001</Name>
            <Precision>FP32</Precision>
            <SourceFramework>OpenVINO DLDT</SourceFramework>
            <ModelPath>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-ava-0001/FP32/yolo-v2-ava-0001.xml</ModelPath>
            <WeightsPath>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-ava-0001/FP32/yolo-v2-ava-0001.bin</WeightsPath>
        </Model>
        <Dataset>
            <Name>PASCAL_VOC</Name>
            <Path>/tmp/itlab-vision-dl-benchmark-data/Datasets/PASCAL_VOC</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <BatchSize>1</BatchSize>
            <Device>CPU</Device>
            <IterationCount>100</IterationCount>
            <TestTimeLimit>180</TestTimeLimit>
        </FrameworkIndependent>
        <FrameworkDependent>
            <Mode>sync</Mode>
            <Extension></Extension>
            <AsyncRequestCount></AsyncRequestCount>
            <ThreadCount></ThreadCount>
            <StreamCount></StreamCount>
        </FrameworkDependent>
    </Test>
    <Test>
        <Model>
            <Task>object detection</Task>
            <Name>yolo-v2-ava-0001</Name>
            <Precision>FP32</Precision>
            <SourceFramework>OpenVINO DLDT</SourceFramework>
            <ModelPath>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-ava-0001/FP32/yolo-v2-ava-0001.xml</ModelPath>
            <WeightsPath>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-ava-0001/FP32/yolo-v2-ava-0001.bin</WeightsPath>
        </Model>
        <Dataset>
            <Name>PASCAL_VOC</Name>
            <Path>/tmp/itlab-vision-dl-benchmark-data/Datasets/PASCAL_VOC</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <BatchSize>1</BatchSize>
            <Device>CPU</Device>
            <IterationCount>100</IterationCount>
            <TestTimeLimit>180</TestTimeLimit>
        </FrameworkIndependent>
        <FrameworkDependent>
            <Mode>async</Mode>
            <Extension></Extension>
            <AsyncRequestCount></AsyncRequestCount>
            <ThreadCount></ThreadCount>
            <StreamCount></StreamCount>
        </FrameworkDependent>
    </Test>
    <Test>
        <Model>
            <Task>object detection</Task>
            <Name>yolo-v2-ava-0001</Name>
            <Precision>FP32</Precision>
            <SourceFramework>OpenVINO DLDT</SourceFramework>
            <ModelPath>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-ava-0001/FP32/yolo-v2-ava-0001.xml</ModelPath>
            <WeightsPath>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-ava-0001/FP32/yolo-v2-ava-0001.bin</WeightsPath>
        </Model>
        <Dataset>
            <Name>PASCAL_VOC</Name>
            <Path>/tmp/itlab-vision-dl-benchmark-data/Datasets/PASCAL_VOC</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <BatchSize>8</BatchSize>
            <Device>CPU</Device>
            <IterationCount>100</IterationCount>
            <TestTimeLimit>180</TestTimeLimit>
        </FrameworkIndependent>
        <FrameworkDependent>
            <Mode>sync</Mode>
            <Extension></Extension>
            <AsyncRequestCount></AsyncRequestCount>
            <ThreadCount></ThreadCount>
            <StreamCount></StreamCount>
        </FrameworkDependent>
    </Test>
    <Test>
        <Model>
            <Task>object detection</Task>
            <Name>yolo-v2-ava-0001</Name>
            <Precision>FP32</Precision>
            <SourceFramework>OpenVINO DLDT</SourceFramework>
            <ModelPath>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-ava-0001/FP32/yolo-v2-ava-0001.xml</ModelPath>
            <WeightsPath>/opt/intel/openvino_2021.4.689/deployment_tools/open_model_zoo/tools/downloader/intel/yolo-v2-ava-0001/FP32/yolo-v2-ava-0001.bin</WeightsPath>
        </Model>
        <Dataset>
            <Name>PASCAL_VOC</Name>
            <Path>/tmp/itlab-vision-dl-benchmark-data/Datasets/PASCAL_VOC</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <BatchSize>8</BatchSize>
            <Device>CPU</Device>
            <IterationCount>100</IterationCount>
            <TestTimeLimit>180</TestTimeLimit>
        </FrameworkIndependent>
        <FrameworkDependent>
            <Mode>async</Mode>
            <Extension></Extension>
            <AsyncRequestCount></AsyncRequestCount>
            <ThreadCount></ThreadCount>
            <StreamCount></StreamCount>
        </FrameworkDependent>
    </Test>
</Tests>

```

### Пример конфигурационного файла для удаленного запуска экспериментов

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Computers>
    <Computer>
        <IP>10.0.16.18</IP>
        <Login>itmm</Login>
        <Password>itmm</Password>
        <OS>Linux</OS>
        <FTPClientPath>/home/itmm/sidorova/dl-benchmark/src/remote_control/ftp_client.py</FTPClientPath>
        <Benchmark>
            <Config>/home/itmm/ftp/benchmark_configs/example/i3/benchmark_config.xml</Config>
            <Executor>docker_container</Executor>
            <LogFile>/home/itmm/sidorova/dl-benchmark/src/remote_control/log_bench.txt</LogFile>
            <ResultFile>/home/itmm/sidorova/dl-benchmark/src/remote_control/result_bench_table.csv</ResultFile>
        </Benchmark>
        <AccuracyChecker>
            <Config>/home/itmm/ftp/benchmark_configs/example/i3/accuracy_checker_config.xml</Config>
            <Executor>docker_container</Executor>
            <DatasetPath>/mnt/datasets/</DatasetPath>
            <DefinitionPath>/home/itmm/sidorova/open_model_zoo/tools/accuracy_checker/dataset_definitions.yml</DefinitionPath>
            <LogFile>/home/itmm/sidorova/dl-benchmark/src/remote_control/log_ac.txt</LogFile>
            <ResultFile>/home/itmm/sidorova/dl-benchmark/src/remote_control/result_ac_table.csv</ResultFile>
        </AccuracyChecker>
    </Computer>
    <Computer>
        <IP>10.0.16.52</IP>
        <Login>itmm</Login>
        <Password>itmm</Password>
        <OS>Linux</OS>
        <FTPClientPath>/home/itmm/sidorova/dl-benchmark/src/remote_control/ftp_client.py</FTPClientPath>
        <Benchmark>
            <Config>/home/itmm/ftp/benchmark_configs/example/i7/benchmark_config.xml</Config>
            <Executor>docker_container</Executor>
            <LogFile>/home/itmm/sidorova/dl-benchmark/src/remote_control/log_bench.txt</LogFile>
            <ResultFile>/home/itmm/sidorova/dl-benchmark/src/remote_control/result_bench_table.csv</ResultFile>
        </Benchmark>
        <AccuracyChecker>
            <Config>/home/itmm/ftp/benchmark_configs/example/i7/accuracy_checker_config.xml</Config>
            <Executor>docker_container</Executor>
            <DatasetPath>/mnt/datasets/</DatasetPath>
            <DefinitionPath>/home/itmm/sidorova/open_model_zoo/tools/accuracy_checker/dataset_definitions.yml</DefinitionPath>
            <LogFile>/home/itmm/sidorova/dl-benchmark/src/remote_control/log_ac.txt</LogFile>
            <ResultFile>/home/itmm/sidorova/dl-benchmark/src/remote_control/result_ac_table.csv</ResultFile>
        </AccuracyChecker>
    </Computer>
</Computers>

```