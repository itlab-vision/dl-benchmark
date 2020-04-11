from PyQt5.QtWidgets import QWidget, QPushButton, QGroupBox, QVBoxLayout


class GroupButton(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.list_name_buttons = []
        self.initUI()

    def initUI(self):
        self.groupbox = QGroupBox()
        vbox = QVBoxLayout()
        self.list_buttons = []
        for name, i in self.list_name_buttons:
            self.list_buttons.append(QPushButton(self.list_name_buttons[i]))
            vbox.addWidget(self.list_buttons[i])
        self.groupbox.setLayout(vbox)


class GroupButtonModels(GroupButton):
    def __init__(self):
        super(self).__init__()
        self.list_name_buttons = ['Добавить модель', 'Удалить модель']
        self.initUI()