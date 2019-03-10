import os
from lxml import etree


class conversion_options:
    def __init__(self, args):
        self.modelfile = args[0]
        self.outdir = args[1]
        self.additional_options = args[2]


def process_config(config):
    with open(config) as file:
        openconfig = file.read()
    utf_parser = etree.XMLParser(encoding = 'utf-8')
    root = etree.fromstring(openconfig.encode('utf-8'), parser = utf_parser)
    conversion_list = []
    for model in root.getchildren():
        options_for_model = []
        for parameter in model.getchildren():
            if parameter.text is None:
                options_for_model.append('None')
            else:
                options_for_model.append(parameter.text)
        convert_opt = conversion_options(options_for_model)
        conversion_list.append(convert_opt)
    return conversion_list