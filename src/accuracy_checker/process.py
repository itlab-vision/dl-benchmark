import abc
from result import Result


class ProcessHandler(metaclass=abc.ABCMeta):
    def __init__(self, log, executor, test):
        self.__log = log
        self._executor = executor
        self._test = test
        self._output = None
        self._status = None
        self.supported_frameworks = {'OpenVINO DLDT': 'dlsdk', 'Caffe': 'caffe', 'TensorFlow': 'tf2',
                                     'TensorFlowLite': 'tf_lite', 'TensorFlowLite Cpp': 'tf_lite',
                                     'ONNX Runtime Python': 'onnx_runtime', 'ONNX Runtime': 'onnx_runtime',
                                     'OpenCV DNN Python': 'opencv', 'OpenCV DNN Cpp': 'opencv',
                                     'PyTorch': 'pytorch', 'PyTorch Cpp': 'pytorch',
                                     'MXNet': 'mxnet', 'TVM': 'tvm'}
        self.csv_name = executor.get_csv_file()

    @staticmethod
    def _add_argument_to_cmd_line(command_line, argument, value):
        return f'{command_line} {argument} {value}'

    def execute(self, idx):
        command_line = self.__fill_command_line()
        if command_line == '':
            self.__log.error('Command line is empty')
        self.__log.info(f'Start accuracy check for {idx+1} test: {self._test.model.name}')
        self.__log.info(f'Command line is : {command_line}')
        self._executor.set_target_framework(self._test.framework)
        command_line = self._executor.prepare_command_line(self._test, command_line)
        self._status, self._output = self._executor.execute_process(command_line)
        if type(self._output) is not list:
            self._output = self._output.decode('utf-8').split('\n')

    def get_status(self):
        return self._status

    def get_result_parameters(self):
        result_file = self._executor.get_path_to_result_file()
        return Result.parser_test_result(self.get_status() == 0, self._test, result_file)

    def __fill_command_line(self):
        command_line = 'accuracy_check -c {0} -m {1} -s {2} -td {3} --csv_result {4}'.format(
            self._test.config, self._test.model.directory,
            self._test.parameters.source,
            self._test.device,
            self.csv_name)
        test_framework = self.supported_frameworks[self._test.framework]
        command_line = self._add_argument_to_cmd_line(command_line, '-tf', test_framework)
        if self._test.parameters.annotations:
            command_line = self._add_argument_to_cmd_line(command_line, '-a', self._test.parameters.annotations)
        if self._test.parameters.definitions:
            command_line = self._add_argument_to_cmd_line(command_line, '-d', self._test.parameters.definitions)
        if self._test.parameters.extensions:
            command_line = self._add_argument_to_cmd_line(command_line, '-e', self._test.parameters.extensions)

        return command_line
