from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from view.tables import TableBenchmarkConfig, TableRemoteConfig, TableDeployConfig
from view.buttons import GroupButtons
from view.dialogs import BenchmarkDialog, RemoteDialog, DeployDialog
from presenters.presenters import BenchmarkPresenter, RemotePresenter, DeployPresenter
from models.models import BenchmarkConfig, RemoteConfig, DeployConfig


class WidgetBenchmarkConfigs(QWidget):

    delSignal = QtCore.pyqtSignal(list)
    loadSignal = QtCore.pyqtSignal(str)
    saveSignal = QtCore.pyqtSignal()
    clearSignal = QtCore.pyqtSignal()

    addTestSignal = QtCore.pyqtSignal(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    changeTestSignal = QtCore.pyqtSignal(int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableBenchmarkConfig(self)
        self.__buttons = GroupButtons(self)
        self.__dialog = BenchmarkDialog(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_test)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_test)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save table'].clicked.connect(self.saveSignal.emit)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.delSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def __show_dialog_add_test(self):
        dialog = self.__dialog
        dialog.clear()
        if dialog.exec():
            if dialog.framework.currentText() == 'OpenVINO DLDT':
                mode = dialog.mode.text()
                extension = dialog.extension.text()
                async_req_count = dialog.async_req_count.text()
                thread_count = dialog.thread_count.text()
                stream_count = dialog.stream_count.text()
                channel_swap = None
                mean = None
                input_scale = None
            elif dialog.framework.currentText() == 'Caffe':
                mode = None
                extension = None
                async_req_count = None
                thread_count = None
                stream_count = None
                channel_swap = dialog.channel_swap.text()
                mean = dialog.mean.text()
                input_scale = dialog.input_scale.text()
            self.addTestSignal.emit(dialog.model.text(), dialog.dataset.text(), dialog.framework.currentText(),
                                    dialog.batch_size.text(), dialog.device.text(),  dialog.iter_count.text(),
                                    dialog.test_time_limit.text(),  mode,  extension, async_req_count,  thread_count,
                                    stream_count,  channel_swap,  mean, input_scale)

    def __show_dialog_change_test(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = self.__dialog
        row = self.__table.get_selected_rows()[0]
        dialog.model.setText(self.__table.item(row, 0).text())
        dialog.dataset.setText(self.__table.item(row, 1).text())
        dialog.framework.setCurrentText(self.__table.item(row, 2).text())
        dialog.batch_size.setText(self.__table.item(row, 3).text())
        dialog.device.setText(self.__table.item(row, 4).text())
        dialog.iter_count.setText(self.__table.item(row, 5).text())
        dialog.test_time_limit.setText(self.__table.item(row, 6).text())
        dialog.mode.setText(self.__table.item(row, 7).text())
        dialog.extension.setText(self.__table.item(row, 8).text())
        dialog.async_req_count.setText(self.__table.item(row, 9).text())
        dialog.thread_count.setText(self.__table.item(row, 10).text())
        dialog.stream_count.setText(self.__table.item(row, 11).text())
        dialog.channel_swap.setText(self.__table.item(row, 12).text())
        dialog.mean.setText(self.__table.item(row, 13).text())
        dialog.input_scale.setText(self.__table.item(row, 14).text())
        if dialog.exec():
            if dialog.framework.currentText() == 'OpenVINO DLDT':
                mode = dialog.mode.text()
                extension = dialog.extension.text()
                async_req_count = dialog.async_req_count.text()
                thread_count = dialog.thread_count.text()
                stream_count = dialog.stream_count.text()
                channel_swap = None
                mean = None
                input_scale = None
            elif dialog.framework.currentText() == 'Caffe':
                mode = None
                extension = None
                async_req_count = None
                thread_count = None
                stream_count = None
                channel_swap = dialog.channel_swap.text()
                mean = dialog.mean.text()
                input_scale = dialog.input_scale.text()
            self.changeTestSignal.emit(row, dialog.model.text(), dialog.dataset.text(), dialog.framework.currentText(),
                                    dialog.batch_size.text(), dialog.device.text(), dialog.iter_count.text(),
                                    dialog.test_time_limit.text(), mode, extension, async_req_count, thread_count,
                                    stream_count, channel_swap, mean, input_scale)
        self.__table.remove_selection()

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, "Open File", "", "XML files (*.xml)")
        if path_to_config:
            self.loadSignal.emit(path_to_config[0])

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, "Success", "Benchmark configuration was created successfully!")
        else:
            QMessageBox.warning(self, "Fail", "Benchmark configuration was not created!")

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model)


