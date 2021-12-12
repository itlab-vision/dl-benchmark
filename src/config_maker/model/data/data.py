import os
from xml.dom import minidom
from .dataset import Dataset  # pylint: disable=E0402
from tags import CONFIG_DATASETS_TAG  # pylint: disable=E0401


class Data:
    def __init__(self):
        self.__data = []

    def get_data(self):
        return self.__data

    def get_dataset_list_in_strings(self):
        data_list = []
        for data in self.__data:
            data_list.append(data.get_str())
        return data_list

    def set_data(self, data):
        self.__data.clear()
        for dataset in data:
            if dataset not in self.__data:
                self.__data.append(dataset)

    def add_dataset(self, name, path):
        self.__data.append(Dataset(name, path))

    def change_dataset(self, row, name, path):
        self.__data[row] = Dataset(name, path)

    def delete_dataset(self, index):
        self.__data.pop(index)

    def delete_data(self, indexes):
        for index in indexes:
            if index < len(self.__data):
                self.delete_dataset(index)

    def copy_data(self, indexes):
        for index in indexes:
            if index < len(self.__data):
                self.__data.append(self.__data[index])

    def clear(self):
        self.__data.clear()

    def parse_config(self, path_to_config):
        parsed_config = minidom.parse(path_to_config)
        self.__data = Dataset.parse(parsed_config)

    def create_config(self, path_to_config):
        if len(self.__data) == 0:
            return False
        file = minidom.Document()
        DOM_ROOT_TAG = file.createElement(CONFIG_DATASETS_TAG)
        file.appendChild(DOM_ROOT_TAG)
        for model in self.__data:
            DOM_ROOT_TAG.appendChild(model.create_dom(file))
        xml_str = file.toprettyxml(indent="\t", encoding="utf-8")
        with open(path_to_config, 'wb') as f:
            f.write(xml_str)
        return os.path.exists(path_to_config)
