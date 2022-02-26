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
