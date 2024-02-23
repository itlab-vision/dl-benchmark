from .graph_adapter import IOGraphAdapter
import pandas as pd


class NodeClassification(IOGraphAdapter):
    def __init__(self, args, io_model_wrapper):
        super().__init__(args, io_model_wrapper)

    def process_output(self, result, log, filename='out_graph_classification.csv', labels_file=None):
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
            data['Type'].append(self._labels_map[val - 1])

        df = pd.DataFrame(data)
        df.set_index('Node ID')
        with open(filename, 'w+') as file:
            df.to_csv(file, sep='\t', encoding='utf-8')

        log.info(f'Results save to {filename}')
