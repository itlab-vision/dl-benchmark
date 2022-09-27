import copy
import json
import os

from parameters import AllParameters
from utils import get_correct_path


class ConfigParser:
    def __init__(self, json_config_file_path):
        if not os.path.isfile(json_config_file_path):
            raise ValueError('Wrong path to configuration file!')
        self.__config_path = get_correct_path(json_config_file_path)
        self.__pot_parameters = []
        self.__config_file_paths = []
        self.__folder_with_configs = 'quantization_config_files'
        if not os.path.isdir(self.__folder_with_configs):
            os.mkdir(self.__folder_with_configs)

    def parse(self):
        with open(self.__config_path, 'r') as config_file:
            all_params = AllParameters(json.load(config_file))
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
                indent=4
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
