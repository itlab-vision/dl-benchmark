# Создание образа тестового вычислительного узла

## Установка и настройка Docker

1. Установить Docker.

   ```bash
   sudo apt install docker.io
   ```

1. Добавить пользователя в группу docker.

   ```bash
   sudo usermod -aG docker ${USER}
   ```

1. Перелогиниться, чтобы активировать изменения.

   ```bash
   su ${USER}
   ```

## Сборка образа и архивирование образа

1. Cобрать образ.

   ```bash
   docker build -t <image_name>
   ```

1. Cохранить образ в архив.

   ```bash
   docker save <image_name> > <image_name>.tar
   ```

## Загрузка заархивированного образа и его запуск

1. Загрузить образ в систему.

   ```bash
   docker load < <image_name>.tar
   ```

1. Запустить docker.

   ```bash
   docker run -it <image_name>
   ```

## Пример последовательности команд для сбора образа OpenVINO и запуска бенчмарка

   ```bash
   cd docker/OpenVINO_DLDT
   docker build -t dli_openvino:2022.2 .
   docker save dli_openvino:2022.2 > dli_openvino:2022.2.tar
   docker load < dli_openvino:2022.2.tar
   sudo docker run --privileged -it -d -v /dev:/dev \
      -v /tmp/:/media/models \
      -v /tmp/:/media/datasets \
      --name OpenVINO_DLDT \
      dli_openvino:2022.2
   cd ../../src/benchmark
   python3 inference_benchmark.py --executor_type docker_container \
      -c benchmark_config.xml -r results.csv 

   ```

   Скрипт `inference_benchmark.py` из конфигурации теста получает имя фреймворка \
   (`OpenVINO_DLDT`) и подключается к запущенному образу по данному имени, поэтому задание имени \
   образа `--name OpenVINO_DLDT` обязательно.
