from PyQt5.QtWidgets import *


class WidgetConfig(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        grid = QGridLayout()
        self._widgets = self.__create_dict()
        grid.addWidget(self.__create_combobox(), 0, 0)
        grid.addWidget(self._widgets['Составить конфигурацию тестов'], 1, 0)
        self._widgets['Составить конфигурацию тестов'].show()
        grid.addWidget(self._widgets['Составить конфигурацию удаленного запуска'], 1, 0)
        self._widgets['Составить конфигурацию удаленного запуска'].hide()
        grid.addWidget(self._widgets['Составить конфигурацию резвертки'], 1, 0)
        self._widgets['Составить конфигурацию резвертки'].hide()
        self.setLayout(grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(self._widgets.keys())
        menu.activated[str].connect(self.onActivated)
        return menu

    def __create_dict(self):
        tests_configs = QWidget()
        remote_configs = QWidget()
        deploy_configs = QWidget()
        dictionary = {'Составить конфигурацию тестов': tests_configs,
                      'Составить конфигурацию удаленного запуска': remote_configs,
                      'Составить конфигурацию резвертки': deploy_configs}
        return dictionary

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()