import abc
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QMessageBox
# pylint: disable-next=E0401
from tags import CONFIG_MODEL_TAG, CONFIG_PARAMETERS_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_DEVICE_TAG, CONFIG_CONFIG_TAG


class AccuracyCheckerConfigDialog(QDialog):
    def __init__(self, parent, models):
        self.__parent = parent
        self.__models = models
        super().__init__(parent)
        self.__tags = [CONFIG_MODEL_TAG, CONFIG_PARAMETERS_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_DEVICE_TAG,
                       CONFIG_CONFIG_TAG]
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle('Information about test')
        self.__create_labels()
        self.__create_edits()
        self.__create_layout()

    def __create_labels(self):
        self.__labels = dict.fromkeys(self.__tags)
        for key in self.__labels:
            self.__labels[key] = QLabel(key)
        self._labels[CONFIG_PARAMETERS_TAG].setStyleSheet("font-weight: bold")

    def __create_edits(self):
        self.__edits[CONFIG_MODEL_TAG] = QComboBox(self.__parent)
        self.__edits[CONFIG_MODEL_TAG].addItems(self.__models)
        for tag in self.__tags[2:]:
            self.__edits[tag] = QLineEdit(self.__parent)

    def __create_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.__labels[CONFIG_MODEL_TAG], 0, 0)
        layout.addWidget(self.__edits[CONFIG_MODEL_TAG], 0, 1)
        layout.addWidget(self.__labels[CONFIG_PARAMETERS_TAG], 1, 0)
        idx = 2
        for tag in self.__tags[idx:]:
            layout.addWidget(self.__labels[tag], idx, 0)
            layout.addWidget(self.__edits[tag], idx, 1)
            idx += 1
        ok_btn = QPushButton('Ok')
        cancel_btn = QPushButton('Cancel')
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(ok_btn, idx, 0)
        layout.addWidget(cancel_btn, idx, 1)
        self.setLayout(layout)

    def get_values(self):
        values = []
        values.append(self.__edits[CONFIG_MODEL_TAG].currentText())
        for tag in self.__tags[2:]:
            values.append(self.__edits[tag].text())
        return values

    def load_values_from_table_row(self, table, row):
        self.__edits[CONFIG_MODEL_TAG].setCurrentText(table.item(row, 0).text())
        self.__edits[CONFIG_FRAMEWORK_TAG].setCurrentText(table.item(row, 1).text())
        self.__edits[CONFIG_DEVICE_TAG].setCurrentText(table.item(row, 2).text())
        self.__edits[CONFIG_CONFIG_TAG].setCurrentText(table.item(row, 3).text())

    def accept(self):
        if self.check():
            super().accept()
        else:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')

    def check(self):
        for tag in self._tags:
            if self._edits[tag].text() == '':
                return False
        return True
