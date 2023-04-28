from ..config_parser.test_reporter import Test


class OpenCVDNNPythonTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        parameters = {}
        parameters.update({'Device': self.indep_parameters.device})
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Backend': self.dep_parameters.backend})
        parameters.update({'Input scale': self.dep_parameters.input_scale})
        parameters.update({'Input shape': self.dep_parameters.input_shape})
        parameters.update({'Input name': self.dep_parameters.input_name})
        parameters.update({'Output names': self.dep_parameters.output_names})
        parameters.update({'Mean': self.dep_parameters.mean})
        parameters.update({'Std': self.dep_parameters.std})
        parameters.update({'Channel swap': self.dep_parameters.swapRB})
        parameters.update({'Crop': self.dep_parameters.crop})
        parameters.update({'Layout': self.dep_parameters.layout})
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
