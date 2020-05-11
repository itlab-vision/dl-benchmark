class DeployPresenter(object):
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__view.delSignal.connect(self.handle_del_button)
        self.__view.clearSignal.connect(self.handle_clear_button)
        self.__view.addComputerSignal.connect(self.handle_add_computer)
        self.__view.changeComputerSignal.connect(self.handle_change_computer)
        self.__model.updateSignal.connect(self.update_view)

    def handle_del_button(self, indexes):
        self.__model.delete_computers(indexes)

    def handle_clear_button(self):
        self.__model.clear()

    def handle_add_computer(self, ip, login, password, os, download_folder):
        self.__model.add_computer(ip, login, password, os, download_folder)

    def handle_change_computer(self, row, ip, login, password, os, download_folder):
        self.__model.change_computer(row, ip, login, password, os, download_folder)

    def update_view(self, models):
        self.__view.update(models)
