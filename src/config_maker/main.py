import sys
from PyQt5.QtWidgets import QApplication
from model.database import DataBase
from view.view import View
from presenter.presenter import Presenter


def main():
    try:
        app = QApplication([])
        model = DataBase()
        view = View()
        _ = Presenter(model, view)
        sys.exit(app.exec_())
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
