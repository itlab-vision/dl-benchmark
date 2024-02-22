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
        model = self._test.model.model
        module = self._test.model.module
        weights = self._test.model.weight
        dataset = self._test.dataset.path if self._test.dataset else None
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration
        time_limit = self._test.indep_parameters.test_time_limit
        raw_output = self._test.indep_parameters.raw_output
        common_params = (f'-mn {name} -b {batch_size} -ni {iteration} --report_path {self.report_path}')

        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '-i', dataset)

        if model and model != 'none':
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--model', model)

        task = self._test.model.task
        if task and task.lower() != 'n/a':
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--task', task)

        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--module', module)

        if self._test.dep_parameters.use_model_config:
            common_params = PyTorchProcess._add_flag_to_cmd_line(common_params, '--use_model_config')

        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--weights', weights)

        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--time', time_limit)

        input_name = self._test.dep_parameters.input_name
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--input_name', input_name)

        input_shape = self._test.dep_parameters.input_shape
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--input_shapes',
                                                                          input_shape)

        mean = self._test.dep_parameters.mean
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--mean', mean)

        input_scale = self._test.dep_parameters.input_scale
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--input_scale', input_scale)

        output_name = self._test.dep_parameters.output_name
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--output_name', output_name)

        custom_models_links = self._test.indep_parameters.custom_models_links
        if custom_models_links and custom_models_links.lower() != 'n/a':
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--custom_models_links', custom_models_links)

        device = self._test.indep_parameters.device
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--device', device)

        num_gpu_devices = self._test.indep_parameters.num_gpu_devices
        if num_gpu_devices:
            common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--num_gpu_devices',
                                                                              num_gpu_devices)

        if raw_output:
            common_params = PyTorchProcess._add_argument_to_cmd_line(common_params, '--raw_output', 'true')

        model_type = self._test.dep_parameters.model_type
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--model_type', model_type)

        inference_mode = self._test.dep_parameters.inference_mode
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--inference_mode',
                                                                          inference_mode)

        tensor_rt_precision = self._test.dep_parameters.tensor_rt_precision
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--tensor_rt_precision',
                                                                          tensor_rt_precision)

        precision = self._test.model.precision
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--precision', precision)

        layout = self._test.dep_parameters.layout
        if f'"{layout}"' != '"None"':
            common_params = self._add_optional_argument_to_cmd_line(common_params, '--layout', f'"{layout}"')

        input_type = self._test.dep_parameters.input_type
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--input_type', input_type)

        compile_with_backend = self._test.dep_parameters.compile_with_backend
        common_params = PyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--compile_with_backend',
                                                                          compile_with_backend)

        num_inter_threads = self._test.dep_parameters.num_inter_threads
        if num_inter_threads:
            common_params = PyTorchProcess._add_argument_to_cmd_line(
                common_params, '--num_inter_threads', num_inter_threads)

        num_intra_threads = self._test.dep_parameters.num_intra_threads
        if num_intra_threads:
            common_params = PyTorchProcess._add_argument_to_cmd_line(
                common_params, '--num_intra_threads', num_intra_threads)

        command_line = f'{python} {path_to_pytorch_script} {common_params}'

        return command_line
