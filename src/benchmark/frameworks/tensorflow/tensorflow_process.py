from pathlib import Path

from ..processes import ProcessHandler


class TensorFlowProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def __add_channel_swap_for_cmd_line(command_line, channel_swap):
        return f'{command_line} --channel_swap {channel_swap}'

    @staticmethod
    def __add_mean_for_cmd_line(command_line, mean):
        return f'{command_line} --mean {mean}'

    @staticmethod
    def __add_input_scale_for_cmd_line(command_line, input_scale):
        return f'{command_line} --input_scale {input_scale}'

    @staticmethod
    def __add_input_shape_for_cmd_line(command_line, input_shape):
        return f'{command_line} --input_shape {input_shape}'

    @staticmethod
    def __add_input_name_for_cmd_line(command_line, input_name):
        return f'{command_line} --input_name {input_name}'

    @staticmethod
    def __add_output_names_for_cmd_line(command_line, output_names):
        return f'{command_line} --output_names {output_names}'

    @staticmethod
    def __add_nthreads_for_cmd_line(command_line, nthreads):
        return f'OMP_NUM_THREADS={command_line} {nthreads}'

    @staticmethod
    def __add_num_inter_threads_for_cmd_line(command_line, num_inter_threads):
        return f'{command_line} --num_inter_threads {num_inter_threads}'

    @staticmethod
    def __add_num_intra_threads_for_cmd_line(command_line, num_intra_threads):
        return f'{command_line} --num_intra_threads {num_intra_threads}'

    @staticmethod
    def __add_kmp_affinity_for_cmd_line(command_line, kmp_affinity):
        return f'KMP_AFFINITY={command_line} {kmp_affinity}'

    @staticmethod
    def __add_raw_output_time_for_cmd_line(command_line, raw_output):
        return f'{command_line} {raw_output}'

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
        path_to_tensorflow_scrypt = Path.joinpath(self.inference_script_root, 'inference_tensorflow.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        common_params = f'-m {model} -i {dataset} -b {batch} -d {device} -ni {iteration}'

        channel_swap = self._test.dep_parameters.channel_swap
        if channel_swap:
            common_params = TensorFlowProcess.__add_channel_swap_for_cmd_line(common_params, channel_swap)
        mean = self._test.dep_parameters.mean
        if mean:
            common_params = TensorFlowProcess.__add_mean_for_cmd_line(common_params, mean)
        input_scale = self._test.dep_parameters.input_scale
        if input_scale:
            common_params = TensorFlowProcess.__add_input_scale_for_cmd_line(common_params, input_scale)
        input_shape = self._test.dep_parameters.input_shape
        if input_shape:
            common_params = TensorFlowProcess.__add_input_shape_for_cmd_line(common_params, input_shape)
        input_name = self._test.dep_parameters.input_name
        if input_name:
            common_params = TensorFlowProcess.__add_input_name_for_cmd_line(common_params, input_name)
        output_names = self._test.dep_parameters.output_names
        if output_names:
            common_params = TensorFlowProcess.__add_output_names_for_cmd_line(common_params, output_names)
        num_inter_threads = self._test.dep_parameters.num_inter_threads
        if num_inter_threads:
            common_params = TensorFlowProcess.__add_num_inter_threads_for_cmd_line(common_params, num_inter_threads)
        num_intra_threads = self._test.dep_parameters.num_intra_threads
        if num_intra_threads:
            common_params = TensorFlowProcess.__add_num_intra_threads_for_cmd_line(common_params, num_intra_threads)

        common_params = TensorFlowProcess.__add_raw_output_time_for_cmd_line(common_params, '--raw_output true')

        command_line = f'{python} {path_to_tensorflow_scrypt} {common_params}'

        nthreads = self._test.dep_parameters.nthreads
        if nthreads:
            command_line = TensorFlowProcess.__add_nthreads_for_cmd_line(command_line, nthreads)
        kmp_affinity = self._test.dep_parameters.kmp_affinity
        if kmp_affinity:
            command_line = TensorFlowProcess.__add_kmp_affinity_for_cmd_line(command_line, kmp_affinity)

        return command_line
