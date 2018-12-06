# Результаты проверки корректности вывода с использованием разных режимов

## Результаты классификации

### Тестовое изображение 1

Источник: набор данных [ImageNet][imagenet]

Разрешение: 709 x 510
﻿

<img src="..\data\ILSVRC2012_val_00000023.JPEG" width="150">


   Название модели   |            C++ (синхронный режим)              |            C++ (асинхронный режим)              |             Python (синхронный режим)             |             Python (асинхронный режим)             |
---------------------|------------------------------------------------|-------------------------------------------------|---------------------------------------------------|----------------------------------------------------|
alexnet              |![](/res/с++/sync/img_1/alexnet.png)            |![](/res/c++/async/img_1/alexnet.png)            |![](res/python/sync/img_1/alexnet.png)            |![](/res/python/async/img_1/alexnet.png)            |
densenet-121         |![](/res/с++/sync/img_1/densenet-121.png)       |![](/res/c++/async/img_1/densenet-121.png)       |![](res/python/sync/img_1/densenet-121.png)       |![](/res/python/async/img_1/densenet-121.png)       |
densenet-161         |![](/res/с++/sync/img_1/densenet-161.png)       |![](/res/c++/async/img_1/densenet-161.png)       |![](res/python/sync/img_1/densenet-161.png)       |![](/res/python/async/img_1/densenet-161.png)       |
densenet-201         |![](/res/с++/sync/img_1/densenet-201.png)       |![](/res/c++/async/img_1/densenet-201.png)       |![](res/python/sync/img_1/densenet-201.png)       |![](/res/python/async/img_1/densenet-201.png)       |
googlenet-v1         |![](/res/с++/sync/img_1/googlenet-v1.png)       |![](/res/c++/async/img_1/googlenet-v1.png)       |![](res/python/sync/img_1/googlenet-v1.png)       |![](/res/python/async/img_1/googlenet-v1.png.png)   |
googlenet-v2         |![](/res/с++/sync/img_1/googlenet-v2.png)       |![](/res/c++/async/img_1/googlenet-v2.png)       |![](res/python/sync/img_1/googlenet-v2.png)       |![](/res/python/async/img_1/googlenet-v2.png.png)   |
googlenet-v4         |![](/res/с++/sync/img_1/googlenet-v4.png)       |![](/res/c++/async/img_1/googlenet-v4.png)       |![](res/python/sync/img_1/googlenet-v4.png)       |![](/res/python/async/img_1/googlenet-v4.png.png)   |
inception-resnet-v2  |![](/res/с++/sync/img_1/inception-resnet-v2.png)|![](/res/c++/async/img_1/inception-resnet-v2.png)|![](res/python/sync/img_1/inception-resnet-v2.png)|![](/res/python/async/img_1/inception-resnet-v2.png)|
squeezenet-1.0       |![](/res/с++/sync/img_1/squeezenet-1.0.png)     |![](/res/c++/async/img_1/squeezenet-1.0.png)     |![](res/python/sync/img_1/squeezenet-1.0.png)     |![](/res/python/async/img_1/squeezenet-1.0.png)     |
squeezenet-1.1       |![](/res/с++/sync/img_1/squeezenet-1.1.png)     |![](/res/c++/async/img_1/squeezenet-1.1.png)     |![](res/python/sync/img_1/squeezenet-1.1.png)     |![](/res/python/async/img_1/squeezenet-1.1.png)     |
vgg-16               |![](/res/с++/sync/img_1/vgg-16.png)             |![](/res/c++/async/img_1/vgg-16.png)             |![](res/python/sync/img_1/vgg-16.png)             |![](/res/python/async/img_1/vgg-16.png)             |
vgg-19               |![](/res/с++/sync/img_1/vgg-19.png)             |![](/res/c++/async/img_1/vgg-19.png)             |![](res/python/sync/img_1/vgg-19.png)             |![](/res/python/async/img_1/vgg-19.png)             |
 
### Тестовое изображение 2

Источник: набор данных [ImageNet][imagenet]

Разрешение: 500 x 500
﻿

<img src="..\data\ILSVRC2012_val_00000247.JPEG" width="150">

   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |                           |                           |                              |                            |
densenet-121         |                           |                           |                              |                            |
densenet-161         |                           |                           |                              |                            |
densenet-169         |                           |                           |                              |                            |
densenet-201         |                           |                           |                              |                            |
googlenet-v1         |                           |                           |                              |                            |
googlenet-v2         |                           |                           |                              |                            |
googlenet-v4         |                           |                           |                              |                            |
inception-resnet v2  |                           |                           |                              |                            |
squeezenet-1.0       |                           |                           |                              |                            |
squeezenet-1.1       |                           |                           |                              |                            |
vgg-16               |                           |                           |                              |                            |
vgg-19               |                           |                           |                              |                            |

### Тестовое изображение 3

Источник: набор данных [ImageNet][imagenet]

Разрешение: 333 x 500
﻿

<img src="..\data\ILSVRC2012_val_00018592.JPEG" width="150">

   Название модели   |   C++ (синхронный режим)  |  C++ (асинхронный режим)  |   Python (синхронный режим)  |  Python (асинхронный режим)|
---------------------|---------------------------|---------------------------|------------------------------|----------------------------|
alexnet              |                           |                           |                              |                            |
densenet-121         |                           |                           |                              |                            |
densenet-161         |                           |                           |                              |                            |
densenet-169         |                           |                           |                              |                            |
densenet-201         |                           |                           |                              |                            |
googlenet-v1         |                           |                           |                              |                            |
googlenet-v2         |                           |                           |                              |                            |
googlenet-v4         |                           |                           |                              |                            |
inception-resnet v2  |                           |                           |                              |                            |
squeezenet-1.0       |                           |                           |                              |                            |
squeezenet-1.1       |                           |                           |                              |                            |
vgg-16               |                           |                           |                              |                            |
vgg-19               |                           |                           |                              |                            |


<!-- LINKS -->
[imagenet]: http://www.image-net.org