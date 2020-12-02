class output_handler:
    def __init__(self, table_name):
        self.__table_name = table_name

    def create_table(self):
        HEADERS = 'Status;Task type;Topology name;Inference Framework;Dataset;Precision;Objects;Type accuracy;Accuracy;'  # noqa: E501
        with open(self.__table_name, 'w') as table:
            table.write(HEADERS + '\n')
            table.close()

    def add_results(self, process, tests):
        results = process.get_result_parameters()
        for idx, result in enumerate(results):
            self.__add_row_to_table(result, tests[idx])

    def __add_row_to_table(self, result, test):
        report_row = self.__create_table_row(result, test)
        with open(self.__table_name, 'a') as table:
            table.write(report_row + '\n')
            table.close()

    def __create_table_row(self, result, test):
        return '{0}'.format(self.__prepare_result(result.get_result(), test))

    def __prepare_result(self, result, test):
        if result['model'] != test.model_name:
            raise ValueError('Result model name and config model name do not match!')
        elif result['dataset'] not in [dataset.dataset_name for dataset in test.datasets]:
            raise ValueError('Result dataset name and config dataset name do not match!')
        elif result['launcher'] not in [launcher.framework for launcher in test.launchers]:
            raise ValueError('Result launcher name and config launcher name do not match!')
        else:
            result_str = result['status'] + ';' + test.launchers[0].adapter + ';' + result['model'] + ';' + result['launcher'] + \
                  ';' + result['dataset'] + ';' + result['precision'] + ';' + result['objects'] + ';' + 'accuracy' + \
                  ';' + result['accuracy'][0]
        return result_str
