from ..config_parser.test_reporter import Test


class OnnxRuntimeTest(Test):
    def __init__(self, model, dataset, indep_parameters, dep_parameters):
        super().__init__(model, dataset, indep_parameters, dep_parameters)

    def get_report(self, process):
        tensors_num = self.dep_parameters.inference_requests_count
        json_report_content = process.get_json_report_content()
        if process.get_status() == 0 and not tensors_num:
            self._log.info('InferenceRequestsCount is not set in XML config, '
                           'will try to extract it from the launcher JSON report or console output')
            tensors_num = json_report_content['configurations_setup']['tensors_num']
        print(f'Json report content:\n'
              f'{json_report_content}')

        batch_size = self.indep_parameters.batch_size
        if process.get_status() == 0 and not batch_size:
            self._log.info('BatchSize is not set in XML config, '
                           'will try to extract it from the launcher JSON report')
            batch_size = json_report_content['configurations_setup']['batch_size']

        actual_iterations = json_report_content['execution_results']['iterations_num']

        parameters = {}
        parameters.update({'Iteration count': actual_iterations})
        parameters.update({'Shape': self.dep_parameters.shape})
        parameters.update({'Layout': self.dep_parameters.layout})
        parameters.update({'Mean': self.dep_parameters.mean})
        parameters.update({'Scale': self.dep_parameters.scale})
        parameters.update({'Thread count': self.dep_parameters.thread_count})
        parameters.update({'Infer request count': 1})
        parameters.update({'Number of tensors': tensors_num})
        optional_parameters_string = self._get_optional_parameters_string(parameters)

        report_res = {
            'task': self.model.task,
            'model': self.model.name,
            'dataset': self.dataset.name,
            'source_framework': self.model.source_framework,
            'inference_framework': self.indep_parameters.inference_framework,
            'precision': self.model.precision,
            'batch_size': batch_size,
            'mode': 'Sync',
            'framework_params': optional_parameters_string,
        }

        return report_res
