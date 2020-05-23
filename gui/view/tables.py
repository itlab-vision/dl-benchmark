from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from models.models import *


class Table(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._selected_rows = []
        self.clicked.connect(self.clicked_table)

    def _resize_columns(self):
        header = self.horizontalHeader()
        self.resizeColumnsToContents()
        header.setStretchLastSection(True)

    def _create_cell(self, text):
        cell = QTableWidgetItem(text)
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        return cell

    def clicked_table(self):
        self._selected_rows = list(dict.fromkeys([index.row() for index in self.selectedIndexes()]))
        self._selected_rows.sort(reverse=True)

    def get_selected_rows(self):
        return self._selected_rows

    def remove_selection(self):
        for index in self.selectedIndexes():
            self.itemFromIndex(index).setSelected(False)


class TableModel(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.__count_col = 6
        self.__count_row = 50
        self.__headers = ['Task', 'Name', 'Precision', 'SourceFramework', 'ModelPath', 'WeightsPath']
        self.setColumnCount(self.__count_col)
        self.setRowCount(self.__count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()
        self.clicked.connect(self.clicked_table)

    def clear(self):
        for i in range(self.__count_row):
            for j in range(self.__count_col):
                self.setItem(i, j, self._create_cell(''))

    def update(self, models):
        self.clear()
        count = 0
        for i in range(len(models)):
            self.setItem(i, 0, self._create_cell(models[i].task))
            self.setItem(i, 1, self._create_cell(models[i].name))
            self.setItem(i, 2, self._create_cell(models[i].precision))
            self.setItem(i, 3, self._create_cell(models[i].framework))
            self.setItem(i, 4, self._create_cell(models[i].model_path))
            self.setItem(i, 5, self._create_cell(models[i].weights_path))
            count += 1


class TableData(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.__count_col = 2
        self.__count_row = 100
        self.__headers = ['Name', 'Path']
        self.setColumnCount(self.__count_col)
        self.setRowCount(self.__count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()

    def clear(self):
        for i in range(self.__count_row):
            for j in range(self.__count_col):
                self.setItem(i, j, self._create_cell(''))

    def update(self, data):
        self.clear()
        count = 0
        for i in range(len(data)):
            self.setItem(i, 0, self._create_cell(data[i].name))
            self.setItem(i, 1, self._create_cell(data[i].path))
            count += 1


class TableTestConfig(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.__tests = []
        self.__count_col = 12
        self.__count_row = 20
        self.__headers = ['Model', 'Dataset', 'InferenceFramework', 'BatchSize', 'Device', 'IterationCount',
                         'TestTimeLimit', 'Mode', 'Extension', 'AsyncRequestCount', 'ThreadCount', 'StreamCount']
        self.setColumnCount(self.__count_col)
        self.setRowCount(self.__count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()

    def clear(self):
        for i in range(self.__count_row):
            for j in range(self.__count_col):
                self.setItem(i, j, self._create_cell(''))

    def update(self):
        self.clear()
        count = 0
        # заполнение


class TableRemoteConfig(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.__parameters = []
        self.__count_col = 8
        self.__count_row = 100
        self.__headers = ['IP', 'Login', 'Password', 'OS', 'FTPClientPath', 'BenchmarkConfig', 'LogFile', 'ResultFile']
        self.setColumnCount(self.__count_col)
        self.setRowCount(self.__count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()
        self.clicked.connect(self.clicked_table)

    def clear(self):
        for i in range(self.__count_row):
            for j in range(self.__count_col):
                self.setItem(i, j, self._create_cell(''))

    def update(self, computers):
        self.clear()
        count = 0
        for i in range(len(computers)):
            self.setItem(i, 0, self._create_cell(computers[i].ip))
            self.setItem(i, 1, self._create_cell(computers[i].login))
            self.setItem(i, 2, self._create_cell(computers[i].password))
            self.setItem(i, 3, self._create_cell(computers[i].os))
            self.setItem(i, 4, self._create_cell(computers[i].path_to_ftp_client))
            self.setItem(i, 5, self._create_cell(computers[i].benchmark_config))
            self.setItem(i, 6, self._create_cell(computers[i].log_file))
            self.setItem(i, 7, self._create_cell(computers[i].res_file))
            count += 1


class TableDeployConfig(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.__count_col = 5
        self.__count_row = 100
        self.__headers = ['IP', 'Login', 'Password', 'OS', 'DownloadFolder']
        self.__selected_rows = []
        self.setColumnCount(self.__count_col)
        self.setRowCount(self.__count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self._resize_columns()
        self.clear()
        self.clicked.connect(self.clicked_table)

    def clear(self):
        for i in range(self.__count_row):
            for j in range(self.__count_col):
                self.setItem(i, j, self._create_cell(''))

    def update(self, computers):
        self.clear()
        count = 0
        for i in range(len(computers)):
            self.setItem(i, 0, self._create_cell(computers[i].ip))
            self.setItem(i, 1, self._create_cell(computers[i].login))
            self.setItem(i, 2, self._create_cell(computers[i].password))
            self.setItem(i, 3, self._create_cell(computers[i].os))
            self.setItem(i, 4, self._create_cell(computers[i].download_folder))
            count += 1
