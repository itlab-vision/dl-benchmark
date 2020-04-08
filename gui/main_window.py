import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QVBoxLayout, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(920, 560)
        self.setWindowTitle('Configuration Creator')
        self.table_widget = MainTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class MainTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.tab_data = QWidget()  # data widget
        self.tab_configuration = QWidget()  # configuration widget
        self.tabs.resize(920, 560)
        self.tabs.addTab(self.tab_data, "Работа с данными")
        self.tabs.addTab(self.tab_configuration, "Создание конфигураций")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout((self.layout))


def main():
    app = QApplication([])
    main_window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main() or 0)
