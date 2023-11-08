import argparse
import json
import logging as log
import sys
import importlib
import traceback

from pathlib import Path
from tvm_converter import MXNetToTVMConverter


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mn', '--model_name',
                        help='Model name to download using packages from GluonCV.',
                        type=str,
                        required=True,
                        dest='model_name')
    parser.add_argument('-m', '--model',
                        help='Path to an .json file with a trained model.',
                        type=str,
                        dest='model_path')
    parser.add_argument('-w', '--weights',
                        help='Path to an .params file with a trained weights.',
                        type=str,
                        dest='model_params')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxWxHxC, B is a batch size,'
                             'W is an input tensor width,'
                             'H is an input tensor height,'
                             'C is an input tensor number of channels.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-in', '--input_name',
                        help='Input name.',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on CPU or '
                             'NVIDIA_GPU (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    args = parser.parse_args()
    return args


def create_dict_for_converter_mxnet(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
        'model_path': args.model_path,
        'model_params': args.model_params,
        'device': args.device,
        'opt_level': 0,
    }
    return dictionary


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    converter = MXNetToTVMConverter(create_dict_for_converter_mxnet(args))
    converter.get_tvm_model()
    converter.save_tvm_model()


if __name__ == '__main__':
    sys.exit(main() or 0)
