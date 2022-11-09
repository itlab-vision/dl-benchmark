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
            'dataset': 'Dataset',
            'source_framework': 'Framework',
            'inference_framework': 'Inference Framework',
            'input_shape': 'Input blob sizes',
            'precision': 'Precision',
            'batch_size': 'Batch size',
            'mode': 'Mode',
            'framework_params': 'Parameters',
            'hardware': 'Infrastructure',
            'average_time': 'Average time of single pass (s)',
            'latency': 'Latency',
            'fps': 'FPS',
        }

        self._report = CsvReport(self.__table_name, self._column_names.values(), output_delimiter=csv_delimiter)

    @staticmethod
    def __create_table_row(executor, test, process):
        report = test.get_report()
        if process is not None:
            report['input_shape'] = process.get_model_shape()
            report['status'] = 'Success' if process.get_status() == 0 else 'Failed'
            report['average_time'], report['fps'], report['latency'] = process.get_performance_metrics()
        else:
            report['input_shape'] = 'Undefined'
            report['status'] = 'Failed'
            report['average_time'], report['fps'], report['latency'] = None, None, None
        report['hardware'] = executor.get_infrastructure()
        return report

    def create_table(self):
        self._report.write_headers()

    def add_row_to_table(self, executor, test, process):
        report_row = self.__create_table_row(executor, test, process)
        row_dict = {column_name: report_row[key] for key, column_name in self._column_names.items()}
        self._report.append_row(row_dict)
