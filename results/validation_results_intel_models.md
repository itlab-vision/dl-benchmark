# Результаты проверки корректности вывода с использованием разных режимов

## Результаты детектирования

### Тестовое изображение 1

Источник: набор данных [CityScapes][cityscapes] 

Разрешение: 2048 x 1024

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

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
pedestrian-and-vehicle-detector-adas-0001 | Окаймляющий прямоугольник:<br>CAR (720, 439), (821, 505),<br>CAR (824, 424), (967, 525),<br>CAR (945, 420), (1023, 486),<br>CAR (1092, 422), (1188, 501),<br>PERSON (1474, 416), (1499, 481)<br>| Окаймляющий прямоугольник:<br>CAR (720, 439), (821, 505),<br>CAR (824, 424), (967, 525),<br>CAR (945, 420), (1023, 486),<br>CAR (1092, 422), (1188, 501),<br>PERSON (1474, 416), (1499, 481)<br>|

### Тестовое изображение 2

Источник: набор данных [CityScapes][cityscapes] 

Разрешение: 2048 x 1024

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

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
vehicle-detection-adas-0002 | Окаймляющий прямоугольник:<br>CAR (384, 363), (921, 754),<br>CAR (909, 407), (1056, 509),<br>CAR (1272, 348), (1742, 592),<br>CAR (1618, 305), (2036, 669)<br>| Окаймляющий прямоугольник:<br>CAR (384, 363), (921, 754),<br>CAR (909, 407), (1056, 509),<br>CAR (1272, 348), (1742, 592),<br>CAR (1618, 305), (2036, 669)|
vehicle-detection-adas-binary-0001 | Окаймляющий прямоугольник:<br>CAR (370, 353), (905, 756),<br>CAR (902, 406), (1048, 509),<br>CAR (1246, 320), (2022, 650)<br>| Окаймляющий прямоугольник:<br>CAR (370, 353), (905, 756),<br>CAR (902, 406), (1048, 509),<br>CAR (1246, 320), (2022, 650)<br>|

### Тестовое изображение 3

Источник: набор данных [CityScapes][cityscapes] 

Разрешение: 2048 x 1024

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

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
person-vehicle-bike-detection-crossroad-0078 | Окаймляющий прямоугольник:<br>CAR (-4, 400), (80, 515),<br>CAR (114, 392), (326, 480),<br>CAR (547, 382), (645, 457),<br>CAR (627, 379), (724, 444),<br>BIKE (319, 232), (546, 717),<br>PERSON (329, 228), (541, 697),<br>PERSON (1783, 278), (1887, 530),<br>PERSON (1882, 294), (1974, 524)<br>| Окаймляющий прямоугольник:<br>CAR (-4, 400), (80, 515),<br>CAR (114, 392), (326, 480),<br>CAR (547, 382), (645, 457),<br>CAR(627, 379), (724, 444),<br>BIKE(319, 232), (546, 717),<br>PERSON (329, 228), (541, 697),<br>PERSON (1783, 278), (1887, 530),<br>PERSON (1882, 294), (1974, 524)<br>|
person-vehicle-bike-detection-crossroad-1016 | Окаймляющий прямоугольник:<br>CAR (-1, 405), (85, 518),<br>CAR (533, 370), (637, 455),<br>PERSON (319, 213), (554, 722),<br>PERSON (1783, 270), (1884, 536),<br>PERSON (1883, 299), (1975, 513)<br>| Окаймляющий прямоугольник:<br>CAR (-1, 405), (85, 518),<br>CAR (533, 370), (637, 455),<br>PERSON (319, 213), (554, 722),<br>PERSON (1783, 270), (1884, 536),<br>PERSON (1883, 299), (1975, 513)<br>|

### Тестовое изображение 4

Источник: набор данных [GitHub][github_plate] 

Разрешение: 799 x 637

<div style='float: center'>
<img width="300" height="239" src="images\vehicle-license-plate-detection-barrier-01.png">
<img width="300" height="239" src="detection\vehicle-license-plate-detection-barrier-01.png">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
CAR (232, 119), (509, 466)<br>
PLATE (330, 410), (393, 436)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
vehicle-license-plate-detection-barrier-0106 | Окаймляющий прямоугольник:<br>CAR (232, 119), (509, 466),<br>PLATE (330, 410), (393, 436)<br>| Окаймляющий прямоугольник:<br>CAR (232, 119), (509, 466),<br>PLATE (330, 410), (393, 436)<br>|

### Тестовое изображение 5

Источник: набор данных [Интернет][internet_person_asl] 

