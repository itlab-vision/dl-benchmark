from PyQt5.QtWidgets import *
from view.tables import *
from view.buttons import *
from presenters.deploy_presenter import *
from view.dialogs import *


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
        self.__table = TableDeployConfig()
        self.__buttons = GroupButtonDeployConfig()
        self.__dialog_add_computer = DeployDialog(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__buttons.addSignal.connect(self.__show_dialog_add_computer)

    def __show_dialog_add_computer(self):
        self.__dialog_add_computer.clear()
        self.__dialog_add_computer.exec()

    def get_table(self):
        return self.__table

    def get_dialog_add_computer(self):
        return self.__dialog_add_computer

    def get_buttons(self):
        return self.__buttons

    def get_data_dialog_add(self):
        return self.__dialog_add_computer.get_ip(), self.__dialog_add_computer.get_login(), \
               self.__dialog_add_computer.get_password(), self.__dialog_add_computer.get_os(),\
               self.__dialog_add_computer.get_download_folder()


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
        model = DeployConfig()
        self._deploy_presenter = DeployPresenter(self._widgets['Составить конфигурацию резвертки'], model)
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