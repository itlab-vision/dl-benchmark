from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class GroupButtonModels(QGroupBox):
    def __init__(self):
        super().__init__()
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Добавить модель', 'Удалить модель', 'Загрузить таблицу', 'Сохранить таблицу',
                             'Очистить таблицу']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox


class GroupButtonData(QGroupBox):
    def __init__(self):
        super().__init__()
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Добавить данные', 'Удалить данные', 'Загрузить таблицу', 'Сохранить таблицу',
                             'Очистить таблицу']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox


class GroupButtonTestConfig(QGroupBox):
    def __init__(self):
        super().__init__()
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Добавить информацию', 'Удалить информацию', 'Загрузить таблицу', 'Сохранить таблицу',
                             'Очистить таблицу']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox


class GroupButtonRemoteConfig(QGroupBox):
    def __init__(self):
        super().__init__()
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Добавить информацию', 'Удалить информацию', 'Загрузить таблицу', 'Сохранить таблицу',
                             'Очистить таблицу']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox


class GroupButtonDeployConfig(QGroupBox):

    addSignal = QtCore.pyqtSignal()
    delSignal = QtCore.pyqtSignal()
    clearSelectedSignal = QtCore.pyqtSignal()
    loadSignal = QtCore.pyqtSignal()
    saveSignal = QtCore.pyqtSignal()
    clearSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Добавить информацию', 'Удалить информацию', 'Загрузить таблицу', 'Сохранить таблицу',
                             'Очистить таблицу']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        buttons['Добавить информацию'].clicked.connect(self.add_click)
        buttons['Удалить информацию'].clicked.connect(self.del_click)
        buttons['Загрузить таблицу'].clicked.connect(self.load_click)
        buttons['Сохранить таблицу'].clicked.connect(self.save_click)
        buttons['Очистить таблицу'].clicked.connect(self.clear_click)
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox

    def add_click(self):
        self.addSignal.emit()

    def del_click(self):
        self.delSignal.emit()
        self.clearSelectedSignal.emit()

    def load_click(self):
        self.loadSignal.emit()

    def save_click(self):
        self.saveSignal.emit()

    def clear_click(self):
        self.clearSignal.emit()
