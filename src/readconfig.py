import os
from lxml import etree

class model:
    def __init__(self, model):
        self.name = model[0]
        file = os.listdir(model[1])
		self.model = os.path.join(model[1], file.endswith('.bin'))
		self.weigh = os.path.join(model[1], file.endswith('.xml'))

class dataset:
    def __init__(self, dataset):
        self.name = dataset[0]
        self.path = dataset[1]

class parameter:
    def __init__(self, parameters):
        self.batchsize = parameters[0]
        self.mode = parameters[1]
        self.plugin = parameters[2]
        self.asyncrequest = parameters[3]
        self.iteration = parameters[4]
        self.mininferencetime = parameters[5]

class test:
    def __init__(self, args):
        self.model = args[0]
        self.dataset = args[1]
        self.parameters = args[2]
    
def process_config(config):
    with open(config) as file:
        openconfig = file.read()
    
    utf_parser = etree.XMLParser(encoding = 'utf-8')
    root = etree.fromstring(openconfig.encode('utf-8'), parser = utf_parser)
    
    test_list = []
    
    for tag in root.getchildren():
    
        tmp = []
        
        for test_parameter in tag.getchildren():
            childrens = []
            for param in test_parameter.getchildren():
                childrens.append(param.text)
                
            if test_parameter.tag == 'Model':
                mdl = model(childrens)
                tmp.append(mdl)
                
            if test_parameter.tag == 'Dataset':
                data = dataset(childrens)
                tmp.append(data)
                
            if test_parameter.tag == 'Parameters':
                param = parameter(childrens)
                tmp.append(param)
                
        t = test(tmp)
        test_list.append(t)
    
    return test_list