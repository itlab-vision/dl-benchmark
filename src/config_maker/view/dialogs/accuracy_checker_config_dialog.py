import abc
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QMessageBox
# pylint: disable-next=E0401
from tags import CONFIG_MODEL_TAG, CONFIG_PARAMETERS_TAG, CONFIG_FRAMEWORK_TAG, CONFIG_DEVICE_TAG, CONFIG_CONFIG_TAG


class AccuracyCheckerConfigDialog(QDialog):
    def __init__(self, parent, models):
        super().__init__(parent)
        self.__parent = parent
        self.__models = models
        self.__frameworks = ['OpenVINO DLDT', 'Caffe', 'TensorFlow']
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
        self.__labels[CONFIG_PARAMETERS_TAG].setStyleSheet("font-weight: bold")

    def __create_edits(self):
        self.__edits = dict.fromkeys(self.__tags)
        self.__edits[CONFIG_MODEL_TAG] = QComboBox(self.__parent)
        self.__edits[CONFIG_MODEL_TAG].addItems(self.__models)
        self.__edits[CONFIG_FRAMEWORK_TAG] = QComboBox(self.__parent)
        self.__edits[CONFIG_FRAMEWORK_TAG].addItems(self.__frameworks)
        self.__edits[CONFIG_DEVICE_TAG] = QComboBox(self.__parent)
        self.__edits[CONFIG_DEVICE_TAG].addItems(('CPU', 'GPU', 'MYRIAD', 'CPU;GPU', 'CPU;MYRIAD', 'GPU;MYRIAD',
                                                  'CPU;GPU;MYRIAD'))
        self.__edits[CONFIG_CONFIG_TAG] = QLineEdit(self.__parent)

    def __create_layout(self):
        layout = QGridLayout()
        idx = 0
        layout.addWidget(self.__labels[CONFIG_PARAMETERS_TAG], 1, 0)
        for tag in self.__tags:
            if tag != CONFIG_PARAMETERS_TAG:
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
        values.append(self.__edits[CONFIG_FRAMEWORK_TAG].currentText())
        values.append(self.__edits[CONFIG_DEVICE_TAG].currentText())
        values.append(self.__edits[CONFIG_CONFIG_TAG].text())
        return values

    def load_values_from_table_row(self, table, row):
        self.__edits[CONFIG_MODEL_TAG].setCurrentText(table.item(row, 0).text())
        self.__edits[CONFIG_FRAMEWORK_TAG].setCurrentText(table.item(row, 1).text())
        self.__edits[CONFIG_DEVICE_TAG].setCurrentText(table.item(row, 2).text())
        self.__edits[CONFIG_CONFIG_TAG].setText(table.item(row, 3).text())

    def accept(self):
        if self.check():
            super().accept()
        else:
            QMessageBox.warning(self, 'Warning!', 'Not all lines are filled!')

    def check(self):
        return self.__edits[CONFIG_CONFIG_TAG].text() != ''
