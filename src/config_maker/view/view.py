from PyQt5.QtWidgets import QMainWindow

from .widgets.main_widget import MainWidget  # pylint: disable=E0402


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(920, 560)
        self.setWindowTitle('Configuration Creator')
        self.tabs = MainWidget(self)
        self.setCentralWidget(self.tabs)
        self.show()

    def update(self, model):
        self.tabs.update(model)
