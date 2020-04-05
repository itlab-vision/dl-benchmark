# Установка докера

1. Установить docker.
 ```
 sudo apt install docker.io
 ```
2. Добавить пользователя в группу docker.
 ```
 sudo usermod -aG docker ${USER}
 ```
3. Перелогиниться, чтобы активировать изменения.
 ```
 su ${USER}
 ```

# Сборка образа и архивирование образа

1. Cобрать образ.
 ```
 docker build -t <image_name>
 ```
2. Cохранить образ в архив.
 ```
 docker save <image_name> > <image_name>.tar
 ```

# Загрузка заархивированного образа и его запуск

1. Загрузить образ в систему.
 ```
 docker load < <image_name>.tar
 ```
2. Запустить docker.
 ```
 docker run -it <image_name>
 ```
