import cv2
import argparse
import numpy as np
import os
import subprocess
import sys
import onnxruntime as ort
from io_model_wrapper import OnnxRuntimeWrapper
from transformer import OnnxRuntimeTransformer
from io_adapter import IOAdapter
import tempfile


class OnnxRuntimeProcess():
    def __init__(self):
        self._command_line = './'

    def _add_argument(self, name_of_arg, value_of_arg):
        if name_of_arg == ' -bch ':
            self._command_line += value_of_arg
        elif name_of_arg == ' -l ':
            if value_of_arg != '':
                self._command_line += ' --dump_flag '
        elif value_of_arg != '':
            self._command_line += name_of_arg + value_of_arg

    def create_command_line(self, dict_of_args):
        for name, arg in dict_of_args.items():
            self._add_argument(name, arg)
        self._command_line += ' -niter 1 '

    def execute(self):
        subprocess.run(self._command_line, shell=True)

    def parse_output(self, labels, tmp_dir):
        print('\n')
        with open(labels) as file:
            classes = file.readlines()
            classes = [line.rstrip('\n') for line in classes]
        for i in range(0, len(os.listdir(tmp_dir.name))):
            out = np.loadtxt('output' + str(i))
            result = np.argsort(out)[995:]
            for j in result[::-1]:
                print(f'{classes[j]} {out[j]}')
            print('\n')
            os.remove('output' + str(i))


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
                        required=True,
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
                        required=False,
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
    parser.add_argument('-task',
                        help='Scale values in <[R,G,B]>',
                        required=False,
                        default='',
                        type=str,
                        dest='task')
    parser.add_argument('-batch',
                        help='Scale values in <[R,G,B]>',
                        required=False,
                        default=1,
                        type=int,
                        dest='batch_size')
    args = parser.parse_args()

    return args


def std_transformer(std):
    std = std[1:-1]
    tmp = np.array(std.split(','), dtype=float)[::-1] * 255
    return f'[{tmp[0]},{tmp[1]},{tmp[2]}]'


def create_dict_from_args_for_process(args, nireq):
    return {' -bch ': args.benchmark_path,
            ' -m ': args.model_path,
            ' -i ': args.input,
            ' -w ': args.weights,
            ' --shape ': args.shape,
            ' --scale ': args.scale,
            ' --mean ': args.mean,
            ' -l ': args.labels,
            ' -nireq ': nireq}


def prepare_images_for_benchmark(io, tmp_dir, names_of_output, cur_path):
    os.chdir(tmp_dir)
    for i in range(0, len(names_of_output)):
        for val in io.get_slice_input(i).values():
            cv2.imwrite(names_of_output[i], val[0])
    os.chdir(cur_path)


def prepare_output_names(input_):
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

    model = ort.InferenceSession(args.model_path)

    model_wrapper = OnnxRuntimeWrapper(model)
    model_data = OnnxRuntimeTransformer(model)
    io = IOAdapter.get_io_adapter(args, model_wrapper, model_data)
    io.prepare_input(model, args.input)

    if args.mean != '' and args.scale != '':
        args.mean = std_transformer(args.mean)
        args.scale = std_transformer(args.scale)

    list_of_names = prepare_output_names(args.input)
    prepare_images_for_benchmark(io, tmp.name, list_of_names, cur_path)

    args.input = tmp.name
    proc = OnnxRuntimeProcess()
    proc.create_command_line(create_dict_from_args_for_process(args, str(len(os.listdir(tmp.name)))))
    proc.execute()
    proc.parse_output(args.labels, tmp)
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
