import argparse
import numpy as np
import subprocess
import sys
import traceback
import json
from pathlib import Path

from io_adapter import IOAdapter
from io_model_wrapper import RknnIOModelWrapperCpp
from transformer import Transformer

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))  # noqa: E402
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()

# list of io-adapters that require original images
ADAPTERS_WITH_ORIG_IMAGES = [
    'blaze_face_rknn',
]


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-bch', '--benchmark_app',
                        help='Path to RKNN_benchmark',
                        required=True,
                        type=str,
                        dest='benchmark_path')
    parser.add_argument('-m', '--model',
                        help='Path to RKNN model with format .rknn.',
                        type=str,
                        dest='model_path')
    parser.add_argument('-w', '--weights',
                        help='Path to a model weights file',
                        type=str,
                        required=False,
                        default=None,
                        dest='weights')
    parser.add_argument('-i', '--input',
                        help='Path to data.',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('--input_shape',
                        help='Shape for network input <[N,C,H,W]>',
                        required=False,
                        default='',
                        type=str,
                        dest='shape')
    parser.add_argument('--dtype',
                        help='data type of network input. ex.: "input1[U8],input2[U8]" or just "[U8]"',
                        required=False,
                        default='[U8]',
                        type=str,
                        dest='data_type')
    parser.add_argument('--layout',
                        help='Parameter input layout in format [value]',
                        default=None,
                        type=str,
                        dest='layout')
    parser.add_argument('--mean',
                        help='Mean values in <[R,G,B]>',
                        required=False,
                        default='',
                        type=str,
                        dest='mean')
    parser.add_argument('--scale',
                        help='Scale values in <[R,G,B]>',
                        required=False,
                        default='',
                        type=str,
                        dest='input_scale')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['face_recognition_tflite_cpp'] + ADAPTERS_WITH_ORIG_IMAGES,
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('--swap_channels',
                        help='Parameter channel swap',
                        required=False,
                        default=False,
                        type=bool,
                        dest='swap_channels')
    parser.add_argument('--background',
                        help='Path to background image',
                        type=str,
                        dest='background')
    parser.add_argument('--output_path',
                        help='Path to save processed output',
                        type=Path,
                        dest='output_path')
    parser.add_argument('--only_process_output',
                        help='Run without model execution',
                        required=False,
                        default=False,
                        type=bool,
                        dest='only_process_output')
    parser.add_argument('--output_json_path',
                        help='Path to save raw output of cpp_dl_benchmark',
                        default=Path(__file__).parent / '_validation' / 'json_output' / 'output.json',
                        type=Path,
                        dest='output_json_path')
    parser.add_argument('--ref_input',
                        help='Path to reference data',
                        type=str,
                        dest='ref_input')
    parser.add_argument('--use_bin_input',
                        help='Use binary input',
                        required=False,
                        default=False,
                        type=bool,
                        dest='use_bin_input')
    args = parser.parse_args()

    return args


class RknnProcess():
    def __init__(self):
        self._command_line = ''

    def _add_argument(self, name_of_arg, value_of_arg):
        self._command_line += f' {name_of_arg} {value_of_arg}'

    def _add_option(self, name_of_arg):
        self._command_line += f' {name_of_arg}'

    def create_command_line(self, dict_of_args):
        for name, arg in dict_of_args.items():
            if name == '-bch':
                self._add_option(arg)
            elif arg != '' and arg is not None:
                self._add_argument(name, arg)
        self._add_argument('--nthreads', 1)
        self._add_option('--dump_output')

    def execute(self):
        print(f'Command line: {self._command_line}')
        proc = subprocess.run(self._command_line, shell=True)
        if proc.returncode != 0:
            log.error(traceback.format_exc())
            sys.exit(1)

    def process_benchmark_output(self, output_filename):
        result = {}
        with open(output_filename, 'r') as file:
            for output in json.load(file)[0]:
                layer_name = output['output_name']
                shape = output['shape']
                data = output['data']
                result[layer_name] = np.reshape(data, shape)
        return result

    def prepare_orig_images(self, io, args):
        if args.task in ADAPTERS_WITH_ORIG_IMAGES:
            io.set_image(args.input)


def create_dict_from_args_for_process(args, io):
    args_dict = {'-bch': args.benchmark_path,
                 '-m': args.model_path,
                 '-d': 'NPU',
                 '-b': args.batch_size,
                 '--shape': args.shape,
                 '--layout': args.layout,
                 '--channel_swap': '' if not args.swap_channels else True,
                 '--output_path': args.output_json_path,
                 '-dtype': args.data_type}
    if not args.use_bin_input:
        args_dict['-i'] = args.input[0]
    else:
        log.info('Converting input to .bin')
        bin_input = io.convert_input_to_bin_file(args, normalize=False, data_type=np.uint8)
        args_dict['--layout'] = args.layout
        args_dict['-i'] = bin_input
    return args_dict


def get_output_json_path(args):
    if args.output_json_path is None:
        return Path(__file__).parent / '_validation' / 'json_output' / 'output.json'
    return Path(args.output_json_path)


def main():
    args = cli_argument_parser()
    try:
        model_wrapper = RknnIOModelWrapperCpp(args)

        args.output_json_path = get_output_json_path(args)
        data_transformer = Transformer()
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        log.info('Initializing rknn process')
        process = RknnProcess()
        process.create_command_line(create_dict_from_args_for_process(args, io))

        if not args.only_process_output:
            log.info('RKNN benchmark process:\n')
            process.execute()

        log.info('Process benchmark output:\n')
        result = process.process_benchmark_output(args.output_json_path)

        log.info('Process output using io_adapter:\n')
        process.prepare_orig_images(io, args)
        io.process_output(result, log)

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
