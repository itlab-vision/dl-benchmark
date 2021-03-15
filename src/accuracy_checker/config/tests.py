from .launchers import launcher  # pylint: disable=E0402
from .datasets import dataset  # pylint: disable=E0402


class test:
    def __init__(self, data):
        MODEL_NAME_TAG = 'name'
        LAUNCHERS_TAG = 'launchers'
        DATATSETS_TAG = 'datasets'

        self.model_name = data[MODEL_NAME_TAG]
        self.launchers = [launcher(launcher_data) for launcher_data in data[LAUNCHERS_TAG]]
        self.datasets = [dataset(dataset_data) for dataset_data in data[DATATSETS_TAG]]
