from .metrics import MetricAccuracy  # pylint: disable=E0402


class Dataset:
    def __init__(self, data, adapter):
        DATATSET_NAME_TAG = 'name'
        SIZE_TAG = 'subsample_size'
        METRICS_TAG = 'metrics'

        self.dataset_name = data[DATATSET_NAME_TAG]
        self.size = data[SIZE_TAG]
        self.metrics = []
        for metric_data in data[METRICS_TAG]:
            if adapter == 'classification':
                self.metrics.append(MetricAccuracy(metric_data))
