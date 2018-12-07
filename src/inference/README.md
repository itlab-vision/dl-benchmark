# Тестирование глубоких моделей

## Тестирование глубоких моделей в синхронном режиме

```bash
inference_sync_mode.py [TBD]
```

Параметры запуска:
- [TBD]

## Тестирование глубоких моделей в асинхронном режиме


### Задача классификации
```bash
python inference_async_mode.py \
    -t classification -i <path_to_image>/image.png \
    -m <path_to_model>/<model_name>.xml -w <path_to_weights>/<model_name>.bin \
    -r 1 --labels <path_to_labels>/image_net_synset.txt -ni 10
```

Результат выполнения: определяет номер (или наименование класса),
к которому относится объект на изображении.


### Задача детектирования
```bash
python inference_async_mode.py \
    -t detection -i <path_to_image>/image.png \
    -m <path_to_model>/<model_name>.xml -w <path_to_weights>/<model_name>.bin \
    -r 1 -d GPU -ni 10
```

Результат выполнения: определяет наличие объекта на изображении,
а также находит его положение в системе координат пикселей исходного
изображения, выделяя его в прямоугольник.


### Задача Семантическая сегментация
```bash
python inference_async_mode.py \
    -t segmentation -i <path_to_image>/image.png \
    -m <path_to_model>/<model_name>.xml -w <path_to_weights>/<model_name>.bin \
    -r 1 --color_map <path_to_color_map>/color_map.txt -ni 10
```

Результат выполнения: позволяет разделить объекты на классы по их структуре,
ничего не зная об этих объектах, то есть еще до их распознавания.


Параметры запуска:
-    `-t / --model_type`     - задача, которую собираемся решать.
-    `-i / --input`          - путь до картинки или папки с картинками. 
                               расширения картинок ".jpg", ".png", ".bmp" и т.д.
-    `-m / --model`          - путь до модели.
-    `-w / --weights`        - путь до весов модели.
-    `-r / --request`        - положительное целочисленное  число 
                               запросов на одновременную обработку. 
                               Возможные значения: 1 и 2.
-    `--labels`              - путь до карты классов.
-    `-d / --device`         - устройство, на котором будем производить работу.
-    `--color_map`           - путь до карты цветов.
-    `-ni / --number_iter`   - число итераций.