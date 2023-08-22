from pathlib import Path

from ..processes import ProcessHandler


class ONNXRuntimePythonProcess(ProcessHandler):
    benchmark_app_name = 'ort_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return ONNXRuntimePythonProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_onnx_script = Path.joinpath(self.inference_script_root, 'inference_onnx_runtime.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        dataset = self._test.dataset.path if self._test.dataset else None
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        common_params = (f'-m {model} -b {batch} -d {device} -ni {iteration} '
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
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_names', input_name)

        layout = self._test.dep_parameters.layout
        if layout:
            common_params = self._add_optional_argument_to_cmd_line(common_params, '--layout', f'"{layout}"')

        execution_providers = self._test.dep_parameters.execution_providers
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--execution_providers',
                                                                execution_providers)

        num_threads = self._test.dep_parameters.num_threads
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--number_threads', num_threads)
        num_inter_threads = self._test.dep_parameters.num_inter_threads
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--number_inter_threads',
                                                                num_inter_threads)

        execution_mode = self._test.dep_parameters.execution_mode
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--execution_mode', execution_mode)

        common_params = self._add_argument_to_cmd_line(common_params, '--raw_output', 'true')

        command_line = f'{python} {path_to_onnx_script} {common_params}'

        return command_line
