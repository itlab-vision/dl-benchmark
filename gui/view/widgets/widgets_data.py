from PyQt5.QtWidgets import *
from view.tables import *
from view.buttons import *


class WidgetModelSettings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self._table = TableModel(self)
        self._buttons = GroupButtonModels(self)
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons)
        self.setLayout(layouts)


class WidgetDataSettings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self._table = TableData(self)
        self._buttons = GroupButtonData(self)
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons)
        self.setLayout(layouts)


class WidgetData(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        grid = QGridLayout()
        self._widgets = self.__create_dict()
        grid.addWidget(self.__create_combobox(), 0, 0)
        grid.addWidget(self._widgets['Models'], 1, 0)
        self._widgets['Models'].show()
        grid.addWidget(self._widgets['Data'], 1, 0)
        self._widgets['Data'].hide()
        self.setLayout(grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(self._widgets.keys())
        menu.activated[str].connect(self.onActivated)
        return menu

    def __create_dict(self):
        model_settings = WidgetModelSettings(self)
        data_settings = WidgetDataSettings(self)
        dictionary = {'Models': model_settings, 'Data': data_settings}
        return dictionary

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()
