# Установка докера

1. `sudo apt install docker.io` - команда для установки docker
2. `sudo usermod -aG docker ${USER}` - добавить пользователя в группу docker
3. `su ${USER}` - перезайти, чтобы изменения вступили в силу.

# Сборка образа и архивирование образа

1. `docker build -t <image_name> .` - сборка образа
2. `docker save <image_name> > <image_name>.tar` - сохранение образа в архив

# Загрузка заархивированного образа и его запуск

1. `docker load < <image_name>.tar` - загрузка образа в систему
2. `docker run -it <image_name>` - запуск docker с активной консолью
