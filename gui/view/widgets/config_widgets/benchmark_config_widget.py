from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox, QFileDialog
from ...buttons.group_buttons import GroupButtons  # pylint: disable=E0402
from ...dialogs.benchmark_config_dialog import BenchmarkConfigDialog  # pylint: disable=E0402
from ...tables.benchmark_config_table import BenchmarkConfigTable  # pylint: disable=E0402


class BenchmarkConfigWidget(QWidget):

    addTestSignal = pyqtSignal(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    deleteTestSignal = pyqtSignal(list)
    changeTestSignal = pyqtSignal(int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)

    showAddTestDialogSignal = pyqtSignal()
    showChangeTestDialogSignal = pyqtSignal()
    loadSignal = pyqtSignal(str)
    saveSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = BenchmarkConfigTable(self)
        self.__buttons = GroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.showAddTestDialogSignal.emit)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__click_delete_button)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.showChangeTestDialogSignal.emit)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save table'].clicked.connect(self.__show_dialog_create_config)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def show_add_test_dialog(self, models, data):
        if not models:
            QMessageBox.warning(self, "Warning!", "Models list is empty!")
            return
        if not data:
            QMessageBox.warning(self, "Warning!", "Datasets list is empty!")
            return
        dialog = BenchmarkConfigDialog(self, models, data)
        if dialog.exec():
            framework_independent_values = dialog.get_framework_independent_values()
            if dialog.get_selected_framework() == 'OpenVINO DLDT':
                openvino_values = dialog.get_openvino_values()
                caffe_values = ['None', 'None', 'None']
            elif dialog.get_selected_framework() == 'Caffe':
                openvino_values = ['None', 'None', 'None', 'None', 'None']
                caffe_values = dialog.get_caffe_values()
            self.addTestSignal.emit(*framework_independent_values, *openvino_values, *caffe_values)

    def show_change_test_dialog(self, models, data):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = BenchmarkConfigDialog(self, models, data)
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

    def __click_delete_button(self):
        self.deleteTestSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, "Success", "Benchmark configuration was created successfully!")
        else:
            QMessageBox.warning(self, "Fail", "Benchmark configuration was not created!")

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_tests())
