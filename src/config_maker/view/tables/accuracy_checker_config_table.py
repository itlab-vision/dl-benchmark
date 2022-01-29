from .table import Table  # pylint: disable=E0402
# pylint: disable-next=E0401
from tags import CONFIG_MODEL_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_DEVICE_TAG, CONFIG_CONFIG_TAG


class AccuracyCheckerConfigTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self.headers = [CONFIG_MODEL_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_DEVICE_TAG, CONFIG_CONFIG_TAG]
        self._count_col = len(self.headers)
        self._count_row = 350
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.headers)
        self._resize_columns()
        self.clear()

    def update(self, tests):
        self.clear()
        count = 0
        for i in range(len(tests)):
            test_dict = tests[i].get_values_dict()
            self.setItem(i, 0, self._create_cell(test_dict[CONFIG_MODEL_TAG].get_str()))
            self.setItem(i, 1, self._create_cell(test_dict[CONFIG_FRAMEWORK_TAG]))
            self.setItem(i, 2, self._create_cell(test_dict[CONFIG_DEVICE_TAG]))
            self.setItem(i, 3, self._create_cell(test_dict[CONFIG_CONFIG_TAG]))
            count += 1
