from pathlib import Path

from ..processes import ProcessHandler


class OpenCVProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return OpenCVProcess(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    def _fill_command_line(self):
        path_to_opencv_script = Path.joinpath(self.inference_script_root, 'inference_opencv.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        weights = self._test.model.weight
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration
        common_params = f'-m {model} -w {weights} -i {dataset} -b {batch} -d {device} -ni {iteration}'

        backend = self._test.dep_parameters.backend
        common_params = OpenCVProcess._add_optional_argument_to_cmd_line(common_params, '--backend', backend)

        scalefactor = self._test.dep_parameters.scalefactor
        common_params = OpenCVProcess._add_optional_argument_to_cmd_line(common_params, '--scalefactor',
                                                                         scalefactor)

        size = self._test.dep_parameters.size
        common_params = OpenCVProcess._add_optional_argument_to_cmd_line(common_params, '--size', size)
        
        mean = self._test.dep_parameters.mean
        common_params = OpenCVProcess._add_optional_argument_to_cmd_line(common_params, '--mean', mean)

        swapRB = self._test.dep_parameters.swapRB
        common_params = OpenCVProcess._add_optional_argument_to_cmd_line(common_params, '--swapRB', swapRB)

        common_params = OpenCVProcess._add_argument_to_cmd_line(common_params, '--raw_output', 'true')
        command_line = f'{python} {path_to_opencv_script} {common_params}'

        return command_line
