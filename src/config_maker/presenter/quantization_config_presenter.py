class QuantizationConfigPresenter:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__connect_signals()

    def __connect_signals(self):
        self.__view.tabs.config_tab.quantization_configs.showAddQModelDialogSignal.connect(self.__show_add_q_model_dialog)
        self.__view.tabs.config_tab.quantization_configs.showChangeQModelDialogSignal.connect(self.__show_change_q_model_dialog)
        self.__view.tabs.config_tab.quantization_configs.addQModelSignal.connect(self.__handle_add_button)
        self.__view.tabs.config_tab.quantization_configs.changeQModelSignal.connect(self.__handle_change_button)
        self.__view.tabs.config_tab.quantization_configs.deleteQModelSignal.connect(self.__handle_delete_button)
        self.__view.tabs.config_tab.quantization_configs.copyQModelSignal.connect(self.__handle_copy_button)
        self.__view.tabs.config_tab.quantization_configs.loadSignal.connect(self.__handle_load_button)
        self.__view.tabs.config_tab.quantization_configs.saveSignal.connect(self.__handle_save_button)
        self.__view.tabs.config_tab.quantization_configs.clearSignal.connect(self.__handle_clear_button)

    def __show_add_q_model_dialog(self):
        self.__view.tabs.config_tab.quantization_configs.show_add_q_model_dialog(
            self.__model.models.get_model_list_in_strings(), self.__model.data.get_dataset_list_in_strings())

    def __show_change_q_model_dialog(self):
        self.__view.tabs.config_tab.quantization_configs.show_change_q_model_dialog(
            self.__model.models.get_model_list_in_strings(), self.__model.data.get_dataset_list_in_strings())

    def __handle_add_button(self, pot_params, model_params, dependent_params):
        self.__model.quantization_config.add_q_model(pot_params, model_params, dependent_params)
        self.__update_view()

    def __handle_change_button(self, row, pot_params, model_params, dependent_params):
        self.__model.quantization_config.change_q_model(row, pot_params, model_params, dependent_params)
        self.__update_view()

    def __handle_delete_button(self, indexes):
        self.__model.quantization_config.delete_q_models(indexes)
        self.__update_view()

    def __handle_copy_button(self, indexes):
        self.__model.quantization_config.copy_q_models(indexes)
        self.__update_view()

    def __handle_load_button(self, path_to_config):
        self.__model.quantization_config.parse_config(path_to_config)
        self.__update_view()

    def __handle_save_button(self, path_to_config):
        status = self.__model.quantization_config.create_config(path_to_config)
        self.__view.tabs.config_tab.quantization_configs.show_message_status_saving(status)

    def __handle_clear_button(self):
        self.__model.quantization_config.clear()
        self.__update_view()

    def __update_view(self):
        self.__view.update(self.__model)
