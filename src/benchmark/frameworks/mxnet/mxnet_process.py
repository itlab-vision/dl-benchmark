from pathlib import Path

from ..processes import ProcessHandler


class MXNetProcess(ProcessHandler):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    @staticmethod
    def create_process(test, executor, log):
        return MXNetProcess(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    def _fill_command_line(self):
        path_to_mxnet_script = Path.joinpath(self.inference_script_root, 'inference_mxnet.py')
        python = ProcessHandler.get_cmd_python_version()

        name = self._test.model.name
        model_json = self._test.model.model
        model_params = self._test.model.weight
        dataset = self._test.dataset.path
        input_shape = self._test.dep_parameters.input_shape
        batch_size = self._test.indep_parameters.batch_size
        iteration = self._test.indep_parameters.iteration
        if ((name is not None)
                and (model_json is None or model_json == '')
                and (model_params is None or model_params == '')):
            common_params = (f'-mn {name} -i {dataset} -is {input_shape} '
                             f'-b {batch_size} -ni {iteration}')
        elif (name is None) and (model_json is not None) and (model_params is not None):
            common_params = (f'-m {model_json} -w {model_params} -i {dataset} '
                             f'-is {input_shape} -b {batch_size} -ni {iteration}')
        else:
            raise Exception('Incorrect model parameters. Set model name or file names.')

        input_name = self._test.dep_parameters.input_name
        common_params = MXNetProcess._add_optional_argument_to_cmd_line(
            common_params, '--input_name', input_name)

        normalize = self._test.dep_parameters.normalize
        common_params = MXNetProcess._add_optional_argument_to_cmd_line(
            common_params, '--norm', normalize)

        mean = self._test.dep_parameters.mean
        common_params = MXNetProcess._add_optional_argument_to_cmd_line(
            common_params, '--mean', mean)

        std = self._test.dep_parameters.std
        common_params = MXNetProcess._add_optional_argument_to_cmd_line(
            common_params, '--std', std)

        channel_swap = self._test.dep_parameters.channel_swap
        common_params = MXNetProcess._add_optional_argument_to_cmd_line(
            common_params, '--channel_swap', channel_swap)

        device = self._test.indep_parameters.device
        common_params = MXNetProcess._add_optional_argument_to_cmd_line(
            common_params, '--device', device)

        common_params = MXNetProcess._add_argument_to_cmd_line(
            common_params, '--raw_output', 'true')

        command_line = f'{python} {path_to_mxnet_script} {common_params}'

        return command_line
