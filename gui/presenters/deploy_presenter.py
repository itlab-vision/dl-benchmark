class DeployPresenter(object):
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__view.get_buttons().clearSignal.connect(self.handle_clear_button)
        self.__view.get_dialog_add_computer().addComputerSignal.connect(self.handle_add_computer)
        self.__model.updateSignal.connect(self.update_model)

    def handle_clear_button(self):
        self.__model.clear()

    def handle_add_computer(self):
        dialog = self.__view.get_dialog_add_computer()
        self.__model.add_computer(dialog.get_ip(), dialog.get_login(), dialog.get_password(),
                                  dialog.get_os(), dialog.get_download_folder())

    def update_model(self):
        self.__view.get_table().update(self.__model.get_computers())
