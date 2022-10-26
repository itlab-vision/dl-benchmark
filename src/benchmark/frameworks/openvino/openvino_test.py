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
        other_param = []
        for key in parameters:
            if parameters[key] is not None:
                other_param.append(f'{key}: {parameters[key]}')
        other_param = ', '.join(other_param)

        report_res = (f'{self.model.task};{self.model.name};{self.dataset.name};{self.model.source_framework};'
                      f'{self.indep_parameters.inference_framework};input_shape;{self.model.precision};'
                      f'{self.indep_parameters.batch_size};{self.dep_parameters.mode};{other_param}')

        return report_res
