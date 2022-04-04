import os
from subprocess import Popen, PIPE, STDOUT
from shape_parser import get_new_input_shape_by_model_name


class process:
    def __init__(self, model, batch, parameters, log):
        self.__model = model
        self.__batch = batch
        self.__my_log = log
        self.__my_parameters = parameters
        self.__my_output = None

    @staticmethod
    def __add_output_dir_for_cmd_line(command_line, output_dir, batch):
        if batch == 1:
            new_path_with_batch = output_dir
        else:
            new_path_with_batch = os.path.join(output_dir, str(batch))
        return '{0} --output_dir "{1}"'.format(command_line, new_path_with_batch)

    @staticmethod
    def __add_shape_for_cmd_line(command_line, zoo_dir, model_name, batch):
        shape_line = get_new_input_shape_by_model_name(zoo_dir, model_name, batch)
        return '{0}{1}'.format(command_line, shape_line)

    def _fill_command_line(self):
        cmd_line_base = 'omz_converter --name {0}'.format(self.__model)

        add_mo_params = ''
        add_mo_params = self.__add_shape_for_cmd_line(
            add_mo_params,
            self.__my_parameters.zoo_config_dir,
            self.__model,
            self.__batch
        )

        common_params = ''
        if self.__my_parameters.dir:
            common_params = self.__add_output_dir_for_cmd_line(
                common_params,
                self.__my_parameters.dir,
                self.__batch
            )

        add_mo_params = f'--add_mo_arg="{add_mo_params}"'
        command_line = '{0} {1} {2}'.format(cmd_line_base, add_mo_params, common_params)
        return command_line

    def execute(self):
        command_line = self._fill_command_line()
        if command_line == '':
            self.__my_log.error('Command line is empty')
        self.__my_log.info(f'Start converting with command line: {command_line}')

        process = Popen(
            command_line,
            env=os.environ.copy(),
            shell=True,
            stdout=PIPE,
            stderr=STDOUT,
            universal_newlines=True
        )
        out, _ = process.communicate()
        self.__my_log.info(f'{out}')
        # if type(out) is not list:
        #     self.__my_log.info(self.__my_output)
