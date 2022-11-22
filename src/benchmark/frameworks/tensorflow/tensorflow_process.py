from pathlib import Path

from ..processes import ProcessHandler


class TensorFlowProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return TensorFlowProcess(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    def _fill_command_line(self):
        path_to_tensorflow_script = Path.joinpath(self.inference_script_root, 'inference_tensorflow.py')
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
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_shape', input_shape)
        input_name = self._test.dep_parameters.input_name
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_name', input_name)
        output_names = self._test.dep_parameters.output_names
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--output_names', output_names)
        num_inter_threads = self._test.dep_parameters.num_inter_threads
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--num_inter_threads', num_inter_threads)
        num_intra_threads = self._test.dep_parameters.num_intra_threads
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--num_intra_threads', num_intra_threads)

        common_params = self._add_argument_to_cmd_line(common_params, '--raw_output', 'true')

        command_line = f'{python} {path_to_tensorflow_script} {common_params}'

        nthreads = self._test.dep_parameters.nthreads
        if nthreads:
            command_line = self._add_env_to_cmd_line(command_line, 'OMP_NUM_THREADS', nthreads)
        kmp_affinity = self._test.dep_parameters.kmp_affinity
        if kmp_affinity:
            command_line = TensorFlowProcess._add_env_to_cmd_line(command_line, 'KMP_AFFINITY', kmp_affinity)

        return command_line
