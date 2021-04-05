class result:
    def __init__(self, status, model, launcher, device, dataset, precision, objects, accuracy):
        self.__status = status
        self.__model = model
        self.__launcher = launcher
        self.__device = device
        self.__dataset = dataset
        self.__precision = precision
        self.__objects = objects
        self.__accuracy = accuracy

    def is_failed(self):
        return self.__status == 'FAILED'

    def get_result_dict(self):
        return {'status': self.__status, 'model': self.__model, 'launcher': self.__launcher, 'device': self.__device,
                'dataset': self.__dataset, 'precision': self.__precision, 'objects': self.__objects,
                'accuracy': self.__accuracy}

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
        TAG_PRECISION = 'precision:'
        TAG_OBJECTS = 'objects'
        TAG_ACCURACY = 'accuracy:'

        res = [str.replace(' ', '') for str in res]
        res = [str.replace('\t', "") for str in res]

        error = result.has_error(res)
        status = 'FAILED' if error else 'SUCCESS'
        models = [value[len(TAG_MODEL):] for value in res if TAG_MODEL in value]
        if not models:
            raise ValueError('Information about model was not found in test result', idx)
        launchers = [value[len(TAG_LAUNCHER):] for value in res if TAG_LAUNCHER in value]
        if not launchers:
            raise ValueError('Information about launcher was not found in test result', idx)
        devices = [value[len(TAG_DEVICE):] for value in res if TAG_DEVICE in value]
        if not devices:
            raise ValueError('Information about device was not found in test result', idx)
        datasets = [value[len(TAG_DATASET):] for value in res if TAG_DATASET in value]
        if not datasets:
            raise ValueError('Information about dataset was not found in test result', idx)
        precisions = [value[len(TAG_PRECISION):] for value in res if TAG_PRECISION in value] if not error else ['']
        if not precisions:
            raise ValueError('Information about precision was not found in test result', idx)
        objects = [value[:value.find(TAG_OBJECTS)] for value in res if TAG_OBJECTS in value] if not error else ['']
        if not objects:
            raise ValueError('Information about objects was not found in test result', idx)
        accuracies = [value[len(TAG_ACCURACY):] for value in res if TAG_ACCURACY in value] if not error else ['']
        if not accuracies:
            raise ValueError('Information about accuracy was not found in test result', idx)

        return [result(status, models[0], launchers[0], devices[0], datasets[0], precisions[0], objects[0], accuracy)
                for accuracy in accuracies]

    @staticmethod
    def parser_test_results(out):
        results = []
        result_start = 'Processing info:'
        count = out.count(result_start)
        begin = out.index(result_start)
        for idx in range(count):
            if idx != (count - 1):
                end = out.index(result_start, begin + 1) + 1
                results.append(result.parser_test_result(out[begin:end], idx))
                begin = end
            else:
                results.append(result.parser_test_result(out[begin:], idx))
        return results
