from PyQt5.QtWidgets import *


class TableModel(QTableWidget):
    def __init__(self):
        super().__init__()
        self._model = []
        self._headers = ['Название модели', 'Абсолютный путь']
        self._count_col = 2
        self._count_row = 50
        self.setHorizontalHeaderLabels(self._headers)
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.clear_table()

    def __create_cell(self, text):
        cell = QTableWidgetItem(text)
        return cell

    def clear_table(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self.__create_cell(''))

    def update_table(self):
        pass

    def add_model(self, model):
        pass

    def remove_model(self, number):
        self._model.pop(number - 1)
        self.update_table()


class TableData(QTableWidget):
    def __init__(self):
        super().__init__()
        self._data = []
        self._headers = ['Название датасета', 'Абсолютный путь']
        self._count_col = 2
        self._count_row = 20
        self.setHorizontalHeaderLabels(self._headers)
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.clear_table()

    def __create_cell(self, text):
        cell = QTableWidgetItem(text)
        return cell

    def clear_table(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self.__create_cell(''))

    def update_table(self):
        pass

    def add_data(self, data):
        pass

    def remove_data(self, number):
        self._data.pop(number - 1)
        self.update_table()


class ParametersTable(QTableWidget):
    def __init__(self):
        super().__init__()
        pass