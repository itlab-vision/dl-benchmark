import argparse
import json
import logging as log
import sys
from pathlib import Path

from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from reporter.report_writer import ReportWriter

import cv2
from ncnn.model_zoo import get_model
from ncnn.utils import print_topk
import numpy as np

sys.path.append(str(Path(__file__).parent.parent.parent))

def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-m', '--model',
                        help='Model name',
                        choices=['squeezenet', 'shufflenetv2'],
                        default='squeezenet',
                        type=str,
                        dest='model')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file',
                        default=None,
                        type=str,
                        dest='labels')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results',
                        default=3,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['ncnn_classification'],
                        default='ncnn_classification',
                        type=str,
                        dest='task')
    parser.add_argument('-ni', '--number_iter',
                        help='Number of inference iterations',
                        default=1,
                        type=int,
                        dest='number_iter')
    parser.add_argument('--raw_output',
                        help='Raw output without logs',
                        default=False,
                        type=bool,
                        dest='raw_output')
    parser.add_argument('--target_size',
                        help='Parameter image target size',
                        default=256,
                        type=int,
                        dest='target_size')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--num_threads',
                        help='Number of threads',
                        default=4,
                        type=int,
                        dest='num_threads')
    parser.add_argument('--time',
                        required=False,
                        default=0,
                        type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'ncnn_inference_report.json',
                        dest='report_path')
    args = parser.parse_args()

    return args

def inference_ncnn(args, images, number_iter, get_slice, test_duration):
    result = None
    time_infer = []
    log.info(f'Starting inference ({number_iter} iterations)')
    if number_iter == 1:
        slice_input = get_slice(images, 1)
        result, exec_time = infer_slice(args, slice_input)
        time_infer.append(exec_time)
    else:
        time_infer = loop_inference(number_iter, test_duration)(inference_iteration)(get_slice)
    log.info('Inference completed')
    return result, time_infer

def inference_iteration(get_slice):
    slice_input = get_slice(images, 1)
    print(slice_input)
    _, exec_time = infer_slice(args, slice_input)
    return exec_time

@get_exec_time()
def infer_slice(args, slice_input):
    use_gpu = False
    if args.device =='GPU':
        use_gpu = True
    net = get_model(args.model, num_threads=args.num_threads, use_gpu=use_gpu)
    res = dict()
    for i in range(args.batch_size):
        image = cv2.imread(slice_input[i])
        cls_scores = net(image)
        res[slice_input[i]] = cls_scores
    return res

if __name__ == '__main__':
    args = cli_argument_parser()
    io = IOAdapter.get_io_adapter(args, None, None)

    report_writer = ReportWriter()
    report_writer.update_framework_info(name='ncnn')
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)
    images = io._IOAdapter__create_list_images(args.input)
    result, inference_time = inference_ncnn(args, images, args.number_iter,
                                            io.get_slice_input, args.time)
    if not args.raw_output:
        if args.number_iter == 1:
            io.process_output(result, log)
