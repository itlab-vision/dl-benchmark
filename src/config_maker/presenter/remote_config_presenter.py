class RemoteConfigPresenter:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__connect_signals()

    def __connect_signals(self):
        self.__view.addComputerSignal.connect(self.__handle_add_button)
        self.__view.deleteComputerSignal.connect(self.__handle_delete_button)
        self.__view.changeComputerSignal.connect(self.__handle_change_button)
        self.__view.copyComputerSignal.connect(self.__handle_copy_button)
        self.__view.loadSignal.connect(self.__handle_load_button)
        self.__view.saveSignal.connect(self.__handle_save_button)
        self.__view.clearSignal.connect(self.__handle_clear_button)

    def __handle_add_button(self, *args):
        self.__model.add_computer(*args)
        self.__update_view()

    def __handle_delete_button(self, indexes):
        self.__model.delete_computers(indexes)
        self.__update_view()

    def __handle_change_button(self, row, *args):
        self.__model.change_computer(row, *args)
        self.__update_view()

    def __handle_copy_button(self, indexes):
        self.__model.copy_computers(indexes)
        self.__update_view()

    def __handle_load_button(self, path_to_config):
        self.__model.parse_config(path_to_config)
        self.__update_view()

    def __handle_save_button(self, path_to_config):
        status = self.__model.create_config(path_to_config)
        self.__view.show_message_status_saving(status)

    def __handle_clear_button(self):
        self.__model.clear()
        self.__update_view()

    def __update_view(self):
        self.__view.update(self.__model)
