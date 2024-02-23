import json
from pathlib import Path
import numpy as np

class IOGraphAdapter():
    def __init__(self, args, io_model_wrapper):
        self._batch_size = args.batch_size
        self._labels = getattr(args, 'labels', None)
        self._labels_map = []
        self._io_model_wrapper = io_model_wrapper

    @staticmethod
    def get_io_adapter(args, io_model_wrapper):
        from .node_classification import NodeClassification
        from .feed_dorward import FeedForwardIO

        task = args.task
        if task == 'node-classification':
            return NodeClassification(args, io_model_wrapper)
        elif task == 'feedforward':
            return FeedForwardIO(args, io_model_wrapper)
        else:
            raise ValueError(f"Invalid task type '{task}'")

    @staticmethod
    def _not_valid_result(result):
        return result is None

    def load_labels_map(self, default_labels_map_file):
        if not self._labels:
            self._labels = Path(__file__).parent / 'labels' / default_labels_map_file
        file_extension = Path(self._labels).suffix
        if file_extension == '.json':
            self._labels_map = np.array(json.load(open(self._labels, 'r'))).tolist()
        else:
            with open(self._labels, 'r') as f:
                self._labels_map = [line.strip() for line in f]
