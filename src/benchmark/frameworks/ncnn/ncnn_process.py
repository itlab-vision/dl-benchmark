from pathlib import Path

from ..processes import ProcessHandler


class NcnnProcess(ProcessHandler):
    benchmark_app_name = 'ncnn_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        log.info('Initialize ncnn process')
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return NcnnProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_ncnn_script = Path.joinpath(self.inference_script_root, 'inference_ncnn.py')
        python = ProcessHandler.get_cmd_python_version()

        name = self._test.model.name
        model = self._test.model.model
        dataset = self._test.dataset.path
        input_shape = self._test.dep_parameters.input_shape
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration
        time_limit = self._test.indep_parameters.test_time_limit
        raw_output = self._test.indep_parameters.raw_output
        common_params = (f'-m {name} -i {dataset} -is {input_shape} -b {batch_size} '
                         f'-ni {iteration} --report_path {self.report_path}')

        if model and model != 'none':
            common_params = NcnnProcess._add_optional_argument_to_cmd_line(
                common_params, '--model', model)

        task = self._test.model.task
        if task and task.lower() != 'n/a':
            common_params = NcnnProcess._add_optional_argument_to_cmd_line(
                common_params, '--task', task)

        input_name = self._test.dep_parameters.input_name
        if input_name:
            common_params = NcnnProcess._add_optional_argument_to_cmd_line(
                common_params, '--input_name', input_name)

        thread_count = self._test.dep_parameters.thread_count
        if thread_count:
            common_params = NcnnProcess._add_optional_argument_to_cmd_line(
                common_params, '--num_threads', thread_count)

        device = self._test.indep_parameters.device
        if device:
            common_params = NcnnProcess._add_optional_argument_to_cmd_line(
                common_params, '--device', device)

        if time_limit:
            common_params = NcnnProcess._add_optional_argument_to_cmd_line(
                common_params, '--time', time_limit)

        if raw_output:
            common_params = NcnnProcess._add_argument_to_cmd_line(
                common_params, '--raw_output', 'true')

        command_line = f'{python} {path_to_ncnn_script} {common_params}'

        return command_line
