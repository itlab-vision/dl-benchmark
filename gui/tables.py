from PyQt5.QtWidgets import *


class Table(QTableWidget):
    def __init__(self):
        super().__init__()
        self._items = []
        self._count_col = 5
        self._count_row = 10
        self.setColCount(self._count_col)
        self.setRowCount(self._count_row)
        self.clear_table()

    def __create_cell(self, text):
        cell = QTableWidgetItem(text)
        return cell

    def clear_table(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self.__create_cell(''))


class ModelTable(Table):
    def __init__(self):
        super().__init__()


class DataTable(Table):
    def __init__(self):
        super().__init__()


class ParametersTable(Table):
    def __init__(self):
        super().__init__()