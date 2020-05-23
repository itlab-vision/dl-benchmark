from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from view.tables import TableModel, TableData
from view.buttons import GroupButtons
from view.dialogs import ModelDialog
from presenters.presenters import ModelPresenter
from models.models import Models


class WidgetModelSettings(QWidget):

    delSignal = QtCore.pyqtSignal(list)
    loadSignal = QtCore.pyqtSignal(str)
    saveSignal = QtCore.pyqtSignal()
    clearSignal = QtCore.pyqtSignal()

    addModelSignal = QtCore.pyqtSignal(str, str, str, str, str, str)
    changeModelSignal = QtCore.pyqtSignal(int, str, str, str, str, str, str)

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = TableModel(self)
        self.__buttons = GroupButtons(self)
        self.__dialog = ModelDialog(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_model)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__del_click)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_model)
        self.__buttons.get_buttons()['Load table'].clicked.connect(self.__show_dialog_parser_config)
        #self.__buttons.get_buttons()['Save table'].clicked.connect(self.saveSignal.emit)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __del_click(self):
        self.delSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def __show_dialog_add_model(self):
        dialog = self.__dialog
        dialog.clear()
        if dialog.exec():
            self.addModelSignal.emit(dialog.task.text(), dialog.name.text(), dialog.precision.text(),
                                        dialog.framework.text(), dialog.model_path.text(),  dialog.weights_path.text())

    def __show_dialog_change_model(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = self.__dialog
        row = self.__table.get_selected_rows()[0]
        dialog.task.setText(self.__table.item(row, 0).text())
        dialog.name.setText(self.__table.item(row, 1).text())
        dialog.precision.setText(self.__table.item(row, 2).text())
        dialog.framework.setText(self.__table.item(row, 3).text())
        dialog.model_path.setText(self.__table.item(row, 4).text())
        dialog.weights_path.setText(self.__table.item(row, 5).text())
        if dialog.exec():
            self.changeModelSignal.emit(row, dialog.task.text(), dialog.name.text(), dialog.precision.text(),
                                           dialog.framework.text(), dialog.model_path.text(), dialog.weights_path.text())
        self.__table.remove_selection()

    def __show_dialog_parser_config(self):
        path_to_config = QFileDialog.getOpenFileName(self, "Open File", "", "XML files (*.xml)")
        if path_to_config:
            self.loadSignal.emit(path_to_config[0])

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model)


class WidgetDataSettings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self._table = TableData(self)
        self._buttons = GroupButtons(self)
        layouts.addWidget(self._table)
        layouts.addWidget(self._buttons)
        self.setLayout(layouts)


class WidgetData(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        grid = QGridLayout()
        self._widgets = self.__create_dict()
        grid.addWidget(self.__create_combobox(), 0, 0)
        grid.addWidget(self._widgets['Models'], 1, 0)
        self._widgets['Models'].show()
        grid.addWidget(self._widgets['Data'], 1, 0)
        self._widgets['Data'].hide()
        models = Models()
        self._models_presenter = ModelPresenter(self._widgets['Models'], models)
        self.setLayout(grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(self._widgets.keys())
        menu.activated[str].connect(self.onActivated)
        return menu

    def __create_dict(self):
        model_settings = WidgetModelSettings(self)
        data_settings = WidgetDataSettings(self)
        dictionary = {'Models': model_settings, 'Data': data_settings}
        return dictionary

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()
