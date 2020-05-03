from lxml import etree


class machine:
    def __init__(self, params):
        self.ip = params[0]
        self.login = params[1]
        self.password = params[2]
        self.os_type = params[3]
        self.path_to_ftp_client = params[4]
        self.path_to_OpenVINO_env = params[5]
        self.benchmark_config = params[6]
        self.benchmark_executor = params[7]
        self.log_file = params[8]
        self.res_file = params[9]


def parse_config(config):
    with open(config) as file:
        openconfig = file.read()
    utf_parser = etree.XMLParser(encoding = 'utf-8')
    root = etree.fromstring(openconfig.encode('utf-8'), parser = utf_parser)
    machine_list = []
    for machine_tag in root.getchildren():
        machine_parameters = [None] * 10
        for machine_parameter in machine_tag.getchildren():
            if machine_parameter.tag == 'IP':
                machine_parameters[0] = machine_parameter.text
            if machine_parameter.tag == 'Login':
                machine_parameters[1] = machine_parameter.text
            if machine_parameter.tag == 'Password':
                machine_parameters[2] = machine_parameter.text
            if machine_parameter.tag == 'OS':
                machine_parameters[3] = machine_parameter.text
            if machine_parameter.tag == 'FTPClientPath':
                machine_parameters[4] = (machine_parameter.text)
            if machine_parameter.tag == 'OpenVINOEnvironmentPath':
                machine_parameters[5] = (machine_parameter.text)
            if machine_parameter.tag == 'BenchmarkConfig':
                machine_parameters[6] = (machine_parameter.text)
            if machine_parameter.tag == 'BenchmarkExecutor':
                machine_parameters[7] = (machine_parameter.text)
            if machine_parameter.tag == 'LogFile':
                machine_parameters[8] = (machine_parameter.text)
            if machine_parameter.tag == 'ResultFile':
                machine_parameters[9] = (machine_parameter.text)
        machine_list.append(machine(machine_parameters))
    return machine_list
