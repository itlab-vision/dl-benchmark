# Проверка корректности вывода для моделей Intel с использованием разных режимов

## Результаты детектирования

### Тестовое изображение 1

Источник: набор данных [Cityscapes][cityscapes] 

Исходное разрешение: 2048 x 1024


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" height="150" src="images\berlin_000000_000019_leftImg8bit.png">
<img width="300" height="150" src="detection\pedestrian-and-vehicle-detector.png">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
CAR (0, 431), (231, 914)<br>
CAR (279, 430), (442, 519)<br>
CAR (428, 444), (494, 498)<br>
CAR (719, 431), (827, 519)<br>
CAR (789, 405), (874, 493)<br>
CAR (828, 413), (970, 536)<br>
CAR (938, 417), (1021, 497)<br>
CAR (1037, 428), (1069, 457)<br>
CAR (1092, 413), (1196, 509)<br>
PERSON (1455, 419), (1482, 491)<br>
PERSON (1476, 416), (1503, 481)<br>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
pedestrian-and-vehicle-detector-adas-0001 | Окаймляющий прямоугольник:<br>CAR (720, 439), (821, 505),<br>CAR (824, 424), (967, 525),<br>CAR (945, 420), (1023, 486),<br>CAR (1092, 422), (1188, 501),<br>PERSON (1474, 416), (1499, 481)<br>| Окаймляющий прямоугольник:<br>CAR (720, 439), (821, 505),<br>CAR (824, 424), (967, 525),<br>CAR (945, 420), (1023, 486),<br>CAR (1092, 422), (1188, 501),<br>PERSON (1474, 416), (1499, 481)<br>|

### Тестовое изображение 2

Источник: набор данных [Cityscapes][cityscapes] 

Исходное разрешение: 2048 x 1024


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" height="150" src="images\vehicle-detection-adas-0002.png">
<img width="300" height="150" src="detection\vehicle-detection.png">
</div>

Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
CAR (360, 354), (917, 781)<br>
CAR (906, 402), (1059, 522)<br>
CAR (1175, 366), (1745, 497)<br>
CAR (1245, 372), (1449, 504)<br>
CAR (1300, 311), (1825, 605)<br>
CAR (1599, 314), (2048, 625)<br>
CAR (1697, 315), (2048, 681)<br>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
vehicle-detection-adas-0002 | Окаймляющий прямоугольник:<br>CAR (384, 363), (921, 754),<br>CAR (909, 407), (1056, 509),<br>CAR (1272, 348), (1742, 592),<br>CAR (1618, 305), (2036, 669)<br>| Окаймляющий прямоугольник:<br>CAR (384, 363), (921, 754),<br>CAR (909, 407), (1056, 509),<br>CAR (1272, 348), (1742, 592),<br>CAR (1618, 305), (2036, 669)|
vehicle-detection-adas-binary-0001 | Окаймляющий прямоугольник:<br>CAR (370, 353), (905, 756),<br>CAR (902, 406), (1048, 509),<br>CAR (1246, 320), (2022, 650)<br>| Окаймляющий прямоугольник:<br>CAR (370, 353), (905, 756),<br>CAR (902, 406), (1048, 509),<br>CAR (1246, 320), (2022, 650)<br>|

### Тестовое изображение 3

Источник: набор данных [Cityscapes][cityscapes] 

