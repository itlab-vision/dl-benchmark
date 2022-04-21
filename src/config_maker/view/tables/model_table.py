from .table import Table  # pylint: disable=E0402


class ModelTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self._count_col = 6
        self._count_row = 250
        self.__headers = ['Task', 'Name', 'Precision', 'SourceFramework', 'ModelPath', 'WeightsPath']
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()
        self.clicked().connect(self.clicked_table)

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
