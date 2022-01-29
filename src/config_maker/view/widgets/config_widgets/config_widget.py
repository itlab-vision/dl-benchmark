from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox
from .benchmark_config_widget import BenchmarkConfigWidget  # pylint: disable=E0402
from .accuracy_checker_config_widget import AccuracyCheckerConfigWidget  # pylint: disable=E0402
from .remote_config_widget import RemoteConfigWidget  # pylint: disable=E0402
from .deploy_config_widget import DeployConfigWidget  # pylint: disable=E0402


class ConfigWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        grid = QGridLayout()
        self._widgets = self.__create_dict()
        grid.addWidget(self.__create_combobox(), 0, 0)
        grid.addWidget(self._widgets['Benchmark configuration'], 1, 0)
        self._widgets['Benchmark configuration'].show()
        grid.addWidget(self._widgets['AccuracyChecker configuration'], 1, 0)
        self._widgets['AccuracyChecker configuration'].hide()
        grid.addWidget(self._widgets['Remote configuration'], 1, 0)
        self._widgets['Remote configuration'].hide()
        grid.addWidget(self._widgets['Deploy configuration'], 1, 0)
        self._widgets['Deploy configuration'].hide()
        self.setLayout(grid)

    def __create_combobox(self):
        menu = QComboBox()
        menu.addItems(self._widgets.keys())
        menu.activated[str].connect(self.onActivated)  # pylint: disable=E1136
        return menu

    def __create_dict(self):
        self.benchmark_configs = BenchmarkConfigWidget(self)
        self.accuracy_checker_configs = AccuracyCheckerConfigWidget(self)
        self.remote_configs = RemoteConfigWidget(self)
        self.deploy_configs = DeployConfigWidget(self)
        dictionary = {'Benchmark configuration': self.benchmark_configs,
                      'AccuracyChecker configuration': self.accuracy_checker_configs,
                      'Remote configuration': self.remote_configs,
                      'Deploy configuration': self.deploy_configs}
        return dictionary

    def onActivated(self, type):
        for key in self._widgets:
            if key == type:
                self._widgets[key].show()
            else:
                self._widgets[key].hide()

    def update(self, model):
        self.benchmark_configs.update(model.benchmark_config)
        self.accuracy_checker_configs.update(model.accuracy_checker_config)
        self.remote_configs.update(model.remote_config)
        self.deploy_configs.update(model.deploy_config)
