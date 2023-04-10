from collections import OrderedDict

from ..config_parser.test_reporter import Test


class OpenVINOTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self, process):
        tensors_num = self.dep_parameters.infer_request
        if process.get_status() == 0 and not tensors_num:
            self._log.info('InferenceRequestsCount is not set in XML config, '
                           'will try to extract it from launcher JSON report or console output')
            tensors_num = process.extract_inference_param('nireq')

        if self.dep_parameters.mode.lower() == 'sync':
            infer_requests_count = 1
        else:
            infer_requests_count = tensors_num

        RUNTIME_PARAMETER_NAMES = ('INFERENCE_PRECISION_HINT', 'INFERENCE_NUM_THREADS', 'NUM_STREAMS',
                                   'OPTIMAL_NUMBER_OF_INFER_REQUESTS', 'AFFINITY')
        runtime_parameters = {key: process.extract_inference_param(key) for key in RUNTIME_PARAMETER_NAMES}

        parameters = OrderedDict()
        parameters.update({'Device': self.indep_parameters.device})
        parameters.update({'Frontend': self.dep_parameters.frontend})
        parameters.update({'Async request count': self.dep_parameters.async_request})
        parameters.update({'Infer request count': infer_requests_count})
        parameters.update({'Number of tensors': tensors_num})
        parameters.update({'Iteration count': self.indep_parameters.iteration})
        parameters.update({'Thread count': self.dep_parameters.nthreads})
        parameters.update({'Stream count': self.dep_parameters.nstreams})
        parameters.update({'Mean': self.dep_parameters.mean})
        parameters.update({'Scale': self.dep_parameters.input_scale})
        parameters.update({'Shape': self.dep_parameters.shape})
        parameters.update(runtime_parameters)
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
