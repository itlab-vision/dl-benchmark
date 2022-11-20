# Руководство по запуску системы


## Введение
Данное руководство предлагает ознакомиться с этапами запуска системы бенчмаркинга
на удаленных узлах в Docker-контейнерах. В примере используется OpenVINO 2022.1. Заметим, что
данная инструкция также подходит и для остальных поддерживаемых фреймворков.


## Развертывание системы
Раздел расскажет, как развернуть систему DLI на удаленных узлах с помощью
модуля удаленного развертывания системы.
Если система уже развернута, данный этап можно пропустить.
Для начала необходимо подготовить Docker-образ системы, который
будет удаленно развернут на необходимых инфраструктурах. Для этого переходим
в директорию с Docker-файлами и собираем необходимый образ, используя инструкцию, которая
находится в соответствующей директории [docker][docker]. После чего сохраняем образ в архив, который
будет скопирован на необходимые удаленные узлы.

```bash
   docker build -t openvino:2022.1
   docker save openvino:2022.1 > openvino_2022.1.tar
```

Теперь подготовим удаленные узлы, на которых будут запущены массовые эксперименты.
Для удобства пусть на каждой машине будет создана директория `/home/itmm/validation`, в которой будут храниться
все необходимые файлы для работы. А именно репозиторий системы [DLI][dli], репозиторий [OpenModelZoo][omz] и файлы
с результатами экспериментов. Кроме того, необходимо заранее на удаленных машинах примаунтить шаренные директории
с моделями и наборами данных. Это можно сделать с помощью следующей команды:

```bash
   sudo mount -t cifs -o username=itmm,password=itmm //10.0.16.43/linuxshare /mnt
```

После чего, по адресу `/mnt` появятся новые директории: `/mnt/models/` - директория с моделями и
`/mnt/datasets` - директория с наборами данных для запуска модуля оценки качества работы моделей.

Рассмотрим конфигурационный файл для модуля удаленного развертывания системы. Пусть в нашем пуле имеется три машины.
Пример заполненного конфигурационного файла представлен ниже.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Computers>
    <Computer>
        <IP>10.0.16.31</IP>
        <Login>itmm</Login>
        <Password>itmm</Password>
        <OS>Linux</OS>
        <DownloadFolder>/home/itmm/validation</DownloadFolder>
        <DatasetFolder>/mnt/datasets</DatasetFolder>
        <ModelFolder>/mnt/models</ModelFolder>
    </Computer>
    <Computer>
        <IP>10.0.16.76</IP>
        <Login>itmm</Login>
        <Password>itmm</Password>
        <OS>Linux</OS>
        <DownloadFolder>/home/itmm/validation</DownloadFolder>
        <DatasetFolder>/mnt/datasets</DatasetFolder>
        <ModelFolder>/mnt/models</ModelFolder>
    </Computer>
    <Computer>
        <IP>10.0.16.21</IP>
        <Login>itmm</Login>
        <Password>itmm</Password>
        <OS>Linux</OS>
        <DownloadFolder>/home/itmm/validation</DownloadFolder>
        <DatasetFolder>/mnt/datasets</DatasetFolder>
        <ModelFolder>/mnt/models</ModelFolder>
    </Computer>
</Computers>
```

Запустим модуль автоматического развертывания системы, используя [руководство][config].

```bash
python3 deploy.py -s 10.0.16.125 -l itmm -p itmm \
                  -i ~/dl-benchmark/docker/OpenVINO_DLDT/openvino_22.1.tar \
                  -d /home/itmm/ftp \
                  -n OpenVINO_DLDT \
                  --machine_list ~/deploy_config.xml \
                  --project_folder /home/itmm/validation/dl-benchmark
