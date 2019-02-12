from lxml import etree


class machine:
    def __init__(self, params):
        self.ip = params[0]
        self.login = params[1]
        self.psw = params[2]
        self.os_type = params[3]
        self.client_path = params[4]


def parse_config(config):
    with open(config) as file:
        openconfig = file.read()
    utf_parser = etree.XMLParser(encoding = 'utf-8')
    root = etree.fromstring(openconfig.encode('utf-8'), parser = utf_parser)
    machine_list = []
    for machine_tag in root.getchildren():
        machine_parameters = []
        for machine_parameter in machine_tag.getchildren():
            if machine_parameter.tag == 'Ip':
                machine_parameters.append(machine_parameter.text)
            if machine_parameter.tag == 'Login':
                machine_parameters.append(machine_parameter.text)
            if machine_parameter.tag == 'Password':
                machine_parameters.append(machine_parameter.text)
            if machine_parameter.tag == 'Os_Type':
                machine_parameters.append(machine_parameter.text)
            if machine_parameter.tag == 'Client_Path':
                machine_parameters.append(machine_parameter.text)
        machine_list.append(machine(machine_parameters))
    return machine_list