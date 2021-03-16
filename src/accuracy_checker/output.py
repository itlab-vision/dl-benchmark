class output_handler:
    def __init__(self, table_name):
        self.__table_name = table_name

    def create_table(self):
        HEADERS = 'Status;Task type;Topology name;Inference Framework;Device;Dataset;Accuracy type;Precision;Objects;Accuracy;'  # noqa: E501
        with open(self.__table_name, 'w') as table:
            table.write(HEADERS + '\n')
            table.close()

    def add_results(self, process, tests):
        results = process.get_result_parameters()
        for idx, result in enumerate(results):
            if result[0].is_failed():
                for i in range(len(tests[idx].datasets[0].metrics)):
                    self.__add_row_to_table(result[0], tests[idx], i)
            else:
                for i in range(len(result)):
                    self.__add_row_to_table(result[i], tests[idx], i)

    def __add_row_to_table(self, result, test, index):
        report_row = self.__create_table_row(result, test, index)
        with open(self.__table_name, 'a') as table:
            table.write(report_row + '\n')
            table.close()

    def __create_table_row(self, result, test, index):
        return '{0}'.format(self.__prepare_result(result.get_result_dict(), test, index))

    def __prepare_result(self, result, test, index):
        if result['model'] is not None and result['model'] != test.model_name:
            raise ValueError('Result model name and config model name do not match!')
        elif result['launcher'] is not None and result['launcher'] not in [launcher.framework.replace(' ', '') for launcher in test.launchers]:
            raise ValueError('Result launcher name and config launcher name do not match!')
        elif result['device'] is not None and result['device'] not in [launcher.device.replace(' ', '') for launcher in test.launchers]:
            raise ValueError('Result device name and config device name do not match!')
        elif result['dataset'] is not None and result['dataset'] not in [dataset.dataset_name.replace(' ', '') for dataset in test.datasets]:
            raise ValueError('Result dataset name and config dataset name do not match!')
        else:
            result_str = result['status'] + ';' + test.launchers[0].adapter + ';' + test.model_name + ';' +\
                         test.launchers[0].framework + ';' + test.launchers[0].device + ';' +\
                         test.datasets[0].dataset_name + ';' + test.datasets[0].metrics[index].get_type() + ';' +\
                         result['precision'] + ';' + result['objects'] + ';' + result['accuracy']
        return result_str
