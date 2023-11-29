import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

import numpy as np

import preprocessing_data as prep
from inference_pytorch import load_model_from_file, load_model_from_module, compile_model
from io_adapter import IOAdapter
from io_model_wrapper import PyTorchIOModelWrapper
from transformer import PyTorchTransformerCpp

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-bch', '--benchmark_app',
                        help='Path to PYTORCH_benchmark',
                        required=True,
                        type=str,
                        dest='benchmark_path')
    parser.add_argument('-m', '--model',
                        help='Path to PyTorch model with format .pt.',
                        type=str,
                        dest='model')
    parser.add_argument('-w', '--weights',
                        help='Path to file with format .pth with weights of PyTorch model',
                        type=str,
                        default=None,
                        dest='weights')
    parser.add_argument('-mm', '--module',
                        help='Module with model architecture.',
                        default='torchvision.models',
                        type=str,
                        dest='module')
    parser.add_argument('-mn', '--model_name',
                        help='Model name from the module.',
                        required=True,
                        type=str,
                        dest='model_name')
    parser.add_argument('-i', '--input',
                        help='Path to data.',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-in', '--input_names',
                        help='Names of the input tensors',
                        required=True,
                        default=None,
                        type=prep.names_arg,
                        dest='input_names')
    parser.add_argument('-is', '--input_shapes',
                        help='Input tensor shapes',
                        default=None,
                        type=str,
                        dest='input_shapes')
    parser.add_argument('--input_type',
                        help='Parameter input type in format [value]',
                        default='[FP32]',
                        type=str,
                        dest='input_type')
    parser.add_argument('--layout',
                        help='Parameter input layout in format [value]',
                        default=None,
                        type=str,
                        dest='layout')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=None,
                        type=str,
                        dest='mean')
    parser.add_argument('--input_scale',
                        help='Parameter input scale',
                        type=str,
                        dest='input_scale')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file.',
                        default=None,
                        type=str,
                        dest='labels')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results.',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Task type determines the type of output processing '
                             'method. Available values: feedforward - without'
                             'postprocessing (by default), classification - output'
                             'is a vector of probabilities.',
                        choices=['feedforward', 'classification'],
                        default='feedforward',
                        type=str,
                        dest='task')
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


class PyTorchProcess():
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
            elif arg != '' and arg is not None:
                self._add_argument(name, arg)

    def execute(self):
        proc = subprocess.run(self._command_line, shell=True)
        if proc.returncode != 0:
            log.error(traceback.format_exc())
            sys.exit(1)

    def process_benchmark_output(self, output_filename):
        result = {}
        with open(output_filename, 'r') as file:
            name = 'output'
            out = json.load(file)[0][0]
            shape = out['shape']
            data = out['data']
            result[name] = np.reshape(data, shape)
        return result


def save_model(model_path, model_name, compiled_model, input_shapes, save_dir):
    if model_path is not None:
        return model_path
    import torch
    model_path = os.path.join(save_dir, model_name + '.pt')
    log.info(f'Saving model to file {model_path}')
    traced_script_module = torch.jit.trace(compiled_model, [torch.rand(*input_shapes[layer]) for layer in input_shapes])
    traced_script_module.save(model_path)
    return model_path


def dict_to_string(input_params):
    def get_values(values):
        values = ','.join(map(str, values)) if not isinstance(values, str) else values
        return values if re.match(r'\[(.*?)\]', values) else f'[{values}]'
    return ','.join(f'{layer_name}{get_values(input_params[layer_name])}' for layer_name in input_params)


def create_dict_from_args_for_process(args):
    return {'-bch': args.benchmark_path,
            '-m': args.model,
            '-i': args.input,
            '--shape': dict_to_string(args.input_shapes),
            '--scale': dict_to_string(args.input_scale),
            '--mean': dict_to_string(args.mean),
            '--layout': dict_to_string(args.layout),
            '-dtype': dict_to_string(args.input_type),
            '-l': args.labels,
            '-b': args.batch_size,
            '--channel_swap': '' if not args.swap_channels else True,
            '--output_path': args.output_json_path,
            '-nireq': 1,
            '-niter': 1}


def prepare_images_for_benchmark(inputs, tmp_dir):
    if os.path.isdir(inputs[0]):
        return inputs[0]
    for path in inputs[0].split(','):
        shutil.copy2(path, tmp_dir)
    return tmp_dir


def main():
    tmp_input = tempfile.TemporaryDirectory()
    tmp_model = tempfile.TemporaryDirectory()
    args = cli_argument_parser()
    device = 'cpu'
    precision = 'FP32'
    try:
        args.input_shapes = prep.parse_input_arg(args.input_shapes, args.input_names)
        args.mean = prep.parse_input_arg(args.mean, args.input_names)
        args.input_scale = prep.parse_input_arg(args.input_scale, args.input_names)
        args.layout = prep.parse_layout_arg(args.layout, args.input_names)
        args.input_type = prep.parse_layout_arg(args.input_type, args.input_names)

        log.info('Loading the model')
        model_wrapper = PyTorchIOModelWrapper(args.input_shapes, args.batch_size, None, precision, args.input_type)
        data_transformer = PyTorchTransformerCpp()
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        if args.model is not None:
            model = load_model_from_file(args.model)
        else:
            model = load_model_from_module(args.model_name, args.module, args.weights, device)
        compiled_model = compile_model(model=model, device=device, model_type='baseline',
                                       shapes=args.input_shapes, input_type=args.input_type,
                                       tensor_rt_dtype=None,
                                       precision=precision,
                                       compile_backend=None,
                                       custom_compile_func=None,
                                       custom_trace_func=None)
        args.model = save_model(args.model, args.model_name, compiled_model, args.input_shapes, tmp_model.name)

        log.info('Preparing input images for the model output processing')
        io.prepare_input(compiled_model, args.input)

        log.info('Preparing images for benchmark in temporary directory')
        args.input = prepare_images_for_benchmark(args.input, tmp_input.name)

        log.info('Initializing PyTorch process')
        proc = PyTorchProcess()
        proc.create_command_line(create_dict_from_args_for_process(args))

        log.info('PyTorch benchmark process:\n')
        proc.execute()
        io.process_output(proc.process_benchmark_output(args.output_json_path), log)

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