Исходное разрешение: 2048 x 1024


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" height="150" src="images\person-vehicle-bike-detection-crossroad.png">
<img width="300" height="150" src="detection\person-vehicle-bike-detection-crossroad.png">
</div>

Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
CAR (0, 380), (88, 524)<br>
CAR (107, 384), (327, 480)<br>
CAR (506, 375), (623, 458)<br>
CAR (626, 367), (734, 452)<br>
CAR (919, 362), (968, 401)<br>
CAR (1053, 360), (1091, 388)<br>
BIKE (300, 402), (558, 778)<br>
PERSON (310, 171), (536, 749)<br>
PERSON (1779, 268), (1882, 539)<br>
PERSON (1874, 288), (1976, 545)<br>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
person-vehicle-bike-detection-crossroad-0078 | Окаймляющий прямоугольник:<br>CAR (-4, 400), (80, 515),<br>CAR (114, 392), (326, 480),<br>CAR (547, 382), (645, 457),<br>CAR (627, 379), (724, 444),<br>BIKE (319, 232), (546, 717),<br>PERSON (329, 228), (541, 697),<br>PERSON (1783, 278), (1887, 530),<br>PERSON (1882, 294), (1974, 524)<br>| Окаймляющий прямоугольник:<br>CAR (-4, 400), (80, 515),<br>CAR (114, 392), (326, 480),<br>CAR (547, 382), (645, 457),<br>CAR(627, 379), (724, 444),<br>BIKE(319, 232), (546, 717),<br>PERSON (329, 228), (541, 697),<br>PERSON (1783, 278), (1887, 530),<br>PERSON (1882, 294), (1974, 524)<br>|
person-vehicle-bike-detection-crossroad-1016 | Окаймляющий прямоугольник:<br>CAR (-1, 405), (85, 518),<br>CAR (533, 370), (637, 455),<br>PERSON (319, 213), (554, 722),<br>PERSON (1783, 270), (1884, 536),<br>PERSON (1883, 299), (1975, 513)<br>| Окаймляющий прямоугольник:<br>CAR (-1, 405), (85, 518),<br>CAR (533, 370), (637, 455),<br>PERSON (319, 213), (554, 722),<br>PERSON (1783, 270), (1884, 536),<br>PERSON (1883, 299), (1975, 513)<br>|

### Тестовое изображение 4

Источник: [GitHub][github_plate] 

Исходное разрешение: 799 x 637


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" height="239" src="images\vehicle-license-plate-detection-barrier-01.png">
<img width="300" height="239" src="detection\vehicle-license-plate-detection-barrier-01.png">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
CAR (232, 119), (509, 466)<br>
PLATE (330, 410), (393, 436)<br>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
vehicle-license-plate-detection-barrier-0106 | Окаймляющий прямоугольник:<br>CAR (232, 119), (509, 466),<br>PLATE (330, 410), (393, 436)<br>| Окаймляющий прямоугольник:<br>CAR (232, 119), (509, 466),<br>PLATE (330, 410), (393, 436)<br>|

### Тестовое изображение 5

Источник: [Интернет][internet_person_asl] 

Исходное разрешение: 320 x 320


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="320" height="320" src="images\person-detection-asl-0001.bmp">
<img width="320" height="320" src="detection\out_person_detection_asl.bmp">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
PERSON (35, 17), (84, 192)<br>
PERSON (79, 13), (122, 194)<br>
PERSON (211, 78), (273, 279)<br>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
person-detection-asl-0001 | Окаймляющий прямоугольник:<br>PERSON (35, 17), (84, 192),<br>PERSON (79, 13), (122, 194),<br>PERSON (211, 78), (273, 279)<br>| Окаймляющий прямоугольник:<br>PERSON (35, 17), (84, 192),<br>PERSON (79, 13), (122, 194),<br>PERSON (211, 78), (273, 279)<br>|

### Тестовое изображение 6

Источник: [Интернет][internet_product] 

Исходное разрешение: 512 x 512


Изображение и результат детектирования:

<div style='float: center'>
<img width="300" height="300" src="images\product-detection-0001.bmp">
<img width="300" height="300" src="detection\product-detection-0001.png">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
PRINGLES (133, 195), (257, 195)<br>
SPRITE (240, 487), (380, 10)<br>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
product-detection-0001 | Окаймляющий прямоугольник:<br>PRINGLES (130, 178), (275, 493)<br>| Окаймляющий прямоугольник:<br>PRINGLES (130, 178), (275, 493)<br>|

### Тестовое изображение 7

Источник: набор данных [Wider Face][widerface]

Исходное разрешение: 1024 x 678


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" src="images\1_Handshaking_Handshaking_1_209.jpg">
<img width="300" src="detection\1_Handshaking_Handshaking_1_209.bmp">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
(189, 140) (288, 284) <br>
(616, 45) (704, 213)<br>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
---------------------|--------------------------------------|--------------------------------------|
face-detection-adas-0001 | Окаймляющий прямоугольник:<br>(189, 140) (288, 284),<br>(616, 45) (704, 213)<br>| Окаймляющий прямоугольник :<br>(189, 140) (288, 284),<br>(616, 45) (704, 213)<br>|
face-detection-adas-binary-0001 | Окаймляющий прямоугольник:<br>(186, 137) (289, 277),<br> (616, 53) (706, 211)<br>| Окаймляющий прямоугольник:<br>(186, 137) (289, 277),<br> (616, 53) (706, 211)<br>|
face-detection-retail-0004 | Окаймляющий прямоугольник:<br>(189, 143) (286, 275),<br>(613, 57) (694, 201)<br>| Окаймляющий прямоугольник:<br>(189, 143) (286, 275),<br>(613, 57) (694, 201)<br>|
face-detection-retail-0005 | Окаймляющий прямоугольник:<br>(189, 140) (296, 277),<br>(609, 44) (714, 206)<br>| Окаймляющий прямоугольник:<br>(189, 140) (296, 277),<br>(609, 44) (714, 206)<br>|

