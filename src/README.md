# How to use the converter.

**Использование конвертера**  
Конвертер запускается из коммандной строки и принимает на вход 3 аргумента.  
Список аргументов:  
	-m / --mo_dir <Путь до директории, где лежит Model Optimizer>  
	-i / --input_dir <Путь до директории, где лежат скаченные модели>  
	-d / --data_type <Допустимые аргументы: FP16/FP32/float/half>  
Пример запуска:  
	converter.py -m C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_optimizer -i C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_downloader -d FP32  
	converter.py --mo_dir C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_optimizer --input_dir C:\Intel\computer_vision_sdk_2018.3.343\deployment_tools\model_downloader --data_type FP32  
Предыдущие примеры эквивалентны.  
В случае, когда агрументы не переданы или переданы некорректно, конвертер сообщит об ошибке и закончит свою работу.  

**Сохранение результатов**  
Конвертер преобразует модели в промежуточное значение.  
Результаты работы конвертера находятся в директории: <Путь до модели>\ir\ <Точность, с которой модель была преобразована>  
Например:  
	<...>\deployment_tools\model_downloader\object_detection\common\ssd_mobilenet_v2_coco\tf\ssd_mobilenet_v2_coco_2018_03_29\ir\FP32  
В этой директории лежит модель ssd_mobilenet_v2_coco в своем промежуточном состоянии с точностью FP32  