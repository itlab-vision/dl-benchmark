import abc
import platform
from pathlib import Path


class ProcessHandler(metaclass=abc.ABCMeta):
    def __init__(self, test, executor, log):
        self.__log = log
        self._test = test
        self._executor = executor
        self._output = None
        self._status = None
        self.inference_script_root = Path(self._executor.get_path_to_inference_folder())

    @staticmethod
    def get_cmd_python_version():
        cmd_python_version = ''
        os_type = platform.system()
        if os_type == 'Linux':
            cmd_python_version = 'python3'
        else:
            cmd_python_version = 'python'

        return cmd_python_version

    def get_model_shape(self):
        input_shape = []
        for line in self._output:
            if 'Shape for input layer' in line:
                input_shape.append(line.split(':')[-1].strip())

        return ', '.join(input_shape) if len(input_shape) > 0 else 'Undefined'

    def execute(self):
        command_line = self._fill_command_line()
        if command_line == '':
            self.__log.error('Command line is empty')
        self.__log.info(f'Start inference test on model : {self._test.model.name}')
        self.__log.info(f'Command line is : {command_line}')
        self._executor.set_target_framework(self._test.indep_parameters.inference_framework)
        self._status, self._output = self._executor.execute_process(command_line,
                                                                    self._test.indep_parameters.test_time_limit)

        if type(self._output) is not list:
            self._output = self._output.decode('utf-8').split('\n')[:-1]

        if self._status == 0:
            self.__log.info(f'End inference test on model : {self._test.model.name}')
        else:
            self.__log.warning(f'Inference test on model: {self._test.model.name} was ended with error. '
                               'Process logs:')
            self.__print_error()
            self.__save_failed_test_log()

    def get_status(self):
        return self._status

    @abc.abstractmethod
    def get_performance_metrics(self):
        pass

    @abc.abstractmethod
    def _fill_command_line(self):
        pass

    @staticmethod
    def _add_argument_to_cmd_line(command_line, argument, value):
        return f'{command_line} {argument} {value}'

    @staticmethod
    def _add_env_to_cmd_line(command_line, name, value):
        return f'{name}={value} {command_line}'

    def __print_error(self):
        out = self._output
        is_error = False
        for line in out:
            if line.rfind('ERROR! :') != -1:
                is_error = True
                self.__log.error(f'    {line[8:]}')
                continue
            if is_error:
                self.__log.error(f'    {line}')

    def __save_failed_test_log(self):
        log_filename = self.__make_log_filename()
        out = self._output
        with open(log_filename, 'w', encoding='utf-8') as file:
            for line in out:
                file.write(line)

    def __make_log_filename(self):
        test_settings = [self._test.model.name,
                         self._test.indep_parameters.inference_framework.replace(' ', '_'),
                         self._test.indep_parameters.device,
                         self._test.model.precision,
                         str(self._test.indep_parameters.batch_size),
                         ]
        if hasattr(self._test.dep_parameters, 'mode'):
            test_settings.append(self._test.dep_parameters.mode)
        filename = '_'.join(test_settings)
        filename += '.log'
        return filename
