from PyQt5.QtWidgets import QWidget, QTableWidget, QGridLayout, QComboBox, QLabel


class WidgetData(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.menu = QComboBox()
        self.menu.addItems(['Управление моделями', 'Управление данными', 'Управление тестами'])
        self.menu.activated[str].connect(self.onActivated)
        self.grid.addWidget(self.menu, 0, 0)
        self.setLayout(self.grid)

    def onActivated(self, type):
        if type == 'Управление моделями':
            ...
        elif type == 'Управление данными':
            ...
        elif type == 'Управление тестами':
            ...


class WidgetTableSetting(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.column_count = None
        self.row_count = 1
        self.initUI()

    def initUI(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount((self.column_count))
        self.table.setRowCount((self.row_count))