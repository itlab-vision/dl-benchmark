from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from .data_widgets.data_widget import DataWidget  # pylint: disable=E0402
from .config_widgets.config_widget import ConfigWidget  # pylint: disable=E0402


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        tabs = self.__create_tabs()
        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        self.setLayout(layout)

    def __create_tabs(self):
        tabs = QTabWidget()
        self.data_tab = DataWidget(self)
        self.config_tab = ConfigWidget(self)
        tabs.resize(920, 560)
        tabs.addTab(self.data_tab, 'Data information')
        tabs.addTab(self.config_tab, 'Creating Configurations')
        return tabs

    def update(self, model):
        self.data_tab.update(model)
        self.config_tab.update(model)