### Тестовое изображение 8

Источник: [из Интернет][internet_walksf]

Исходное разрешение: 1999 x 1333


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" src="images\person-detection-retail-00013-1.jpg">
<img width="300" src="detection\person-detection-retail-00013-1.bmp">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>(1537, 385) (1792, 1184),<br>(541, 299) (845, 1161)<br>(229, 337) (453, 1048),<br>(0, 293) (193, 1129)<br>(955, 387) (1169, 1009),<br>(435, 370) (599, 1019)<br>(887, 292) (951, 479),<br>(749, 252) (866, 657)<br>(515, 317) (599, 580),<br>(833, 264) (894, 464)<br>(954, 283) (1020, 476)<br>

Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
------------------|------------------------------------------|----------------------------------------|
person-detection-retail-0002 | Окаймляющий прямоугольник:<br>(252, 294) (465, 1048),<br>(966, 361) (1183, 1028),<br>(429, 262) (849, 1048),<br>(695, 283) (872, 839),<br>(421, 315) (612, 986),<br>(1560, 360) (1766, 1204),<br>(885, 283) (944, 503),<br>(771, 276) (868, 574),<br>(0, 314) (180, 941),<br>(1879, 459) (1936, 694),<br>(962, 279) (1023, 499),<br>(1890, 302) (1992, 638)<br>|  Окаймляющий прямоугольник:<br>(252, 294) (465, 1048),<br>(966, 361) (1183, 1028),<br>(429, 262) (849, 1048),<br>(695, 283) (872, 839),<br>(421, 315) (612, 986),<br>(1560, 360) (1766, 1204),<br>(885, 283) (944, 503),<br>(771, 276) (868, 574),<br>(0, 314) (180, 941),<br>(1879, 459) (1936, 694),<br>(962, 279) (1023, 499),<br>(1890, 302) (1992, 638)<br>|

### Тестовое изображение 9
Источник: [Cityscapes][cityscapes]

Исходное разрешение: 1999 x 1333


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" src="images\pedestrian-detection-adas-1.png">
<img width="300" src="detection\pedestrian-detection-adas-1.bmp">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>(629, 310) (934, 811),<br>(392, 435) (440, 525)

Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
------------------|------------------------------------------|----------------------------------------|
pedestrian-detection-adas-0002 | Окаймляющий прямоугольник:<br>(614, 307) (945, 803) | Окаймляющий прямоугольник:<br>(614, 307) (945, 803)<br>|
pedestrian-detection-adas-binary-0001 | Окаймляющие прямоугольники:<br> (629, 310) (934, 811),<br>(392, 435) (440, 525)<br>|<br>(629, 310) (934, 811),<br>(392, 435) (440, 525)

## Результаты классификации

### Тестовое изображение 1

Источник: набор данных [ImageNet][imagenet]

Исходное разрешение: 709 x 510


Изображение:

<div style='float: center'>
<img width="300" src="images\ILSVRC2012_val_00000023.JPEG"></img>
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
efficientnet-b0 | 9.8424797 Granny Smith<br>4.8622112 fig<br>4.3583665 lemon<br>3.8766663 bell pepper<br>3.4526284 orange | 9.8424797 Granny Smith<br>4.8622112 fig<br>4.3583665 lemon<br>3.8766663 bell pepper<br>3.4526284 orange |
efficientnet-b0_auto_aug | 10.1708317 Granny Smith<br>4.3690400 tennis ball<br>4.2338214 lemon<br>3.8555355 pomegranate<br>3.8175268 fig | 10.1708317 Granny Smith<br>4.3690400 tennis ball<br>4.2338214 lemon<br>3.8555355 pomegranate<br>3.8175268 fig |

