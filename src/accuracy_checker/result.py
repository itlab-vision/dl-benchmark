class result:
    def __init__(self, status, model, launcher, device, dataset, accuracy):
        self.__status = status
        self.__model = model
        self.__launcher = launcher
        self.__device = device
        self.__dataset = dataset
        self.__accuracy = accuracy

    def is_failed(self):
        return self.__status == 'FAILED'

    def get_result_dict(self):
        return {'status': self.__status, 'model': self.__model, 'launcher': self.__launcher, 'device': self.__device,
                'dataset': self.__dataset, 'accuracy': self.__accuracy}

    @staticmethod
    def has_error(strings):
        has_error = False
        for str in strings:
            if 'ERROR:' in str:
                has_error = True
                break
        return has_error

    @staticmethod
    def parser_test_result(res, idx):
        TAG_MODEL = 'model:'
        TAG_LAUNCHER = 'launcher:'
        TAG_DEVICE = 'device:'
        TAG_DATASET = 'dataset:'
        TAG_OBJECTS = 'objects'

        res = [str.replace(' ', '') for str in res]
        res = [str.replace('\t', "") for str in res]
        tmp = [str for str in res if str != '']
        res = tmp

        error = result.has_error(res)
        status = 'FAILED' if error else 'SUCCESS'
        models = [value[len(TAG_MODEL):].replace('\r', '') for value in res if TAG_MODEL in value]
        if not models:
            raise ValueError('Information about model was not found in test result', idx)
        launchers = [value[len(TAG_LAUNCHER):].replace('\r', '') for value in res if TAG_LAUNCHER in value]
        if not launchers:
            raise ValueError('Information about launcher was not found in test result', idx)
        devices = [value[len(TAG_DEVICE):].replace('\r', '') for value in res if TAG_DEVICE in value]
        if not devices:
            raise ValueError('Information about device was not found in test result', idx)
        datasets = [value[len(TAG_DATASET):].replace('\r', '') for value in res if TAG_DATASET in value]
        if not datasets:
            raise ValueError('Information about dataset was not found in test result', idx)
        if not error:
            idx = [res.index(value) for value in res if TAG_OBJECTS in value]
            accuracies = [res[i][res[i].index(':') + 1:].replace('\r', '') for i in range(idx[0] + 1, len(res))]
        else:
            accuracies = ['']
        if not accuracies:
            raise ValueError('Information about accuracy was not found in test result', idx)

        return [result(status=status, model=models[0], launcher=launchers[0], device=devices[0],
                       dataset=datasets[0], accuracy=accuracy) for accuracy in accuracies]

    @staticmethod
    def parser_test_results(out):
        results = []
        RESULT_START_TAG = 'Processing info:'
        results_idx = [out.index(value) for value in out if RESULT_START_TAG in value]
        count = len(results_idx)
        begin = results_idx[0]
        for idx in range(count):
            if idx != (count - 1):
                end = results_idx[idx + 1]
                results.append(result.parser_test_result(out[begin:end], idx))
                begin = end
            else:
                results.append(result.parser_test_result(out[begin:], idx))
        return results
