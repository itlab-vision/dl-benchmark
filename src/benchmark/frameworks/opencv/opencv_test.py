from ..config_parser.test_reporter import Test


class OpenCVTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        parameters = {}
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Target device': self.indep_parameters.device})
        parameters.update({'Backend': self.dep_parameters.backend})
        parameters.update({'Scale': self.dep_parameters.scalefactor})
        parameters.update({'Size': self.dep_parameters.size})
        parameters.update({'Mean': self.dep_parameters.mean})
        parameters.update({'Channel swap': self.dep_parameters.swapRB})
        parameters.update({'Crop': self.dep_parameters.crop})
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
