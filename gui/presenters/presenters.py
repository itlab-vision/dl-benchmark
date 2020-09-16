class ModelPresenter(object):
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__view.delSignal.connect(self.handle_del_button)
        self.__view.loadSignal.connect(self.handle_load_button)
        #self.__view.saveSignal.connect(self.handle_save_button)
        self.__view.clearSignal.connect(self.handle_clear_button)
        self.__view.addModelSignal.connect(self.handle_add_model)
        self.__view.changeModelSignal.connect(self.handle_change_model)

    def handle_del_button(self, indexes):
        self.__model.delete_models(indexes)
        self.update_view(self.__model.get_models())

    def handle_load_button(self, path_to_config):
        self.__model.parse_config(path_to_config)
        self.update_view(self.__model.get_models())

    def handle_save_button(self):
        self.__view.show_message_status_saving(self.__model.create_config())

    def handle_clear_button(self):
        self.__model.clear()
        self.update_view(self.__model.get_models())

    def handle_add_model(self, task, name, precision, framework, model_path, weights_path):
        self.__model.add_model(task, name, precision, framework, model_path, weights_path)
        self.update_view(self.__model.get_models())

    def handle_change_model(self, row, task, name, precision, framework, model_path, weights_path):
        self.__model.change_model(row, task, name, precision, framework, model_path, weights_path)
        self.update_view(self.__model.get_models())

    def update_view(self, models):
        self.__view.update(models)


class DataPresenter(object):
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__view.delSignal.connect(self.handle_del_button)
        self.__view.loadSignal.connect(self.handle_load_button)
        #self.__view.saveSignal.connect(self.handle_save_button)
        self.__view.clearSignal.connect(self.handle_clear_button)
        self.__view.addDatasetSignal.connect(self.handle_add_dataset)
        self.__view.changeDatasetSignal.connect(self.handle_change_dataset)

    def handle_del_button(self, indexes):
        self.__model.delete_data(indexes)
        self.update_view(self.__model.get_data())

    def handle_load_button(self, path_to_config):
        self.__model.parse_config(path_to_config)
        self.update_view(self.__model.get_data())

    def handle_save_button(self):
        self.__view.show_message_status_saving(self.__model.create_config())

    def handle_clear_button(self):
        self.__model.clear()
        self.update_view(self.__model.get_data())

    def handle_add_dataset(self, name, path):
        self.__model.add_dataset(name, path)
        self.update_view(self.__model.get_data())

    def handle_change_dataset(self, row, name, path):
        self.__model.change_dataset(row, name, path)
        self.update_view(self.__model.get_data())

    def update_view(self, models):
        self.__view.update(models)


class BenchmarkPresenter(object):
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__view.delSignal.connect(self.handle_del_button)
        self.__view.loadSignal.connect(self.handle_load_button)
        self.__view.saveSignal.connect(self.handle_save_button)
        self.__view.clearSignal.connect(self.handle_clear_button)
        self.__view.addTestSignal.connect(self.handle_add_test)
        self.__view.changeTestSignal.connect(self.handle_change_test)

    def handle_del_button(self, indexes):
        self.__model.delete_tests(indexes)
        self.update_view(self.__model.get_tests())

    def handle_load_button(self, path_to_config):
        self.__model.parse_config(path_to_config)
        self.update_view(self.__model.get_tests())

    def handle_save_button(self):
        self.__view.show_message_status_saving(self.__model.create_config())

    def handle_clear_button(self):
        self.__model.clear()
        self.update_view(self.__model.get_tests())

    def handle_add_test(self, model, dataset, framework, batch_size, device, iter_count, test_time_limit, mode,
                        extension, async_req_count, thread_count, stream_count, channel_swap, mean, input_scale):
        self.__model.add_test(model, dataset, framework, batch_size, device, iter_count, test_time_limit, mode,
                        extension, async_req_count, thread_count, stream_count, channel_swap, mean, input_scale)
        self.update_view(self.__model.get_tests())

    def handle_change_test(self, row, model, dataset, framework, batch_size, device, iter_count, test_time_limit, mode,
                        extension, async_req_count, thread_count, stream_count, channel_swap, mean, input_scale):
        self.__model.change_test(row, model, dataset, framework, batch_size, device, iter_count, test_time_limit, mode,
                        extension, async_req_count, thread_count, stream_count, channel_swap, mean, input_scale)
        self.update_view(self.__model.get_tests())

    def update_view(self, models):
        self.__view.update(models)


