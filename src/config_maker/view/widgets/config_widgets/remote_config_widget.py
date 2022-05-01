from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox, QFileDialog
from view.buttons.group_buttons import ConfigGroupButtons  # pylint: disable=E0401
from view.dialogs.remote_config_dialog import RemoteConfigDialog  # pylint: disable=E0401
from view.tables.remote_config_table import RemoteConfigTable  # pylint: disable=E0401


class RemoteConfigWidget(QWidget):

    addComputerSignal = pyqtSignal(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    deleteComputerSignal = pyqtSignal(list)
    changeComputerSignal = pyqtSignal(int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    copyComputerSignal = pyqtSignal(list)

    loadSignal = pyqtSignal(str)
    saveSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = RemoteConfigTable(self)
        self.__buttons = ConfigGroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_computer)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_computer)
        self.__buttons.get_buttons()['Copy information'].clicked.connect(self.__copy_computers)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        self.__buttons.get_buttons()['Save table'].clicked.connect(self.__show_dialog_create_config)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.deleteComputerSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def __show_dialog_add_computer(self):
        dialog = RemoteConfigDialog(self)
        if dialog.exec():
            self.addComputerSignal.emit(*dialog.get_values())

    def __show_dialog_change_computer(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = RemoteConfigDialog(self)
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

    def __copy_computers(self):
        self.copyComputerSignal.emit(self.get_selected_rows())

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_computers())
