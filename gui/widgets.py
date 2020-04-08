from PyQt5.QtWidgets import QWidget, QTableWidget, QGridLayout, QComboBox


class WidgetData(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.menu = QComboBox()
        self.menu.addItems(['Управление моделями', 'Управление данными', 'Управление тестами'])
        grid.addWidget(self.menu, 0, 0)
        self.setLayout(grid)