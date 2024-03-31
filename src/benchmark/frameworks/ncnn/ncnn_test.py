from collections import OrderedDict

from ..config_parser.test_reporter import Test


class NcnnTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self):
        parameters = OrderedDict()
        parameters.update({'Device': self.indep_parameters.device})
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Input name': self.dep_parameters.input_name})
        parameters.update({'Input shape': self.dep_parameters.input_shape})
        parameters.update({'Thread count': self.dep_parameters.thread_count})
        other_param = self._get_optional_parameters_string(parameters)

        report_res = {
            'task': self.model.task,
            'model': self.model.name,
            'dataset': self.dataset.name,
            'batch_size': self.indep_parameters.batch_size,
            'framework_params': other_param,
        }

        return report_res
