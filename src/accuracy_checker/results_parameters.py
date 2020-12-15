class ResultParameters:
    def __init__(self, status, model, launcher, dataset, precision, objects, accuracy):
        print(status, model, launcher, dataset, precision, objects, accuracy)
        self.status = status
        self.model = model
        self.launcher = launcher
        self.dataset = dataset
        self.precision = precision
        self.objects = objects
        self.accuracy = accuracy

    def get_result(self):
        return {'status': self.status, 'model': self.model, 'launcher': self.launcher, 'dataset': self.dataset,
                'precision': self.precision, 'objects': self.objects, 'accuracy': self.accuracy}

    @staticmethod
    def parser_test_result(result):
        TAG_MODEL = 'model:'
        TAG_LAUNCHER = 'launcher:'
        TAG_DATASET = 'dataset:'
        TAG_PRECISION = 'precision:'
        TAG_OBJECTS = 'objects'
        TAG_ACCURACY = 'accuracy:'

        result = [str.replace(' ', '') for str in result]
        result = [str.replace('\t', "") for str in result]

        has_error = False
        for str in result:
            if 'ERROR:' in str:
                has_error = True
                break

        status = 'FAILED' if has_error else 'SUCCESS'
        model = [value[len(TAG_MODEL):] for value in result if TAG_MODEL in value][0] if not has_error else ''
        launcher = [value[len(TAG_LAUNCHER):] for value in result if TAG_LAUNCHER in value][0] if not has_error else ''
        dataset = [value[len(TAG_DATASET):] for value in result if TAG_DATASET in value][0] if not has_error else ''
        precision = [value[len(TAG_PRECISION):] for value in result if TAG_PRECISION in value][0] if not has_error else ''
        objects = [value[:value.find(TAG_OBJECTS)] for value in result if TAG_OBJECTS in value][0] if not has_error else ''
        accuracies = [value[len(TAG_ACCURACY):] for value in result if TAG_ACCURACY in value] if not has_error else ['']

        return [ResultParameters(status, model, launcher, dataset, precision, objects, accuracy) for accuracy in accuracies]

    @staticmethod
    def parser_test_results(out):
        result_parameters = []
        start_result = 'Processing info:'
        count = out.count(start_result)
        begin = 0
        for idx in range(count):
            if idx != (count - 1):
                end = out.index(start_result, begin + 1) + 1
                result_parameters.append(ResultParameters.parser_test_result(out[begin:end]))
                begin = end
            else:
                result_parameters.append(ResultParameters.parser_test_result(out[begin:]))
        return result_parameters