## Результаты детектирования и распознования действия

### Тестовое изображение 1

Источник: набор данных [sample-videos][sample_videos]

Исходное разрешение: 1920 x 1080


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" src="images\classroom.jpg">
<img width="300" src="person_detection_action_recognition\person-detection-action-recognition.bmp">
</div>

Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов) и действие:<br>sitting (1157,517) (1407,1057)<br>sitting (452,495) (627,874)<br>sitting (201,555) (469,1084)<br>raising hand (874,444) (1052,849)<br>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
person-detection-action-recognition-0006 | Окаймляющий прямоугольник и действие:<br>sitting (1157,517) (1407,1057)<br>sitting (452,495) (627,874)<br>sitting (201,555) (469,1084)<br> raising hand (874,444) (1052,849)<br>| Окаймляющий прямоугольник и действие:<br> sitting (1157,517) (1407,1057)<br>sitting (452,495) (627,874)<br>sitting (201,555) (469,1084)<br>raising hand (874,444) (1052,849)<br>|
person-detection-action-recognition-0005 | Окаймляющий прямоугольник и действие:<br>sitting (1160,528) (1409,1082)<br>sitting (202,569) (455,1079)<br>standing (453,495) (624,869)<br>raising hand (836,404) (1048,862)<br>| Окаймляющий прямоугольник и действие:<br>sitting (1160,528) (1409,1082)<br>sitting (202,569) (455,1079)<br>standing (453,495) (624,869)<br>raising hand (836,404) (1048,862)<br>|
person-detection-raisinghand-recognition-0001 | Окаймляющий прямоугольник и действие:<br>sitting (1160,528) (1409,1082)<br>sitting (202,569) (455,1079)<br>sitting (453,495) (624,869)<br>other (836,404) (1048,862)<br>| Окаймляющий прямоугольник и действие:<br> sitting (1160,528) (1409,1082)<br>sitting (202,569) (455,1079)<br>sitting (453,495) (624,869)<br>other (836,404) (1048,862)<br>|

### Тестовое изображение 2

Источник: набор данных [из Интернет][internet_taringa]

Исходное разрешение: 1920 x 1080


Входное изображение и результат детектирования:

<div style='float: center'>
<img width="300" src="images\person-detection-action-recognition-teacher-0001.jpg">
<img width="300" src="person_detection_action_recognition\person-detection-action-recognition-teacher-0001.jpg">
</div>

Окаймляющие прямоугольники (координаты левого верхнего и правого нижнего углов) и действия:<br>standing (186,15) (276,224)

   Название модели   |   Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)        |
---------------------|-----------------------------|------------------------------------|
person-detection-action-recognition-teacher-0002 | Окаймляющий прямоугольник и действие:<br>standing (286,84) (357,283)<br>standing (0,81) (101,281)<br>standing (186,15) (276,224)<br>| Окаймляющие прямоугольники и действия:<br>standing (286,84) (357,283)<br>standing (0,81) (101,281)<br>standing (186,15) (276,224)<br>|

## Результаты распознавания

### Тестовое изображение 1

Источник: [GitHub][github_age_gender] 

Исходное разрешение: 62 x 62


Изображение:

<div style='float: center'>
<img src="images\age-gender-recognition-retail-0001.jpg">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
age-gender-recognition-retail-0013 | Female, 25.19 | Female, 25.19 |

### Тестовое изображение 2

Источник: [GitHub][github_age_gender] 

Исходное разрешение: 62 x 62


Изображение:

<div style='float: center'>
<img src="images\age-gender-recognition-retail-0002.png">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
age-gender-recognition-retail-0013 | Male, 43.43 | Male, 43.43 |

### Тестовое изображение 3

Источник: [GitHub][github_age_gender] 

Исходное разрешение: 62 x 62


Изображение:

<div style='float: center'>
<img src="images\age-gender-recognition-retail-0003.png">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
age-gender-recognition-retail-0013 | Male, 28.49 | Male, 28.49 |

### Тестовое изображение 4

Источник: набор данных [VGGFace2][vgg_face2] 

Исходное разрешение: 48 x 48


Изображение и результат распознавания:

<div style='float: center'>
<img src="images\landmarks.jpg">
<img src="recognition\out_recognition_face_1.bmp">
</div>

