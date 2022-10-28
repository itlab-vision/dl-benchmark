class OutputHandler:
    def __init__(self, table_name):
        self.__table_name = table_name

    @staticmethod
    def __create_table_row(executor, test, process):
        status = 'Success' if process.get_status() == 0 else 'Failed'
        test_parameters = test.get_report().replace('input_shape', process.get_model_shape())
        average_time, fps, latency = process.get_performance_metrics()
        hardware_info = executor.get_infrastructure()

        return ';'.join([status, test_parameters, hardware_info, str(average_time), str(latency), str(fps)])

    def create_table(self):
        headers = ';'.join(['Status',
                            'Task type',
                            'Topology name',
                            'Dataset',
                            'Framework',
                            'Inference Framework',
                            'Input blob sizes',
                            'Precision',
                            'Batch size',
                            'Mode',
                            'Parameters',
                            'Infrastructure',
                            'Average time of single pass (s)',
                            'Latency',
                            'FPS'])
        with open(self.__table_name, 'w') as table:
            table.write(headers + '\n')
            table.close()

    def add_row_to_table(self, executor, test, process):
        report_row = self.__create_table_row(executor, test, process)
        with open(self.__table_name, 'a') as table:
            table.write(report_row + '\n')
            table.close()
