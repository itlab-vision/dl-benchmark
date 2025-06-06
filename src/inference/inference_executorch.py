import argparse
import importlib
import json
import re
import sys
import traceback

from functools import partial
from pathlib import Path
from time import time

import postprocessing_data as pp
import preprocessing_data as prep
from pathlib import Path
import numpy as np
from executorch.runtime import Verification, Runtime, Program, Method
from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from io_model_wrapper import ExecuTorchIOModelWrapper
from reporter.report_writer import ReportWriter
from configs.config_utils import prepend_to_path, to_camel_case, get_model_config
from transformer import ExecuTorchTransformer
from tvm_auxiliary import create_dict_for_transformer, create_dict_for_modelwrapper

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))  # noqa: E402
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()

def cli_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mn', '--model_name',
                        help='Model name.',
                        type=str,
                        dest='model_name')
    parser.add_argument('-m', '--model',
                        help='Path to an .pte file with a trained model.',
                        type=Path,
                        dest='model_path')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
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
    parser.add_argument('--color_map',
                        help='Classes color map',
                        type=str,
                        default=None,
                        dest='color_map')
    parser.add_argument('-in', '--input_name',
                        help='Input name.',
                        default='data',
                        type=str,
                        dest='input_name')
    parser.add_argument('--time', required=False, default=0, type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')
    parser.add_argument('-is', '--input_shape',
                        help='Input shape NxHxWxC, N is a batch size,'
                             'H is an input tensor height,'
                             'W is an input tensor width,'
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
    parser.add_argument('--not_softmax',
                        help='Flag to do not use softmax function.',
                        action='store_true',
                        dest='not_softmax')
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
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file.',
                        default='image_net_labels.json',
                        type=str,
                        dest='labels')
    parser.add_argument('--layout',
                        help='Parameter input layout',
                        default='NHWC',
                        type=str,
                        dest='layout')
    parser.add_argument('--channel_swap',
                        help='Parameter of channel swap (RGB to BGR by default).',
                        default=[2, 1, 0],
                        type=int,
                        nargs=3,
                        dest='channel_swap')
    parser.add_argument('--threshold',
                        help='Probability threshold for detections filtering',
                        default=0.5,
                        type=float,
                        dest='threshold')
    parser.add_argument('--raw_output',
                        help='Raw output without logs.',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'tvm_inference_report.json',
                        dest='report_path')
    args = parser.parse_args()

    return args


def load_model(model_path):
     et_runtime = Runtime.get()
     program = et_runtime.load_program(
          model_path,
          verification=Verification.Minimal,
     )
     return program.load_method("forward")


def inference_executorch(net, num_iterations, get_slice, input_name, test_duration):
     predictions = None
     time_infer = []
     if num_iterations == 1:
        t0 = time()
        slice_input = get_slice()
        predictions = net.execute((slice_input[input_name],))
        t1 = time()
        time_infer.append(t1 - t0)
     else:
        loop_results = loop_inference(num_iterations, test_duration)(inference_iteration)(get_slice, input_name, net)
        time_infer = loop_results['time_infer']
     return predictions, time_infer


def inference_iteration(get_slice, input_name, net):
    slice_input = get_slice()
    _, exec_time = infer_slice(input_name, net, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(input_name, net, slice_input):
    res = net.execute((slice_input[input_name],))
    return res


def prepare_output(result, output_names, task_type):
     if task_type in ['feedforward']:
        return {}
     elif task_type in ['classification']:
        log.info('Converting output tensor to print results')
        return {output_names[0]: result[0].numpy()}
     else:
        raise ValueError(f'Unsupported task {task_type} to print inference results')    


def main():
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)
    try:
        wrapper = ExecuTorchIOModelWrapper(create_dict_for_modelwrapper(args))
        transformer = ExecuTorchTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, wrapper, transformer)

        log.info(f'Shape for input layer {args.input_name}: {args.input_shape}')
        #report_writer.update_framework_info(name='ExecuTorch', version=executorch.__version__)
        net = load_model(args.model_path)

        log.info(f'Preparing input data: {args.input}')
        io.prepare_input(net, args.input)

        log.info(f'Starting inference ({args.number_iter} iterations) on {args.device}')
        result, infer_time = inference_executorch(net,
                                                  args.number_iter,
                                                  io.get_slice_input_executorch,
                                                  args.input_name,
                                                  args.time)
        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    res = prepare_output(result, args.output_names, args.task)
                    log.info('Inference results')
                    io.process_output(res, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, infer_time)
        report_writer.update_execution_results(**inference_result)
        report_writer.write_report(args.report_path)
        log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)