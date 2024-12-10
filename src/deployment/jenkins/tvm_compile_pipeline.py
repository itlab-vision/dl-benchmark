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


class TVMCompilerProcess:
    def __init__(self, models_dir, conda, output_dir):
        self.converter = Path(__file__).parents[2]
        self.converter = self.converter.joinpath('model_converters')
        self.converter = self.converter.joinpath('tvm_converter')
        self.converter = str(self.converter.joinpath('tvm_compiler.py'))
        self.conda = conda
        self.models_dir = models_dir.absolute().as_posix()
        if output_dir is not None:
            self.output_dir = output_dir
        else:
            self.output_dir = models_dir
        self._command_line = f''

    def _add_argument(self, name_of_arg, value_of_arg):
        if value_of_arg != '':
            self._command_line += f' {name_of_arg} {value_of_arg}'

    def _add_option(self, name_of_arg):
        self._command_line += f' {name_of_arg}'      

    def create_command_line(self, model_name, target, batch, opt_level):
        self._command_line = (f'{self.conda}/envs/tvm_main/bin/python3 ' + f'{self.converter}')
        self._add_argument('-m', f'{self.models_dir}/{model_name}/batch_{batch}/{model_name}.json')            
        self._add_argument('-p', f'{self.models_dir}/{model_name}/batch_{batch}/{model_name}.params')
        self._add_argument('-t', f'{target}')
        self._add_argument('--opt_level', f'{opt_level}')
        self._add_argument('--lib_name', f'{model_name}.so')
        self._add_argument('-op', f'{self.output_dir}/{model_name}/batch_{batch}/opt_level{opt_level}')

    def execute(self):
        log.info(f'Starting process: {self._command_line}\n')
        proc = subprocess.run(self._command_line, shell=True)
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
    parser.add_argument('-op', '--output_dir',
                        help='Path to save the model.',
                        default=None,
                        type=str,
                        dest='output_dir')
    parser.add_argument('--opt_level',
                        help='The optimization level of the task extractions.',
                        type=list,
                        default=[0, 1, 2, 3],
                        dest='opt_levels')
    parser.add_argument('--target',
                        help='Parameter for hardware-dependent optimizations.',
                        default='llvm',
                        type=str,
                        dest='target')
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
    proc = TVMCompilerProcess(args.models_dir, args.conda)
    for (model_name, _, _,
         _, _, batches, _) in models:
        for batch in batches:
            for level in args.opt_levels:
                proc.create_command_line(
                    model_name, args.target,
                    batch, level
                )
                proc.execute()




if __name__=='__main__':
    sys.exit(main() or 0)