```

Скрипт копирует архив с Docker-образом на FTP-сервер, после чего FTP-сервер копирует его на все удаленные узлы,
описанные в соответствующем конфигурационном файле, а после развертывает их.

Таким образом, система развернута на необходимых удаленных узлах.


## Подготовка конфигурационного файла для модуля оценки производительности глубоких моделей
Для каждого узла можно создать свой конфигурационный файл для запуска экспериментов производительности.
Это удобно, когда на одном из них, например, нет GPU (Xeon), и соответственно на такой машине есть смысл запускать
эксперименты только на CPU. Создадим конфигурационные файлы, используя [руководство][config]. Для примера запустим
эксперимент для классической модели `alexnet` в latency-режиме на всех трех машинах.

```xml
<?xml version="1.0" encoding="utf-8"?>
<Tests>
    <Test>
        <Model>
            <Task>classification</Task>
            <Name>alexnet</Name>
            <Precision>FP32</Precision>
            <SourceFramework>Caffe</SourceFramework>
            <ModelPath>/mnt/models/public/alexnet/FP32/alexnet.xml</ModelPath>
            <WeightsPath>/mnt/models/public/alexnet/FP32/alexnet.bin</WeightsPath>
        </Model>
        <Dataset>
            <Name>ImageNET</Name>
            <Path>/tmp/itlab-vision-dl-benchmark-data/Datasets/ImageNET/</Path>
        </Dataset>
        <FrameworkIndependent>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <BatchSize>1</BatchSize>
            <Device>CPU</Device>
            <IterationCount>1000</IterationCount>
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
</Tests>
```

Заметим, что пути прописываем относительно работы внутри Docker-контейнера. Сам конфигурационный файл мы сохраняем
и копируем на FTP-сервер, который в свою очередь потом их перенесет на соответствующие удаленные машины. Пусть в нашем примере
на FTP-сервере мы сохраняем файлы по адресу `/home/itmm/ftp/remote`.


## Подготовка конфигурационного файла для модуля проверки качества работы глубоких моделей
Аналогично создаем конфигурационные файлы для модуля проверки качества работы глубоких моделей.
В качестве примера возьмем ту же модель `alexnet`, что и для системы бенчмаркинга.

```xml
<?xml version="1.0" encoding="utf-8"?>
<Tests>
    <Test>
        <Model>
            <Task>classification</Task>
            <Name>alexnet</Name>
            <Precision>FP32</Precision>
            <SourceFramework>Caffe</SourceFramework>
            <Directory>/mnt/models/public/alexnet/FP32</Directory>
        </Model>
        <Parameters>
            <InferenceFramework>OpenVINO DLDT</InferenceFramework>
            <Device>CPU</Device>
            <Config>/tmp/open_model_zoo/tools/accuracy_checker/configs/alexnet.yml</Config>
        </Parameters>
    </Test>
</Tests>
```

Конфигурационный файл мы сохраняем и копируем на FTP-сервер, который в свою очередь
потом их перенесет на соответствующие удаленные машины. Пусть в нашем примере
на FTP-сервере мы сохраняем файлы по адресу `/home/itmm/ftp/remote`.


## Удаленный запуск экспериментов
Для начала подготовим конфигурационный файл для модуля удаленного запуска
экспериментов, используя [руководство][config].

```xml
<?xml version="1.0" encoding="utf-8" ?>
<Computers>
    <Computer>
        <IP>10.0.16.31</IP>
        <Login>itmm</Login>
        <Password>itmm</Password>
        <OS>Linux</OS>
        <FTPClientPath>/home/itmm/validation/dl-benchmark/src/remote_control/ftp_client.py</FTPClientPath>
        <Benchmark>
            <Config>/home/itmm/ftp/remote/i3/benchmark_config.xml</Config>
            <Executor>docker_container</Executor>
            <LogFile>/home/itmm/validation/log_bench.txt</LogFile>
            <ResultFile>/home/itmm/validation/result_bench_table.csv</ResultFile>
        </Benchmark>
        <AccuracyChecker>
            <Config>/home/itmm/ftp/remote/i3/ac_config.xml</Config>
            <Executor>docker_container</Executor>
            <DatasetPath>/mnt/datasets/</DatasetPath>
            <DefinitionPath>/home/itmm/validation/open_model_zoo/tools/accuracy_checker/dataset_definitions.yml</DefinitionPath>
            <LogFile>/home/itmm/validation/log_ac.txt</LogFile>
            <ResultFile>/home/itmm/validation/result_ac_table.csv</ResultFile>
        </AccuracyChecker>
    </Computer>
    <Computer>
        <IP>10.0.16.76</IP>
        <Login>itmm</Login>
        <Password>itmm</Password>
        <OS>Linux</OS>
        <FTPClientPath>/home/itmm/validation/dl-benchmark/src/remote_control/ftp_client.py</FTPClientPath>
        <Benchmark>
            <Config>/home/itmm/ftp/remote/i7/benchmark_config.xml</Config>
            <Executor>docker_container</Executor>
            <LogFile>/home/itmm/validation/log_bench.txt</LogFile>
            <ResultFile>/home/itmm/validation/result_bench_table.csv</ResultFile>
        </Benchmark>
        <AccuracyChecker>
            <Config>/home/itmm/ftp/remote/i7/ac_config.xml</Config>
            <Executor>docker_container</Executor>
            <DatasetPath>/mnt/datasets/</DatasetPath>
            <DefinitionPath>/home/itmm/validation/open_model_zoo/tools/accuracy_checker/dataset_definitions.yml</DefinitionPath>
            <LogFile>/home/itmm/validation/log_ac.txt</LogFile>
            <ResultFile>/home/itmm/validation/result_ac_table.csv</ResultFile>
        </AccuracyChecker>
    </Computer>
        <Computer>
        <IP>10.0.16.21</IP>
        <Login>itmm</Login>
        <Password>itmm</Password>
        <OS>Linux</OS>
        <FTPClientPath>/home/itmm/validation/dl-benchmark/src/remote_control/ftp_client.py</FTPClientPath>
        <Benchmark>
            <Config>/home/itmm/ftp/remote/tower/benchmark_config.xml</Config>
            <Executor>docker_container</Executor>
            <LogFile>/home/itmm/validation/log_bench.txt</LogFile>
            <ResultFile>/home/itmm/validation/result_bench_table.csv</ResultFile>
        </Benchmark>
        <AccuracyChecker>
            <Config>/home/itmm/ftp/remote/tower/ac_config.xml</Config>
            <Executor>docker_container</Executor>
            <DatasetPath>/mnt/datasets/</DatasetPath>
            <DefinitionPath>/home/itmm/validation/open_model_zoo/tools/accuracy_checker/dataset_definitions.yml</DefinitionPath>
            <LogFile>/home/itmm/validation/log_ac.txt</LogFile>
            <ResultFile>/home/itmm/validation/result_ac_table.csv</ResultFile>
        </AccuracyChecker>
    </Computer>
