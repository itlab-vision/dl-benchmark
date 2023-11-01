from pathlib import Path

from ..processes import ProcessHandler


class IntelCaffeProcess(ProcessHandler):
    benchmark_app_name = 'intel_caffe_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return IntelCaffeProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_intelcaffe_script = Path.joinpath(self.inference_script_root, 'inference_caffe.py')
        python = ProcessHandler.get_cmd_python_version()

        model_prototxt = self._test.model.model
        model_caffemodel = self._test.model.weight
        dataset = self._test.dataset.path if self._test.dataset else None
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        common_params = (f'-m {model_prototxt} -w {model_caffemodel} -b {batch} -d {device}'
                         f' -ni {iteration} --report_path {self.report_path}')

        common_params = IntelCaffeProcess._add_optional_argument_to_cmd_line(common_params, '-i', dataset)

        channel_swap = self._test.dep_parameters.channel_swap
        common_params = IntelCaffeProcess._add_optional_argument_to_cmd_line(common_params, '--channel_swap',
                                                                             channel_swap)
        mean = self._test.dep_parameters.mean
        common_params = IntelCaffeProcess._add_optional_argument_to_cmd_line(common_params, '--mean', mean)
        input_scale = self._test.dep_parameters.input_scale
        common_params = IntelCaffeProcess._add_optional_argument_to_cmd_line(common_params, '--input_scale',
                                                                             input_scale)

        common_params = IntelCaffeProcess._add_argument_to_cmd_line(common_params, '--raw_output', 'true')
        command_line = f'{python} {path_to_intelcaffe_script} {common_params}'

        nthreads = self._test.dep_parameters.nthreads
        if nthreads:
            command_line = IntelCaffeProcess._add_env_to_cmd_line(command_line, 'OMP_NUM_THREADS', nthreads)
        kmp_affinity = self._test.dep_parameters.kmp_affinity
        if kmp_affinity:
            command_line = IntelCaffeProcess._add_env_to_cmd_line(command_line, 'KMP_AFFINITY', kmp_affinity)

        return command_line
