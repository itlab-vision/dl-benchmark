from pathlib import Path

from ..processes import ProcessHandler


class NcnnProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return NcnnProcess(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    def _fill_command_line(self):
        path_to_ncnn_script = Path.joinpath(self.inference_script_root, 'inference_ncnn.py')
        python = ProcessHandler.get_cmd_python_version()

        name = self._test.model.name
        dataset = self._test.dataset.path
        input_shape = self._test.dep_parameters.input_shape
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration
        common_params = (f'-m {name} -i {dataset} -is {input_shape} -b {batch_size} -ni {iteration}')

        input_name = self._test.dep_parameters.input_name
        if input_name:
            common_params = NcnnProcess._add_optional_argument_to_cmd_line(
                common_params, '--input_name', input_name)

        thread_count = self._test.dep_parameters.thread_count
        if thread_count:
            common_params = NcnnProcess._add_flag_to_cmd_line(
                common_params, '--num_threads')

        device = self._test.indep_parameters.device
        if device:
            common_params = NcnnProcess._add_optional_argument_to_cmd_line(
                common_params, '--device', device)

        common_params = NcnnProcess._add_argument_to_cmd_line(
            common_params, '--raw_output', 'true')

        command_line = f'{python} {path_to_ncnn_script} {common_params}'

        return command_line
