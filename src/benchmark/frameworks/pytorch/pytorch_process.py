from pathlib import Path

from ..processes import ProcessHandler


class PyTorchProcess(ProcessHandler):
    benchmark_app_name = 'pytorch_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        log.info('Initialize pytorch process')
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return PyTorchProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_pytorch_script = Path.joinpath(self.inference_script_root, 'inference_pytorch.py')
        python = ProcessHandler.get_cmd_python_version()

        name = self._test.model.name
        model_pt = self._test.model.model
        dataset = self._test.dataset.path
        input_shape = self._test.dep_parameters.input_shape
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration
        report_path = self.report_path
        if ((name is not None)
                and (model_pt is None or model_pt == '')):
            common_params = (f'-mn {name} -i {dataset} -is {input_shape} '
                             f'-b {batch_size} -ni {iteration} --report_path {report_path}')
        elif ((model_pt is not None) or (model_pt != '')):
            common_params = (f'-m {model_pt} -i {dataset} -is {input_shape} '
                             f'-b {batch_size} -ni {iteration} --report_path {report_path}')
        else:
            raise Exception('Incorrect model parameters. Set model name or file name.')

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
