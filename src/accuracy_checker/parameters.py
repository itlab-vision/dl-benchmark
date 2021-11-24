import os
import yaml


class parameters:
    def __init__(self, source, annotations=None, definitions=None, extensions=None):
        self.source = source
        self.annotations = annotations
        self.definitions = definitions
        self.extensions = extensions
        self.list_of_datasets = self.__load_dataset_definitions(definitions)

    def __load_dataset_definitions(self, path_to_dataset_definitions):
        datasets = None
        if path_to_dataset_definitions is not None:
            if not os.path.isfile(path_to_dataset_definitions):
                raise ValueError('Wrong path to dataset definitions file!')
            with open(path_to_dataset_definitions, 'r') as f:
                datasets = yaml.safe_load(f)['datasets']
        return datasets
