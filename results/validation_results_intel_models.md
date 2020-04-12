# Результаты проверки корректности вывода с использованием разных режимов

## Результаты обработки изображений

### Тестовое изображение 1

Источник: набор данных [GitHub][github_single_image_super_resolution]

Разрешение: 720 x 480

<div style='float: center'>
<img width="300" src="images\street_480x270.png"></img>
<img width="300" src="images\x4c_street_480x270.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
single-image-super-resolution-1032             |<div style='float: center'><img width="300" src="image_processing\python_sync_street_480x270_1.png"></img></div>|<div style='float: center'><img width="300" src="image_processing\python_async_street_480x270_1.png"></img></div>|
single-image-super-resolution-1033             |<div style='float: center'><img width="300" src="image_processing\python_sync_street_480x270_2.png"></img></div>|<div style='float: center'><img width="300" src="image_processing\python_async_street_480x270_2.png"></img></div>|


## Результаты распознавания позы человека

### Тестовое изображение 1

Источник: набор данных [MS COCO][ms_coco]

Разрешение: 640 x 425

<div style='float: center'>
<img width="300" src="images\COCO_val2014_000000453166.jpg"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
human-pose-estimation-0001             |<div style='float: center'><img width="300" src="human_pose_estimation\python_sync_COCO_val2014_000000453166.png"></img></div>|<div style='float: center'><img width="300" src="human_pose_estimation\python_async_COCO_val2014_000000453166.png"></img></div>|


## Результаты семантической сегментации

### Тестовое изображение 1

Источник: набор данных [The Cityscapes Dataset][cityscapes]

Разрешение: 2048 x 1024

<div style='float: center'>
<img width="300" src="images\bielefeld_000000_038924_leftImg8bit.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
semantic-segmentation-adas-0001             |<div style='float: center'><img width="300" src="semantic_segmentation\python_sync_bielefeld_000000_038924_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="300" src="semantic_segmentation\python_async_bielefeld_000000_038924_leftImg8bit.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="200" src="semantic_segmentation\cityscapes_colormap.jpg">
</div>


### Тестовое изображение 2

Источник: набор данных [GitHub][github_road_segmentation]

Разрешение: 640 x 365

<div style='float: center'>
<img width="300" src="images\road-segmentation-adas-1.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
road-segmentation-adas-0001             |<div style='float: center'><img width="300" src="semantic_segmentation\python_sync_road-segmentation-adas-1.bmp"></img></div>|<div style='float: center'><img width="300" src="semantic_segmentation\python_async_road-segmentation-adas-1.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="200" src="semantic_segmentation\road_segmentation_colormap.jpg">
</div>


## Результаты экземплярной сегментации

### Тестовое изображение 1

Источник: набор данных [MS COCO][ms_coco]

Разрешение: 640 x 480

<div style='float: center'>
<img width="300" src="images\000000118209.jpg"></img>
</div>
<div style='float: center'>
Входной тензор: 480; 640; 1
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0083             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_000000118209.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_000000118209.bmp"></img></div>|


### Тестовое изображение 2

Источник: набор данных [MS COCO][ms_coco]

Разрешение: 640 x 640

<div style='float: center'>
<img width="300" src="images\COCO_val2014_000000203438.jpg"></img>
</div>
<div style='float: center'>
Входной тензор: 480; 480; 1
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0050             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_COCO_val2014_000000203438.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_COCO_val2014_000000203438.bmp"></img></div>|


### Тестовое изображение 3

Источник: набор данных [MS COCO][ms_coco]

Разрешение: 640 x 427

<div style='float: center'>
<img width="300" src="images\000000367818.jpg"></img>
</div>
<div style='float: center'>
Входной тензор: 800; 1344; 1
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0010             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_000000367818.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_000000367818.bmp"></img></div>|


Карта цветов:

<div style='float: center'>
<img width="200" src="instance_segmentation\mscoco_colormap.jpg">
</div>

<!-- LINKS -->
[github_road_segmentation]: https://github.com/opencv/open_model_zoo/tree/master/models/intel/road-segmentation-adas-0001/description
[github_single_image_super_resolution]: https://github.com/opencv/open_model_zoo/tree/master/models/intel/single-image-super-resolution-1032/description
[cityscapes]: https://www.cityscapes-dataset.com
[ms_coco]: http://cocodataset.org