import csv


class Result:
    def __init__(self, status, task, model, launcher, source_framework, device, dataset, precision, metric, accuracy):
        self.__params = {
            'status': status,
            'task': task,
            'model': model,
            'source_framework': source_framework,
            'launcher': launcher,
            'device': device,
            'dataset': self.update_dataset(dataset),
            'metric': metric,
            'precision': precision,
            'accuracy': accuracy,
        }

    @staticmethod
    def update_dataset(dataset):
        if 'imagenet' in dataset.lower():
            return 'ImageNet'
        elif 'coco' in dataset.lower():
            return 'MS COCO'
        else:
            return dataset

    @staticmethod
    def has_error(strings):
        has_error = False
        for str_ in strings:
            if 'error' in str_.lower():
                has_error = True
                break
        return has_error

    @staticmethod
    def parser_test_result(res, test, csv_file_name):
        res = [str_.replace(' ', '') for str_ in res]
        res = [str_.replace('\t', '') for str_ in res]
        tmp = [str_ for str_ in res if str_ != '']
        res = tmp

        error = Result.has_error(res)
        status = 'FAILED' if error else 'SUCCESS'
        accuracies = {}
        dataset = None
        if not error:
            try:
                with open(csv_file_name) as csvfile:
                    csv_file = csv.DictReader(csvfile, delimiter=',')
                    for row in csv_file:
                        value = float(row['metric_value']) * 100
                        accuracies[row['metric_name']] = f'{value:.{2}f}%'
                        dataset = row['dataset']
            except Exception as ex:
                print(f'ERROR! : {str(ex)}')
        else:
            accuracies = {'N/A': 'N/A'}
            dataset = 'N/A'
        if not accuracies:
            raise ValueError('Information about accuracy was not found in test result')

        test_result = [Result(status=status, task=test.model.task, model=test.model.name, launcher=test.framework,
                              source_framework=test.model.framework, device=test.device, dataset=dataset,
                              precision=test.model.precision, metric=metric, accuracy=accuracies[metric]) for metric in
                       accuracies.keys()]

        return test_result

    def is_failed(self):
        return self.__params['status'] == 'FAILED'

    def get_result_dict(self):
        return self.__params
