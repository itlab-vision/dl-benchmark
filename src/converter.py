import os
import sys
import argparse

#---------------Парсер аргументов---------------
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mo_dir', action = 'store', type = str, dest = 'path_to_mo', help = 'Path to model optimizer')
parser.add_argument('-i', '--input_dir', action = 'store', type = str, dest = 'path_to_models', help = 'Path to folder with models')
parser.add_argument('-o', '--output_dir', action = 'store', type = str, dest = 'path_to_convert', help = 'Path for save')
parser.add_argument('-d', '--data_type', action = 'store', type = str, dest = 'data_type', help = 'Data type for convert models')
args = parser.parse_args()
#-----------------------------------------------

#---------------Расширения моделей--------------
file_extensions = ['.caffemodel', '.pb', '.json']
data_types = [ 'FP16', 'FP32', 'half', 'float']
#-----------------------------------------------

#--------Проверка корректности аргументов-------
def parse_arg():
	error = 0
	if (os.path.exists(str(args.path_to_mo))):
		if(os.path.isdir(str(args.path_to_mo))):
			if('mo.py' not in os.listdir(args.path_to_mo)):
				error += 1
				print ('Model optimizer not found!')
		else:
			error += 1
			print('Wrong path to model optimizer')
	
	if(os.path.isdir(str(args.path_to_models))):
		if not(os.path.exists(str(args.path_to_models))):
			error += 1
			print('Wrong path to folder with models')
	else:
		error += 1
		print('Wrong path to folder with models')
		
	if(os.path.isdir(str(args.path_to_convert))):
		if not(os.path.exists(str(args.path_to_convert))):
			os.makedirs(path_to_convert)
	else:
		error += 1
		print('Wrong path for save models')
		
	if(args.data_type not in data_types):
		error += 1
		print('Wrong data type')
		
	if (error!=0):
		print ('Expression expected : converter.py --mo_dir <path to model oprimizer> --input_dir <path to folder with models> --output_dir <path to save> --data_type <data type for convert model>')
		sys.exit()

	result = [args.path_to_mo, args.path_to_models, args.path_to_convert, args.data_type]
	return result
#--------------------------------------------

#---------Функция конвертации моделей--------
def models_converter(arg):
	count = 0
	arg[0] = arg[0] + '\\mo.py'
	for root, dirs, files in os.walk(arg[1]):
		for file in files:
			if file.endswith(file_extensions[0]):
				model = os.path.join(root, file)
				count += 1
				command = arg[0] + ' --input_model ' + model + ' --output_dir ' + arg[2] + ' --data_type ' + arg[3]
				os.system(command)
			if file.endswith(file_extensions[1]):
				model = os.path.join(root, file)
				count += 1
				command = arg[0] + ' --input_model_is_text ' + model + ' --output_dir ' + arg[2] + ' --data_type ' + arg[3]
				os.system(command)
			if file.endswith(file_extensions[2]):
				model = os.path.join(root, file)
				count += 1
				command = arg[0] + ' --input_symbol ' + model + ' --output_dir ' + arg[2] + ' --data_type ' + arg[3]
				os.system(command)
	if (count == 0):
		print('No models')
		sys.exit()
	return 0
#-------------------------------------------

arg = parse_arg()
models_converter(arg)
print('Convert complited!')