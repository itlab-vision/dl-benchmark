class ModelPresenter:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__connect_signals()

    def __connect_signals(self):
        self.__view.addModelSignal.connect(self.__handle_add_button)
        self.__view.deleteModelSignal.connect(self.__handle_delete_button)
        self.__view.changeModelSignal.connect(self.__handle_change_button)
        self.__view.clearSignal.connect(self.__handle_clear_button)

    def __handle_add_button(self, task, name, precision, framework, model_path, weights_path):
        self.__model.add_model(task, name, precision, framework, model_path, weights_path)
        self.__update_view()

    def __handle_delete_button(self, indexes):
        self.__model.delete_models(indexes)
        self.__update_view()

    def __handle_change_button(self, row, task, name, precision, framework, model_path, weights_path):
        self.__model.change_model(row, task, name, precision, framework, model_path, weights_path)
        self.__update_view()

    def __handle_clear_button(self):
        self.__model.clear()
        self.__update_view()

    def __update_view(self):
        self.__view.update(self.__model)
