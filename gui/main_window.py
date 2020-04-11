import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QVBoxLayout, QApplication
from widgets.widgets_data import WidgetData


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(920, 560)
        self.setWindowTitle('Configuration Creator')
        table_widget = MainTabWidget(self)
        self.setCentralWidget(table_widget)
        self.show()


class MainTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        tabs = self.__create_tabs()
        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        self.setLayout(layout)

    def __create_tabs(self):
        tabs = QTabWidget()
        tab_data = WidgetData(self)
        tab_configuration = QWidget()  # configuration widget
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
