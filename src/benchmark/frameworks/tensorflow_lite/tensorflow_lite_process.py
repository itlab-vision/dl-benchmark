from pathlib import Path

from ..processes import ProcessHandler


class TensorFlowLiteProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return TensorFlowLiteProcess(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    def _fill_command_line(self):
        path_to_tensorflow_script = Path.joinpath(self.inference_script_root, 'inference_tensorflowlite.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        common_params = f'-m {model} -i {dataset} -b {batch} -d {device} -ni {iteration}'

        channel_swap = self._test.dep_parameters.channel_swap
        if channel_swap:
            common_params = self._add_argument_to_cmd_line(common_params, '--channel_swap', channel_swap)
        mean = self._test.dep_parameters.mean
        if mean:
            common_params = self._add_argument_to_cmd_line(common_params, '--mean', mean)
        input_scale = self._test.dep_parameters.input_scale
        if input_scale:
            common_params = self._add_argument_to_cmd_line(common_params, '--input_scale', input_scale)
        input_shape = self._test.dep_parameters.input_shape
        if input_shape:
            common_params = self._add_argument_to_cmd_line(common_params, '--input_shapes', input_shape)
        input_name = self._test.dep_parameters.input_name
        if input_name:
            common_params = self._add_argument_to_cmd_line(common_params, '--input_name', input_name)
        layout = self._test.dep_parameters.layout
        if layout:
            common_params = self._add_argument_to_cmd_line(common_params, '--layout', layout)

        common_params = self._add_argument_to_cmd_line(common_params, '--raw_output', 'true')

        command_line = f'{python} {path_to_tensorflow_script} {common_params}'

        nthreads = self._test.dep_parameters.nthreads
        if nthreads:
            command_line = self._add_env_to_cmd_line(command_line, '--nthreads', nthreads)

        delegate = self._test.dep_parameters.delegate
        if delegate:
            command_line = self._add_env_to_cmd_line(command_line, '--delegate_ext', delegate)

        delegate_options = self._test.dep_parameters.delegate_options
        if delegate_options:
            command_line = self._add_env_to_cmd_line(command_line, '--delegate_options', delegate_options)

        return command_line