Разрешение: 320 x 320

<div style='float: center'>
<img width="320" height="320" src="images\person-detection-asl-0001.bmp">
<img width="320" height="320" src="detection\out_person_detection_asl.bmp">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
PERSON (35, 17), (84, 192)<br>
PERSON (79, 13), (122, 194)<br>
PERSON (211, 78), (273, 279)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
person-detection-asl-0001 | Окаймляющий прямоугольник:<br>PERSON (35, 17), (84, 192),<br>PERSON (79, 13), (122, 194),<br>PERSON (211, 78), (273, 279)<br>| Окаймляющий прямоугольник:<br>PERSON (35, 17), (84, 192),<br>PERSON (79, 13), (122, 194),<br>PERSON (211, 78), (273, 279)<br>|

### Тестовое изображение 6

Источник: набор данных [Интернет][internet_product] 

Разрешение: 512 x 512

<div style='float: center'>
<img width="300" height="300" src="images\product-detection-0001.bmp">
<img width="300" height="300" src="detection\product-detection-0001.png">
</div>
Окаймляющий прямоугольник (координаты левого верхнего и правого нижнего углов):<br>
PRINGLES (133, 195), (257, 195)<br>
SPRITE (240, 487), (380, 10)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
product-detection-0001 | Окаймляющий прямоугольник:<br>PRINGLES (130, 178), (275, 493)<br>| Окаймляющий прямоугольник:<br>PRINGLES (130, 178), (275, 493)<br>|

## Результаты распознования

### Тестовое изображение 1

Источник: набор данных [GitHub][github_age_gender] 

Разрешение: 62 x 62

<div style='float: center'>
<img src="images\age-gender-recognition-retail-0001.jpg">
</div>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
age-gender-recognition-retail-0013 | Female, 25.19 | Female, 25.19 |

### Тестовое изображение 2

Источник: набор данных [GitHub][github_age_gender] 

Разрешение: 64 x 77

<div style='float: center'>
<img src="images\age-gender-recognition-retail-0002.png">
</div>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
age-gender-recognition-retail-0013 | Male, 43.43 | Male, 43.43 |

### Тестовое изображение 3

Источник: набор данных [GitHub][github_age_gender] 

Разрешение: 71 x 77

<div style='float: center'>
<img src="images\age-gender-recognition-retail-0003.png">
</div>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
age-gender-recognition-retail-0013 | Male, 28.49 | Male, 28.49 |

### Тестовое изображение 4

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 123 x 151

<div style='float: center'>
<img src="images\landmarks_1.jpg">
<img src="recognition\out_recognition_face_1.jpg">
</div>

Лицевые метки:<br>
EYE (24, 21),<br>
EYE (39, 20),<br>
NOSE (37, 25),<br>
LIP CORNER (26, 35),<br>
LIP CORNER (41, 34)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (23, 20),<br>EYE (39, 20),<br>NOSE (37, 25),<br>LIP CORNER (26, 35),<br>LIP CORNER (41, 34) | Лицевые метки:<br>EYE (23, 20),<br>EYE (39, 20),<br>NOSE (37, 25),<br>LIP CORNER (26, 35),<br>LIP CORNER (41, 34) |

### Тестовое изображение 5

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 105 x 133

<div style='float: center'>
<img src="images\landmarks_2.jpg">
<img src="recognition\out_recognition_face_2.bmp">
</div>

Лицевые метки:<br>
EYE (17, 18),<br>
EYE (35, 21),<br>
NOSE (24, 27),<br>
LIP CORNER (15, 34),<br>
LIP CORNER (28, 36)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (17, 18),<br>EYE (35, 21),<br>NOSE (24, 27),<br>LIP CORNER (15, 34),<br>LIP CORNER (28, 36)<br>| Лицевые метки:<br>EYE (17, 18),<br>EYE (35, 21),<br>NOSE (24, 27),<br>LIP CORNER (15, 34),<br>LIP CORNER (28, 36)<br>|

### Тестовое изображение 6

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 117 x 146

<div style='float: center'>
<img src="images\landmarks_3.jpg">
<img src="recognition\out_recognition_face_3.jpg">
</div>

Лицевые метки:<br>
EYE (14, 20),<br>
EYE (30, 19),<br>
NOSE (20, 29),<br>
LIP CORNER (15, 33),<br>
LIP CORNER (31, 34)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (14, 20),<br>EYE (31, 20),<br>NOSE (20, 29),<br>LIP CORNER (15, 33),<br>LIP CORNER (31, 34)<br>| Лицевые метки:<br>EYE (14, 20),<br>EYE (31, 20),<br>NOSE (20, 29),<br>LIP CORNER (15, 33),<br>LIP CORNER (31, 34)<br>|

