from .launchers import Launcher
from .datasets import Dataset


class Test:
    def __init__(self, data):
        MODEL_NAME_TAG = 'name'
        LAUNCHERS_TAG = 'launchers'
        DATATSETS_TAG = 'datasets'

        self.model_name = data[MODEL_NAME_TAG]
        self.launchers = [Launcher(launcher_data) for launcher_data in data[LAUNCHERS_TAG]]
        self.datasets = [Dataset(dataset_data, self.launchers[0].adapter) for dataset_data in data[DATATSETS_TAG]]
