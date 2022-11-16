from collections import OrderedDict

from ..config_parser.test_reporter import Test


class OpenVINOTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        parameters = OrderedDict()
        parameters.update({'Device': self.indep_parameters.device})
        parameters.update({'Async request count': self.dep_parameters.async_request})
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Thread count': self.dep_parameters.nthreads})
        parameters.update({'Stream count': self.dep_parameters.nstreams})
        parameters.update({'Mean': self.dep_parameters.mean})
        parameters.update({'Scale': self.dep_parameters.input_scale})
        parameters.update({'Shape': self.dep_parameters.shape})
        other_param = self._get_optional_parameters_string(parameters)

        report_res = {
            'task': self.model.task,
            'model': self.model.name,
            'dataset': self.dataset.name,
            'source_framework': self.model.source_framework,
            'inference_framework': self.indep_parameters.inference_framework,
            'precision': self.model.precision,
            'batch_size': self.indep_parameters.batch_size,
            'mode': self.dep_parameters.mode,
            'framework_params': other_param,
        }

        return report_res
