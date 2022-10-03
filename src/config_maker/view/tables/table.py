from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class Table(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._count_row = 0
        self._count_col = 0
        self._selected_rows = []
        self.clicked.connect(self.clicked_table)  # noqa: E1120

    def _resize_columns(self):
        header = self.horizontalHeader()
        self.resizeColumnsToContents()
        header.setStretchLastSection(True)

    def _create_cell(self, text):
        cell = QTableWidgetItem(text)
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        return cell

    def clear(self):
        for i in range(self._count_row):
            for j in range(self._count_col):
                self.setItem(i, j, self._create_cell(''))

    def clicked_table(self):
        self._selected_rows = list(dict.fromkeys([index.row() for index in self.selectedIndexes()]))
        self._selected_rows.sort(reverse=False)

    def get_selected_rows(self):
        return self._selected_rows

    def remove_selection(self):
        for index in self.selectedIndexes():
            self.itemFromIndex(index).setSelected(False)
