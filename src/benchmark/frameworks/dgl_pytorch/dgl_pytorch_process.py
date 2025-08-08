from pathlib import Path

from ..processes import ProcessHandler


class DGLPyTorchProcess(ProcessHandler):
    benchmark_app_name = 'dgl_pytorch_python_benchmark'
    launcher_latency_units = 'seconds'

    def __init__(self, test, executor, log):
        log.info('Initialize pytorch process')
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return DGLPyTorchProcess(test, executor, log)

    def get_performance_metrics(self):
        return self.get_performance_metrics_from_json_report()

    def _fill_command_line(self):
        path_to_pytorch_script = Path.joinpath(self.inference_script_root, 'inference_dgl_pytorch.py')
        python = ProcessHandler.get_cmd_python_version(self._test)

        name = self._test.model.name
        model = self._test.model.model
        module = self._test.model.module
        dataset = self._test.dataset.path if self._test.dataset else None
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration
        time_limit = self._test.indep_parameters.test_time_limit
        common_params = (f'-mn {name} -b {batch_size} -ni {iteration} --report_path {self.report_path}')

        common_params = DGLPyTorchProcess._add_optional_argument_to_cmd_line(common_params, '-i', dataset)

        task = self._test.model.task
        if task:
            common_params = DGLPyTorchProcess._add_optional_argument_to_cmd_line(
                common_params, '--task', task)

        common_params = DGLPyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--module', module)
        common_params = DGLPyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--model', model)

        common_params = DGLPyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--time', time_limit)

        device = self._test.indep_parameters.device
        common_params = DGLPyTorchProcess._add_optional_argument_to_cmd_line(common_params, '--device', device)

        common_params = DGLPyTorchProcess._add_argument_to_cmd_line(common_params, '--raw_output', 'true')

        num_inter_threads = self._test.dep_parameters.num_inter_threads
        if num_inter_threads:
            common_params = DGLPyTorchProcess._add_argument_to_cmd_line(
                common_params, '--num_inter_threads', num_inter_threads)

        num_intra_threads = self._test.dep_parameters.num_intra_threads
        if num_intra_threads:
            common_params = DGLPyTorchProcess._add_argument_to_cmd_line(
                common_params, '--num_intra_threads', num_intra_threads)

        command_line = f'{python} {path_to_pytorch_script} {common_params}'

        return command_line
