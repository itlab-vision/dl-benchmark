import os
from lxml import etree


class model:
    def _parameter_not_is_none(self, parameter):
        if not parameter is None:
            return True
        return False


    def __init__(self, name, path, weight_type):
        self.name = None
        self.model = None
        self.weight = None
        self.datatype = None
        if self._parameter_not_is_none(name):
            self.name = name
        else:
            raise ValueError('Model name is required parameter.')
        if self._parameter_not_is_none(path):    
            for file in os.listdir(path):
                if file.endswith('.xml'):
                    self.model = os.path.join(path, file)
                if file.endswith('.bin'):            
                    self.weight = os.path.join(path, file)
            if (self.model is None) or (self.weight is None):
                raise ValueError('Wrong model IR format. \
                    The folder should contain .xml and .bin files for only one model.')
        else:
            raise ValueError('Path to folder with IR format model is required parameter.')
        if self._parameter_not_is_none(weight_type):
            self.datatype = weight_type
        else:
            raise ValueError('Weight type is required parameter.')


class dataset:
    def _parameter_not_is_none(self, parameter):
        if not parameter is None:
            return True
        return False


    def __init__(self, name, path):
        self.name = None
        self.path = None
        if self._parameter_not_is_none(name):
            self.name = name
        else:
            raise ValueError('Dataset name is required parameter.')
        if self._parameter_not_is_none(path):
            if os.path.isdir(path):
                self.path = path
            else:
                raise ValueError('Wrong path to folder with dataset')
        else:
            raise ValueError('Path to dataset is required parameter.')


class parameters:
    def _parameter_not_is_none(self, parameter):
        if not parameter is None:
            return True
        return False


    def _int_value_is_correct(self, int_value):
        for i in range(len(int_value)):
            if (i < 0) or (9 < i):
                return False
        return True


    def _float_value_is_correct(self, float_value):
        for i in float_value.split('.'):
            if not self._int_value_is_correct(i):
                return False
        return True


    def _mode_is_correct(self, mode):
        const_correct_mode = ['sync', 'async']
        if mode.lower() in const_correct_mode:
            return True
        return False


    def _device_is_correct(self, device):
        const_correct_devices = ['CPU', 'GPU', 'MYRIAD', 'FPGA']
        if device.upper() in const_correct_devices:
            return True
        return False


    def _extension_path_is_correct(self, extension):
        if not self._parameter_not_is_none(extension) or os.path.exists(extension):
            return True
        return False


    def __init__(self, batch_size, mode, device, extension, async_request_count, iterarion_count, thread_count, stream_count, min_inference_time):
        self.batch_size = None
        self.mode = None
        self.device = None
        self.extension = None
        self.async_request = None
        self.iteration = None
        self.nthreads = None
        self.nstreams = None
        self.min_inference_time = None
        if self._parameter_not_is_none(batch_size) and self._int_value_is_correct(batch_size):
            self.batch_size = int(batch_size)
        else:
            raise ValueError('Batch size is required parameter. \
                Batch size can only take values: integer greater than zero.')
        if self._mode_is_correct(mode):
            self.mode = mode.title()
        else:
            raise ValueError('Mode is required parameter. \
                Mode can only take values: Sync, Async.')
        if self._device_is_correct(device):
            self.device = device.upper()
        else:
            raise ValueError('Device is required parameter. \
                Device can only take values: CPU, GPU, FPGA, MYRIAD.')
        if self._extension_path_is_correct(extension):
            self.extension = extension
        else:
            raise ValueError('Wrong extension path for device. File not found.')
        if self._parameter_not_is_none(iterarion_count) and self._int_value_is_correct(iterarion_count):
            self.iteration = int(iterarion_count)
        else:
            raise ValueError('Iteration count is required parameter. \
                Iteration count can only take values: integer greater than zero.')
        if self.mode == 'Sync':
            if self._parameter_not_is_none(thread_count):
                if self._int_value_is_correct(thread_count):
                    self.nthreads = int(thread_count)
                else:
                    raise ValueError('Thread count can only take values: integer greater than zero.')
            if self._parameter_not_is_none(min_inference_time) and self._float_value_is_correct(min_inference_time):
                self.min_inference_time = float(min_inference_time)
            else:
                raise ValueError('Min inference time is required parameter for sync mode. \
                    Min inference time can only take values: float greater than zero.')
        if self.mode == 'Async':
            if self._parameter_not_is_none(async_request_count):
                if self._int_value_is_correct(async_request_count):
                    self.async_request = async_request_count
                else:
                    raise ValueError('Async requiest count can only take values: integer greater than zero.')
            if self._parameter_not_is_none(stream_count):
                if self._int_value_is_correct(stream_count):
                    self.nstreams = stream_count
                else:
                    raise ValueError('Stream count can only take values: integer greater than zero.')


class test:
    def __init__(self, model, dataset, parameter):
        self.model = model
        self.dataset = dataset
        self.parameter = parameter


def process_config(config, log):
    with open(config) as file:
        openconfig = file.read()
    utf_parser = etree.XMLParser(encoding = 'utf-8')
    root = etree.fromstring(openconfig.encode('utf-8'), parser = utf_parser)
    list = []
    test_number = 0
    for tag in root.getchildren():
        test_number += 1
        try:
            test_parameters = ['Model', 'Dataset', 'Parameters']
            for child in tag.getchildren():
                if child.tag == 'Model':
                    options = ['Name', 'Path', 'Weight type']
                    i = 0
                    for option in child.getchildren():
                        options[i] = option.text
                        i += 1
                    test_parameters[0] = model(*options)
                if child.tag == 'Dataset':
                    options = ['Name', 'Path']
                    i = 0
                    for option in child.getchildren():
                        options[i] = option.text
                        i += 1
                    test_parameters[1] = dataset(*options)
                if child.tag == 'Parameters':
                    options = ['Batch Size', 'Mode', 'Device', 'Extension', 
                               'Async Request Count', 'Iterarions', 'Threads', 
                               'Streams', 'Min Infer Time']
                    i = 0
                    for option in child.getchildren():
                        options[i] = option.text
                        i += 1
                    test_parameters[2] = parameters(*options)
        except ValueError as valerr:
            log.warning('Test {} not added to test list: {}'.format(test_number, valerr))
            continue
        list.append(test(*test_parameters))
    return list