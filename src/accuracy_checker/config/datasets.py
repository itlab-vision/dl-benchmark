from .metrics import Metric  # pylint: disable=E0402


class Dataset:
    def __init__(self, data):
        DATATSET_NAME_TAG = 'name'
        SIZE_TAG = 'subsample_size'
        METRICS_TAG = 'metrics'

        self.dataset_name = data[DATATSET_NAME_TAG]
        self.size = data[SIZE_TAG]
        self.metrics = [Metric.get_metric(metric_data) for metric_data in data[METRICS_TAG]]
