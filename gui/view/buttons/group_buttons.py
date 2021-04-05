from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout


class GroupButtons(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.__buttons = self._create_dict_buttons()
        self.setLayout(self._create_buttons_vbox())

    def _create_dict_buttons(self):
        list_name_buttons = ['Add information', 'Delete information', 'Change information', 'Load table',
                             'Save table', 'Clear table']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons

    def _create_buttons_vbox(self):
        vbox = QVBoxLayout()
        for name_button in self.__buttons:
            vbox.addWidget(self.__buttons[name_button])
        return vbox

    def get_buttons(self):
        return self.__buttons
