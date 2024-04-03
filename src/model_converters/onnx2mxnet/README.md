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

|Model|Opset version|ONNX|MXNet|
|-|-|-|-|
|AlexNet|7|0.0130791 vase <br/>0.0113130 candle, taper, wax light <br/>0.0094803 lotion <br/>0.0092394 piggy bank, penny bank <br/>0.0088509 pitcher, ewer|0.0010122 vase <br/>0.0010104 candle, taper, wax light <br/>0.0010085 lotion <br/>0.0010083 piggy bank, penny bank <br/>0.0010079 pitcher, ewer|
|VGG 16|7|14.2978382 Granny Smith <br/>10.1649094 piggy bank, penny bank <br/>10.0847054 dumbbell <br/>9.7713060 maraca <br/>9.7364922 tennis ball|0.9017522 Granny Smith <br/>0.0144603 piggy bank, penny bank <br/>0.0133458 dumbbell <br/>0.0097552 maraca <br/>0.0094215 tennis ball|
|VGG 19|7|9.5931635 Granny Smith <br/>7.2290239 piggy bank, penny bank <br/>7.1850996 saltshaker, salt shaker <br/>6.7277513 dumbbell <br/>6.7231359 pencil sharpener|0.4857184 Granny Smith <br/>0.0456722 piggy bank, penny bank <br/>0.0437094 saltshaker, salt shaker <br/>0.0276663 dumbbell <br/>0.0275389 pencil sharpener|

### Тестовое изображение 2

<img width="150" src="../../../results/validation/images/ILSVRC2012_val_00000247.JPEG" alt="junco, snowbird"/>

|Model|Opset version|ONNX|MXNet|
|-|-|-|-|
|AlexNet|7|0.0075100 shower curtain <br/>0.0060643 mosquito net <br/>0.0054148 dtingray <br/>0.0053229 oxygen mask <br/>0.0051818 plastic bag|0.0010065 shower curtain <br/>0.0010051 mosquito net <br/>0.0010044 dtingray <br/>0.0010043 oxygen mask <br/>0.0010042 plastic bag||
|VGG 16|7|30.0659161 junco, snowbird <br/>24.4124374 chickadee <br/>24.2297859 brambling, Fringilla montifringilla <br/>20.3612823 goldfinch, Carduelis carduelis <br/>19.7643280 water ouzel, dipper|0.9934963 junco, snowbird <br/>0.0034825 chickadee <br/>0.0029011 brambling, Fringilla montifringilla <br/>0.0000606 goldfinch, Carduelis carduelis <br/>0.0000334 water ouzel, dipper|
|VGG 19|7|27.8706684 junco, snowbird <br/>22.1559544 chickadee <br/>20.9320812 water ouzel, dipper <br/>20.1566486 brambling, Fringilla montifringilla <br/>16.6844444 house finch, linnet, Carpodacus mexicanus|0.9952694 junco, snowbird <br/>0.0032815 chickadee <br/>0.0009651 water ouzel, dipper <br/>0.0004444 brambling, Fringilla montifringilla <br/>0.0000138 house finch, linnet, Carpodacus mexicanus|

### Тестовое изображение 3

<img width="150" src="../../../results/validation/images/ILSVRC2012_val_00018592.JPEG" alt="liner, ocean liner"/>

|Model|Opset version|ONNX|MXNet|
|-|-|-|-|
|AlexNet|7|0.0075198 snowplow, snowplough <br/>0.0066294 wreck <br/>0.0061572 beaker <br/>0.0059997 mosquito net <br/>0.0046403 submarine, pigboat, sub, U-boat|0.0010065 snowplow, snowplough <br/>0.0010056 wreck <br/>0.0010052 beaker <br/>0.0010050 mosquito net <br/>0.0010036 submarine, pigboat, sub, U-boat|
|VGG 16|7|12.9318199 container ship, containership, container vessel <br/>11.5314579 liner, ocean liner <br/>11.3399763 fireboat <br/>10.8501625 breakwater, groin, groyne, mole, bulwark, seawall, jetty <br/>10.4625912 lifeboat|0.5196506 container ship, containership, container vessel <br/>0.1280980 liner, ocean liner <br/>0.1057751 fireboat <br/>0.0648128 breakwater, groin, groyne, mole, bulwark, seawall, jetty <br/>0.0439886 lifeboat|
|VGG 19|7|12.8443079 container ship, containership, container vessel <br/>12.2016411 drilling platform, offshore rig <br/>11.3992987 breakwater, groin, groyne, mole, bulwark, seawall, jetty <br/>11.3968639 liner, ocean liner <br/>10.8498840 fireboat|0.4066454 container ship, containership, container vessel <br/>0.2138496 drilling platform, offshore rig <br/>0.0958640 breakwater, groin, groyne, mole, bulwark, seawall, jetty <br/>0.0956311 liner, ocean liner <br/>0.0553411 fireboat|