</Computers>
```

Теперь удаленно запустим эксперименты. Для этого советую воспользоваться инструментов `screen` для Linux,
который позволяет создавать фоновые процессы, что позволит нам запустить скрипт удаленного запуска экспериментов, а после
выключить терминал. Поскольку массовые эксперименты длятся несколько суток, а держать терминал открытым все это время мы не можем.
Создадим сначала новую screen-сессию.

```bash
screen -S validation
```

У нас создатся новое окно `validation`, в котором мы уже можем смело работать.
Теперь для запуска нам необходимо прописать следующую команду на FTP-сервере:

```bash
 python3 remote_start.py -c ~/ftp/remote/config.xml \
                         -s 10.0.16.125 -l itmm -p itmm \
                         -br benchmark_results.csv \
                         -acr ac_results.csv \
                         --ftp_dir /home/itmm/ftp/results
```

Таким образом, скрипт пройдется по всем описанным машинам из конфигурационного файла `~/ftp/remote/config.xml`,
скопирует соответствующие конфигурационные файлы с описанием экспериментов и запустит их.
Для перехода из данной сессии необходимо нажать следующие клавиши: `CTRL + A + D`. Чтобы вернуться к нашей сессии
с запуском экспериментов и узнать статус, необходимо прописать следующую команду:

```bash
screen -R validation
```

## Результат работы системы
По окончании работы в screen-сессии `validation` мы увидим следующие строки:

```bash
[ INFO ] Ended process on Linux with id 0
[ INFO ] Ended process on Linux with id 0
[ INFO ] Ended process on Linux with id 0
```

Что означает завершение экспериментов. Таким образом, на FTP-сервере в директории `/home/itmm/ftp/results`
будут храниться csv-таблицы с результатами экспериментов оценки производительности глубоких моделей и проверки
качества их работы с каждого удаленного узла, а также обобщенные таблицы `benchmark_results.csv` и `ac_results.csv`.
Данные файлы можно скачать себе на локальную машину и уже сконвертировать в HTML  и XSLX форматы.



<!-- LINKS -->
[docker]: docker/README.md
[dli]: https://github.com/itlab-vision/dl-benchmark
[omz]: https://github.com/openvinotoolkit/open_model_zoo/
[config]: src/configs/README.md
