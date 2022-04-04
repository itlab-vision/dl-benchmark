from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox, QFileDialog
from view.buttons.group_buttons import ConfigGroupButtons  # pylint: disable=E0401
from view.dialogs.accuracy_checker_config_dialog import AccuracyCheckerConfigDialog  # pylint: disable=E0401
from view.tables.accuracy_checker_config_table import AccuracyCheckerConfigTable  # pylint: disable=E0401


class AccuracyCheckerConfigWidget(QWidget):

    addTestSignal = pyqtSignal(list)
    deleteTestSignal = pyqtSignal(list)
    changeTestSignal = pyqtSignal(list)
    copyTestSignal = pyqtSignal(list)

    showAddTestDialogSignal = pyqtSignal()
    showChangeTestDialogSignal = pyqtSignal()
    loadSignal = pyqtSignal(str)
    saveSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = AccuracyCheckerConfigTable(self)
        self.__buttons = ConfigGroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.showAddTestDialogSignal.emit)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__click_delete_button)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.showChangeTestDialogSignal.emit)
        self.__buttons.get_buttons()['Copy information'].clicked.connect(self.__copy_tests)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save table'].clicked.connect(self.__show_dialog_create_config)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def show_add_test_dialog(self, models):
        if not models:
            QMessageBox.warning(self, "Warning!", "Models list is empty!")
            return
        dialog = AccuracyCheckerConfigDialog(self, models)
        if dialog.exec():
            values = dialog.get_values()
            self.addTestSignal.emit(values)

    def show_change_test_dialog(self, models):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        row = self.__table.get_selected_rows()[0]
        dialog = AccuracyCheckerConfigDialog(self, models)
        dialog.load_values_from_table_row(self.__table, row)
        if dialog.exec():
            values = dialog.get_values()
            self.changeTestSignal.emit([row, *values])
            self.__table.remove_selection()

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, "Open File", __file__, "XML files (*.xml)")
        if path_to_config[0]:
            self.loadSignal.emit(path_to_config[0])

    def __show_dialog_create_config(self):
        path_to_config = QFileDialog.getSaveFileName(self, "Save File", __file__, "XML files (*.xml)")
        if path_to_config[0]:
            self.saveSignal.emit(path_to_config[0])

    def __click_delete_button(self):
        self.deleteTestSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def show_message_status_saving(self, status):
        if status:
            QMessageBox.information(self, "Success", "AccuracyChecker configuration was created successfully!")
        else:
            QMessageBox.warning(self, "Fail", "AccuracyChecker configuration was not created!")

    def __copy_tests(self):
        self.copyTestSignal.emit(self.get_selected_rows())

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_tests())
