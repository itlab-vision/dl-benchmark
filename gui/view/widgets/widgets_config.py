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
    loadSignal = QtCore.pyqtSignal(str)
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
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_computer)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_computer)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save table'].clicked.connect(self.saveSignal.emit)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

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

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, "Open File", "", "XML files (*.xml)")
        if path_to_config:
            self.loadSignal.emit(path_to_config[0])

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, "Success", "Deploy configuration was created successfully!")
        else:
            QMessageBox.warning(self, "Fail", "Deploy configuration was not created!")

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
        grid.addWidget(self._widgets['Test configuration'], 1, 0)
        self._widgets['Test configuration'].show()
        grid.addWidget(self._widgets['Remote configuration'], 1, 0)
        self._widgets['Remote configuration'].hide()
        grid.addWidget(self._widgets['Deploy configuration'], 1, 0)
        self._widgets['Deploy configuration'].hide()
        model = DeployConfig()
        self._deploy_presenter = DeployPresenter(self._widgets['Deploy configuration'], model)
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
        dictionary = {'Test configuration': tests_configs,
                      'Remote configuration': remote_configs,
                      'Deploy configuration': deploy_configs}
        return dictionary

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()
