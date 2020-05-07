from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from models.deploy_config import *


class TableModel(QTableWidget):
    def __init__(self):
        super().__init__()
        self._models = []
        self._count_col = 5
        self._count_row = 50
        self._headers = ['Task', 'Name', 'Precision', 'SourceFramework', 'Path']
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
        cell.setFlags(QtCore.Qt.ItemIsEnabled)
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
            self.setItem(count, 3, self.__create_cell(model.path))
            self.setItem(count, 4, self.__create_cell(model.path))
            count += 1
        self.resizeColumnsToContents()

    def add_model(self, model):
        self._models.append(model)
        self.setItem(len(self._models), 0, self.__create_cell(model.name))
        self.setItem(len(self._models), 1, self.__create_cell(model.type))
        self.setItem(len(self._models), 2, self.__create_cell(model.path))
        self.setItem(len(self._models), 3, self.__create_cell(model.path))
        self.setItem(len(self._models), 4, self.__create_cell(model.path))

    def remove_model(self, number):
        self._model.pop(number - 1)
        self.update_table()


class TableData(QTableWidget):
    def __init__(self):
        super().__init__()
        self._data = []
        self._count_col = 2
        self._count_row = 20
        self._headers = ['Name', 'Path']
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
        cell.setFlags(QtCore.Qt.ItemIsEnabled)
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


class TableTestConfig(QTableWidget):
    def __init__(self):
        super().__init__()
        self._tests = []
        self._count_col = 12
        self._count_row = 20
        self._headers = ['Model', 'Dataset', 'InferenceFramework', 'BatchSize', 'Device', 'IterationCount',
                         'TestTimeLimit', 'Mode', 'Extension', 'AsyncRequestCount', 'ThreadCount', 'StreamCount']
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
        cell.setFlags(QtCore.Qt.ItemIsEnabled)
        return cell

    def clear_table(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self.__create_cell(''))

    def update_table(self):
        self.clear_table()
        count = 0
        # заполнение
        self.resizeColumnsToContents()

    def add_test(self, test):
        self._test.append(test)
        # поэлементно

    def remove_test(self, number):
        self._test.pop(number - 1)
        self.update_table()


class TableRemoteConfig(QTableWidget):
    def __init__(self):
        super().__init__()
        self._parameters = []
        self._count_col = 8
        self._count_row = 100
        self._headers = ['IP', 'Login', 'Password', 'OS', 'FTPClientPath', 'BenchmarkConfig', 'LogFile', 'ResultFile']
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
        cell.setFlags(QtCore.Qt.ItemIsEnabled)
        return cell

    def clear_table(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self.__create_cell(''))

    def update_table(self):
        self.clear_table()
        count = 0
        # заполнение
        self.resizeColumnsToContents()

    def add_test(self, parameter):
        self._parameters.append(parameter)
        # поэлементно

    def remove_test(self, number):
        self._parameters.pop(number - 1)
        self.update_table()


class TableDeployConfig(QTableWidget):
    def __init__(self):
        super().__init__()
        self._count_col = 5
        self._count_row = 100
        self._headers = ['IP', 'Login', 'Password', 'OS', 'DownloadFolder']
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self._headers)
        self.__resize_columns()
        self.clear()

    def __resize_columns(self):
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        self.resizeColumnsToContents()

    def __create_cell(self, text):
        cell = QTableWidgetItem(text)
        cell.setFlags(QtCore.Qt.ItemIsEnabled)
        return cell

    def clear(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self.__create_cell(''))

    def update(self, computers):
        self.clear()
        count = 0
        for i in range(len(computers)):
            self.setItem(i, 0, self.__create_cell(computers[i].ip))
            self.setItem(i, 1, self.__create_cell(computers[i].login))
            self.setItem(i, 2, self.__create_cell(computers[i].password))
            self.setItem(i, 3, self.__create_cell(computers[i].os))
            self.setItem(i, 4, self.__create_cell(computers[i].download_folder))
            count += 1
        self.resizeColumnsToContents()
