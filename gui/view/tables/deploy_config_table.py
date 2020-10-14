# from PyQt5.QtWidgets import QAbstractScrollArea
from view.tables.table import Table


class DeployConfigTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self._count_col = 5
        self._count_row = 100
        self.__headers = ['IP', 'Login', 'Password', 'OS', 'DownloadFolder']
        self.__selected_rows = []
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        #self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self._resize_columns()
        self.clear()
        self.clicked.connect(self.clicked_table)

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
