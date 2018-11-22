import os
import argparse
from lxml import etree

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
        raise ValueError('Config not fount!')
    
    return config

def process_config(config):
    print(config)
    with open(config) as file:
        xml = file.read()
    
    utf_parser = etree.XMLParser(encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser = utf_parser)
    
    for appt in root.getchildren():
        for elem in appt.getchildren():
            for el in elem.getchildren():
        
if __name__ == "__main__":
    config = build_parser()
    process_config(config)