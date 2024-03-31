import argparse
import sys
import traceback
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.joinpath('tvm_auxiliary')))
from tvm_format import TVMConverterTVMFormat  # noqa: E402

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from utils.logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mod',
                        help='Path to an .json file with a model.',
                        required=True,
                        type=str,
                        dest='model_json')
    parser.add_argument('-p', '--params',
                        help='Path to an .params file with a model parameters.',
                        required=True,
                        type=str,
                        dest='model_params')
    parser.add_argument('-t', '--target',
                        help='Target device information, for example "llvm" for CPU.',
                        required=True,
                        type=str)
    parser.add_argument('--opt_level',
                        help='The optimization level of the task extractions.',
                        type=int,
                        choices=[0, 1, 2, 3, 4],
                        default=2)
    parser.add_argument('-vm', '--virtual_machine',
                        help='Flag to use VirtualMachine API',
                        action='store_true',
                        dest='vm')
    parser.add_argument('--lib_name',
                        help='File name to save.',
                        required=True,
                        type=str)
    parser.add_argument('-op', '--output_dir',
                        help='Path to save the model.',
                        default=None,
                        type=str,
                        dest='output_dir')
    args = parser.parse_args()
    return args


def create_dict_for_compilation(args):
    dictionary = {
        'model_path': args.model_json,
        'model_params': args.model_params,
        'target': args.target,
        'opt_level': args.opt_level,
        'device': 'CPU',
        'vm': args.vm,
        'lib_name': args.lib_name,
        'output_dir': args.output_dir,
    }
    return dictionary


def main():
    args = cli_argument_parser()
    try:
        converter = TVMConverterTVMFormat(create_dict_for_compilation(args))
        converter.export_lib()
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
