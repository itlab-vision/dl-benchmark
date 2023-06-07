from pathlib import Path

from ..processes import ProcessHandler


class OpenCVDNNPythonProcess(ProcessHandler):
    benchmark_app_name = 'opencv_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return OpenCVDNNPythonProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_opencv_script = Path.joinpath(self.inference_script_root, 'inference_opencv.py')
        python = ProcessHandler.get_cmd_python_version()

        model = self._test.model.model
        weights = self._test.model.weight
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration
        time_limit = self._test.indep_parameters.test_time_limit

        common_params = (f'-m {model} -w {weights} -i {dataset} -b {batch} -d {device} -ni {iteration}')

        time_limit = self._test.indep_parameters.test_time_limit
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--time', time_limit)

        common_params = self._add_optional_argument_to_cmd_line(common_params, '--report_path', self.report_path)

        precision = self._test.model.precision
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--precision', precision)

        backend = self._test.dep_parameters.backend
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--backend', backend)

        input_scale = self._test.dep_parameters.input_scale
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_scale', input_scale)

        input_shape = self._test.dep_parameters.input_shape
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_shape', input_shape)

        input_name = self._test.dep_parameters.input_name
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--input_name', input_name)

        output_names = self._test.dep_parameters.output_names
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--output_names', output_names)

        mean = self._test.dep_parameters.mean
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--mean', mean)

        std = self._test.dep_parameters.std
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--std', std)

        swapRB = self._test.dep_parameters.swapRB
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--swapRB', swapRB)

        crop = self._test.dep_parameters.crop
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--crop', crop)

        layout = self._test.dep_parameters.layout
        common_params = self._add_optional_argument_to_cmd_line(common_params, '--layout', layout)

        common_params = self._add_argument_to_cmd_line(common_params, '--raw_output', 'true')
        command_line = f'{python} {path_to_opencv_script} {common_params}'

        return command_line
