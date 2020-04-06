# Результаты проверки корректности вывода с использованием разных режимов

## Результаты обработки изображений

### Тестовое изображение 1

Источник: набор данных [GitHub][github_single_image_super_resolution]

Разрешение: 720 x 480

<div style='float: center'>
<img width="150" src="images\street_480x270.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
single-image-super-resolution-1032             |<div style='float: center'><img width="150" src="image_processing\python_sync_street_480x270_1.png"></img></div>|<div style='float: center'><img width="150" src="image_processing\python_async_street_480x270_1.png"></img></div>|
single-image-super-resolution-1033             |<div style='float: center'><img width="150" src="image_processing\python_sync_street_480x270_2.png"></img></div>|<div style='float: center'><img width="150" src="image_processing\python_async_street_480x270_2.png"></img></div>|


## Результаты сегментации

### Тестовое изображение 1

Источник: набор данных [The Cityscapes Dataset][cityscapes]

Разрешение: 2048 x 1024

<div style='float: center'>
<img width="150" src="images\bielefeld_000000_038924_leftImg8bit.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
semantic-segmentation-adas-0001             |<div style='float: center'><img width="150" src="segmentation\python_sync_bielefeld_000000_038924_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="150" src="segmentation\python_async_bielefeld_000000_038924_leftImg8bit.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="300" src="segmentation\cityscapes_colormap.jpg">
</div>


### Тестовое изображение 2

Источник: набор данных [GitHub][github_road_segmentation]

Разрешение: 640 x 365

<div style='float: center'>
<img width="150" src="images\road-segmentation-adas-1.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
road-segmentation-adas-0001             |<div style='float: center'><img width="150" src="segmentation\python_sync_road-segmentation-adas-1.bmp"></img></div>|<div style='float: center'><img width="150" src="segmentation\python_async_road-segmentation-adas-1.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="300" src="segmentation\road_segmentation_colormap.jpg">
</div>


### Тестовое изображение 3

Источник: набор данных [MS COCO][ms_coco]

Разрешение: 480 x 640

<div style='float: center'>
<img width="150" src="images\is0083.jpg"></img>
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0083             |<div style='float: center'><img width="150" src="segmentation\python_sync_is0083.bmp"></img></div>|<div style='float: center'><img width="150" src="segmentation\python_async_is0083.bmp"></img></div>|


### Тестовое изображение 4

Источник: набор данных [MS COCO][ms_coco]

Разрешение: 480 x 480

<div style='float: center'>
<img width="150" src="images\is0050.jpg"></img>
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0050             |<div style='float: center'><img width="150" src="segmentation\python_sync_is0050.bmp"></img></div>|<div style='float: center'><img width="150" src="segmentation\python_async_is0050.bmp"></img></div>|


### Тестовое изображение 5

Источник: набор данных [MS COCO][ms_coco]

Разрешение: 1344 x 800

<div style='float: center'>
<img width="150" src="images\is0010.jpg"></img>
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0010             |<div style='float: center'><img width="150" src="segmentation\python_sync_is0010.bmp"></img></div>|<div style='float: center'><img width="150" src="segmentation\python_async_is0010.bmp"></img></div>|


Карта цветов:

<div style='float: center'>
<img width="300" src="segmentation\mscoco_colormap.jpg">
</div>

<!-- LINKS -->
[github_road_segmentation]: https://docs.openvinotoolkit.org/2019_R1.1/_road_segmentation_adas_0001_description_road_segmentation_adas_0001.html
[github_single_image_super_resolution]: https://docs.openvinotoolkit.org/latest/_models_intel_single_image_super_resolution_1032_description_single_image_super_resolution_1032.html
[cityscapes]: https://www.cityscapes-dataset.com
[ms_coco]: http://cocodataset.org