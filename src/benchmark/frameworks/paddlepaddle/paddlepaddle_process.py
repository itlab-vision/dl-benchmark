from pathlib import Path

from ..processes import ProcessHandler


class PaddlePaddleProcess(ProcessHandler):
    benchmark_app_name = 'paddlepaddle_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return PaddlePaddleProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_paddlepaddle_script = Path.joinpath(self.inference_script_root, 'inference_paddlepaddle.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        params = self._test.model.weight
        dataset = self._test.dataset.path if self._test.dataset else None
        iteration = self._test.indep_parameters.iteration
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device

        common_params = (f'-m {model} -p {params} -ni {iteration} -i {dataset} -b {batch} -d {device} '
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

        output_names = self._test.dep_parameters.output_names
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--output_names', output_names)

        gpu_mem_size = self._test.dep_parameters.gpu_mem_size
        common_params = (
            self._add_optional_argument_to_cmd_line(common_params, '--memory_pool_init_size_mb', gpu_mem_size))

        common_params = self._add_argument_to_cmd_line(common_params, '--raw_output', 'true')

        command_line = f'{python} {path_to_paddlepaddle_script} {common_params}'

        nthreads = self._test.dep_parameters.nthreads
        command_line = self._add_optional_argument_to_cmd_line(command_line, '-nthreads', nthreads)

        return command_line
