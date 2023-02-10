from ..config_parser.test_reporter import Test


class MXNetTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        other_param = ', '.join([f'Device: {self.indep_parameters.device}',
                                 f'Iteration count: {self.indep_parameters.iteration}',
                                 f'Input name: {self.dep_parameters.input_name}',
                                 f'Input shape: {self.dep_parameters.input_shape}',
                                 f'Normalization flag: {self.dep_parameters.normalize}',
                                 f'Mean: {self.dep_parameters.mean}',
                                 f'Standard deviation: {self.dep_parameters.std}',
                                 f'Channel swap: {self.dep_parameters.channel_swap}'])

        report_res = {
            'task': self.model.task,
            'model': self.model.name,
            'dataset': self.dataset.name,
            'source_framework': self.model.source_framework,
            'inference_framework': self.indep_parameters.inference_framework,
            'precision': self.model.precision,
            'batch_size': self.indep_parameters.batch_size,
            'framework_params': other_param,
        }

        return report_res
