class output_handler:
    def __init__(self, table_name):
        self.__table_name = table_name

    def create_table(self):
        HEADERS = 'Status;Task type;Topology name;Inference Framework;Device;Dataset;Accuracy type;Precision;Objects;Accuracy;'  # noqa: E501
        with open(self.__table_name, 'w') as table:
            table.write(HEADERS + '\n')
            table.close()

    def add_results(self, process, tests):
        result_list = process.get_result_parameters()
        for results in result_list:
            for idx, result in enumerate(results):
                result_dict = result.get_result_dict()
                result_list = [result_dict['model'], result_dict['launcher'], result_dict['dataset'],
                               result_dict['device']]
                test = self.__find_test(tests, *result_list)
                if not test:
                    raise ValueError('Test "', *result_dict, '" was not found!')
                result_dict['adapter'] = test['adapter']
                if result.is_failed():
                    for metric in test['metrics']:
                        result_dict['metric'] = metric.get_type()
                        self.__add_row_to_table(result_dict)
                else:
                    result_dict['metric'] = test['metrics'][idx].get_type()
                    self.__add_row_to_table(result_dict)

    def __find_test(self, tests, model, framework, dataset, device):
        for test in tests:
            if model == test.model_name:
                for launcher in test.launchers:
                    if framework == launcher.framework and device == launcher.device:
                        for data in test.datasets:
                            if dataset == data.dataset_name:
                                return {'adapter': launcher.adapter, 'metrics': data.metrics}
        return None

    def __add_row_to_table(self, result_dict):
        report_row = self.__create_table_row(result_dict)
        with open(self.__table_name, 'a') as table:
            table.write(report_row + '\n')
            table.close()

    def __create_table_row(self, result_dict):
        return '{status};{adapter};{model};{launcher};{device};{dataset};{metric};{precision};{objects};{accuracy};'.\
            format(**result_dict)
