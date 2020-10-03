from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from view.tables import TableBenchmarkConfig, TableRemoteConfig, TableDeployConfig
from view.buttons import GroupButtons
from view.dialogs import BenchmarkDialog, RemoteDialog, DeployDialog


class WidgetBenchmarkConfigs(QWidget):

    addTestSignal = QtCore.pyqtSignal(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    delTestSignal = QtCore.pyqtSignal(list)
    changeTestSignal = QtCore.pyqtSignal(int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)

    buttonAddSignal = QtCore.pyqtSignal()
    buttonChangeSignal = QtCore.pyqtSignal()
    loadSignal = QtCore.pyqtSignal(str)
    saveSignal = QtCore.pyqtSignal(str)
    clearSignal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableBenchmarkConfig(self)
        self.__buttons = GroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.buttonAddSignal.emit)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.buttonChangeSignal.emit)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save table'].clicked.connect(self.__show_dialog_create_config)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.delSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def show_dialog_add_test(self, models, data):
        if not models:
            QMessageBox.warning(self, "Warning!", "Models list is empty!")
            return
        if not data:
            QMessageBox.warning(self, "Warning!", "Datasets list is empty!")
            return
        dialog = BenchmarkDialog(self, models, data)
        if dialog.exec():
            framework_independent_values = dialog.get_framework_independent_values()
            if dialog.get_selected_framework() == 'OpenVINO DLDT':
                openvino_values = dialog.get_openvino_values()
                caffe_values = ['None', 'None', 'None']
            elif dialog.get_selected_framework() == 'Caffe':
                openvino_values = ['None', 'None', 'None', 'None', 'None']
                caffe_values = dialog.get_caffe_values()
            self.addTestSignal.emit(*framework_independent_values, *openvino_values, *caffe_values)

    def show_dialog_change_test(self, models, data):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = BenchmarkDialog(self, models, data)
        row = self.__table.get_selected_rows()[0]
        dialog.framework_independent_edits['Model'].setCurrentText(self.__table.item(row, 0).text())
        dialog.framework_independent_edits['Dataset'].setCurrentText(self.__table.item(row, 1).text())
        dialog.framework_independent_edits['Framework'].setCurrentText(self.__table.item(row, 2).text())
        dialog.framework_independent_edits['Device'].setCurrentText(self.__table.item(row, 4).text())
        idx = 3
        for tag in dialog.framework_independent_tags[4:]:
            if tag != 'Device':
                dialog.framework_independent_edits[tag].setText(self.__table.item(row, idx).text())
            idx += 1
        framework = dialog.get_selected_framework()
        if framework == 'OpenVINO DLDT':
            for tag in dialog.openvino_tags[1:]:
                dialog.openvino_edits[tag].setText(self.__table.item(row, idx).text())
                idx += 1
        elif framework == 'Caffe':
            for tag in dialog.caffe_tags[1:]:
                dialog.caffe_edits[tag].setText(self.__table.item(row, idx + 5).text())
                idx += 1
        if dialog.exec():
            framework_independent_values = dialog.get_framework_independent_values()
            if dialog.get_selected_framework() == 'OpenVINO DLDT':
                openvino_values = dialog.get_openvino_values()
                caffe_values = ['None', 'None', 'None']
            elif dialog.get_selected_framework() == 'Caffe':
                openvino_values = ['None', 'None', 'None', 'None', 'None']
                caffe_values = dialog.get_caffe_values()
            self.changeTestSignal.emit(row, *framework_independent_values, *openvino_values, *caffe_values)
            self.__table.remove_selection()

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, "Open File", "", "XML files (*.xml)")
        if path_to_config[0]:
            self.loadSignal.emit(path_to_config[0])

    def __show_dialog_create_config(self):
        path_to_config = QFileDialog.getSaveFileName(self, "Save File", "", "XML files (*.xml)")
        if path_to_config[0]:
            self.saveSignal.emit(path_to_config[0])

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, "Success", "Benchmark configuration was created successfully!")
        else:
            QMessageBox.warning(self, "Fail", "Benchmark configuration was not created!")

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_tests())


