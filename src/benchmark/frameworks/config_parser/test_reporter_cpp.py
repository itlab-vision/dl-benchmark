from .test_reporter import Test


class CppTest(Test):
    def get_report(self, process):
        tensors_num = self.dep_parameters.inference_requests_count
        json_report_content = process.get_json_report_content()
        if process.get_status() == 0 and not tensors_num:
            self._log.info('InferenceRequestsCount is not set in XML config, '
                           'will try to extract it from the launcher JSON report or console output')
            tensors_num = json_report_content['configurations_setup']['tensors_num']

        batch_size = self.indep_parameters.batch_size
        if process.get_status() == 0 and not batch_size:
            self._log.info('BatchSize is not set in XML config, '
                           'will try to extract it from the launcher JSON report')
            batch_size = json_report_content['configurations_setup']['batch_size']

        actual_iterations = json_report_content['execution_results'].get('iterations_num', 'N/A')

        parameters = self.prepare_framework_params()
        parameters['Infer request count'] = 1
        parameters['Number of tensors'] = tensors_num
        parameters['Iteration count'] = actual_iterations
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
