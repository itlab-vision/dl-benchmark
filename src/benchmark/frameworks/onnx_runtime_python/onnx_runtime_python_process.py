from pathlib import Path

from ..processes import ProcessHandler


class ONNXRuntimePythonProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return ONNXRuntimePythonProcess(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    def _fill_command_line(self):
        path_to_onnx_script = Path.joinpath(self.inference_script_root, 'inference_onnx_runtime.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        common_params = f'-m {model} -i {dataset} -b {batch} -d {device} -ni {iteration}'

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
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--layout', layout)

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
