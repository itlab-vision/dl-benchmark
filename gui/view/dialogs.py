from PyQt5.QtWidgets import *
from models.deploy_config import *
from PyQt5 import QtCore


class DeployDialog(QDialog):
    addComputerSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._ip = QLineEdit(self)
        self._login = QLineEdit(self)
        self._password = QLineEdit(self)
        self._os = QLineEdit(self)
        self._download_folder = QLineEdit(self)
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
            self.addComputerSignal.emit()
            super().accept()

    def get_computer(self):
        computer = DeployComputer(self._ip.text(), self._login.text(), self._password.text(), self._os.text(),
                              self._download_folder.text())
        self.__clear()
        return computer

    def __clear(self):
        self._ip.clear()
        self._login.clear()
        self._password.clear()
        self._os.clear()
        self._download_folder.clear()
