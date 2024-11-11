from pathlib import Path

from ..processes import ProcessHandler


class TensorFlowProcess(ProcessHandler):
    benchmark_app_name = 'tensorflow_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return TensorFlowProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_tensorflow_script = Path.joinpath(self.inference_script_root, 'inference_tensorflow.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        dataset = self._test.dataset.path if self._test.dataset else None
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration
        raw_output = self._test.indep_parameters.raw_output

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
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_shape', input_shape)

        input_name = self._test.dep_parameters.input_name
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_name', input_name)

        output_names = self._test.dep_parameters.output_names
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--output_names', output_names)

        num_inter_threads = self._test.dep_parameters.num_inter_threads
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--num_inter_threads', num_inter_threads)

        num_intra_threads = self._test.dep_parameters.num_intra_threads
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--num_intra_threads', num_intra_threads)

        task = self._test.model.task
        if task and task.lower() != 'n/a':
            common_params = self._add_optional_argument_to_cmd_line(common_params, '--task', task)

        if raw_output:
            common_params = self._add_argument_to_cmd_line(common_params, '--raw_output', 'true')
        common_params = self._add_flag_to_cmd_line(common_params, '--restrisct_gpu_usage')

        use_xla = self._test.dep_parameters.use_xla
        if use_xla:
            common_params = self._add_optional_argument_to_cmd_line(common_params, '--use_xla', 'true')

        command_line = f'{python} {path_to_tensorflow_script} {common_params}'

        nthreads = self._test.dep_parameters.nthreads
        if nthreads:
            command_line = self._add_env_to_cmd_line(command_line, 'OMP_NUM_THREADS', nthreads)
        kmp_affinity = self._test.dep_parameters.kmp_affinity
        if kmp_affinity:
            command_line = self._add_env_to_cmd_line(command_line, 'KMP_AFFINITY', kmp_affinity)
        if use_xla:
            command_line = self._add_env_to_cmd_line(command_line, 'TF_XLA_FLAGS',
                                                     '--tf_xla_auto_jit=2 \
                                                     --tf_xla_cpu_global_jit')

        return command_line
