import copy
import json
import os

from xml.etree import ElementTree as ET
from parameters import AllParameters
from utils import get_correct_path, camel_to_snake, get_typed_from_str


class ConfigParser:
    def __init__(self, config_file_path):
        if not os.path.isfile(config_file_path):
            raise ValueError('Wrong path to configuration file!')
        self.__config_path = get_correct_path(config_file_path)
        self.__pot_parameters = []
        self.__config_file_paths = []
        # self.__folder_with_configs = 'quantization_config_files'
        self.__configs_folder = 'quantization_config_files'
        self.__tmp_folder = 'tmp'
        if not os.path.isdir(self.__tmp_folder):
            os.mkdir(self.__tmp_folder)
        self.__folder_with_configs = os.path.join(self.__tmp_folder, self.__configs_folder)
        if not os.path.isdir(self.__folder_with_configs):
            os.mkdir(self.__folder_with_configs)

    def parse(self):
        with open(self.__config_path, 'r') as config_file:
            if self.__config_path[-4:] == '.xml':
                xml_config_file = ET.parse(self.__config_path)
                json_config_file = self.parse_xml_to_json(xml_config_file.getroot())
            elif self.__config_path[-5:] == '.json':
                json_config_file = json.load(config_file)
            else:
                raise ValueError('Wrong path to configuration file!')
            all_params = AllParameters(json_config_file)
        for m_params in all_params.models_list:
            config_file_path = self.__create_pot_config_file(m_params)
            self.__config_file_paths.append(config_file_path)
            config_path = get_correct_path(config_file_path)
            pot_params = m_params.get_pot_parameters()
            pot_params.rewrite_config_path(config_path)
            self.__pot_parameters.append(copy.copy(pot_params))
        return self.__pot_parameters

    def __create_pot_config_file(self, model_params):
        filename = model_params.get_config_json_filename()
        filename = os.path.join(self.__folder_with_configs, filename)
        with open(filename, 'w') as config_file:
            json.dump(
                model_params.get_config_parameters(),
                config_file,
                indent=4,
            )
        return os.path.abspath(filename)

    def clean(self):
        for config_file_path in self.__config_file_paths:
            if os.path.isfile(config_file_path):
                os.remove(config_file_path)
            else:
                raise ValueError('Wrong path to configuration file!')
        if os.path.isdir(self.__folder_with_configs):
            os.rmdir(self.__folder_with_configs)

    @staticmethod
    def parse_xml_to_json(xml_config):
        res = {}
        lists_names = ['algorithms', 'quantization_config']
        for child in list(xml_config):
            child_name = camel_to_snake(child.tag)

            if child_name == 'output_dir_path':
                child_name = 'output_dir'

            if len(list(child)) > 0:
                child_of_child = config_parser.parse_xml_to_json(child)
            else:
                child_text = child.text
                child_of_child = get_typed_from_str(child_text)

            if child_name in lists_names:
                if res.get(child_name) is None:
                    res[child_name] = []
                res[child_name].append(child_of_child)
            else:
                res[child_name] = child_of_child

        return res
