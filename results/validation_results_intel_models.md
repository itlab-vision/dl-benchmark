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


## Результаты векторного описания

### Тестовое изображение 1

Источник: набор данных [LFW][LFW]

Разрешение: 250 x 250

<div style='float: center'>
<img width="300" src="images\Aaron_Peirsol_0002.jpg"></img>
</div>
<div style='float: center'>
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
face-reidentification-retail-0095 | -0.1658423  -0.5230426<br> -1.4679441  0.0983598<br> ...<br> 0.8537527  0.8713884<br> -0.8769233  0.6840097<br> [Полный тензор][face_reidentification_sync] | -0.1658423  -0.5230426<br> -1.4679441  0.0983598<br> ...<br> 0.8537527  0.8713884<br> -0.8769233  0.6840097<br> [Полный тензор][face_reidentification_async] |


### Тестовое изображение 2

Источник: набор данных [GitHub][github_ARE]

Разрешение: 960 x 720

<div style='float: center'>
<img width="300" src="images\demo.png"></img>
</div>
<div style='float: center'>
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
action-recognition-0001-encoder | 0.0794002  0.0583136<br> 0.0020747  0.0903931<br> ...<br> 0.0785143  0.0922345<br> 0.0033597  0.3115494<br> [Полный тензор][ARE_sync] | 0.0794002  0.0583136<br> 0.0020747  0.0903931<br> ...<br> 0.0785143  0.0922345<br> 0.0033597  0.3115494<br> [Полный тензор][ARE_async] |


### Тестовое изображение 3

Источник: набор данных [GitHub][github_DARE]

Разрешение: 1922 x 1080

<div style='float: center'>
<img width="300" src="images\action-recognition-kelly.png"></img>
</div>
<div style='float: center'>
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
driver-action-recognition-adas-0002-encoder | -0.0142664  -0.0064784<br> -0.0334583  -0.0108943<br> ...<br> -0.2324419  0.2686763<br> 0.0168234  0.0029897<br> [Полный тензор][DARE_sync] | -0.0142664  -0.0064784<br> -0.0334583  -0.0108943<br> ...<br> -0.2324419  0.2686763<br> 0.0168234  0.0029897<br> [Полный тензор][DARE_async] |


## Результаты распознования действий

### Тестовый тензор 1

Источник: [Результат работы модели action-recognition-0001-encoder][ARD]

<div style='float: center'>
0.0794002  0.0583136  0.0020747  0.0903931<br>
0.0154800  0.3712009  0.4007360  0.0830761<br>
...<br>
0.1126685  0.1257046  0.1392988  0.5075323<br>
0.0785143  0.0922345  0.0033597  0.3115494
</div>
<div style='float: center'>
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
action-recognition-0001-decoder |  |  |


### Тестовый тензор 2

Источник: [Результат работы модели driver-action-recognition-adas-0002-encoder][DARD]

<div style='float: center'>
-0.0142664  -0.0064780  -0.0334583  -0.0108943<br>
-0.0555940  -0.0013968   0.0001638  -0.0007524<br>
...<br>
-0.0093990  -0.0028726   0.0074722   0.0303789<br>
-0.2324419   0.2686763   0.0168234   0.0029897
</div>
<div style='float: center'>
</div>


   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
driver-action-recognition-adas-0002-decoder |  |  |


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
[ARD]: action_recognition/action_recognition_encoder_out.csv
[DARD]: action_recognition/driver_action_recognition_encoder_out.csv
[ARE_sync]: encoding/python_sync_demo.csv
[ARE_async]: encoding/python_async_demo.csv
[DARE_sync]: encoding/python_sync_action-recognition-kelly.csv
[DARE_async]: encoding/python_async_action-recognition-kelly.csv
[face_reidentification_sync]: encoding/python_sync_Aaron_Peirsol_0002.csv
[face_reidentification_async]: encoding/python_async_Aaron_Peirsol_0002.csv
[github_ARE]: https://github.com/opencv/open_model_zoo/tree/master/models/intel/action-recognition-0001-encoder/description
[github_DARE]: https://github.com/opencv/open_model_zoo/tree/master/models/intel/driver-action-recognition-adas-0002-encoder/description
[github_road_segmentation]: https://github.com/opencv/open_model_zoo/tree/master/models/intel/road-segmentation-adas-0001/description
[github_single_image_super_resolution]: https://github.com/opencv/open_model_zoo/tree/master/models/intel/single-image-super-resolution-1032/description
[LFW]: http://vis-www.cs.umass.edu/lfw/index.html
[cityscapes]: https://www.cityscapes-dataset.com
[ms_coco]: http://cocodataset.org