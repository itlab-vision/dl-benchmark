# Руководство по запуску системы

## Введение

Данное руководство содержит подробное описание процедуры запуска основного сценария работы системы бенчмаркинга DLI
на удаленных вычислительных узлах в Docker-контейнерах.
В примере для вывода глубоких моделей используется Intel Dstribution of OpenVINO toolkit 2022.1.
Отметим, что данная инструкция справедлива и для остальных поддерживаемых фреймворков.

## Развертывание системы

Настоящий раздел содержит пошаговое описание процедуры развертывания системы DLI на
удаленных вычислительных узлах с использованием модуля развертывания `deployment`, входящего в состав системы.
Если система уже развернута, данный этап можно пропустить.

Процедура развертывания предполагает выполнение следующих действий.

1. Подготовить Docker-образ системы, который будет удаленно развернут на вычислительных узлах.
Для этого необходимо перейти в директорию с Docker-файлами и собрать необходимый образ,
используя инструкцию, которая находится в соответствующей директории [docker][docker] и
указав все необходимые переменные `ARG` из соответствующего Docker-файла.
Сохранить образ в архив, который будет скопирован на необходимые удаленные узлы.

   ```bash
   docker build -t openvino:2022.1 --build-arg DATASET_DOWNLOAD_LINK=<path>
   docker save openvino:2022.1 > openvino_2022.1.tar
   ```

2. Подготовить удаленные вычислительные узлы для запуска массовых экспериментов.
Для удобства предположим, что на каждой машине с пользователем `itmm` создается директория `/home/itmm/validation`,
в которой содержатся все необходимые файлы для работы: репозиторий системы [DLI][dli] и репозиторий [OpenVINO™ Toolkit - Open Model Zoo][omz].
Помимо клонирования репозиториев в директории следует создать отдельную папку `results`,
в которой в будущем будут хранится файлы с результатами экспериментов.
Кроме того, необходимо заранее на удаленных машинах примонтировать расшаренные директории с моделями и наборами данных.
Это можно сделать с помощью следующих команд:

   ```bash
   cd ~
   mkdir validation && cd validation
   git clone https://github.com/itlab-vision/dl-benchmark.git
   git clone https://github.com/openvinotoolkit/open_model_zoo.git --recursive --branch 2022.1.0 --single-branch
   mkdir results
   sudo mount -t cifs -o username=itmm,password=itmm //10.0.16.43/linuxshare /mnt
   ```

   Далее считаем, что по адресу `/mnt` содержатся новые директории: `/mnt/models/` - директория с моделями и  `/mnt/datasets` - директория с наборами данных для запуска модуля оценки качества работы моделей.

3. Подготовить конфигурационный файл для модуля удаленного развертывания системы.
В текущем эксперименте предполагается наличие трех вычислительных узлов.
Для каждого узла имеется IP-адрес (тег `IP`), логин и пароль для доступа к узлу (теги `Login` и `Password`), ОС (тег `OS`),
название рабочей директории с исходными кодами системы бенчмаркинга DLI (тег `DownloadFolder`) и
пути до расшаренных директорий с тестовыми наборами данных и моделями (теги `DatasetFolder` и `ModelFolder`).
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