Лицевые метки:<br>
EYE (17, 18),<br>
EYE (35, 21),<br>
NOSE (24, 27),<br>
LIP CORNER (15, 34),<br>
LIP CORNER (28, 36)<br>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (17, 18),<br>EYE (35, 21),<br>NOSE (24, 27),<br>LIP CORNER (15, 34),<br>LIP CORNER (28, 36)<br>| Лицевые метки:<br>EYE (17, 18),<br>EYE (35, 21),<br>NOSE (24, 27),<br>LIP CORNER (15, 34),<br>LIP CORNER (28, 36)<br>|

### Тестовое изображение 5

Источник: [Интернет][internet_kerzhakov]

Исходное разрешение: 60 x 60


Изображение и результат распознавания:

<div style='float: center'>
<img src="images\facial-landmarks-35-adas.png">
<img src="recognition\out_recognition_face_facial_landmarks_1.bmp">
</div>

Лицевые метки:<br>
LEFT EYE (17, 22), (9, 22),<br>
RIGHT EYE (30, 21), (39, 20),<br>
NOSE (21, 33), (23, 37), (17, 35), (30, 34),<br>
MOUTH (17, 44), (34, 42), (23, 41), (24, 48),<br>
LEFT EYEBROW (6, 17), (11, 15), (18, 17),<br>
RIGHT EYEBROW (27, 15), (35, 12), (43, 14),<br>
FACE CONTOUR (5, 22), (5, 28), (6, 33), (8, 38), (10, 43), (12, 48), (16, 52), (20, 56), (25, 57), (33, 56), (39, 53), (44, 48), (49, 43), (51, 38), (52, 31), (53, 25), (53, 18)<br>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
facial-landmarks-35-adas-0002 | Лицевые метки:<br>LEFT EYE (17, 22), (9, 22),<br>RIGHT EYE (30, 21), (39, 20),<br>NOSE (21, 33), (23, 37), (17, 35), (30, 34),<br>MOUTH (17, 44), (34, 42), (23, 41), (24, 48),<br>LEFT EYEBROW (6, 17), (11, 15), (18, 17),<br>RIGHT EYEBROW (27, 15), (35, 12), (43, 14),<br>FACE CONTOUR (5, 22), (5, 28), (6, 33), (8, 38), (10, 43), (12, 48), (16, 52), (20, 56), (25, 57), (33, 56), (39, 53), (44, 48), (49, 43), (51, 38), (52, 31), (53, 25), (53, 18)<br>| Лицевые метки:<br>LEFT EYE (17, 22), (9, 22),<br>RIGHT EYE (30, 21), (39, 20),<br>NOSE (21, 33), (23, 37), (17, 35), (30, 34),<br>MOUTH (17, 44), (34, 42), (23, 41), (24, 48),<br>LEFT EYEBROW (6, 17), (11, 15), (18, 17),<br>RIGHT EYEBROW (27, 15), (35, 12), (43, 14),<br>FACE CONTOUR (5, 22), (5, 28), (6, 33), (8, 38), (10, 43), (12, 48), (16, 52), (20, 56), (25, 57), (33, 56), (39, 53), (44, 48), (49, 43), (51, 38), (52, 31), (53, 25), (53, 18)<br>|

### Тестовое изображение 6

Источник: набор данных [Cityscapes][cityscapes] 

Исходное разрешение: 80 x 160


Изображение:

<div style='float: center'>
<img width="80" height="160" src="images\person-attributes-recognition-crossroad-01.png">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
person-attributes-recognition-crossroad-0230 | <img src="recognition\out_person_attributes_sync_1.bmp"> | <img src="recognition\out_person_attributes_async_1.bmp"> |

### Тестовое изображение 7

Источник: набор данных [Cityscapes][cityscapes] 

Исходное разрешение: 80 x 160


Изображение:

<div style='float: center'>
<img width="80" height="160" src="images\person-attributes-recognition-crossroad-02.png">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
person-attributes-recognition-crossroad-0230 | <img src="recognition\out_person_attributes_sync_2.bmp"> | <img src="recognition\out_person_attributes_async_2.bmp"> |

### Тестовое изображение 8

Источник: набор данных [BKHD][bkhd] 

Исходное разрешение: 60 x 60


Изображение и результат распознавания:

