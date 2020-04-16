from PyQt5.QtWidgets import *


class GroupButtonModels(QGroupBox):
    def __init__(self):
        super().__init__()
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Добавить модель', 'Удалить модель']
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
        list_name_buttons = ['Добавить данные', 'Удалить данные']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox


class GroupButtonTest(QGroupBox):
    def __init__(self):
        super().__init__()
        self._buttons = self.__create_dict_buttons()
        self.setLayout(self.__create_buttons_vbox())

    def __create_dict_buttons(self):
        list_name_buttons = ['Добавить тест', 'Удалить тест']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def __create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self._buttons:
            vbox.addWidget(self._buttons[name_button])
        return vbox