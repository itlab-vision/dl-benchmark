# Установка конвертера

Командная строка:

```bash
pip install -U tf2onnx
```
## Валидация моделей

### Тестовое изображение 1

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000023.JPEG"></img>

|Model|TensorFlow|ONNX|
|-|-|-|
|resnet50|0.9553036 Granny Smith<br/>0.0052123 lemon<br/>0.0047185 piggy bank, penny bank<br/>0.0045875 orange<br/>0.0044233 necklace|0.9553036 Granny Smith<br/>0.0052123 lemon<br/>0.0047185 piggy bank, penny bank<br/>0.0045875 orange<br/>0.0044233 necklace|
|mobilenet_v2|0.8931149 Granny Smith<br/>0.0335340 piggy bank, penny bank<br/>0.0027360 saltshaker, salt shaker<br/>0.0021255 vase<br/>0.0016607 pitcher, ewer|0.8931142 Granny Smith<br/>0.0335344 piggy bank, penny bank<br/>0.0027360 saltshaker, salt shaker<br/>0.0021255 vase<br/>0.0016607 pitcher, ewer|

### Тестовое изображение 2

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00000247.JPEG"></img>

|Model|TensorFlow|ONNX|
|-|-|-|
|resnet50|0.9983400 junco, snowbird<br/>0.0004680 brambling, Fringilla montifringilla<br/>0.0003848 chickadee<br/>0.0003656 water ouzel, dipper<br/>0.0003383 goldfinch, Carduelis carduelis|0.9983401 junco, snowbird<br/>0.0004680 brambling, Fringilla montifringilla<br/>0.0003848 chickadee<br/>0.0003656 water ouzel, dipper<br/>0.0003383 goldfinch, Carduelis carduelis|
|mobilenet_v2|0.8770279 junco, snowbird<br/>0.0143870 water ouzel, dipper<br/>0.0103317 chickadee<br/>0.0063064 brambling, Fringilla montifringilla<br/>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|0.8770282 junco, snowbird<br/>0.0143869 water ouzel, dipper<br/>0.0103318 chickadee<br/>0.0063063 brambling, Fringilla montifringilla<br/>0.0013868 red-backed sandpiper, dunlin, Erolia alpina|


### Тестовое изображение 3

<img width="150" src="..\..\..\results\validation\images\ILSVRC2012_val_00018592.JPEG"></img>

|Model|TensorFlow|ONNX|
|-|-|-|
|resnet50|0.2357710 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1480761 liner, ocean liner<br/>0.1104689 container ship, containership, container vessel<br/>0.1095407 drilling platform, offshore rig<br/>0.0915569 beacon, lighthouse, beacon light, pharos|0.2357716 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.1480758 liner, ocean liner<br/>8.9234753 drilling platform, offshore rig<br/>0.1104690 container ship, containership, container vessel<br/>0.1095406 drilling platform, offshore rig<br/>0.0915569 beacon, lighthouse, beacon light, pharos|
|mobilenet_v2|0.1885895 beacon, lighthouse, beacon light, pharos<br/>0.1434041 liner, ocean liner<br/>0.0768167 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0497301 drilling platform, offshore rig<br/>0.0225758 container ship, containership, container vessel|0.1885887 beacon, lighthouse, beacon light, pharos<br/>0.1434043 liner, ocean liner<br/>0.0768168 breakwater, groin, groyne, mole, bulwark, seawall, jetty<br/>0.0497301 drilling platform, offshore rig<br/>0.0225758 container ship, containership, container vessel|