<div style='float: center'>
<img src="images\out_head_pose.bmp">
<img src="recognition\out_head_pose_1_sync.bmp">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
head-pose-estimation-adas-0001 | <img src="recognition\out_head_pose_1_sync.bmp"> | <img src="recognition\out_head_pose_1_async.bmp"> |

### Тестовое изображение 9

Источник: набор данных [BKHD][bkhd] 

Исходное разрешение: 60 x 60


Изображение и результат распознавания:

<div style='float: center'>
<img src="images\left_eye.jpg">
<img src="images\right_eye.jpg">
<img src="recognition\out_gaze_1_sync.bmp">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
gaze-estimation-adas-0002 | <img src="recognition\out_gaze_1_sync.bmp"> | <img src="recognition\out_gaze_1_async.bmp"> |

### Тестовое изображение 10

Источник: [GitHub][github_license_plate] 

Исходное разрешение: 24 x 94


Изображение:

<div style='float: center'>
<img height = '24' width = '94' src="images\license-plate-recognition-barrier.JPG">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
license-plate-recognition-barrier-0001 | &lt;Beijing&gt;FA9512 | &lt;Beijing&gt;FA9512 |

## Результаты распознавания лиц

### Тестовое изображение 1

Источник: набор данных [VGGFace2][vgg_face2]  

Исходное разрешение: 96 x 112


Изображение:

