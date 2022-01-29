from result import result


class process:
    def __init__(self, log, executor, test):
        self.__log = log
        self.__executor = executor
        self.__test = test
        self.__output = None
        self.__supported_frameworks = {'OpenVINO DLDT': 'dlsdk', 'Caffe': 'caffe', 'TensorFlow': 'tf'}

    def __fill_command_line(self):
        command_line = 'accuracy_check -c {0} -m {1} -s {2} -td {3}'.format(self.__test.config,
                                                                            self.__test.model.directory,
                                                                            self.__test.parameters.source,
                                                                            self.__test.device
                                                                            )
        command_line = self.__add_framework_for_cmd_line(command_line, self.__supported_frameworks[self.__test.framework])
        if self.__test.parameters.annotations:
            command_line = self.__add_annotations_for_cmd_line(command_line, self.__test.parameters.annotations)
        if self.__test.parameters.definitions:
            command_line = self.__add_definitions_for_cmd_line(command_line, self.__test.parameters.definitions)
        if self.__test.parameters.extensions:
            command_line = self.__add_extensions_for_cmd_line(command_line, self.__test.parameters.extensions)
        return command_line

    @staticmethod
    def __add_annotations_for_cmd_line(command_line, annotations):
        return '{0} -a {1}'.format(command_line, annotations)

    @staticmethod
    def __add_definitions_for_cmd_line(command_line, definitions):
        return '{0} -d {1}'.format(command_line, definitions)

    @staticmethod
    def __add_extensions_for_cmd_line(command_line, extensions):
        return '{0} -e {1}'.format(command_line, extensions)

    @staticmethod
    def __add_framework_for_cmd_line(command_line, framework):
        return '{0} -tf {1}'.format(command_line, framework)

    def execute(self, idx):
        command_line = self.__fill_command_line()
        if command_line == '':
            self.__log.error('Command line is empty')
        self.__log.info('Start accuracy check for {0} test: {1}'.format(idx, self.__test.model.name))
        self.__executor.set_target_framework(self.__test.framework)
        command_line = self.__executor.prepare_command_line(self.__test, command_line)
        self.__output = self.__executor.execute_process(command_line)
        if type(self.__output) is not list:
            self.__output = self.__output.decode("utf-8").split('\n')
        print(self.__output)

    def get_result_parameters(self):
        return result.parser_test_results(self.__output)
