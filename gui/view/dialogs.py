from PyQt5.QtWidgets import *
from models.deploy_config import *
from PyQt5 import QtCore


class DeployDialog(QDialog):

    addComputerSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__ip = QLineEdit(self)
        self.__login = QLineEdit(self)
        self.__password = QLineEdit(self)
        self.__os = QLineEdit(self)
        self.__download_folder = QLineEdit(self)
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Добавить модель")
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
        layout.addWidget(self.__ip, 0, 1)
        layout.addWidget(login_lb, 1, 0)
        layout.addWidget(self.__login, 1, 1)
        layout.addWidget(password_lb, 2, 0)
        layout.addWidget(self.__password, 2, 1)
        layout.addWidget(os_lb, 3, 0)
        layout.addWidget(self.__os, 3, 1)
        layout.addWidget(download_folder_lb, 4, 0)
        layout.addWidget(self.__download_folder, 4, 1)
        layout.addWidget(ok_btn, 5, 0)
        layout.addWidget(cancel_btn, 5, 1)
        self.setLayout(layout)

    def accept(self):
        if ((self.__ip.text() == "") or (self.__login.text() == "") or (self.__password.text() == "") or
                (self.__os.text() == "") or (self.__download_folder.text() == "")):
            QMessageBox.warning(self, "Warning!", "Not all lines are filled!")
        else:
            self.addComputerSignal.emit()
            super().accept()

    def reject(self):
        self.clear()
        super().reject()

    def get_ip(self):
        return self.__ip.text()

    def get_login(self):
        return self.__login.text()

    def get_password(self):
        return self.__password.text()

    def get_os(self):
        return self.__os.text()

    def get_download_folder(self):
        return self.__download_folder.text()

    def clear(self):
        self.__ip.clear()
        self.__login.clear()
        self.__password.clear()
        self.__os.clear()
        self.__download_folder.clear()
