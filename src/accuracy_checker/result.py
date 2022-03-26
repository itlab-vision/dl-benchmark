import csv

class result:
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
            'accuracy': accuracy
        }

    def update_dataset(self, dataset):
        if 'imagenet' in dataset.lower():
            return 'ImageNet'
        elif 'coco' in dataset.lower():
            return 'MS COCO'
        else:
            return dataset

    def is_failed(self):
        return self.__params['status'] == 'FAILED'

    def get_result_dict(self):
        return self.__params

    @staticmethod
    def has_error(strings):
        has_error = False
        for str in strings:
            if 'error' in str.lower():
                has_error = True
                break
        return has_error

    @staticmethod
    def parser_test_result(res, test, csv_file_name):
        res = [str.replace(' ', '') for str in res]
        res = [str.replace('\t', "") for str in res]
        tmp = [str for str in res if str != '']
        res = tmp

        error = result.has_error(res)
        status = 'FAILED' if error else 'SUCCESS'
        accuracies = dict()
        dataset = None
        if not error:
            try:
                with open(csv_file_name) as csvfile:
                    csv_file = csv.DictReader(csvfile, delimiter=',')
                    for row in csv_file:
                        accuracies[row['metric_name']]= row['metric_value']
                        dataset = row['dataset']
            except:
                raise ValueError('File {} is not found!'.format(csv_file_name))
        else:
            accuracies = ['']
            dataset = 'N/A'
        if not accuracies:
            raise ValueError('Information about accuracy was not found in test result')

        return [result(status=status, task=test.model.task, model=test.model.name, launcher=test.framework,
                       source_framework=test.model.framework, device=test.device, dataset=dataset,
                       precision=test.model.precision, metric=metric, accuracy=accuracies[metric]) for metric in accuracies.keys()]
