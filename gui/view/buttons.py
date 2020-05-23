from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class GroupButtonModels(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Add information', 'Delete information', 'Change information', 'Load table',
                             'Save table', 'Clear table']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox


class GroupButtonData(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Add information', 'Delete information', 'Change information', 'Load table',
                             'Save table', 'Clear table']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox


class GroupButtonTestConfig(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Add information', 'Delete information', 'Change information', 'Load table',
                             'Save table', 'Clear table']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox


class GroupButtonRemoteConfig(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Add information', 'Delete information', 'Change information', 'Load table',
                             'Save table', 'Clear table']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox

    def get_buttons(self):
        return self._buttons


class GroupButtonDeployConfig(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Add information', 'Delete information', 'Change information', 'Load table',
                             'Save table', 'Clear table']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox

    def get_buttons(self):
        return self._buttons
