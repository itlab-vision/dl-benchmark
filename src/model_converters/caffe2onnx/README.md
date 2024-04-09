# Конвертер моделей из формата Caffe в ONNX

## Установка репозитория с конвертером

Командная строка:

```bash
git clone https://github.com/asiryan/caffe2onnx
```

## Запуск скрипта конвертации

Название скрипта:

```bash
convert_caffe_to_onnx.py
```

**Аргументы:**

- `-pt / --prototxt` - путь до файла .prototxt.
- `-w / --weights` - путь до файла с весами в формате .caffemodel.
- `-od / --output_dir` - путь для сохранения конвертированной модели. 


**Пример запуска для alexnet**

```bash
python convert_caffe_to_onnx.py -pt ../public/alexnet/alexnet.prototxt \
                                -w ../public/alexnet/alexnet.caffemodel \
                                -od ./converted_models
```

## Результаты валидация моделей из OpenVINO - Open Model Zoo
