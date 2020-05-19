from PyQt5.QtWidgets import *
from models.deploy_config import *
from PyQt5 import QtCore


class DeployDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self._ip = QLineEdit(self)
        self._login = QLineEdit(self)
        self._password = QLineEdit(self)
        self._os = QLineEdit(self)
        self._download_folder = QLineEdit(self)
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
        layout.addWidget(self._ip, 0, 1)
        layout.addWidget(login_lb, 1, 0)
        layout.addWidget(self._login, 1, 1)
        layout.addWidget(password_lb, 2, 0)
        layout.addWidget(self._password, 2, 1)
        layout.addWidget(os_lb, 3, 0)
        layout.addWidget(self._os, 3, 1)
        layout.addWidget(download_folder_lb, 4, 0)
        layout.addWidget(self._download_folder, 4, 1)
        layout.addWidget(ok_btn, 5, 0)
        layout.addWidget(cancel_btn, 5, 1)
        self.setLayout(layout)

    def accept(self):
        if ((self._ip.text() == "") or (self._login.text() == "") or (self._password.text() == "") or
                (self._os.text() == "") or (self._download_folder.text() == "")):
            QMessageBox.warning(self, "Warning!", "Not all lines are filled!")
        else:
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def get_ip(self):
        return self._ip.text()

    def get_login(self):
        return self._login.text()

    def get_password(self):
        return self._password.text()

    def get_os(self):
        return self._os.text()

    def get_download_folder(self):
        return self._download_folder.text()

    def set_ip(self, ip):
        self._ip.setText(ip)

    def set_login(self, login):
        self._login.setText(login)

    def set_password(self, password):
        self._password.setText(password)

    def set_os(self, os):
        self._os.setText(os)

    def set_download_folder(self, download_folder):
        self._download_folder.setText(download_folder)

    def clear(self):
        self._ip.clear()
        self._login.clear()
        self._password.clear()
        self._os.clear()
        self._download_folder.clear()
