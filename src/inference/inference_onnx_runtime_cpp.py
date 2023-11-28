import argparse
import ast
import json
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort

from io_adapter import IOAdapter
from io_model_wrapper import ONNXIOModelWrapper
from transformer import ONNXRuntimeTransformerCpp

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model',
                        help='Path to an .onnx file with a trained model.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-bch', '--benchmark_app',
                        help='Path to onnxruntime_benchmark',
                        required=True,
                        type=str,
                        dest='benchmark_path')
    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=False,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-w', '--weights',
                        help='Path to a model weights file',
                        required=False,
                        type=str,
                        default='',
                        dest='weights')
    parser.add_argument('--input_shape',
                        help='Shape for network input <[N,C,H,W]>',
                        required=False,
                        default='',
                        type=str,
                        dest='shape')
    parser.add_argument('-l', '--labels',
                        help='Path to labels.txt file',
                        required=True,
                        default='',
                        type=str,
                        dest='labels')
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
                        dest='scale')
    parser.add_argument('-t', '--task',
                        help='Task type determines the type of output processing method',
                        required=False,
                        default='',
                        type=str,
                        dest='task')
    parser.add_argument('-batch',
                        help='Batch size',
                        required=False,
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-niter',
                        help='Number of iterations',
                        required=False,
                        default=1,
                        type=int,
                        dest='niter')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results.',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('--swap_channels',
                        help='Parameter channel swap',
                        required=False,
                        default=False,
                        type=bool,
                        dest='swap_channels')
    parser.add_argument('--output_json_path',
                        help='Path to save raw output of cpp_dl_benchmark',
                        default=Path(__file__).parent / '_validation' / 'json_output' / 'output.json',
                        type=Path,
                        dest='output_json_path')
    args = parser.parse_args()

    return args


class OnnxRuntimeProcess():
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
            elif name == '-l':
                if arg != '':
                    self._add_option('--dump_output')
            elif arg != '':
                self._add_argument(name, arg)

    def execute(self):
        proc = subprocess.run(self._command_line, shell=True)
        if proc.returncode != 0:
            log.error(traceback.format_exc())
            sys.exit(1)

    def process_benchmark_output(self, output_filename):
        result = {'images': []}
        with open(output_filename, 'r') as file:
            for outputs in json.load(file):
                for layer in outputs:
                    shape = layer['shape']
                    data = layer['data']
                    result['images'].append(np.reshape(data, shape))
        return result


def std_transformer(std):
    std = ast.literal_eval(std)
    tmp = np.asarray(std)[::-1] * 255
    return f'[{round(tmp[0], 3)},{round(tmp[1], 3)},{round(tmp[2], 3)}]'


def create_dict_from_args_for_process(args, nireq):
    return {'-bch': args.benchmark_path,
            '-m': args.model_path,
            '-i': args.input,
            '-w': args.weights,
            '--shape': args.shape,
            '--scale': args.scale,
            '--mean': args.mean,
            '-l': args.labels,
            '--channel_swap': '' if not args.swap_channels else True,
            '--output_path': args.output_json_path,
            '-nireq': nireq,
            '-niter': args.niter}


def prepare_images_for_benchmark(io, tmp_dir, names_of_output, cur_path):
    os.chdir(tmp_dir)
    for i, name in enumerate(names_of_output):
        for val in io.get_slice_input(i).values():
            cv2.imwrite(name, val[0])
    os.chdir(cur_path)


def prepare_output_file_names(input_):
    list_of_names = []
    if os.path.isdir(input_[0]):
        for entry in os.scandir(input_[0]):
            if entry.is_file():
                list_of_names.append(entry.name)
    else:
        list_of_names.append(os.path.basename(input_[0]))
    return list_of_names


def main():
    tmp = tempfile.TemporaryDirectory()
    cur_path = os.getcwd()
    args = cli_argument_parser()
    try:
        log.info(f'Reading model {args.model_path}')
        model = ort.InferenceSession(args.model_path)
        model_wrapper = ONNXIOModelWrapper('', args.batch_size)
        model_data = ONNXRuntimeTransformerCpp(model)
        io = IOAdapter.get_io_adapter(args, model_wrapper, model_data)

        if args.input:
            log.info(f'Preparing input data: {args.input}')
            io.prepare_input(model, args.input)
        else:
            log.warning('Input data not provided. Using dummy input')

        if args.mean != '' and args.scale != '':
            log.info('Transform mean and std from RGB to BGR')
            args.mean = std_transformer(args.mean)
            args.scale = std_transformer(args.scale)

        log.info('Prepare output file names')
        list_of_names = prepare_output_file_names(args.input)

        log.info('Preparing images for benchmark in temporary directory')
        prepare_images_for_benchmark(io, tmp.name, list_of_names, cur_path)

        args.input = args.input[0]

        log.info('Initializing onnxruntime process')
        proc = OnnxRuntimeProcess()
        proc.create_command_line(create_dict_from_args_for_process(args, str(len(os.listdir(tmp.name)))))

        log.info('Onnxruntime benchmark process:\n')
        proc.execute()
        res = proc.process_benchmark_output(args.output_json_path)
        io.process_output(res, log)

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
