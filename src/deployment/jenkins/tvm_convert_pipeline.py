import argparse
import sys
import subprocess
from logger import configure_logger
import traceback
from pathlib import Path

sys.path.append(str(Path(__file__).parents[3]))


log = configure_logger('tvm_converter_log.txt')


class TXTParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = None

    def parse(self):
        if not self.filepath.exists():
            raise FileNotFoundError('File doesn\'t exist.')
        log.info(f'Parsing file: {self.filepath.as_posix()}')
        with self.filepath.open() as file:
            self.lines = file.read().splitlines()
        for i, line in enumerate(self.lines):
            self.lines[i] = line.split(';')
            self.lines[i][5] = [int(batch) for batch in self.lines[i][5].split(',')]
        return self.lines


class TVMConverterProcess:
    def __init__(self, models_dir, conda):
        self.converter = Path(__file__).parents[2]
        self.conda = conda
        self.converter = self.converter.joinpath('model_converters')
        self.converter = self.converter.joinpath('tvm_converter')
        self.converter = str(self.converter.joinpath('tvm_converter.py'))
        self.models_dir = models_dir.absolute().as_posix()
        self._command_line = f''

    def _add_argument(self, name_of_arg, value_of_arg):
        if value_of_arg != '':
            self._command_line += f' {name_of_arg} {value_of_arg}'

    def _add_option(self, name_of_arg):
        self._command_line += f' {name_of_arg}'      

    def create_command_line(self, model_name, model, weights,
                            framework, input_shape, batch, input_name):
        self._command_line = (f'{self.conda}/envs/tvm_{framework}/bin/python3 ' + f'{self.converter}')
        self._add_argument('-mn', model_name)
        if model != '':
            self._add_argument('-m', f'{self.models_dir}/{model}')
        if weights != '':            
            self._add_argument('-w', f'{self.models_dir}/{weights}')
        if framework == 'torch':
            framework = 'pytorch'
        self._add_argument('-f', framework)
        self._add_argument('-is', f'{batch} {input_shape}')
        self._add_argument('-b', f'{batch}')
        self._add_argument('-op', f'{self.models_dir}/{model_name}/batch_{batch}')
        if input_name != '':
            self._add_argument('-in', f'{input_name}')

    def execute(self):
        log.info(f'Starting process: {self._command_line}\n')
        proc = subprocess.run(self._command_line, shell=True)
        #log.info(f'Subprocess logs: \n\n{proc.stdout.decode()}')
        self.exit_code = proc.returncode
        self._command_line = ''



def cli_arguments_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-md', '--models_dir',
                        help='Path to directory with models.',
                        dest='models_dir',
                        required=True,
                        type=Path)
    parser.add_argument('-mi', '--models_info',
                        help='Txt file with info about models.',
                        dest='models_info',
                        required=True,
                        type=Path)
    parser.add_argument('-cp', '--conda_prefix',
                        help='Path to miniconda3 directory.',
                        dest='conda',
                        required=True,
                        type=str)

    return parser.parse_args()


def main():
    args = cli_arguments_parse()
    parser = TXTParser(args.models_info)
    models = parser.parse()
    proc = TVMConverterProcess(args.models_dir, args.conda)
    for (model_name, model, weights,
         framework, input_shape, batches, input_name) in models:
        for batch in batches:
            proc.create_command_line(
                model_name, model,
                weights, framework,
                input_shape, batch,
                input_name
            )
            proc.execute()




if __name__=='__main__':
    sys.exit(main() or 0)