import abc
import json
from pathlib import Path

import numpy as np
import pandas as pd


class IOGprahAdapter(metaclass=abc.ABCMeta):
    def __init__(self, args, io_model_wrapper):
        self._batch_size = args.batch_size
        self._labels = getattr(args, 'labels', None)
        self._labels_map = []
        self._io_model_wrapper = io_model_wrapper

    @staticmethod
    def get_io_adapter(args, io_model_wrapper):
        task = args.task
        if task == 'node-classification':
            return NodeClassification(args, io_model_wrapper)

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


class NodeClassification(IOGprahAdapter):
    def __init__(self, args, io_model_wrapper):
        super().__init__(args, io_model_wrapper)

    def process_output(self, result, log, labels_file = None):
        if self._not_valid_result(result):
            log.warning('Model output is processed only for the number iteration = 1')
            return

        labels_file = labels_file or 'cora.json'
        self.load_labels_map(labels_file)

        result_layer_name = next(iter(result))
        result = result[result_layer_name]
        
        data = {'Node ID': [], 'Type': []}
        for i, val in enumerate(result):
            data['Node ID'].append(i)
            data['Type'].append(self._labels_map[val-1])

        df = pd.DataFrame(data)
        df.set_index('Node ID')
        with open('out_graph_classification.csv', 'w+') as file:
            df.to_csv(file, sep='\t', encoding='utf-8')
        
        log.info('Results save to out_graph_classification.csv')
        