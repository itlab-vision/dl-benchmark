from collections import OrderedDict

from ..config_parser.test_reporter import Test


class PyTorchTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        parameters = OrderedDict()
        parameters.update({'Device': self.indep_parameters.device})
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Input name': self.dep_parameters.input_name})
        parameters.update({'Normalization flag': self.dep_parameters.normalize})
        parameters.update({'Mean': self.dep_parameters.mean})
        parameters.update({'Standard deviation': self.dep_parameters.std})
        parameters.update({'Output Name': self.dep_parameters.output_name})
        parameters.update({'Model type': self.dep_parameters.model_type})
        parameters.update({'Inference mode': self.dep_parameters.inference_mode})
        other_param = self._get_optional_parameters_string(parameters)

        report_res = {
            'task': self.model.task,
            'model': self.model.name,
            'dataset': self.dataset.name,
            'source_framework': self.model.source_framework,
            'inference_framework': self.indep_parameters.inference_framework,
            'precision': self.model.precision,
            'batch_size': self.indep_parameters.batch_size,
            'mode': 'Sync',
            'framework_params': other_param,
        }

        return report_res
