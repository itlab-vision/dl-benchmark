class process:
    def __init__(self, parameters, executor, log):
        self.__my_log = log
        self.__my_executor = executor
        self.__my_parameters = parameters
        self.__my_output = None


    @staticmethod
    def __add_config_for_cmd_line(command_line, config):
        return '{0} -c {1}'.format(command_line, config)


    @staticmethod
    def __add_quantization_method_for_cmd_line(command_line, q_method):
        return '{0} -q {1}'.format(command_line, q_method)


    @staticmethod
    def __add_model_for_cmd_line(command_line, model):
        return '{0} -m {1}'.format(command_line, model)


    @staticmethod
    def __add_weights_for_cmd_line(command_line, weights):
        return '{0} -w {1}'.format(command_line, weights)


    @staticmethod
    def __add_model_name_for_cmd_line(command_line, name):
        return '{0} -n {1}'.format(command_line, name)


    @staticmethod
    def __add_preset_for_cmd_line(command_line, preset):
        return '{0} --preset {1}'.format(command_line, preset)


    @staticmethod
    def __add_ac_config_for_cmd_line(command_line, ac_config):
        return '{0} --ac-config {1}'.format(command_line, ac_config)


    @staticmethod
    def __add_max_drop_for_cmd_line(command_line, max_drop):
        return '{0} --max-drop {1}'.format(command_line, max_drop)


    @staticmethod
    def __add_eval_for_cmd_line(command_line):
        return command_line + ' -e'
        # return '{0} -e'.format(command_line)


    @staticmethod
    def __add_output_dir_for_cmd_line(command_line, output_dir):
        return '{0} --output-dir "{1}"'.format(command_line, output_dir)


    @staticmethod
    def __add_direct_dump_for_cmd_line(command_line):
        return command_line + ' --direct-dump'


    @staticmethod
    def __add_log_level_for_cmd_line(command_line, log_level):
        return '{0} --log-level {1}'.format(command_line, log_level)


    @staticmethod
    def __add_progress_bar_for_cmd_line(command_line):
        return command_line + ' --progress-bar'


    @staticmethod
    def __add_stream_output_for_cmd_line(command_line):
        return command_line + ' --stream-output'


    @staticmethod
    def __add_keep_weights_for_cmd_line(command_line):
        return command_line + ' --keep-uncompressed-weights'


    def _fill_command_line(self):
        # command_line = 'pot'
        cmd_line_base = 'pot'

        # if self.__my_parameters.config:
        #     return self.__add_config_for_cmd_line(cmd_line_base, self.__my_parameters.config)
        config_params = ''
        if self.__my_parameters.config:
            config_params = self.__add_config_for_cmd_line(
                config_params,
                self.__my_parameters.config
            )
        if self.__my_parameters.quantization_method:
            config_params = self.__add_quantization_method_for_cmd_line(
                config_params,
                self.__my_parameters.quantization_method
            )
            if self.__my_parameters.model:
                config_params = self.__add_model_for_cmd_line(
                    config_params,
                    self.__my_parameters.model
                )
            if self.__my_parameters.weights:
                config_params = self.__add_weights_for_cmd_line(
                    config_params,
                    self.__my_parameters.weights
                )
            if self.__my_parameters.model_name:
                config_params = self.__add_model_name_for_cmd_line(
                    config_params,
                    self.__my_parameters.model_name
                )
            if self.__my_parameters.preset:
                config_params = self.__add_preset_for_cmd_line(
                    config_params,
                    self.__my_parameters.preset
                )
            if self.__my_parameters.ac_config:
                config_params = self.__add_ac_config_for_cmd_line(
                    config_params,
                    self.__my_parameters.ac_config
                )
            if self.__my_parameters.max_drop:
                config_params = self.__add_max_drop_for_cmd_line(
                    config_params,
                    self.__my_parameters.max_drop
                )

        common_params = ''
        if self.__my_parameters.evaluation:
            common_params = self.__add_eval_for_cmd_line(common_params)
        if self.__my_parameters.output_dir:
            common_params = self.__add_output_dir_for_cmd_line(
                common_params,
                self.__my_parameters.output_dir
            )
        if self.__my_parameters.direct_dump:
            common_params = self.__add_direct_dump_for_cmd_line(common_params)
        if self.__my_parameters.log_level:
            common_params = self.__add_log_level_for_cmd_line(
                common_params,
                self.__my_parameters.log_level
            )
        if self.__my_parameters.progress_bar:
            common_params = self.__add_progress_bar_for_cmd_line(common_params)
        if self.__my_parameters.stream_output:
            common_params = self.__add_stream_output_for_cmd_line(common_params)
        if self.__my_parameters.keep_uncompressed_weights:
            common_params = self.__add_keep_weights_for_cmd_line(common_params)

        command_line = '{0} {1} {2}'.format(cmd_line_base, config_params, common_params)
        return command_line


    def execute(self):
        command_line = self._fill_command_line()
        if command_line == '':
            self.__my_log.error('Command line is empty')
        self.__my_log.info('Start quantization with config: {}'.format(self.__my_parameters.config))
        self.__my_output = self.__my_executor.execute_process(command_line)
        if type(self.__my_output) is not list:
            self.__my_log.info(self.__my_output)
        # else:
        #     for out in self.__my_output:
        #         self.__my_log.info(out)

        # if type(self.__my_output) is not list:
        #     self.__my_output = self.__my_output.decode("utf-8").split('\n')[:-1]
