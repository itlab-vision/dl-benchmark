import os
from lxml import etree


class model:
    def __init__(self, mdl):
        self.name = mdl[0]
        self.model = None
        self.weight = None
        for file in os.listdir(mdl[1]):
            if file.endswith('.xml'):
                self.model = os.path.join(mdl[1], file)
            if file.endswith('.bin'):            
                self.weight = os.path.join(mdl[1], file)
        if self.model is None:
            raise ValueError('Wrong path to model file')
        if self.weight is None:
            raise ValueError('Wrong path to model weight file')


class dataset:
    def __init__(self, dataset):
        self.name = dataset[0]
        self.path = dataset[1]
        if not os.path.isdir(self.path):
            raise ValueError('Wrong path to folder with dataset')


class parameters:
    def __init__(self, parameter):
        const_correct_mode = ['sync', 'async']
        if parameter[1].lower() in const_correct_mode:
            self.mode = parameter[1]
        else:
            raise ValueError('Wrong mode')
        if parameter[0] == 'None':
            if self.mode != 'async':
                self.batch_size = 'None'
            else:
                raise ValueError('Wrong batch size')
        else:
            self.batch_size = int(parameter[0])
        self.plugin = parameter[2].upper()
        if parameter[3] == 'None':
            if self.mode != 'async':
                self.async_request = 'None'
            else:
                raise ValueError('Wrong async request number')
        else:
            self.async_request = int(parameter[3])
        if parameter[4] != 'None':
            self.iteration = int(parameter[4])
        else:
            raise ValueError('Wrong iteration number')
        if parameter[5] != 'None':
            self.nthreads = int(parameter[5])
        else:
            self.nthreads = parameter[5]
        if parameter[6] == 'None':
            if self.mode == 'sync':
                raise ValueError('Wrong min inference time number')
            else:
                self.min_inference_time = parameter[6]
        else:
            self.min_inference_time = float(parameter[6])


class test:
    def __init__(self, arg):
        self.model = arg[0]
        self.dataset = arg[1]
        self.parameter = arg[2]


def process_config(config):
    with open(config) as file:
        openconfig = file.read()
    utf_parser = etree.XMLParser(encoding = 'utf-8')
    root = etree.fromstring(openconfig.encode('utf-8'), parser = utf_parser)
    test_list = []
    for test_tag in root.getchildren():
        test_parameters = []
        for test_parameter in test_tag.getchildren():
            options = []
            for option in test_parameter.getchildren():
                if option.text is None:
                    option.text = 'None'
                options.append(option.text)
            if test_parameter.tag == 'Model':
                mdl = model(options)
                test_parameters.append(mdl)
            if test_parameter.tag == 'Dataset':
                data = dataset(options)
                test_parameters.append(data)
            if test_parameter.tag == 'Parameters':
                parameter = parameters(options)
                test_parameters.append(parameter)
        tmp_test = test(test_parameters)
        test_list.append(tmp_test)
    return test_list