class output_handler:
    def __init__(self, table_name):
        self.__table_name = table_name

    def create_table(self):
        HEADERS = 'Status;Task type;Topology name;Framework;Inference Framework;Device;Dataset;Accuracy type;Precision;Accuracy;'  # noqa: E501
        with open(self.__table_name, 'w') as table:
            table.write(HEADERS + '\n')
            table.close()

    def add_results(self, test, process):
        result_list = process.get_result_parameters()
        for results in result_list:
            for idx, result in enumerate(results):
                result_dict = result.get_result_dict()
                result_dict['model'] = test.model.name
                result_dict['launcher'] = test.framework
                result_dict['precision'] = test.model.precision
                result_dict['task'] = test.model.task
                result_dict['source_framework'] = test.model.framework
                if result.is_failed():
                    for metric in test.metrics:
                        result_dict['metric'] = metric
                        self.__add_row_to_table(result_dict)
                else:
                    result_dict['metric'] = test.metrics[idx]
                    self.__add_row_to_table(result_dict)

    def __add_row_to_table(self, result):
        report_row = self.__create_table_row(result)
        with open(self.__table_name, 'a') as table:
            table.write(report_row + '\n')
            table.close()

    def __create_table_row(self, result_dict):
        return '{status};{task};{model};{source_framework};{launcher};{device};{dataset};{metric};' \
               '{precision};{accuracy};'.format(**result_dict)
