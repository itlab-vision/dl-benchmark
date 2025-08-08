from pathlib import Path

from ..processes import ProcessHandler


class ExecuTorchProcess(ProcessHandler):
    benchmark_app_name = 'executorch_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)
        self.path_to_script = Path.joinpath(self.inference_script_root, 'inference_executorch.py')

    @staticmethod
    def create_process(test, executor, log):
        return ExecuTorchProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        python = ProcessHandler.get_cmd_python_version(self._test)
        dataset = self._test.dataset.path
        input_shape = self._test.dep_parameters.input_shape
        layout = self._test.dep_parameters.layout
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration
        name = self._test.model.name
        model = self._test.model.model
        common_params = (f'-i {dataset} -is {input_shape} -b {batch_size} '
                         f'-ni {iteration} --report_path {self.report_path} '
                         f'--layout {layout} ')

        input_name = self._test.dep_parameters.input_name
        common_params = ExecuTorchProcess._add_optional_argument_to_cmd_line(
            common_params, '--input_name', input_name)

        normalize = self._test.dep_parameters.normalize
        if normalize == 'True':
            common_params = ExecuTorchProcess._add_flag_to_cmd_line(
                common_params, '--norm')

        mean = self._test.dep_parameters.mean
        common_params = ExecuTorchProcess._add_optional_argument_to_cmd_line(
            common_params, '--mean', mean)

        std = self._test.dep_parameters.std
        common_params = ExecuTorchProcess._add_optional_argument_to_cmd_line(
            common_params, '--std', std)

        channel_swap = self._test.dep_parameters.channel_swap
        common_params = ExecuTorchProcess._add_optional_argument_to_cmd_line(
            common_params, '--channel_swap', channel_swap)

        device = self._test.indep_parameters.device
        common_params = ExecuTorchProcess._add_optional_argument_to_cmd_line(
            common_params, '--device', device)

        common_params = ExecuTorchProcess._add_optional_argument_to_cmd_line(
            common_params, '-m', model)

        common_params = ExecuTorchProcess._add_optional_argument_to_cmd_line(
            common_params, '-mn', name)

        command_line = f'{python} {self.path_to_script} {common_params}'

        return command_line
