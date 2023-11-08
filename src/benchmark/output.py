import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from csv_wrapper import CsvReport  # noqa: E402
from constants import Status  # noqa: E402


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
            'batch_fps': 'BATCH FPS',
            'latency_per_token': 'Latency per token',
            'error_type': 'Error type',
        }

        self._report = CsvReport(self.__table_name, self._column_names.values(), output_delimiter=csv_delimiter)

    @staticmethod
    def __create_table_row(executor, test, process):
        report = test.get_report(process=process)
        if process is not None:
            status_code = process.get_status()
            process_status = (Status(status_code) if (Status.has_value(status_code) and status_code != 1)
                              else Status.INFERENCE_FAILURE)
            report['input_shape'] = process.get_model_shape()
            report['status'] = 'Success' if status_code == 0 else 'Failed'
            reported_metrics = process.get_performance_metrics()
            report.update(reported_metrics)
            report['error_type'] = process_status.name if status_code else 'NO_ERROR'
        else:
            report['input_shape'] = 'Undefined'
            report['status'] = 'Failed'
            report['average_time'], report['fps'], report['latency'] = None, None, None
            report['error_type'] = Status.INFERENCE_EXCEPTION.name
        report['hardware'] = executor.get_infrastructure()
        return report

    def create_table(self):
        self._report.write_headers()

    def add_row_to_table(self, executor, test, process):
        report_row = self.__create_table_row(executor, test, process)
        row_dict = {column_name: report_row[key] for key, column_name in self._column_names.items()}
        self._report.append_row(row_dict)
