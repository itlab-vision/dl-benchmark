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


class RemotePresenter(object):
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__view.delSignal.connect(self.handle_del_button)
        self.__view.loadSignal.connect(self.handle_load_button)
        self.__view.saveSignal.connect(self.handle_save_button)
        self.__view.clearSignal.connect(self.handle_clear_button)
        self.__view.addComputerSignal.connect(self.handle_add_computer)
        self.__view.changeComputerSignal.connect(self.handle_change_computer)

    def handle_del_button(self, indexes):
        self.__model.delete_computers(indexes)
        self.update_view(self.__model.get_computers())

    def handle_load_button(self, path_to_config):
        self.__model.parse_config(path_to_config)
        self.update_view(self.__model.get_computers())

    def handle_save_button(self):
        self.__view.show_message_status_saving(self.__model.create_config())

    def handle_clear_button(self):
        self.__model.clear()
        self.update_view(self.__model.get_computers())

    def handle_add_computer(self, ip, login, password, os, path_to_ftp_client, benchmark_config,
                            log_file, res_file):
        self.__model.add_computer(ip, login, password, os, path_to_ftp_client,
                                  benchmark_config, log_file, res_file)
        self.update_view(self.__model.get_computers())

    def handle_change_computer(self, row, ip, login, password, os, path_to_ftp_client,
                               benchmark_config, log_file, res_file):
        self.__model.change_computer(row, ip, login, password, os, path_to_ftp_client,
                                     benchmark_config, log_file, res_file)
        self.update_view(self.__model.get_computers())

    def update_view(self, models):
        self.__view.update(models)


class DeployPresenter(object):
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__view.delSignal.connect(self.handle_del_button)
        self.__view.loadSignal.connect(self.handle_load_button)
        self.__view.saveSignal.connect(self.handle_save_button)
        self.__view.clearSignal.connect(self.handle_clear_button)
        self.__view.addComputerSignal.connect(self.handle_add_computer)
        self.__view.changeComputerSignal.connect(self.handle_change_computer)

    def handle_del_button(self, indexes):
        self.__model.delete_computers(indexes)
        self.update_view(self.__model.get_computers())

    def handle_load_button(self, path_to_config):
        self.__model.parse_config(path_to_config)
        self.update_view(self.__model.get_computers())

    def handle_save_button(self):
        self.__view.show_message_status_saving(self.__model.create_config())

    def handle_clear_button(self):
        self.__model.clear()
        self.update_view(self.__model.get_computers())

    def handle_add_computer(self, ip, login, password, os, download_folder):
        self.__model.add_computer(ip, login, password, os, download_folder)
        self.update_view(self.__model.get_computers())

    def handle_change_computer(self, row, ip, login, password, os, download_folder):
        self.__model.change_computer(row, ip, login, password, os, download_folder)
        self.update_view(self.__model.get_computers())

    def update_view(self, models):
        self.__view.update(models)
