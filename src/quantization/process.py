import os
import abc
import shutil
from pathlib import Path


class ProcessHandler(metaclass=abc.ABCMeta):
    def __init__(self, parameters, executor, log):
        self.__log = log
        self._executor = executor
        self._parameters = parameters
        self._output = None
        self._status = None

    def get_status(self):
        return self._status

    @staticmethod
    def _add_argument_to_cmd_line(command_line, argument, value):
        return f'{command_line} {argument} {value}' if value is not None else command_line

    @staticmethod
    def _add_flag_to_cmd_line(command_line, flag, cond):
        return f'{command_line} {flag}' if cond else command_line

    def __fill_command_line(self):
        cmd_line_base = 'pot'

        config_params = ''
        config_params = self._add_argument_to_cmd_line(config_params, '-c', self._parameters.config)
        if self._parameters.quantization_method:
            config_params = self._add_argument_to_cmd_line(config_params, '-q', self._parameters.quantization_method)
            config_params = self._add_argument_to_cmd_line(config_params, '-m', self._parameters.model)
            config_params = self._add_argument_to_cmd_line(config_params, '-w', self._parameters.weights)
            config_params = self._add_argument_to_cmd_line(config_params, '-n', self._parameters.model_name)
            config_params = self._add_argument_to_cmd_line(config_params, '--preset', self._parameters.preset)
            config_params = self._add_argument_to_cmd_line(config_params, '--ac-config', self._parameters.ac_config)
            config_params = self._add_argument_to_cmd_line(config_params, '--max-drop', self._parameters.max_drop)

        common_params = ''
        common_params = self._add_flag_to_cmd_line(common_params, '-e', self._parameters.evaluation is not None)
        if self._parameters.output_dir:
            if not Path(self._parameters.output_dir).is_dir():
                Path(self._parameters.output_dir).mkdir()
        common_params = self._add_argument_to_cmd_line(common_params, '--output-dir', self._parameters.output_dir)
        common_params = self._add_flag_to_cmd_line(common_params, '--direct-dump',
                                                   self._parameters.direct_dump is not None)
        common_params = self._add_argument_to_cmd_line(common_params, '--log-level', self._parameters.log_level)
        common_params = self._add_flag_to_cmd_line(common_params, '--progress-bar',
                                                   self._parameters.progress_bar is not None)
        common_params = self._add_flag_to_cmd_line(common_params, '--stream-output',
                                                   self._parameters.stream_output is not None)
        common_params = self._add_flag_to_cmd_line(common_params, '--keep-uncompressed-weights',
                                                   self._parameters.keep_uncompressed_weights is not None)

        return f'{cmd_line_base}{config_params}{common_params}'

    def __fix_output_dir(self):
        dir_dst = self._parameters.output_dir
        if not Path(dir_dst).is_dir():
            Path(dir_dst).mkdir()
        dir_src = dir_dst
        if not self._parameters.direct_dump:
            curr_dir = os.listdir(dir_src)[0]                        # example: AlexNet_DefaultQuantization
            versions = os.listdir(dir_src + '/' + curr_dir)
            curr_version = sorted(versions, reverse=True)[0]   # example: 2022-05-01_14-48-47
            dir_src = dir_src + '/' + curr_dir + '/' + curr_version
        dir_src = dir_src + '/optimized/'
        files_list = os.listdir(dir_src)
        for f in files_list:
            shutil.move(dir_src + f, dir_dst)

    def execute(self, idx):
        command_line = self.__fill_command_line()
        if command_line == '':
            self.__log.error('Command line is empty')
        self.__log.info(f'Start quantization model #{idx+1}!')
        self.__log.info(f'Command line is : {command_line}')
        self._status, self._output = self._executor.execute_process(command_line)
        if type(self._output) is not list:
            self._output = self._output.decode('utf-8').split('\n')
        self.__fix_output_dir()
