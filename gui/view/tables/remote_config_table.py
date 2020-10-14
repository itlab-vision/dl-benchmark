from view.tables.table import Table


class RemoteConfigTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.__parameters = []
        self._count_col = 8
        self._count_row = 100
        self.__headers = ['IP', 'Login', 'Password', 'OS', 'FTPClientPath', 'BenchmarkConfig', 'LogFile', 'ResultFile']
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.__headers)
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
            self.setItem(i, 4, self._create_cell(computers[i].path_to_ftp_client))
            self.setItem(i, 5, self._create_cell(computers[i].benchmark_config))
            self.setItem(i, 6, self._create_cell(computers[i].log_file))
            self.setItem(i, 7, self._create_cell(computers[i].res_file))
            count += 1