### Тестовое изображение 7

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 93 x 132

<div style='float: center'>
<img src="images\landmarks_4.jpg">
<img src="recognition\out_recognition_face_4.bmp">
</div>

Лицевые метки:<br>
EYE (13, 21),<br>
EYE (30, 20),<br>
NOSE (20, 29),<br>
LIP CORNER (16, 35),<br>
LIP CORNER (32, 34)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (13, 21),<br>EYE (30, 20),<br>NOSE (20, 29),<br>LIP CORNER (16, 35),<br>LIP CORNER (32, 34)<br>| Лицевые метки:<br>EYE (13, 21),<br>EYE (30, 20),<br>NOSE (20, 29),<br>LIP CORNER (16, 35),<br>LIP CORNER (32, 34)<br>|

### Тестовое изображение 8

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 171 x 206

<div style='float: center'>
<img src="images\landmarks_5.jpg">
<img src="recognition\out_recognition_face_5.jpg">
</div>

Лицевые метки:<br>
EYE (21, 23),<br>
EYE (37, 19),<br>
NOSE (32, 27),<br>
LIP CORNER (25, 37),<br>
LIP CORNER (39, 34)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (18, 22),<br>EYE (37, 19),<br>NOSE (32, 27),<br>LIP CORNER (25, 37),<br>LIP CORNER (39, 34)<br>| Лицевые метки:<br>EYE (18, 22),<br>EYE (37, 19),<br>NOSE (32, 27),<br>LIP CORNER (25, 37),<br>LIP CORNER (39, 34)<br>|

### Тестовое изображение 9

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 63 x 77

<div style='float: center'>
<img src="images\landmarks_6.jpg">
<img src="recognition\out_recognition_face_6.jpg">
</div>

Лицевые метки:<br>
EYE (14, 24),<br>
EYE (31, 21),<br>
NOSE (22, 30),<br>
LIP CORNER (17, 36),<br>
LIP CORNER (31, 35)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (14, 22),<br>EYE (31, 21),<br>NOSE (22, 30),<br>LIP CORNER (17, 36),<br>LIP CORNER (31, 35)<br>| Лицевые метки:<br>EYE (14, 22),<br>EYE (31, 21),<br>NOSE (22, 30),<br>LIP CORNER (17, 36),<br>LIP CORNER (31, 35)<br>|

### Тестовое изображение 10

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 86 x 125

<div style='float: center'>
<img src="images\landmarks_7.jpg">
<img src="recognition\out_recognition_face_7.bmp">
</div>

Лицевые метки:<br>
EYE (12, 20),<br>
EYE (31, 20),<br>
NOSE (20, 27),<br>
LIP CORNER (12, 33),<br>
LIP CORNER (30, 33)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (12, 20),<br>EYE (31, 20),<br>NOSE (20, 27),<br>LIP CORNER (12, 33),<br>LIP CORNER (30, 33)<br>| Лицевые метки:<br>EYE (12, 20),<br>EYE (31, 20),<br>NOSE (20, 27),<br>LIP CORNER (12, 33),<br>LIP CORNER (30, 33)<br>|

### Тестовое изображение 12

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 58 x 79

<div style='float: center'>
<img src="images\landmarks_9.jpg">
<img src="recognition\out_recognition_face_9.bmp">
</div>

Лицевые метки:<br>
EYE (18, 20),<br>
EYE (35, 22),<br>
NOSE (28, 30),<br>
LIP CORNER (16, 35),<br>
LIP CORNER (31, 36)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (18, 20),<br>EYE (35, 22),<br>NOSE (28, 30),<br>LIP CORNER (16, 35),<br>LIP CORNER (31, 36)<br>| Лицевые метки:<br>EYE (18, 20),<br>EYE (35, 22),<br>NOSE (28, 30),<br>LIP CORNER (16, 35),<br>LIP CORNER (31, 36)<br>|

### Тестовое изображение 13

Источник: набор данных [VGGFace2][vgg_face2] 

Разрешение: 101 x 125

<div style='float: center'>
<img src="images\landmarks_10.jpg">
<img src="recognition\out_recognition_face_10.bmp">
</div>

