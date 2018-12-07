# Тестирование глубоких моделей

## Тестирование глубоких моделей в синхронном режиме

```bash
inference_sync_mode.py [TBD]
```

Параметры запуска:
- [TBD]

## Тестирование глубоких моделей в асинхронном режиме

```bash
python inference_async_mode.py \
    -t classification -i <path_to_image>/image.png \
    -m <path_to_model>/model.xml -w <path_to_weights>/model.bin \
    -r 1 --labels <path_to_labels>/image_net_synset.txt

python inference_async_mode.py \
    -t detection -i <path_to_image>/image.png \
    -m <path_to_model>/model.xml -w <path_to_weights>/model.bin \
    -r 1 -d GPU

python inference_async_mode.py \
    -t segmentation -i <path_to_image>/image.png \
    -m <path_to_model>/model.xml -w <path_to_weights>/model.bin \
    -r 1 --color_map <path_to_color_map>/color_map.txt
```

Параметры запуска:
-    `-t / --model_type`   - Задача, которую собираемся решать.
-    `-i / --input`   - Путь до картинки или папки с картинками. 
                       Расширения картинок ".jpg", ".png", ".bmp" и т.д.
-    `-m / --model`   - Путь до модели.
-    `-w / --weights`   - Путь до весов модели.
-    `-r / --Request`   - Положительное целочисленное значение infer requests,
                          которые должны быть созданы. Возможные значения: 1 и 2.
-    `--labels`   - Путь до карты классов.
-    `-d / --device`   - Устройство, на котором будем производить работу.
-    `--color_map`   - Путь до карты цветов.