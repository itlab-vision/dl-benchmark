class BenchmarkConfigPresenter:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__connect_signals()

    def __connect_signals(self):
        self.__view.tabs.config_tab.benchmark_configs.showAddTestDialogSignal.connect(self.__show_add_test_dialog)
        self.__view.tabs.config_tab.benchmark_configs.showChangeTestDialogSignal.connect(self.__show_change_test_dialog)
        self.__view.tabs.config_tab.benchmark_configs.addTestSignal.connect(self.__handle_add_button)
        self.__view.tabs.config_tab.benchmark_configs.changeTestSignal.connect(self.__handle_change_button)
        self.__view.tabs.config_tab.benchmark_configs.deleteTestSignal.connect(self.__handle_delete_button)
        self.__view.tabs.config_tab.benchmark_configs.copyTestSignal.connect(self.__handle_copy_button)
        self.__view.tabs.config_tab.benchmark_configs.loadSignal.connect(self.__handle_load_button)
        self.__view.tabs.config_tab.benchmark_configs.saveSignal.connect(self.__handle_save_button)
        self.__view.tabs.config_tab.benchmark_configs.clearSignal.connect(self.__handle_clear_button)

    def __show_add_test_dialog(self):
        self.__view.tabs.config_tab.benchmark_configs.show_add_test_dialog(
            self.__model.models.get_model_list_in_strings(), self.__model.data.get_dataset_list_in_strings())

    def __show_change_test_dialog(self):
        self.__view.tabs.config_tab.benchmark_configs.show_change_test_dialog(
            self.__model.models.get_model_list_in_strings(), self.__model.data.get_dataset_list_in_strings())

    def __handle_add_button(self, args):
        self.__model.benchmark_config.add_test(*args)
        self.__update_view()

    def __handle_change_button(self, args):
        self.__model.benchmark_config.change_test(*args)
        self.__update_view()

    def __handle_delete_button(self, indexes):
        self.__model.benchmark_config.delete_tests(indexes)
        self.__update_view()

    def __handle_copy_button(self, indexes):
        self.__model.benchmark_config.copy_tests(indexes)
        self.__update_view()

    def __handle_load_button(self, path_to_config):
        models, data = self.__model.benchmark_config.parse_config(path_to_config)
        self.__model.models.set_models(models)
        self.__model.data.set_data(data)
        self.__update_view()

    def __handle_save_button(self, path_to_config):
        status = self.__model.benchmark_config.create_config(path_to_config)
        self.__view.tabs.config_tab.benchmark_configs.show_message_status_saving(status)

    def __handle_clear_button(self):
        self.__model.benchmark_config.clear()
        self.__update_view()

    def __update_view(self):
        self.__view.update(self.__model)
