from .table import Table


class DataTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self._count_col = 2
        self._count_row = 100
        self.__headers = ['Name', 'Path']
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()

    def update(self, data):
        self.clear()
        count = 0
        for i in range(len(data)):
            self.setItem(i, 0, self._create_cell(data[i].name))
            self.setItem(i, 1, self._create_cell(data[i].path))
            count += 1
