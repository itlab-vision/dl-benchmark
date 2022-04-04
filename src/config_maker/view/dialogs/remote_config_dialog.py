from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
# pylint: disable-next=E0401
from tags import CONFIG_IP_TAG, CONFIG_LOGIN_TAG, CONFIG_PASSWORD_TAG, CONFIG_OS_TAG, CONFIG_FTP_CLIENT_PATH_TAG, \
    CONFIG_CONFIG_TAG, CONFIG_EXECUTOR_TAG, CONFIG_LOG_FILE_TAG, CONFIG_RESULT_FILE_TAG, CONFIG_AC_DATASET_PATH_TAG, \
    CONFIG_DEFINITION_PATH, CONFIG_BENCHMARK_TAG, CONFIG_ACCURACY_CHECKER_TAG


class RemoteConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        benchmark_tags = [CONFIG_CONFIG_TAG, CONFIG_EXECUTOR_TAG, CONFIG_LOG_FILE_TAG, CONFIG_RESULT_FILE_TAG]
        accuracy_checker_tags = [CONFIG_CONFIG_TAG, CONFIG_EXECUTOR_TAG, CONFIG_AC_DATASET_PATH_TAG,
                                 CONFIG_DEFINITION_PATH, CONFIG_LOG_FILE_TAG, CONFIG_RESULT_FILE_TAG]
        self.tags = [CONFIG_IP_TAG, CONFIG_LOGIN_TAG, CONFIG_PASSWORD_TAG, CONFIG_OS_TAG, CONFIG_FTP_CLIENT_PATH_TAG]
        self.tags.extend(CONFIG_BENCHMARK_TAG + tag for tag in benchmark_tags)
        self.tags.extend(CONFIG_ACCURACY_CHECKER_TAG + tag for tag in accuracy_checker_tags)
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
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
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
