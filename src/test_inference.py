import os
import argparse
from lxml import etree

class Model:
    def __init__(self, model):
        self.name = model[0]
        self.path = model[1]

class Dataset:
    def __init__(self, dataset):
        self.name = dataset[0]
        self.path = dataset[1]

class Parameters:
    def __init__(self, parameters):
        self.batchsize = parameters[0]
        self.mode = parameters[1]
        self.plugin = parameters[2]
        self.asyncrequest = parameters[3]
        self.synciteration = parameters[4]
        self.mininferencetime = parameters[5]

class Test:
    def __init__(self, args):
        self.model = args[0]
        self.dataset = args[1]
        self.parameters = args[2]
        
def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type = str, dest = 'path_to_config',
        help = 'Path to folder with config')
    
    config = parser.parse_args().path_to_config

    if config is None:
        config = os.path.join(os.getcwd(), 'config.xml')
    else:
        config = os.path.join(config, 'config.xml')
    
    if not os.path.isfile(config):
        raise ValueError('Config not found!')
    
    return config

def process_config(config):
    with open(config) as file:
        openconfig = file.read()
    
    utf_parser = etree.XMLParser(encoding='utf-8')
    root = etree.fromstring(openconfig.encode('utf-8'), parser = utf_parser)
    
    TestList = []
    
    for Tag in root.getchildren():
    
        tmp = []
        
        for TestParameter in Tag.getchildren():
            childrens = []
            for Parameter in TestParameter.getchildren():
                childrens.append(Parameter.text)
                
            if TestParameter.tag == 'Model':
                model = Model(childrens)
                tmp.append(model)
                
            if TestParameter.tag == 'Dataset':
                dataset = Dataset(childrens)
                tmp.append(dataset)
                
            if TestParameter.tag == 'Parameters':
                parameters = Parameters(childrens)
                tmp.append(parameters)
                
        test = Test(tmp)
        TestList.append(test)
    
    return TestList

def test_inference(TestList):
    output_data = []
    
    for i in range(len(TestList)):
        if TestList[i].parameters.mode == 'Sync':
            #call sync test
            output_data.append([])
        else:
            #call async test
            output_data.append([])
        
    return output_data
    
if __name__ == "__main__":
    try:
        config = build_parser()
    except Exception as Error:
        print('Error! : {}'.format(str(Error)))
    TestList = process_config(config)
    Output = test_inference(TestList)