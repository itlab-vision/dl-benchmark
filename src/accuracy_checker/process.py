from result import result


class process:
    def __init__(self, log, executor, parameters):
        self.__log = log
        self.__executor = executor
        self.__parameters = parameters
        self.__output = None

    def __fill_command_line(self):
        command_line = 'accuracy_check -c {0} -m {1} -s {2}'.format(self.__parameters.config, self.__parameters.models,
                                                                    self.__parameters.source)
        if self.__parameters.annotations:
            self.__add_annotations_for_cmd_line(command_line, self.__parameters.annotations)
        if self.__parameters.definitions:
            self.__add_definitions_for_cmd_line(command_line, self.__parameters.definitions)
        if self.__parameters.extensions:
            self.__add_extensions_for_cmd_line(command_line, self.__parameters.extensions)
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

    def execute(self):
        command_line = self.__fill_command_line()
        if command_line == '':
            self.__log.error('Command line is empty')
        self.__log.info('Start accuracy check for config: {}'.format(self.__parameters.config))
        self.__output = self.__executor.execute_process(command_line)
        if type(self.__output) is not list:
            self.__output = self.__output.decode("utf-8").split('\n')

    def get_result_parameters(self):
        return result.parser_test_results(self.__output)
