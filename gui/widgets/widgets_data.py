from PyQt5.QtWidgets import *
from tables import *
from buttons import *


class WidgetModelSettings(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        layouts = QHBoxLayout()
        self._table = TableModel()
        self._buttons = GroupButtonModels()
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons.group)
        self.setLayout(layouts)


class WidgetDataSettings(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        layouts = QHBoxLayout()
        self._table = TableData()
        self._buttons = GroupButtonData()
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons.group)
        self.setLayout(layouts)


class WidgetData(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self._grid = QGridLayout()
        self._widgets = self.__create_dict()
        self._grid.addWidget(self.__create_combobox(), 0, 0)
        self._grid.addWidget(self._widgets['Управление моделями'], 1, 0)
        self._widgets['Управление моделями'].show()
        self._grid.addWidget(self._widgets['Управление данными'], 1, 0)
        self._widgets['Управление данными'].hide()
        self._grid.addWidget(self._widgets['Управление тестами'], 1, 0)
        self._widgets['Управление тестами'].hide()
        self.setLayout(self._grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(self._widgets.keys())
        menu.activated[str].connect(self.onActivated)
        return menu

    def __create_dict(self):
        model_settings = WidgetModelSettings(self)
        data_settings = WidgetDataSettings(self)
        tests_settings = QWidget()
        dictionary = {'Управление моделями': model_settings, 'Управление данными': data_settings,
                      'Управление тестами': tests_settings}
        return dictionary

    def __clear_grid(self, number_row):
        pass

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()
