from PyQt5.QtWidgets import *
from models.models import *
from PyQt5 import QtCore


class RemoteDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ip = QLineEdit(self)
        self.login = QLineEdit(self)
        self.password = QLineEdit(self)
        self.os = QLineEdit(self)
        self.path_to_ftp_client = QLineEdit(self)
        self.benchmark_config = QLineEdit(self)
        self.log_file = QLineEdit(self)
        self.res_file = QLineEdit(self)
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Information about computer")
        ip_lb = QLabel("IP")
        login_lb = QLabel("Login")
        password_lb = QLabel("Password")
        os_lb = QLabel("OS")
        path_to_ftp_client_lb = QLabel("FTPClientPath")
        benchmark_config_lb = QLabel("BenchmarkConfig")
        log_file_lb = QLabel("LogFile")
        res_file_lb = QLabel("ResultFile")
        ok_btn = QPushButton("Ok")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout = QGridLayout()
        layout.addWidget(ip_lb, 0, 0)
        layout.addWidget(self.ip, 0, 1)
        layout.addWidget(login_lb, 1, 0)
        layout.addWidget(self.login, 1, 1)
        layout.addWidget(password_lb, 2, 0)
        layout.addWidget(self.password, 2, 1)
        layout.addWidget(os_lb, 3, 0)
        layout.addWidget(self.os, 3, 1)
        layout.addWidget(path_to_ftp_client_lb, 4, 0)
        layout.addWidget(self.path_to_ftp_client, 4, 1)
        layout.addWidget(benchmark_config_lb, 5, 0)
        layout.addWidget(self.benchmark_config, 5, 1)
        layout.addWidget(log_file_lb, 6, 0)
        layout.addWidget(self.log_file, 6, 1)
        layout.addWidget(res_file_lb, 7, 0)
        layout.addWidget(self.res_file, 7, 1)
        layout.addWidget(ok_btn, 8, 0)
        layout.addWidget(cancel_btn, 8, 1)
        self.setLayout(layout)

    def accept(self):
        if ((self.ip.text() == "") or (self.login.text() == "") or (self.password.text() == "") or
                (self.os.text() == "") or (self.path_to_ftp_client.text() == "") or
                (self.benchmark_config.text() == "") or (self.log_file.text() == "") or
                (self.res_file.text() == "")):
            QMessageBox.warning(self, "Warning!", "Not all lines are filled!")
        else:
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def clear(self):
        self.ip.clear()
        self.login.clear()
        self.password.clear()
        self.os.clear()
        self.path_to_ftp_client.clear()
        self.benchmark_config.clear()
        self.log_file.clear()
        self.res_file.clear()


class DeployDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.ip = QLineEdit(self)
        self.login = QLineEdit(self)
        self.password = QLineEdit(self)
        self.os = QLineEdit(self)
        self.download_folder = QLineEdit(self)
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Information about computer")
        ip_lb = QLabel("IP")
        login_lb = QLabel("Login")
        password_lb = QLabel("Password")
        os_lb = QLabel("OS")
        download_folder_lb = QLabel("Download folder")
        ok_btn = QPushButton("Ok")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        layout = QGridLayout()
        layout.addWidget(ip_lb, 0, 0)
        layout.addWidget(self.ip, 0, 1)
        layout.addWidget(login_lb, 1, 0)
        layout.addWidget(self.login, 1, 1)
        layout.addWidget(password_lb, 2, 0)
        layout.addWidget(self.password, 2, 1)
        layout.addWidget(os_lb, 3, 0)
        layout.addWidget(self.os, 3, 1)
        layout.addWidget(download_folder_lb, 4, 0)
        layout.addWidget(self.download_folder, 4, 1)
        layout.addWidget(ok_btn, 5, 0)
        layout.addWidget(cancel_btn, 5, 1)
        self.setLayout(layout)

    def accept(self):
        if ((self.ip.text() == "") or (self.login.text() == "") or (self.password.text() == "") or
                (self.os.text() == "") or (self.download_folder.text() == "")):
            QMessageBox.warning(self, "Warning!", "Not all lines are filled!")
        else:
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def clear(self):
        self.ip.clear()
        self.login.clear()
        self.password.clear()
        self.os.clear()
        self.download_folder.clear()
