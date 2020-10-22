from .model_presenter import ModelPresenter
from .data_presenter import DataPresenter
from .benchmark_config_presenter import BenchmarkConfigPresenter
from .remote_config_presenter import RemoteConfigPresenter
from .deploy_config_presenter import DeployConfigPresenter


class Presenter:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__model_presenter = ModelPresenter(self.__model.models, self.__view.tabs.data_tab.model_settings)
        self.__data_presenter = DataPresenter(self.__model.data, self.__view.tabs.data_tab.data_settings)
        self.__benchmark_config_presenter = BenchmarkConfigPresenter(self.__model, self.__view)
        self.__remote_config_presenter = RemoteConfigPresenter(self.__model.remote_config,
                                                               self.__view.tabs.config_tab.remote_configs)
        self.__deploy_config_presenter = DeployConfigPresenter(self.__model.deploy_config,
                                                               self.__view.tabs.config_tab.deploy_configs)
