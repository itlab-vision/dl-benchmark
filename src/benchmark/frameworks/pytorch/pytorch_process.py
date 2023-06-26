from pathlib import Path

from ..processes import ProcessHandler


class PyTorchProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return PyTorchProcess(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    def _fill_command_line(self):
        path_to_pytorch_script = Path.joinpath(self.inference_script_root, 'inference_pytorch.py')
        python = ProcessHandler.get_cmd_python_version()

        name = self._test.model.name
        model = self._test.model.model
        weight = self._test.model.weight
        module = self._test.model.module
        dataset = self._test.dataset.path
        input_shape = self._test.dep_parameters.input_shape
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration

        common_params = (f'-mn {name} -i {dataset} -is {input_shape} '
                         f'-b {batch_size} -ni {iteration}')

        if model:
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--model', model)

        if weight:
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--weights', weight)

        if module:
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--module', module)

        input_name = self._test.dep_parameters.input_name
        if input_name:
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--input_name', input_name)

        mean = self._test.dep_parameters.mean
        if mean:
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--mean', mean)

        input_scale = self._test.dep_parameters.input_scale
        if input_scale:
            common_params = self._add_argument_to_cmd_line(
                common_params, '--input_scale', input_scale)

        output_name = self._test.dep_parameters.output_name
        if output_name:
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--output_name', output_name)

        device = self._test.indep_parameters.device
        if device:
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--device', device)

        common_params = PyTorchProcess._add_argument_to_cmd_line(
            common_params, '--raw_output', 'true')

        model_type = self._test.dep_parameters.model_type
        if model_type:
            common_params = PyTorchProcess._add_argument_to_cmd_line(
                common_params, '--model_type', model_type)

        inference_mode = self._test.dep_parameters.inference_mode
        if inference_mode:
            common_params = PyTorchProcess._add_argument_to_cmd_line(
                common_params, '--inference_mode', inference_mode)

        tensor_rt_precision = self._test.dep_parameters.tensor_rt_precision
        if tensor_rt_precision:
            common_params = PyTorchProcess._add_argument_to_cmd_line(
                common_params, '--tensor_rt_precision', tensor_rt_precision)

        layout = self._test.dep_parameters.layout
        if layout:
            common_params = self._add_optional_argument_to_cmd_line(common_params, '--layout', f'"{layout}"')

        input_type = self._test.dep_parameters.input_type
        if input_type:
            common_params = PyTorchProcess._add_argument_to_cmd_line(
                common_params, '--input_type', input_type)

        command_line = f'{python} {path_to_pytorch_script} {common_params}'

        return command_line
