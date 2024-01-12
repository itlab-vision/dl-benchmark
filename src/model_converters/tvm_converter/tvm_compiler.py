import argparse
import sys
import traceback
from pathlib import Path
from tvm_converter import TVMConverter

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
    parser.add_argument('--lib_name',
                        help='File name to save.',
                        required=True,
                        type=str)
    args = parser.parse_args()
    return args


def create_dict_for_compilation(args):
    dictionary = {
        'model_path': args.model_json,
        'model_params': args.model_params,
        'target': args.target,
        'opt_level': args.opt_level,
        'device': 'CPU',
    }
    return dictionary


def main():
    args = cli_argument_parser()
    try:
        converter = TVMConverter(create_dict_for_compilation(args))
        lib = converter.get_lib()
        lib.export_library(args.lib_name)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