class WidgetRemoteConfigs(QWidget):

    delSignal = QtCore.pyqtSignal(list)
    loadSignal = QtCore.pyqtSignal(str)
    saveSignal = QtCore.pyqtSignal()
    clearSignal = QtCore.pyqtSignal()

    addComputerSignal = QtCore.pyqtSignal(str, str, str, str, str, str, str, str)
    changeComputerSignal = QtCore.pyqtSignal(int, str, str, str, str, str, str, str, str)

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableRemoteConfig(self)
        self.__buttons = GroupButtons(self)
        self.__dialog = RemoteDialog(self)
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
        dialog = self.__dialog
        dialog.clear()
        if dialog.exec():
            self.addComputerSignal.emit(dialog.ip.text(), dialog.login.text(), dialog.password.text(), dialog.os.text(),
                                        dialog.path_to_ftp_client.text(),  dialog.benchmark_config.text(),
                                        dialog.log_file.text(),  dialog.res_file.text())

    def __show_dialog_change_computer(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = self.__dialog
        row = self.__table.get_selected_rows()[0]
        dialog.ip.setText(self.__table.item(row, 0).text())
        dialog.login.setText(self.__table.item(row, 1).text())
        dialog.password.setText(self.__table.item(row, 2).text())
        dialog.os.setText(self.__table.item(row, 3).text())
        dialog.path_to_ftp_client.setText(self.__table.item(row, 4).text())
        dialog.benchmark_config.setText(self.__table.item(row, 5).text())
        dialog.log_file.setText(self.__table.item(row, 6).text())
        dialog.res_file.setText(self.__table.item(row, 7).text())
        if dialog.exec():
            self.changeComputerSignal.emit(row, dialog.ip.text(), dialog.login.text(), dialog.password.text(),
                                           dialog.os.text(), dialog.path_to_ftp_client.text(),
                                           dialog.benchmark_config.text(), dialog.log_file.text(),
                                           dialog.res_file.text())
        self.__table.remove_selection()

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, "Open File", "", "XML files (*.xml)")
        if path_to_config:
            self.loadSignal.emit(path_to_config[0])

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, "Success", "Remote configuration was created successfully!")
        else:
            QMessageBox.warning(self, "Fail", "Remote configuration was not created!")

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model)


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
        self.__buttons = GroupButtons(self)
        self.__dialog = DeployDialog(self)
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
        dialog = self.__dialog
        dialog.clear()
        if dialog.exec():
            self.addComputerSignal.emit(dialog.ip.text(), dialog.login.text(), dialog.password.text(), dialog.os.text(),
                                        dialog.download_folder.text())

    def __show_dialog_change_computer(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = self.__dialog
        row = self.__table.get_selected_rows()[0]
        dialog.ip.setText(self.__table.item(row, 0).text())
        dialog.login.setText(self.__table.item(row, 1).text())
        dialog.password.setText(self.__table.item(row, 2).text())
        dialog.os.setText(self.__table.item(row, 3).text())
        dialog.download_folder.setText(self.__table.item(row, 4).text())
        if dialog.exec():
            self.changeComputerSignal.emit(row, dialog.ip.text(), dialog.login.text(), dialog.password.text(),
                                           dialog.os.text(), dialog.download_folder.text())
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
        grid.addWidget(self._widgets['Benchmark configuration'], 1, 0)
        self._widgets['Benchmark configuration'].show()
        grid.addWidget(self._widgets['Remote configuration'], 1, 0)
        self._widgets['Remote configuration'].hide()
        grid.addWidget(self._widgets['Deploy configuration'], 1, 0)
        self._widgets['Deploy configuration'].hide()
        benchmark_model = BenchmarkConfig()
        remote_model = RemoteConfig()
        deploy_model = DeployConfig()
        self._benchmark_presenter = BenchmarkPresenter(self._widgets['Benchmark configuration'], benchmark_model)
        self._remote_presenter = RemotePresenter(self._widgets['Remote configuration'], remote_model)
        self._deploy_presenter = DeployPresenter(self._widgets['Deploy configuration'], deploy_model)
        self.setLayout(grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(self._widgets.keys())
        menu.activated[str].connect(self.onActivated)
        return menu

    def __create_dict(self):
        benchmark_configs = WidgetBenchmarkConfigs(self)
        remote_configs = WidgetRemoteConfigs(self)
        deploy_configs = WidgetDeployConfigs(self)
        dictionary = {'Benchmark configuration': benchmark_configs,
                      'Remote configuration': remote_configs,
                      'Deploy configuration': deploy_configs}
        return dictionary

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()
