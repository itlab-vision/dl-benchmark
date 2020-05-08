import sys
from PyQt5.QtWidgets import *
from view.widgets.widgets_data import *
from view.widgets.widgets_config import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(920, 560)
        self.setWindowTitle('Configuration Creator')
        table_widget = MainTabWidget(self)
        self.setCentralWidget(table_widget)
        self.show()


class MainTabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._tabs = self.__create_tabs()
        layout = QVBoxLayout(self)
        layout.addWidget(self._tabs)
        self.setLayout(layout)

    def __create_tabs(self):
        tabs = QTabWidget()
        tab_data = WidgetData(self)
        tab_configuration = WidgetConfig(self)
        tabs.resize(920, 560)
        tabs.addTab(tab_data, 'Работа с данными')
        tabs.addTab(tab_configuration, 'Создание конфигураций')
        return tabs


def main():
    app = QApplication([])
    main_window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main() or 0)
