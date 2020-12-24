class DataPresenter:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__connect_signals()

    def __connect_signals(self):
        self.__view.addDatasetSignal.connect(self.__handle_add_button)
        self.__view.deleteDatasetSignal.connect(self.__handle_delete_button)
        self.__view.changeDatasetSignal.connect(self.__handle_change_button)
        self.__view.clearSignal.connect(self.__handle_clear_button)

    def __handle_add_button(self, name, path):
        self.__model.add_dataset(name, path)
        self.__update_view()

    def __handle_delete_button(self, indexes):
        self.__model.delete_data(indexes)
        self.__update_view()

    def __handle_change_button(self, row, name, path):
        self.__model.change_dataset(row, name, path)
        self.__update_view()

    def __handle_clear_button(self):
        self.__model.clear()
        self.__update_view()

    def __update_view(self):
        self.__view.update(self.__model)
