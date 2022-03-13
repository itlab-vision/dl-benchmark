class result:
    def __init__(self, status, task, model, launcher, source_framework, device, dataset, precision, metric, accuracy):
        self.__params = {
            'status': status,
            'task': task,
            'model': model,
            'source_framework' : source_framework,
            'launcher': launcher,
            'device': device,
            'dataset': dataset,
            'metric': metric,
            'precision': precision,
            'accuracy': accuracy
        }

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
    def parser_test_result(res, test):
        TAG_DATASET = 'dataset:'
        TAG_OBJECTS = 'objects'

        res = [str.replace(' ', '') for str in res]
        res = [str.replace('\t', "") for str in res]
        tmp = [str for str in res if str != '']
        res = tmp

        error = result.has_error(res)
        status = 'FAILED' if error else 'SUCCESS'
        if not error:
            datasets = [value[len(TAG_DATASET):].replace('\r', '') for value in res if TAG_DATASET in value]
            if not datasets:
                raise ValueError('Information about dataset was not found in test result', idx)
            idx = [res.index(value) for value in res if TAG_OBJECTS in value]
            accuracies = [res[i][res[i].index(':') + 1:].replace('\r', '') for i in range(idx[0] + 1, len(res))]
        else:
            accuracies = ['']
            datasets = ['']
        if not accuracies:
            raise ValueError('Information about accuracy was not found in test result', idx)

        return [result(status=status, task=test.model.task, model=test.model.name, launcher=test.framework, \
                       source_framework=test.model.framework, device=test.device, dataset=datasets[0], \
                       precision=test.model.precision, metric='', accuracy=accuracy) for accuracy in accuracies]
