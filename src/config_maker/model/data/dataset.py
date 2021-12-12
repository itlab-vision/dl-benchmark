from tags import CONFIG_DATASET_TAG, CONFIG_NAME_TAG, CONFIG_DATASET_PATH_TAG  # pylint: disable=E0401


class Dataset:
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path

    def __eq__(self, other):
        return self.name == other.name and self.path == other.path

    def get_str(self):
        return ';'.join([self.name, self.path])

    def create_dom(self, file):
        DOM_DATASET_TAG = file.createElement(CONFIG_DATASET_TAG)
        DOM_NAME_TAG = file.createElement(CONFIG_NAME_TAG)
        DOM_PATH_TAG = file.createElement(CONFIG_DATASET_PATH_TAG)

        DOM_NAME_TAG.appendChild(file.createTextNode(self.name))
        DOM_PATH_TAG.appendChild(file.createTextNode(self.path))
        DOM_DATASET_TAG.appendChild(DOM_NAME_TAG)
        DOM_DATASET_TAG.appendChild(DOM_PATH_TAG)
        return DOM_DATASET_TAG

    @staticmethod
    def parse(dom):
        parsed_datasets = dom.getElementsByTagName(CONFIG_DATASET_TAG)
        datasets = []
        for parsed_dataset in parsed_datasets:
            name = parsed_dataset.getElementsByTagName(CONFIG_NAME_TAG)[0].firstChild.data
            path = parsed_dataset.getElementsByTagName(CONFIG_DATASET_PATH_TAG)[0].firstChild.data
            datasets.append(Dataset(name, path))
        return datasets
