# Конвертер моделей из формата ONNX в MXNet

## Установка пакета

```bash
conda create --name onnx2mxnet-3.9.13 python=3.9.13 --yes
conda activate onnx2mxnet-3.9.13
pip install --upgrade pip setuptools wheel
pip install -r ./requirements.txt
conda deactivate
```

## Запуск скрипта конвертации

**Название скрипта:**

```bash
convert_onnx_to_mxnet.py
```

**Обязательные аргументы:**

- `-m / --model` – путь до описания обученной модели, которое хранится в файле расширением `.onnx`.

**Опциональные аргументы:**

- `-mn / --model_name` – название модели для сохранения. (по умолчанию `model`)
- `-p / --path_save_model` – путь для сохранения файлов модели. В процессе сохранения внутри указанной директории
  создается вложенная директория с названием модели `<model_name>`. Формируется два файла:
    - `<model_name>-0000.params` - бинарный файл с обученными параметрами модели
    - `<model_name>-symbol.json` - архитектура модели

  (По умолчанию модель сохраняется в текущей директории)

**Пример запуска**

```bash
python3 convert_onnx_to_mxnet.py \
  --model ./vgg16.onnx \
  --model_name vgg16 \
  --path_save_model ./vgg16
```

## Валидация моделей

### Тестовое изображение 1

<img width="150" src="../../../results/validation/images/ILSVRC2012_val_00000023.JPEG" alt="Granny Smith"/>

| Model | ONNX | MXNet |
|-------|------|-------|

### Тестовое изображение 2

<img width="150" src="../../../results/validation/images/ILSVRC2012_val_00000247.JPEG" alt="junco, snowbird"/>

| Model | ONNX | MXNet |
|-------|------|-------|

### Тестовое изображение 3

<img width="150" src="../../../results/validation/images/ILSVRC2012_val_00018592.JPEG" alt="liner, ocean liner"/>

| Model | ONNX | MXNet |
|-------|------|-------|