4. Запустить модуль автоматического развертывания системы, используя [руководство][config].

   ```bash
   python3 deploy.py -s 10.0.16.125 -l itmm -p itmm \
                     -i ~/dl-benchmark/docker/OpenVINO_DLDT/openvino_22.1.tar \
                     -d /home/itmm/ftp \
                     -n OpenVINO_DLDT \
                     --machine_list ~/deploy_config.xml \
                     --project_folder /home/itmm/validation/dl-benchmark
   ```

   Скрипт копирует архив с Docker-образом на FTP-сервер (в данном примере IP-адрес FTP-сервера - 10.0.16.125,
   после чего уже с FTP-сервера скрипт копирует его на все удаленные узлы,
   описанные в соответствующем конфигурационном файле, а после развертывает их.

## Подготовка конфигурационного файла для модуля оценки производительности глубоких моделей

Для каждого узла можно создать свой конфигурационный файл для запуска экспериментов производительности.
Это удобно, когда на одном из них, например, нет GPU (Xeon), и соответственно на такой машине есть смысл запускать
эксперименты только на CPU. Создадим конфигурационные файлы, используя [руководство][config]. Для примера запустим
эксперимент для классической модели `alexnet` в latency-режиме на всех трех машинах.
Отметим, что для валидации производительности моделей используется отдельный закрытый репозиторий с данными `itlab-vision-dl-benchmark-data`,
клонирование которого происходит в процессе развертывания Docker-образов в директорию `/tmp`.

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

Заметим, что в конфигурационных файлах пути прописываются относительно Docker-контейнера.
Конфигурационные файлы предварительно копируются на FTP-сервер, в процессе развертывания системы скрипт
копируется конфигурации тестов на соответствующие удаленные машины.
Для определенности в примере на FTP-сервере конфигурационные файлы сохраняются по адресу `/home/itmm/ftp/remote`.

```bash
scp benchmark_config_i3.xml itmm@10.0.16.125:/home/itmm/ftp/remote
scp benchmark_config_i7.xml itmm@10.0.16.125:/home/itmm/ftp/remote
scp benchmark_config_tower.xml itmm@10.0.16.125:/home/itmm/ftp/remote
```

## Подготовка конфигурационного файла для модуля проверки качества работы глубоких моделей

Аналогично создаем конфигурационные файлы для модуля проверки качества работы глубоких моделей.
В качестве примера возьмем ту же модель `alexnet`, что и для системы бенчмаркинга. Заметим, что
путь до модели указывается относительно окружения Docker-контейнера, а путь до конфигурационного
файла для инструмента проверки качества модели описывается относительно хост-машины.

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
            <Config>/home/itmm/validation/open_model_zoo/tools/accuracy_checker/configs/alexnet.yml</Config>
        </Parameters>
    </Test>
</Tests>
```

Конфигурационный файл копируется на FTP-сервер, впоследствии скрипт развертывания перенесет
конфигурации тестов на соответствующие удаленные машины. Допустим, что в текущем примере
конфигурационные файлы на FTP-сервере сохраняются по адресу `/home/itmm/ftp/remote`.

```bash
scp accuracy_checker_config_i3.xml itmm@10.0.16.125:/home/itmm/ftp/remote
scp accuracy_checker_config_i7.xml itmm@10.0.16.125:/home/itmm/ftp/remote
scp accuracy_checker_config_tower.xml itmm@10.0.16.125:/home/itmm/ftp/remote
```

## Удаленный запуск экспериментов

Удаленный запуск экспериментов включает следующую последовательность действий.

1. Подготовить конфигурационный файл `config.xml` для модуля удаленного запуска экспериментов, используя [руководство][config],
и сохранить его на FTP-сервере по адресу `/home/itmm/ftp/remote/`.

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
               <Config>/home/itmm/ftp/remote/benchmark_config_i3.xml</Config>
               <Executor>docker_container</Executor>
               <LogFile>/home/itmm/validation/log_bench.txt</LogFile>
               <ResultFile>/home/itmm/validation/result_bench_table.csv</ResultFile>
           </Benchmark>
           <AccuracyChecker>
               <Config>/home/itmm/ftp/remote/accuracy_checker_config_i3.xml</Config>
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
               <Config>/home/itmm/ftp/remote/benchmark_config_i7.xml</Config>
               <Executor>docker_container</Executor>
               <LogFile>/home/itmm/validation/log_bench.txt</LogFile>
               <ResultFile>/home/itmm/validation/result_bench_table.csv</ResultFile>
           </Benchmark>
           <AccuracyChecker>
               <Config>/home/itmm/ftp/remote/accuracy_checker_config_i7.xml</Config>
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
               <Config>/home/itmm/ftp/remote/benchmark_config_tower.xml</Config>
               <Executor>docker_container</Executor>
               <LogFile>/home/itmm/validation/log_bench.txt</LogFile>
               <ResultFile>/home/itmm/validation/result_bench_table.csv</ResultFile>
           </Benchmark>
           <AccuracyChecker>
               <Config>/home/itmm/ftp/remote/accuracy_checker_config_tower.xml</Config>
               <Executor>docker_container</Executor>
               <DatasetPath>/mnt/datasets/</DatasetPath>
               <DefinitionPath>/home/itmm/validation/open_model_zoo/tools/accuracy_checker/dataset_definitions.yml</DefinitionPath>
               <LogFile>/home/itmm/validation/log_ac.txt</LogFile>
               <ResultFile>/home/itmm/validation/result_ac_table.csv</ResultFile>
           </AccuracyChecker>
       </Computer>
   </Computers>
   ```

2. Запустить эксперименты удаленно. Для этого необходимо воспользоваться утилитой `screen` для Linux, которая позволяет создавать фоновые процессы. В результате ее использования можно запустить скрипт с массовыми экспериментами, а после выключить терминал.

   ```bash
   screen -S validation
   ```

   В результате выполнения указанной команды создается новое окно `validation`, в котором можно выполнить удаленный запуск.
   Теперь для запуска необходимо прописать следующую команду на FTP-сервере:

   ```bash
    python3 remote_start.py -c /home/itmm/ftp/remote/config.xml \
                            -s 10.0.16.125 -l itmm -p itmm \
                            -br benchmark_results.csv \
                            -acr accuracy_checker_results.csv \
                            --ftp_dir /home/itmm/ftp/results
   ```

   Таким образом, скрипт пройдется по всем описанным машинам из конфигурационного файла `/home/itmm/ftp/remote/config.xml`,
   скопирует соответствующие конфигурационные файлы с описанием экспериментов и запустит их.
   Для перехода из данной сессии необходимо нажать следующие клавиши: `CTRL + A + D`. Чтобы вернуться к нашей сессии
   с запуском экспериментов и узнать статус, необходимо прописать следующую команду:
   
   ```bash
   screen -R validation
   ```

## Результат работы системы

По окончании работы в screen-сессии `validation` должны выводиться следующие строки:

```bash
[ INFO ] Ended process on Linux with id 0
[ INFO ] Ended process on Linux with id 0
[ INFO ] Ended process on Linux with id 0
```

По завершении экспериментов на FTP-сервере в директории `/home/itmm/ftp/results`
будут храниться csv-таблицы с результатами экспериментов оценки производительности глубоких моделей и
проверки качества их работы с каждого удаленного узла, а также обобщенные таблицы `benchmark_results.csv` и `accuracy_checker_results.csv`.
Данные файлы можно скачать на локальную машину и сконвертировать в HTML- и/или XSLX-формат, с помощью следующих команд.

```bash
scp itmm@10.0.16.125:/home/itmm/ftp/results/benchmark_results.csv /tmp
scp itmm@10.0.16.125:/home/itmm/ftp/results/accuracy_checker_results.csv /tmp

cd /tmp/dl-benchmark/src/csv2html
python3 converter.py -t /tmp/benchmark_results.csv -r /tmp/benchmark_results.html -k benchmark
python3 converter.py -t /tmp/accuracy_checker_results.csv -r /tmp/accuracy_checker_results.html -k accuracy_checker

cd /tmp/dl-benchmark/src/csv2xlsx
python3 converter.py -t /tmp/benchmark_results.csv -r /tmp/benchmark_results.xlsx -k benchmark
python3 converter.py -t /tmp/accuracy_checker_results.csv -r /tmp/accuracy_checker_results.xlsx -k accuracy_checker
```


<!-- LINKS -->
[docker]: docker/README.md
[dli]: https://github.com/itlab-vision/dl-benchmark
[omz]: https://github.com/openvinotoolkit/open_model_zoo/
[config]: src/configs/README.md