<div style='float: center'>
<img src="images\sphereface.jpg">
</div>

   Название модели   |  Python (latency mode, реализация)  |  Python (throughput mode, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
Sphereface | 0.77 0.70 0.77 -1.79 1.00<br> -0.02 0.82 -0.44 -0.96 0.37<br> ...<br> -0.74 0.25 -0.35 2.06 1.16<br> 0.56 -1.14 0.50 0.46 -0.91<br> [Полный тензор][sphereface_sync] | 0.77 0.70 0.77 -1.79 1.00<br> -0.02 0.82 -0.44 -0.96 0.37<br> ...<br> -0.74 0.25 -0.35 2.06 1.16<br> 0.56 -1.14 0.50 0.46 -0.91<br> [Полный тензор][sphereface_async] |


## Результаты обработки изображений

### Тестовое изображение 1

Источник: [GitHub][github_single_image_super_resolution]

Исходное разрешение: 720 x 480


Изображение и результат обработки:

<div style='float: center'>
<img width="300" src="images\street_480x270.png"></img>
<img width="300" src="images\x4c_street_480x270.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
single-image-super-resolution-1032             |<div style='float: center'><img width="300" src="image_processing\python_sync_street_480x270_1.png"></img></div>|<div style='float: center'><img width="300" src="image_processing\python_async_street_480x270_1.png"></img></div>|
single-image-super-resolution-1033             |<div style='float: center'><img width="300" src="image_processing\python_sync_street_480x270_2.png"></img></div>|<div style='float: center'><img width="300" src="image_processing\python_async_street_480x270_2.png"></img></div>|

## Результаты распознавания позы человека

### Тестовое изображение 1

Источник: набор данных [MS COCO][ms_coco]

Исходное разрешение: 640 x 425


Изображение:

<div style='float: center'>
<img width="300" src="images\COCO_val2014_000000453166.jpg"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
human-pose-estimation-0001             |<div style='float: center'><img width="300" src="human_pose_estimation\python_sync_COCO_val2014_000000453166.png"></img></div>|<div style='float: center'><img width="300" src="human_pose_estimation\python_async_COCO_val2014_000000453166.png"></img></div>|

## Результаты семантической сегментации

### Тестовое изображение 1

Источник: набор данных [Cityscapes][cityscapes]

Исходное разрешение: 2048 x 1024


Изображение:

<div style='float: center'>
<img width="300" src="images\bielefeld_000000_038924_leftImg8bit.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
semantic-segmentation-adas-0001             |<div style='float: center'><img width="300" src="semantic_segmentation\python_sync_bielefeld_000000_038924_leftImg8bit.bmp"></img></div>|<div style='float: center'><img width="300" src="semantic_segmentation\python_async_bielefeld_000000_038924_leftImg8bit.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="200" src="semantic_segmentation\cityscapes_colormap.jpg">
</div>

### Тестовое изображение 2

Источник: [GitHub][github_road_segmentation]

Исходное разрешение: 640 x 365


Изображение:

<div style='float: center'>
<img width="300" src="images\road-segmentation-adas-1.png"></img>
</div>

Полученные изображения идентичны и совпадают по пикселям.

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
road-segmentation-adas-0001             |<div style='float: center'><img width="300" src="semantic_segmentation\python_sync_road-segmentation-adas-1.bmp"></img></div>|<div style='float: center'><img width="300" src="semantic_segmentation\python_async_road-segmentation-adas-1.bmp"></img></div>|

Карта цветов:

<div style='float: center'>
<img width="200" src="semantic_segmentation\road_segmentation_colormap.jpg">
</div>

## Результаты векторного описания

### Тестовое изображение 1

Источник: набор данных [LFW][LFW]

Исходное разрешение: 250 x 250


Изображение:

<div style='float: center'>
<img width="300" src="images\Aaron_Peirsol_0002.jpg"></img>
</div>
<div style='float: center'>
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
face-reidentification-retail-0095 | -0.1658423  -0.5230426<br> -1.4679441  0.0983598<br> ...<br> 0.8537527  0.8713884<br> -0.8769233  0.6840097<br> [Полный тензор][face_reidentification_sync] | -0.1658423  -0.5230426<br> -1.4679441  0.0983598<br> ...<br> 0.8537527  0.8713884<br> -0.8769233  0.6840097<br> [Полный тензор][face_reidentification_async] |

### Тестовое изображение 2

Источник: [GitHub][github_ARE]

Исходное разрешение: 960 x 720


Изображение:

<div style='float: center'>
<img width="300" src="images\demo.png"></img>
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
action-recognition-0001-encoder | 0.0794002  0.0583136<br> 0.0020747  0.0903931<br> ...<br> 0.0785143  0.0922345<br> 0.0033597  0.3115494<br> [Полный тензор][ARE_sync] | 0.0794002  0.0583136<br> 0.0020747  0.0903931<br> ...<br> 0.0785143  0.0922345<br> 0.0033597  0.3115494<br> [Полный тензор][ARE_async] |

### Тестовое изображение 3

Источник: [GitHub][github_DARE]

Исходное разрешение: 1922 x 1080


Изображение:

<div style='float: center'>
<img width="300" src="images\action-recognition-kelly.png"></img>
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
driver-action-recognition-adas-0002-encoder | -0.0142664  -0.0064784<br> -0.0334583  -0.0108943<br> ...<br> -0.2324419  0.2686763<br> 0.0168234  0.0029897<br> [Полный тензор][DARE_sync] | -0.0142664  -0.0064784<br> -0.0334583  -0.0108943<br> ...<br> -0.2324419  0.2686763<br> 0.0168234  0.0029897<br> [Полный тензор][DARE_async] |

## Результаты распознавания действий

### Тестовый тензор 1

Источник: [результат работы модели action-recognition-0001-encoder][ARD]


Тензор:

<div style='float: center'>
0.0794002  0.0583136  0.0020747  0.0903931<br>
0.0154800  0.3712009  0.4007360  0.0830761<br>
...<br>
0.1126685  0.1257046  0.1392988  0.5075323<br>
0.0785143  0.0922345  0.0033597  0.3115494
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
action-recognition-0001-decoder | 9.0227661 tying bow tie<br> 7.5208311 tying tie<br> 4.8729849 sign language interpreting<br> 4.3601480 answering questions<br> 4.2990689 tying knot (not on a tie)<br> 4.0868192 whistling<br> 3.9643712 playing harmonica<br> 3.7044604 stretching arm<br> 3.5711651 strumming guitar<br> 3.5514102 playing clarinet | 9.0227661 tying bow tie<br> 7.5208311 tying tie<br> 4.8729849 sign language interpreting<br> 4.3601480 answering questions<br> 4.2990689 tying knot (not on a tie)<br> 4.0868192 whistling<br> 3.9643712 playing harmonica<br> 3.7044604 stretching arm<br> 3.5711651 strumming guitar<br> 3.5514102 playing clarinet |

### Тестовый тензор 2

Источник: [результат работы модели driver-action-recognition-adas-0002-encoder][DARD]


Тензор:

<div style='float: center'>
-0.0142664  -0.0064780  -0.0334583  -0.0108943<br>
-0.0555940  -0.0013968   0.0001638  -0.0007524<br>
...<br>
-0.0093990  -0.0028726   0.0074722   0.0303789<br>
-0.2324419   0.2686763   0.0168234   0.0029897
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
driver-action-recognition-adas-0002-decoder | 4.3797836 texting by right hand<br> 4.1073933 talking on the phone by right hand<br> 1.6492549 drinking<br> 1.2682760 texting by left hand<br> 0.3225771 reaching behind<br> -1.6658649 safe driving<br> -3.3440599 doing hair or making up<br> -4.6270852 operating the radio<br> -5.3927083 talking on the phone by left hand | 4.3797836 texting by right hand<br> 4.1073933 talking on the phone by right hand<br> 1.6492549 drinking<br> 1.2682760 texting by left hand<br> 0.3225771 reaching behind<br> -1.6658649 safe driving<br> -3.3440599 doing hair or making up<br> -4.6270852 operating the radio<br> -5.3927083 talking on the phone by left hand |

## Результаты экземплярной сегментации

### Тестовое изображение 1

Источник: набор данных [MS COCO][ms_coco]

Исходное разрешение: 640 x 480


Изображение:

<div style='float: center'>
<img width="300" src="images\000000118209.jpg"></img>
</div>
<div style='float: center'>
Входной тензор: 480; 640; 1
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0083             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_000000118209.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_000000118209.bmp"></img></div>|

### Тестовое изображение 2

Источник: набор данных [MS COCO][ms_coco]

Исходное разрешение: 640 x 640


Изображение:

<div style='float: center'>
<img width="300" src="images\COCO_val2014_000000203438.jpg"></img>
</div>
<div style='float: center'>
Входной тензор: 480; 480; 1
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0050             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_COCO_val2014_000000203438.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_COCO_val2014_000000203438.bmp"></img></div>|

### Тестовое изображение 3

Источник: набор данных [MS COCO][ms_coco]

Исходное разрешение: 640 x 427


Изображение:

<div style='float: center'>
<img width="300" src="images\000000367818.jpg"></img>
</div>
<div style='float: center'>
Входной тензор: 800; 1344; 1
</div>

   Название модели   |   Python (latency mode, реализация)  |  Python (throughput mode, реализация)        |
---------------------|-----------------------------|------------------------------------|
instance-segmentation-security-0010             |<div style='float: center'><img width="300" src="instance_segmentation\python_sync_000000367818.bmp"></img></div>|<div style='float: center'><img width="300" src="instance_segmentation\python_async_000000367818.bmp"></img></div>|


Карта цветов:

<div style='float: center'>
<img width="300" src="instance_segmentation\mscoco_colormap.jpg">
</div>


<!-- LINKS -->
[cityscapes]: https://www.cityscapes-dataset.com
[github_plate]: https://github.com/opencv/open_model_zoo/blob/master/models/intel/vehicle-license-plate-detection-barrier-0106/description/vehicle-license-plate-detection-barrier-0106.jpeg
[github_age_gender]: https://github.com/opencv/open_model_zoo/blob/master/models/intel/age-gender-recognition-retail-0013/description
[vgg_face2]:http://www.robots.ox.ac.uk/~vgg/data/vgg_face2
[internet_kerzhakov]:http://positime.ru/the-russian-team-contender-for-the-world-cup-alexander-kerzhakov/40266
[internet_person_asl]:http://rasfokus.ru/photos/topweek/photo3138574.html
[internet_product]:https://bendoeslife.tumblr.com/post/48135155548/at-work-forgot-my-lunch-and-not-able-to-leave-at
[bkhd]:https://www.kaggle.com/kmader/biwi-kinect-head-pose-database
[github_license_plate]:https://github.com/opencv/open_model_zoo/blob/master/models/intel/license-plate-recognition-barrier-0001/description
[sphereface_sync]:recognition/sphereface_out_sync.csv
[sphereface_async]:recognition/sphereface_out_async.csv
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
[internet_taringa]: https://www.taringa.net/+ciencia_educacion/busca-tu-propia-respuesta-crisis-en-la-educacion_13n2mk
[internet_walksf]: https://walksf.org/our-work/campaigns/6th-street/
[sample_videos]: https://github.com/intel-iot-devkit/sample-videos
[widerface]: http://shuoyang1213.me/WIDERFACE
[imagenet]: http://www.image-net.org/