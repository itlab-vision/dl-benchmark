import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from csv_wrapper import CsvReport  # noqa: E402


class OutputHandler:
    def __init__(self, table_name, csv_delimiter):
        self.__table_name = table_name

        self._column_names = {
            'status': 'Status',
            'task': 'Task type',
            'model': 'Topology name',
            'source_framework': 'Framework',
            'launcher': 'Inference Framework',
            'device': 'Device',
            'hardware': 'Infrastructure',
            'dataset': 'Dataset',
            'metric': 'Accuracy type',
            'precision': 'Precision',
            'accuracy': 'Accuracy',
        }

        self._report = CsvReport(self.__table_name, self._column_names.values(), output_delimiter=csv_delimiter)

    def create_table(self):
        self._report.write_headers()

    def add_results(self, test, process, executor):
        results = process.get_result_parameters()
        hardware_info = executor.get_infrastructure()
        for result in results:
            result_dict = result.get_result_dict()
            result_dict['hardware'] = hardware_info

            row_dict = {column_name: result_dict[key] for key, column_name in self._column_names.items()}
            self._report.append_row(row_dict)
