from pathlib import Path

from .openvino_process import OpenVINOProcess
from ..processes import ProcessHandler


class OpenVINOPythonAPIProcess(OpenVINOProcess):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    def _fill_command_line(self):
        model_xml = self._test.model.model
        model_bin = self._test.model.weight
        dataset = self._test.dataset.path
        batch = self._test.indep_parameters.batch_size
        device = self._test.indep_parameters.device
        iteration = self._test.indep_parameters.iteration

        command_line = f'-m {model_xml} -w {model_bin} -i {dataset} -b {batch} -d {device} -ni {iteration}'

        extension = self._test.dep_parameters.extension
        if extension:
            command_line = OpenVINOPythonAPIProcess._add_argument_to_cmd_line(command_line, '-l', extension)
        nthreads = self._test.dep_parameters.nthreads
        if nthreads:
            command_line = OpenVINOPythonAPIProcess._add_argument_to_cmd_line(command_line, '-nthreads', nthreads)
        command_line = OpenVINOPythonAPIProcess._add_argument_to_cmd_line(command_line, '--raw_output', 'true')

        return command_line


class AsyncOpenVINOProcess(OpenVINOPythonAPIProcess):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])

        return average_time, fps, 0

    def _fill_command_line(self):
        path_to_async_script = Path.joinpath(self.inference_script_root, 'inference_async_mode.py')
        python = ProcessHandler.get_cmd_python_version()

        common_params = super()._fill_command_line()
        command_line = f'{python} {path_to_async_script} {common_params}'
        nstreams = self._test.dep_parameters.nstreams
        if nstreams:
            command_line = AsyncOpenVINOProcess._add_argument_to_cmd_line(command_line, '-nstreams', nstreams)
        requests = self._test.dep_parameters.async_request
        if requests:
            command_line = AsyncOpenVINOProcess._add_argument_to_cmd_line(command_line, '--requests', requests)

        return command_line


class SyncOpenVINOProcess(OpenVINOPythonAPIProcess):
    def __init__(self, test, executor, log):
        super().__init__(test, executor, log)

    def get_performance_metrics(self):
        if self._status != 0 or len(self._output) == 0:
            return None, None, None

        result = self._output[-1].strip().split(',')
        average_time = float(result[0])
        fps = float(result[1])
        latency = float(result[2])

        return average_time, fps, latency

    def _fill_command_line(self):
        path_to_sync_script = Path.joinpath(self.inference_script_root, 'inference_sync_mode.py')
        python = ProcessHandler.get_cmd_python_version()

        common_params = super()._fill_command_line()
        command_line = f'{python} {path_to_sync_script} {common_params}'

        return command_line
