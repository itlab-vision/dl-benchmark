from xml.etree import ElementTree as ET


class TVMQuantizationConfigParser:
    def __init__(self, config_path):
        self.config_path = config_path

    def _parse_xml(self):
        return ET.parse(self.config_path).getroot()

    def _create_list_from_xml_nodes(self, nodes):
        ls = []
        for i, node in enumerate(nodes):
            ls.append({node.tag: {}})
            for subnode in node:
                ls[i][node.tag][subnode.tag] = subnode.text
        return ls

    def parse(self):
        res = []
        xml = self._parse_xml()
        for config in xml:
            model = config.find('Model')
            dataset = config.find('Dataset')
            quantparam = config.find('QuantizationParameters')
            res.append(self._create_list_from_xml_nodes([model, dataset, quantparam]))
        return res
