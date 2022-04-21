from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox


class DeployConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.tags = ['IP', 'Login', 'Password', 'OS', 'Download folder']
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about computer')
        self.__create_labels()
        self.__create_edits()
        self.__create_layout()

    def __create_labels(self):
        self.labels = dict.fromkeys(self.tags)
        for key in self.labels:
            self.labels[key] = QLabel(key)

    def __create_edits(self):
        self.edits = dict.fromkeys(self.tags)
        for key in self.edits:
            self.edits[key] = QLineEdit(self)

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        for tag in self.tags:
            layout.addWidget(self.labels[tag], idx, 0)
            layout.addWidget(self.edits[tag], idx, 1)
            idx += 1
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked().connect(self.accept)
        cancel_btn.clicked().connect(self.reject)
        layout.addWidget(ok_btn, idx, 0)
        layout.addWidget(cancel_btn, idx, 1)
        self.setLayout(layout)

    def get_values(self):
        values = []
        for tag in self.tags:
            values.append(self.edits[tag].text())
        return values

    def accept(self):
        check = False
        for tag in self.tags:
            if self.edits[tag].text() == '':
                check = True
        if check:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')
        else:
            super().accept()
