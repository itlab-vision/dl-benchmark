from pathlib import Path

from ..processes import ProcessHandler


class TensorFlowLiteProcess(ProcessHandler):
    benchmark_app_name = 'tflite_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return TensorFlowLiteProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_tensorflow_script = Path.joinpath(self.inference_script_root, 'inference_tensorflowlite.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        dataset = self._test.dataset.path if self._test.dataset else None
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        common_params = (f'-m {model} -i {dataset} -b {batch} -d {device} -ni {iteration} '
                         f'--report_path {self.report_path}')

        common_params = self._add_optional_argument_to_cmd_line(common_params, '-i', dataset)

        time_limit = self._test.indep_parameters.test_time_limit
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--time', time_limit)

        channel_swap = self._test.dep_parameters.channel_swap
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--channel_swap', channel_swap)

        mean = self._test.dep_parameters.mean
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--mean', mean)

        input_scale = self._test.dep_parameters.input_scale
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_scale', input_scale)

        input_shape = self._test.dep_parameters.input_shape
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_shapes', input_shape)

        input_name = self._test.dep_parameters.input_name
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_name', input_name)

        layout = self._test.dep_parameters.layout
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--layout', layout)

        common_params = self._add_argument_to_cmd_line(common_params, '--raw_output', 'true')

        command_line = f'{python} {path_to_tensorflow_script} {common_params}'

        nthreads = self._test.dep_parameters.nthreads
        command_line = self._add_optional_argument_to_cmd_line(command_line, '-nthreads', nthreads)

        delegate = self._test.dep_parameters.delegate
        command_line = self._add_optional_argument_to_cmd_line(command_line, '--delegate_ext', delegate)

        delegate_options = self._test.dep_parameters.delegate_options
        command_line = self._add_optional_argument_to_cmd_line(command_line, '--delegate_options', delegate_options)

        return command_line
