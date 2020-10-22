from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox
from .model_settings_widget import ModelSettingsWidget
from .data_settings_widget import DataSettingsWidget


class DataWidget(QWidget):
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
        self.model_settings = ModelSettingsWidget(self)
        self.data_settings = DataSettingsWidget(self)
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
