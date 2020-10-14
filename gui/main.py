import sys
from PyQt5.QtWidgets import QApplication
from model.database import DataBase
from view.view import View
from presenter.presenter import Presenter


def main():
    app = QApplication([])
    model = DataBase()
    view = View()
    presenter = Presenter(model, view)
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main() or 0)