class Presenter:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__connect_signals()

    def __connect_signals(self):
        self.__connect_model_signals()
        self.__connect_data_signals()
        self.__connect_benchmark_signals()
        self.__connect_remote_signals()
        self.__connect_deploy_signals()

    # models signals
    def __connect_model_signals(self):
        self.__view.tabs.data_tab.model_settings.addModelSignal.connect(self.__model_handle_add_button)
        self.__view.tabs.data_tab.model_settings.delModelSignal.connect(self.__model_handle_del_button)
        self.__view.tabs.data_tab.model_settings.changeModelSignal.connect(self.__model_handle_change_button)

    def __model_handle_add_button(self, task, name, precision, framework, model_path, weights_path):
        self.__model.models.add_model(task, name, precision, framework, model_path, weights_path)
        self.__update_view()

    def __model_handle_del_button(self, indexes):
        self.__model.models.delete_models(indexes)
        self.__update_view()

    def __model_handle_change_button(self, row, task, name, precision, framework, model_path, weights_path):
        self.__model.models.change_model(row, task, name, precision, framework, model_path, weights_path)
        self.__update_view()

    # data signals
    def __connect_data_signals(self):
        self.__view.tabs.data_tab.data_settings.addDatasetSignal.connect(self.__data_handle_add_button)
        self.__view.tabs.data_tab.data_settings.delDatasetSignal.connect(self.__data_handle_del_button)
        self.__view.tabs.data_tab.data_settings.changeDatasetSignal.connect(self.__data_handle_change_button)

    def __data_handle_add_button(self, name, path):
        self.__model.data.add_dataset(name, path)
        self.__update_view()

    def __data_handle_del_button(self, indexes):
        self.__model.data.delete_data(indexes)
        self.__update_view()

    def __data_handle_change_button(self, row, name, path):
        self.__model.data.change_dataset(row, name, path)
        self.__update_view()

    # benchmark signals
    def __connect_benchmark_signals(self):
        pass

    # remote signals
    def __connect_remote_signals(self):
        self.__view.tabs.config_tab.remote_configs.addComputerSignal.connect(self.__remote_handle_add_button)
        self.__view.tabs.config_tab.remote_configs.delComputerSignal.connect(self.__remote_handle_del_button)
        self.__view.tabs.config_tab.remote_configs.changeComputerSignal.connect(self.__remote_handle_change_button)
        self.__view.tabs.config_tab.remote_configs.loadSignal.connect(self.__remote_handle_load_button)
        self.__view.tabs.config_tab.remote_configs.saveSignal.connect(self.__remote_handle_save_button)
        self.__view.tabs.config_tab.remote_configs.clearSignal.connect(self.__remote_handle_clear_button)

    def __remote_handle_add_button(self, ip, login, password, os, path_to_ftp_client, benchmark_config, log_file,
                                   res_file):
        self.__model.remote_config.add_computer(ip, login, password, os, path_to_ftp_client, benchmark_config, log_file,
                                                res_file)
        self.__update_view()

    def __remote_handle_del_button(self, indexes):
        self.__model.remote_config.delete_computers(indexes)
        self.__update_view()

    def __remote_handle_change_button(self, row, ip, login, password, os, path_to_ftp_client, benchmark_config,
                                      log_file, res_file):
        self.__model.remote_config.change_computer(row, ip, login, password, os, path_to_ftp_client, benchmark_config,
                                                   log_file, res_file)
        self.__update_view()

    def __remote_handle_load_button(self, path_to_config):
        self.__model.remote_config.parse_config(path_to_config)
        self.__update_view()

    def __remote_handle_save_button(self):
        status = self.__model.remote_config.create_config()
        self.__view.tabs.config_tab.remote_configs.show_message_status_saving(status)

    def __remote_handle_clear_button(self):
        self.__model.remote_config.clear()
        self.__update_view()

    # deploy signals
    def __connect_deploy_signals(self):
        self.__view.tabs.config_tab.deploy_configs.addComputerSignal.connect(self.__deploy_handle_add_button)
        self.__view.tabs.config_tab.deploy_configs.delComputerSignal.connect(self.__deploy_handle_del_button)
        self.__view.tabs.config_tab.deploy_configs.changeComputerSignal.connect(self.__deploy_handle_change_button)
        self.__view.tabs.config_tab.deploy_configs.loadSignal.connect(self.__deploy_handle_load_button)
        self.__view.tabs.config_tab.deploy_configs.saveSignal.connect(self.__deploy_handle_save_button)
        self.__view.tabs.config_tab.deploy_configs.clearSignal.connect(self.__deploy_handle_clear_button)

    def __deploy_handle_add_button(self, ip, login, password, os, download_folder):
        self.__model.deploy_config.add_computer(ip, login, password, os, download_folder)
        self.__update_view()

    def __deploy_handle_del_button(self, indexes):
        self.__model.deploy_config.delete_computers(indexes)
        self.__update_view()

    def __deploy_handle_change_button(self, row, ip, login, password, os, download_folder):
        self.__model.deploy_config.change_computer(row, ip, login, password, os, download_folder)
        self.__update_view()

    def __deploy_handle_load_button(self, path_to_config):
        self.__model.deploy_config.parse_config(path_to_config)
        self.__update_view()

    def __deploy_handle_save_button(self):
        status = self.__model.deploy_config.create_config()
        self.__view.tabs.config_tab.deploy_configs.show_message_status_saving(status)

    def __deploy_handle_clear_button(self):
        self.__model.deploy_config.clear()
        self.__update_view()

    def __update_view(self):
        self.__view.update(self.__model)
