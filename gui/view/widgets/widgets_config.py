from PyQt5.QtWidgets import *
from view.tables import *
from view.buttons import *
from presenters.deploy_presenter import *
from view.dialogs import *


class WidgetTestConfigs(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self._table = TableTestConfig(self)
        self._buttons = GroupButtonTestConfig(self)
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons)
        self.setLayout(layouts)


class WidgetRemoteConfigs(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self._table = TableRemoteConfig(self)
        self._buttons = GroupButtonRemoteConfig(self)
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons)
        self.setLayout(layouts)


class WidgetDeployConfigs(QWidget):

    delSignal = QtCore.pyqtSignal(list)
    loadSignal = QtCore.pyqtSignal()
    saveSignal = QtCore.pyqtSignal()
    clearSignal = QtCore.pyqtSignal()

    addComputerSignal = QtCore.pyqtSignal(str, str, str, str, str)
    changeComputerSignal = QtCore.pyqtSignal(int, str, str, str, str, str)

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableDeployConfig(self)
        self.__buttons = GroupButtonDeployConfig(self)
        self.__dialog_add_computer = DeployDialog(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Добавить информацию'].clicked.connect(self.__show_dialog_add_computer)
        self.__buttons.get_buttons()['Удалить информацию'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Изменить информацию'].clicked.connect(self.__show_dialog_change_computer)
        self.__buttons.get_buttons()['Загрузить таблицу'].clicked.connect(self.loadSignal.emit)
        self.__buttons.get_buttons()['Сохранить таблицу'].clicked.connect(self.saveSignal.emit)
        self.__buttons.get_buttons()['Очистить таблицу'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.delSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def __show_dialog_add_computer(self):
        dialog = self.__dialog_add_computer
        dialog.clear()
        if dialog.exec():
            self.addComputerSignal.emit(dialog.get_ip(), dialog.get_login(), dialog.get_password(), dialog.get_os(),
                                        dialog.get_download_folder())

    def __show_dialog_change_computer(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = self.__dialog_add_computer
        row = self.__table.get_selected_rows()[0]
        dialog.set_ip(self.__table.item(row, 0).text())
        dialog.set_login(self.__table.item(row, 1).text())
        dialog.set_password(self.__table.item(row, 2).text())
        dialog.set_os(self.__table.item(row, 3).text())
        dialog.set_download_folder(self.__table.item(row, 4).text())
        if dialog.exec():
            self.changeComputerSignal.emit(row, dialog.get_ip(), dialog.get_login(), dialog.get_password(),
                                           dialog.get_os(), dialog.get_download_folder())
        self.__table.remove_selection()

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model)


class WidgetConfig(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
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
        tests_configs = WidgetTestConfigs(self)
        remote_configs = WidgetRemoteConfigs(self)
        deploy_configs = WidgetDeployConfigs(self)
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
