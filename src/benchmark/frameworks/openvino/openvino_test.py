from ..config_parser.test_reporter import Test


class OpenVINOTest(Test):
    def get_report(self, process):
        tensors_num = self.dep_parameters.infer_request
        if process.get_status() == 0 and not tensors_num:
            self._log.info('InferenceRequestsCount is not set in XML config, '
                           'will try to extract it from the launcher JSON report or console output')
            tensors_num = process.extract_inference_param('nireq')

        if self.dep_parameters.mode.lower() == 'sync':
            infer_requests_count = 1
        else:
            infer_requests_count = tensors_num

        RUNTIME_PARAMETER_NAMES = ('INFERENCE_PRECISION_HINT', 'INFERENCE_NUM_THREADS', 'NUM_STREAMS',
                                   'OPTIMAL_NUMBER_OF_INFER_REQUESTS', 'AFFINITY', 'Count')
        runtime_parameters = {key: process.extract_inference_param(key) for key in RUNTIME_PARAMETER_NAMES}

        if runtime_parameters['Count'] is not None:
            # for benchmark app
            actual_iterations = int(runtime_parameters['Count'].strip().split(' ')[0])
            runtime_parameters.pop('Count')
        else:
            # effective for sync/async python launchers
            actual_iterations = self.indep_parameters.iteration

        parameters = self.prepare_framework_params()
        parameters['Infer request count'] = infer_requests_count
        parameters['Number of tensors'] = tensors_num
        parameters['Iteration count'] = actual_iterations
        parameters.update(runtime_parameters)
        optional_parameters_string = self._get_optional_parameters_string(parameters)

        report_res = {
            'task': self.model.task,
            'model': self.model.name,
            'dataset': self.dataset.name,
            'source_framework': self.model.source_framework,
            'inference_framework': self.indep_parameters.inference_framework,
            'precision': self.model.precision,
            'batch_size': self.indep_parameters.batch_size,
            'mode': self.dep_parameters.mode,
            'framework_params': optional_parameters_string,
        }

        return report_res
