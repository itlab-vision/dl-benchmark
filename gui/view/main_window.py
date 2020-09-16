import sys
from PyQt5.QtWidgets import *
from view.widgets.widgets_data import *
from view.widgets.widgets_config import *
from models.models import *
from presenters.presenters import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(920, 560)
        self.setWindowTitle('Configuration Creator')
        self.tabs = MainTabsWidget(self)
        self.setCentralWidget(self.tabs)
        self.show()

    def update(self, model):
        self.tabs.update(model)


class MainTabsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        tabs = self.__create_tabs()
        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        self.setLayout(layout)

    def __create_tabs(self):
        tabs = QTabWidget()
        self.data_tab = WidgetData(self)
        self.config_tab = WidgetConfig(self)
        tabs.resize(920, 560)
        tabs.addTab(self.data_tab, 'Data information')
        tabs.addTab(self.config_tab, 'Creating Configurations')
        return tabs

    def update(self, model):
        self.data_tab.update(model)
        self.config_tab.update(model)


def main():
    app = QApplication([])
    main_window = MainWindow()
    data_base = DataBase()
    presenter = Presenter(data_base, main_window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main() or 0)