class WidgetRemoteConfigs(QWidget):

    addComputerSignal = QtCore.pyqtSignal(str, str, str, str, str, str, str, str)
    delComputerSignal = QtCore.pyqtSignal(list)
    changeComputerSignal = QtCore.pyqtSignal(int, str, str, str, str, str, str, str, str)

    loadSignal = QtCore.pyqtSignal(str)
    saveSignal = QtCore.pyqtSignal(str)
    clearSignal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableRemoteConfig(self)
        self.__buttons = GroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_computer)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_computer)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save table'].clicked.connect(self.__show_dialog_create_config)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.delComputerSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def __show_dialog_add_computer(self):
        dialog = RemoteDialog(self)
        if dialog.exec():
            self.addComputerSignal.emit(*dialog.get_values())

    def __show_dialog_change_computer(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = RemoteDialog(self)
        row = self.__table.get_selected_rows()[0]
        idx = 0
        for tag in dialog.tags:
            dialog.edits[tag].setText(self.__table.item(row, idx).text())
            idx += 1
        if dialog.exec():
            self.changeComputerSignal.emit(row, *dialog.get_values())
        self.__table.remove_selection()

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, "Open File", "", "XML files (*.xml)")
        if path_to_config[0]:
            self.loadSignal.emit(path_to_config[0])

    def __show_dialog_create_config(self):
        path_to_config = QFileDialog.getSaveFileName(self, "Save File", "", "XML files (*.xml)")
        if path_to_config[0]:
            self.saveSignal.emit(path_to_config[0])

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, "Success", "Remote configuration was created successfully!")
        else:
            QMessageBox.warning(self, "Fail", "Remote configuration was not created!")

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_computers())


class WidgetDeployConfigs(QWidget):

    addComputerSignal = QtCore.pyqtSignal(str, str, str, str, str)
    delComputerSignal = QtCore.pyqtSignal(list)
    changeComputerSignal = QtCore.pyqtSignal(int, str, str, str, str, str)

    loadSignal = QtCore.pyqtSignal(str)
    saveSignal = QtCore.pyqtSignal(str)
    clearSignal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableDeployConfig(self)
        self.__buttons = GroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_computer)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_computer)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save table'].clicked.connect(self.__show_dialog_create_config)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.delComputerSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def __show_dialog_add_computer(self):
        dialog = DeployDialog(self)
        if dialog.exec():
            self.addComputerSignal.emit(*dialog.get_values())

    def __show_dialog_change_computer(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = DeployDialog(self)
        row = self.__table.get_selected_rows()[0]
        idx = 0
        for tag in dialog.tags:
            dialog.edits[tag].setText(self.__table.item(row, idx).text())
            idx += 1
        if dialog.exec():
            self.changeComputerSignal.emit(row, *dialog.get_values())
        self.__table.remove_selection()

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, "Open File", "", "XML files (*.xml)")
        if path_to_config[0]:
            self.loadSignal.emit(path_to_config[0])

    def __show_dialog_create_config(self):
        path_to_config = QFileDialog.getSaveFileName(self, "Save File", "", "XML files (*.xml)")
        if path_to_config[0]:
            self.saveSignal.emit(path_to_config[0])

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, "Success", "Deploy configuration was created successfully!")
        else:
            QMessageBox.warning(self, "Fail", "Deploy configuration was not created!")

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_computers())


class WidgetConfig(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        grid = QGridLayout()
        self._widgets = self.__create_dict()
        grid.addWidget(self.__create_combobox(), 0, 0)
        grid.addWidget(self._widgets['Benchmark configuration'], 1, 0)
        self._widgets['Benchmark configuration'].show()
        grid.addWidget(self._widgets['Remote configuration'], 1, 0)
        self._widgets['Remote configuration'].hide()
        grid.addWidget(self._widgets['Deploy configuration'], 1, 0)
        self._widgets['Deploy configuration'].hide()
        self.setLayout(grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(self._widgets.keys())
        menu.activated[str].connect(self.onActivated)
        return menu

    def __create_dict(self):
        self.benchmark_configs = WidgetBenchmarkConfigs(self)
        self.remote_configs = WidgetRemoteConfigs(self)
        self.deploy_configs = WidgetDeployConfigs(self)
        dictionary = {'Benchmark configuration': self.benchmark_configs,
                      'Remote configuration': self.remote_configs,
                      'Deploy configuration': self.deploy_configs}
        return dictionary

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()

    def update(self, model):
        self.benchmark_configs.update(model.benchmark_config)
        self.remote_configs.update(model.remote_config)
        self.deploy_configs.update(model.deploy_config)
