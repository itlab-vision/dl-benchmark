import os
from lxml import etree

class model:
    def __init__(self, mdl):
        self.name = mdl[0]
        self.model = None
        self.weigh = None
        for file in os.listdir(mdl[1]):
            if file.endswith('.bin'):
                self.model = os.path.join(mdl[1], file)
            if file.endswith('.xml'):            
                self.weigh = os.path.join(mdl[1], file)
        if self.model is None:
            raise ValueError('Wrong path to model file')
        if self.weigh is None:
            raise ValueError('Wrong path to model weigh file')

class dataset:
    def __init__(self, dataset):
        self.name = dataset[0]
        self.path = dataset[1]

class parameters:
    def __init__(self, parameter):
        self.batchsize = parameter[0]
        self.mode = parameter[1]
        self.plugin = parameter[2]
        self.asyncrequest = parameter[3]
        self.iteration = parameter[4]
        self.mininferencetime = parameter[5]

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
                    raise ValueError('Configuration parse failed')
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