from PyQt5.QtWidgets import *
from buttons import GroupButton, GroupButtonModels

class WidgetData(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self._grid = QGridLayout()
        # self.setLayout(grid)
        menu = self.__create_combobox()
        self._grid.addWidget(menu, 0, 0)
        self.setLayout(self._grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(['Управление моделями', 'Управление данными', 'Управление тестами'])
        menu.activated[str].connect(self.onActivated)
        return menu

    def __clear_grid(self, number_row):
        pass

    def onActivated(self, type):
        if type == 'Управление моделями':
            pass
        elif type == 'Управление данными':
            pass
        elif type == 'Управление тестами':
            pass

class WidgetModelSettings(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layouts = QHBoxLayout()

    def __create_table(self):
        table = QTableWidget(self)
        table.setColumnCount(2)
