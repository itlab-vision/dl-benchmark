import argparse
import json
import logging as log
import os
import sys
import traceback
import warnings
import mxnet
from pathlib import Path
from time import time

import tvm

import postprocessing_data as pp
from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from io_model_wrapper import TVMIOModelWrapper
from transformer import TVMTransformer
from reporter.report_writer import ReportWriter
from tvm_auxiliary import (TVMConverter, create_dict_for_converter,
                           prepare_output)


def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mn', '--model_name',
                        help='Model name to download using packages from framework.',
                        type=str,
                        dest='model_name')
    parser.add_argument('-m', '--model',
                        help='Path to an .json file with a trained model.',
                        type=str,
                        dest='model_path')
    parser.add_argument('-w', '--weights',
                        help='Path to an .params file with a trained weights.',
                        type=str,
                        dest='model_params')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on CPU or '
                             'NVIDIA_GPU (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('-f', '--framework',
                        help='Model name to download using GluonCV package.',
                        type=str,
                        dest='framework')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations.',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--output_names',
                        help='Name of the output tensors.',
                        default='output0',
                        type=str,
                        nargs='+',
                        dest='output_names')
    parser.add_argument('-t', '--task',
                        help='Task type determines the type of output processing '
                             'method. Available values: feedforward - without'
                             'postprocessing (by default), classification - output'
                             'is a vector of probabilities.',
                        choices=['feedforward', 'classification'],
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('-i', '--input',
                        help='Path to data.',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-in', '--input_name',
                        help='Input name.',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape BxWxHxC, B is a batch size,'
                             'W is an input tensor width,'
                             'H is an input tensor height,'
                             'C is an input tensor number of channels.',
                        required=True,
                        type=int,
                        nargs=4,
                        dest='input_shape')
    parser.add_argument('--norm',
                        help='Flag to normalize input images'
                             '(use --mean and --std arguments to set'
                             'required normalization parameters).',
                        action='store_true',
                        dest='norm')
    parser.add_argument('--mean',
                        help='Mean values.',
                        default=[0, 0, 0],
                        type=float,
                        nargs=3,
                        dest='mean')
    parser.add_argument('--std',
                        help='Standard deviation values.',
                        default=[1., 1., 1.],
                        type=float,
                        nargs=3,
                        dest='std')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results to print',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('-b', '--batch_size',
                        help='Batch size.',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('--channel_swap',
                        help='Parameter of channel swap (WxHxC to CxWxH by default).',
                        default=[2, 0, 1],
                        type=int,
                        nargs=3,
                        dest='channel_swap')
    args = parser.parse_args()
    return args

def create_dict_for_transformer(args):
    dictionary = {
        'channel_swap': args.channel_swap,
        'mean': args.mean,
        'std': args.std,
        'norm': args.norm,
        'input_shape': args.input_shape,
        'batch_size': args.batch_size,
    }
    return dictionary


def create_dict_for_modelwrapper(args):
    dictionary = {
        'input_name': args.input_name,
        'input_shape': [args.batch_size] + args.input_shape[1:4],
        'model_name': args.model_name,
    }
    return dictionary


def inference_tvm(module, num_of_iteration, input_name, get_slice):
    if num_of_iteration == 1:
        slice_input = get_slice() 
        module.set_input(input_name, slice_input[input_name].asnumpy())
        module.run()
        result = module.get_output(0)
        return result


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    report_writer = ReportWriter()
    wrapper = TVMIOModelWrapper(create_dict_for_modelwrapper(args))
    transformer = TVMTransformer(create_dict_for_transformer(args))
    io = IOAdapter.get_io_adapter(args, wrapper, transformer)
    converter = TVMConverter(create_dict_for_converter(args))
    graph_module = converter.convert_model_from_framework()
    io.prepare_input(graph_module, args.input)
    res = inference_tvm(graph_module, args.number_iter, args.input_name, io.get_slice_input_mxnet)
    io.process_output(prepare_output(res, args.task, args.output_names), log)




if __name__ == '__main__':
    sys.exit(main() or 0)