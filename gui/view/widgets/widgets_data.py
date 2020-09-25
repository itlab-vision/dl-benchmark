from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from view.tables import TableModel, TableData
from view.buttons import DataGroupButtons
from view.dialogs import ModelDialog, DataDialog


class WidgetModelSettings(QWidget):

    addModelSignal = QtCore.pyqtSignal(str, str, str, str, str, str)
    delModelSignal = QtCore.pyqtSignal(list)
    changeModelSignal = QtCore.pyqtSignal(int, str, str, str, str, str, str)

    clearSignal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableModel(self)
        self.__buttons = DataGroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_model)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_model)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.delModelSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def __show_dialog_add_model(self):
        dialog = ModelDialog(self)
        if dialog.exec():
            self.addModelSignal.emit(*dialog.get_values())

    def __show_dialog_change_model(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = ModelDialog(self)
        row = self.__table.get_selected_rows()[0]
        idx = 0
        for tag in dialog.tags:
            dialog.edits[tag].setText(self.__table.item(row, idx).text())
            idx += 1
        if dialog.exec():
            self.changeModelSignal.emit(row, *dialog.get_values())
        self.__table.remove_selection()

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_models())


class WidgetDataSettings(QWidget):

    addDatasetSignal = QtCore.pyqtSignal(str, str)
    delDatasetSignal = QtCore.pyqtSignal(list)
    changeDatasetSignal = QtCore.pyqtSignal(int, str, str)

    clearSignal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableData(self)
        self.__buttons = DataGroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_dataset)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_dataset)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.delDatasetSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def __show_dialog_add_dataset(self):
        dialog = DataDialog(self)
        if dialog.exec():
            self.addDatasetSignal.emit(*dialog.get_values())

    def __show_dialog_change_dataset(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = DataDialog(self)
        row = self.__table.get_selected_rows()[0]
        idx = 0
        for tag in dialog.tags:
            dialog.edits[tag].setText(self.__table.item(row, idx).text())
            idx += 1
        if dialog.exec():
            self.changeComputerSignal.emit(row, *dialog.get_values())
        self.__table.remove_selection()

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_data())


class WidgetData(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._widgets = self.__create_dict()
        grid = QGridLayout()
        grid.addWidget(self.__create_combobox(), 0, 0)
        grid.addWidget(self._widgets['Models'], 1, 0)
        grid.addWidget(self._widgets['Data'], 1, 0)
        self._widgets['Models'].show()
        self._widgets['Data'].hide()
        self.setLayout(grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(self._widgets.keys())
        menu.activated[str].connect(self.onActivated)
        return menu

    def __create_dict(self):
        self.model_settings = WidgetModelSettings(self)
        self.data_settings = WidgetDataSettings(self)
        dictionary = {'Models': self.model_settings, 'Data': self.data_settings}
        return dictionary

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()

    def update(self, model):
        self.model_settings.update(model.models)
        self.data_settings.update(model.data)
