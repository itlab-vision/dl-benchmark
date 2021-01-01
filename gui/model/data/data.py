from .dataset import Dataset  # pylint: disable=E0402


class Data:
    def __init__(self):
        self.__data = []

    def get_data(self):
        return self.__data

    def get_data_list(self):
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

    def clear(self):
        self.__data.clear()
