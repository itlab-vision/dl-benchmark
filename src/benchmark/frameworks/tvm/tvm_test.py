from collections import OrderedDict

from ..config_parser.test_reporter import Test


class TVMTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self, process):
        parameters = OrderedDict()
        parameters.update({'Device': self.indep_parameters.device})
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Framework': self.dep_parameters.framework})
        parameters.update({'HighLevelAPI': self.dep_parameters.high_level_api})
        parameters.update({'Optimization level': self.dep_parameters.optimization_level})
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
