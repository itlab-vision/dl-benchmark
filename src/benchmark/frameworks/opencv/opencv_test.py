from ..config_parser.test_reporter import Test


class OpenCVTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        parameters = {}
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Shape': self.dep_parameters.shape})
        parameters.update({'Layout': self.dep_parameters.layout})
        parameters.update({'Mean': self.dep_parameters.mean})
        parameters.update({'Scale': self.dep_parameters.scale})
        parameters.update({'Thread count': self.dep_parameters.thread_count})
        parameters.update({'Inference requests count': self.dep_parameters.inference_requests_count})
        optional_parameters_string = self._get_optional_parameters_string(parameters)

        report_res = {
            'task': self.model.task,
            'model': self.model.name,
            'dataset': self.dataset.name,
            'source_framework': self.model.source_framework,
            'inference_framework': self.indep_parameters.inference_framework,
            'precision': self.model.precision,
            'batch_size': self.indep_parameters.batch_size,
            'mode': 'Sync',
            'framework_params': optional_parameters_string,
        }

        return report_res
