from PyQt5.QtWidgets import QPushButton
from .group_buttons import GroupButtons


class DataGroupButtons(GroupButtons):
    def _create_dict_buttons(self):
        list_name_buttons = ['Add information', 'Delete information', 'Change information', 'Clear table']
        buttons = {list_name_buttons[i]: QPushButton(list_name_buttons[i]) for i in range(len(list_name_buttons))}
        return buttons
