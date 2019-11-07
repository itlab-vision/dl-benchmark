# Результаты проверки корректности вывода с использованием разных режимов

## Результаты сегментации

### Тестовое изображение 1


Источник: набор данных [The Cityscapes Dataset][cityscapes]

Разрешение: 2048 x 1024
﻿
<div style='float: center'>
<img width="150" src="images\bielefeld_000000_038924_leftImg8bit.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
semantic-segmentation-adas-0001             |<div style='float: center'><img width="150" src="segmentation\python_sync_bielefeld_000000_038924_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="segmentation\python_async_bielefeld_000000_038924_leftImg8bit.bmp"></img></div>|

### Тестовое изображение 2

Источник: набор данных [GitHub][github]

Разрешение: 640 x 365
﻿
<div style='float: center'>
<img width="150" src="images\road-segmentation-adas-1.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
road-segmentation-adas-0001             |<div style='float: center'><img width="150" src="segmentation\python_sync_road-segmentation-adas-1.bmp"></img></div>|<div style='float: center'><img width="150" src="segmentation\python_async_road-segmentation-adas-1.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="300" src="segmentation\cityscapes_colormap.jpg">
</div>


<!-- LINKS -->
[github]: https://www.github.com
[cityscapes]: https://www.cityscapes-dataset.com