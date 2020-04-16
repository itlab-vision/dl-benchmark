from PyQt5.QtWidgets import *
from tables import *
from buttons import *


class WidgetTestConfigs(QWidget):
    def __init__(self):
        super().__init__()
        layouts = QHBoxLayout()
        self._table = TableTestConfig()
        self._buttons = GroupButtonTestConfig()
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons)
        self.setLayout(layouts)


class WidgetRemoteConfigs(QWidget):
    def __init__(self):
        super().__init__()
        layouts = QHBoxLayout()
        self._table = TableRemoteConfig()
        self._buttons = GroupButtonRemoteConfig()
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons)
        self.setLayout(layouts)


class WidgetDeployConfigs(QWidget):
    def __init__(self):
        super().__init__()
        layouts = QHBoxLayout()
        self._table = TableDeployConfig()
        self._buttons = GroupButtonDeployConfig()
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons)
        self.setLayout(layouts)


class WidgetConfig(QWidget):
    def __init__(self):
        super().__init__()
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
        tests_configs = WidgetTestConfigs()
        remote_configs = WidgetRemoteConfigs()
        deploy_configs = WidgetDeployConfigs()
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