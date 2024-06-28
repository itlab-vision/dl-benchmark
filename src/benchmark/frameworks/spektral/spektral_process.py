from pathlib import Path

from ..processes import ProcessHandler


class SpektralProcess(ProcessHandler):
    benchmark_app_name = 'spektral_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return SpektralProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_spektral_script = Path.joinpath(self.inference_script_root, 'inference_spektral.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        dataset = self._test.dataset.path if self._test.dataset else None
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration
        time_limit = self._test.indep_parameters.test_time_limit
        device = self._test.indep_parameters.device
        raw_output = self._test.indep_parameters.raw_output

        common_params = (f'-m {model} -b {batch_size} -d {device} -ni {iteration} '
                         f'--report_path {self.report_path}')

        common_params = self._add_optional_argument_to_cmd_line(common_params, '-i', dataset)

        common_params = self._add_optional_argument_to_cmd_line(common_params, '--time', time_limit)

        if raw_output:
            common_params = self._add_argument_to_cmd_line(common_params, '--raw_output', 'true')
        common_params = self._add_flag_to_cmd_line(common_params, '--restrisct_gpu_usage')

        command_line = f'{python} {path_to_spektral_script} {common_params}'

        return command_line
