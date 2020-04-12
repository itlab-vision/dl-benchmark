from PyQt5.QtWidgets import *
from objects import *


class TableModel(QTableWidget):
    def __init__(self):
        super().__init__()
        self._models = []
        self._count_col = 3
        self._count_row = 50
        self._headers = ["Название модели", "Тип модели", "Абсолютный путь"]
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self._headers)
        self.__resize_columns()
        self.clear_table()

    def __resize_columns(self):
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.resizeColumnsToContents()

    def __create_cell(self, text):
        cell = QTableWidgetItem(text)
        return cell

    def clear_table(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self.__create_cell(''))

    def update_table(self):
        self.clear_table()
        count = 0
        for model in self._models:
            self.setItem(count, 0, self.__create_cell(model.name))
            self.setItem(count, 1, self.__create_cell(model.type))
            self.setItem(count, 2, self.__create_cell(model.path))
            count += 1
        self.resizeColumnsToContents()

    def add_model(self, model):
        self._models.append(model)
        self.setItem(len(self._models), 0, self.__create_cell(model.name))
        self.setItem(len(self._models), 1, self.__create_cell(model.type))
        self.setItem(len(self._models), 2, self.__create_cell(model.path))

    def remove_model(self, number):
        self._model.pop(number - 1)
        self.update_table()


class TableData(QTableWidget):
    def __init__(self):
        super().__init__()
        self._data = []
        self._count_col = 2
        self._count_row = 20
        self._headers = ['Название датасета', 'Абсолютный путь']
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self._headers)
        self.__resize_columns()
        self.clear_table()

    def __resize_columns(self):
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.resizeColumnsToContents()

    def __create_cell(self, text):
        cell = QTableWidgetItem(text)
        return cell

    def clear_table(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self.__create_cell(''))

    def update_table(self):
        self.clear_table()
        count = 0
        for data in self._data:
            self.setItem(count, 0, self.__create_cell(data.name))
            self.setItem(count, 1, self.__create_cell(data.path))
            count += 1
        self.resizeColumnsToContents()

    def add_data(self, data):
        self._data.append(data)
        self.setItem(len(self._data), 0, self.__create_cell(data.name))
        self.setItem(len(self._data), 1, self.__create_cell(data.path))

    def remove_data(self, number):
        self._data.pop(number - 1)
        self.update_table()


class ParametersTable(QTableWidget):
    def __init__(self):
        super().__init__()
        pass
