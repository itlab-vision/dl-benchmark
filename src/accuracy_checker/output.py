class OutputHandler:
    def __init__(self, table_name):
        self.__table_name = table_name

    def create_table(self):
        HEADERS = 'Status;Task type;Topology name;Framework;Inference Framework;Device;Infrastructure;Dataset;Accuracy type;Precision;Accuracy;'  # pylint: disable=line-too-long
        with open(self.__table_name, 'w') as table:
            table.write(HEADERS + '\n')
            table.close()

    def add_results(self, test, process, executor):
        results = process.get_result_parameters()
        hardware_info = executor.get_infrastructure()
        for idx, result in enumerate(results):
            result_dict = result.get_result_dict()
            result_dict['hardware'] = hardware_info
            self.__add_row_to_table(result_dict)

    def __add_row_to_table(self, result):
        report_row = self.__create_table_row(result)
        with open(self.__table_name, 'a') as table:
            table.write(report_row + '\n')
            table.close()

    @staticmethod
    def __create_table_row(result_dict):
        return '{status};{task};{model};{source_framework};{launcher};{device};{hardware};{dataset};{metric};' \
               '{precision};{accuracy};'.format(**result_dict)