Лицевые метки:<br>
EYE (15, 19),<br>
EYE (32, 20),<br>
NOSE (23, 28),<br>
LIP CORNER (14, 32),<br>
LIP CORNER (30, 33)<br>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
landmarks-regression-retail-0009 | Лицевые метки:<br>EYE (15, 19),<br>EYE (32, 20),<br>NOSE (23, 28),<br>LIP CORNER (14, 32),<br>LIP CORNER (30, 33)<br>| Лицевые метки:<br>EYE (15, 19),<br>EYE (32, 20),<br>NOSE (23, 28),<br>LIP CORNER (14, 32),<br>LIP CORNER (30, 33)<br>|

### Тестовое изображение 14

Источник: набор данных [Интернет][internet_kerzhakov]

Разрешение: 353 x 366

<div style='float: center'>
<img width="200" height="200" src="images\facial-landmarks-35-adas-1.png">
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

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
facial-landmarks-35-adas-0002 | Лицевые метки:<br>LEFT EYE (17, 22), (9, 22),<br>RIGHT EYE (30, 21), (39, 20),<br>NOSE (21, 33), (23, 37), (17, 35), (30, 34),<br>MOUTH (17, 44), (34, 42), (23, 41), (24, 48),<br>LEFT EYEBROW (6, 17), (11, 15), (18, 17),<br>RIGHT EYEBROW (27, 15), (35, 12), (43, 14),<br>FACE CONTOUR (5, 22), (5, 28), (6, 33), (8, 38), (10, 43), (12, 48), (16, 52), (20, 56), (25, 57), (33, 56), (39, 53), (44, 48), (49, 43), (51, 38), (52, 31), (53, 25), (53, 18)<br>| Лицевые метки:<br>LEFT EYE (17, 22), (9, 22),<br>RIGHT EYE (30, 21), (39, 20),<br>NOSE (21, 33), (23, 37), (17, 35), (30, 34),<br>MOUTH (17, 44), (34, 42), (23, 41), (24, 48),<br>LEFT EYEBROW (6, 17), (11, 15), (18, 17),<br>RIGHT EYEBROW (27, 15), (35, 12), (43, 14),<br>FACE CONTOUR (5, 22), (5, 28), (6, 33), (8, 38), (10, 43), (12, 48), (16, 52), (20, 56), (25, 57), (33, 56), (39, 53), (44, 48), (49, 43), (51, 38), (52, 31), (53, 25), (53, 18)<br>|

### Тестовое изображение 15

Источник: набор данных [CityScapes][cityscapes] 

Разрешение: 199 x 436

<div style='float: center'>
<img width="100" height="225"src="images\person-attributes-recognition-crossroad-01.png">
</div>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
person-attributes-recognition-crossroad-0230 | <img src="recognition\out_person_attributes_sync_1.bmp"> | <img src="recognition\out_person_attributes_async_1.bmp"> |

### Тестовое изображение 16

Источник: набор данных [CityScapes][cityscapes] 

Разрешение: 218 x 510

<div style='float: center'>
<img width="100" height="225"src="images\person-attributes-recognition-crossroad-02.png">
</div>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
person-attributes-recognition-crossroad-0230 | <img src="recognition\out_person_attributes_sync_2.bmp"> | <img src="recognition\out_person_attributes_async_2.bmp"> |

### Тестовое изображение 17

Источник: набор данных [BKHD][...] 

Разрешение: 60 x 60

<div style='float: center'>
<img src="images\out_head_pose.bmp">
<img src="recognition\out_head_pose_1_sync.bmp">
</div>

   Название модели   |  Python (синхронный режим, реализация)  |  Python (асинхронный режим, реализация)|
----------------------|-----------------------------------------|-----------------------------------------|
head-pose-estimation-adas-0001 | <img src="recognition\out_head_pose_1_sync.bmp"> | <img src="recognition\out_head_pose_1_async.bmp"> |

[cityscapes]: https://www.cityscapes-dataset.com
[github_plate]: https://github.com/opencv/open_model_zoo/blob/master/models/intel/vehicle-license-plate-detection-barrier-0106/description/vehicle-license-plate-detection-barrier-0106.jpeg
[github_age_gender]: https://github.com/opencv/open_model_zoo/blob/master/models/intel/age-gender-recognition-retail-0013/description
[vgg_face2]:http://www.robots.ox.ac.uk/~vgg/data/vgg_face2/
[internet_kerzhakov]:http://positime.ru/the-russian-team-contender-for-the-world-cup-alexander-kerzhakov/40266
[internet_person_asl]:http://rasfokus.ru/photos/topweek/photo3138574.html
[internet_product]:https://bendoeslife.tumblr.com/post/48135155548/at-work-forgot-my-lunch-and-not-able-to-leave-at