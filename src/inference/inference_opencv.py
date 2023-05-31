import argparse
import json
import logging as log
import sys
import traceback
from pathlib import Path
from time import time

import cv2
import numpy as np

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import OpenCVIOModelWrapper
from reporter.report_writer import ReportWriter
from transformer import OpenCVTransformer


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to file with a trained model.',
                        required=True,
                        type=str,
                        dest='model')
    parser.add_argument('-w', '--weights',
                        help='Path to file with a trained weights.',
                        default=None,
                        type=str,
                        dest='weights')
    parser.add_argument('--precision',
                        help='Specify the precision of weights (FP32 by default)',
                        default='FP32',
                        type=str,
                        dest='precision')
    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--backend',
                        help='Specify the backend of OpenCV to infer on (DNN by default)',
                        default='DNN',
                        choices=['DNN', 'IE'],
                        type=str,
                        dest='backend')
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
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['classification'],
                        default='feedforward',
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
    parser.add_argument('-in', '--input_name',
                        help='Input layer name',
                        default='_input',
                        type=str,
                        dest='input_name')
    parser.add_argument('-on', '--output_names',
                        help='Output layer names',
                        type=str,
                        nargs='*',
                        dest='output_names')
    parser.add_argument('--input_scale',
                        help='Parameter inverse scale factor',
                        default=1.0,
                        type=float,
                        dest='inv_scale_factor')
    parser.add_argument('--input_shape',
                        help='Input tensor shape in "height width channels" order',
                        default=[224, 224, 3],
                        type=int,
                        nargs=3,
                        dest='size')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=[0, 0, 0],
                        type=float,
                        nargs=3,
                        dest='mean')
    parser.add_argument('--std',
                        help='Parameter std',
                        default=[1, 1, 1],
                        type=float,
                        nargs=3,
                        dest='std')
    parser.add_argument('--swapRB',
                        help='Parameter channel swap',
                        default=False,
                        type=bool,
                        dest='swapRB')
    parser.add_argument('--crop',
                        help='Parameter crop',
                        default=False,
                        type=bool,
                        dest='crop')
    parser.add_argument('--layout',
                        help='Parameter input layout',
                        default=None,
                        type=str,
                        dest='layout')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'opencv_inference_report.json',
                        dest='report_path')

    args = parser.parse_args()

    return args


def set_backend_to_infer(net, backend):
    if backend == 'DNN':
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    elif backend == 'IE':
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
    else:
        raise ValueError('The backend is not available')


def set_device_to_infer(net, device, precision):
    if device == 'CPU':
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    elif device == 'GPU':
        if precision == 'FP16':
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL_FP16)
        else:
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)
    elif device == 'MYRIAD':
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
    else:
        raise ValueError('The device is not available')


def load_network(model, weights):
    if weights is not None:
        net = cv2.dnn.readNet(model, weights)
    else:
        net = cv2.dnn.readNet(model)
    return net


def load_images_to_network(net, input_):
    net.setInput(input_)


def inference_opencv(net, input_name, output_names, number_iter, get_slice):
    result = None
    time_infer = []
    slice_input = None

    if number_iter == 1:
        slice_input = get_slice()
        load_images_to_network(net, slice_input[input_name])
        if output_names:
            t0 = time()
            result = net.forward(output_names)
            t1 = time()
        else:
            t0 = time()
            result = net.forward()
            t1 = time()
        time_infer.append(t1 - t0)
    else:
        for _ in range(number_iter):
            slice_input = get_slice()
            load_images_to_network(net, slice_input[input_name])
            if output_names:
                t0 = time()
                result = net.forward(output_names)
                t1 = time()
            else:
                t0 = time()
                result = net.forward()
                t1 = time()
            time_infer.append(t1 - t0)

    return result, time_infer


def prepare_output(result, output_names, task, args):
    if task == 'feedforward':
        return {}
    if (output_names is None) or len(output_names) == 0:
        output_names = ['_output']
    if task == 'classification':
        return {output_names[0]: np.array(result).reshape(args.batch_size, -1)}
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def create_dict_for_transformer(args):
    dictionary = {
        'scalefactor': 1 / args.inv_scale_factor,
        'size': (args.size[0], args.size[1]),
        'mean': tuple(args.mean),
        'swapRB': args.swapRB,
        'crop': args.crop,
        'std': args.std,
        'layout': args.layout,
    }
    return dictionary


def create_dict_for_wrapper(args):
    dictionary = {
        'input_layer_name': args.input_name,
        'input_layer_shape': [args.batch_size, *args.size],
    }
    return dictionary


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='OpenCV', version=cv2.__version__)
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)

    try:
        model_wrapper = OpenCVIOModelWrapper(create_dict_for_wrapper(args))
        data_transformer = OpenCVTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        log.info('Loading network files:\n\t {0}\n\t {1}'.format(args.model, args.weights))
        if args.weights == '' or args.weights == 'none' or args.weights == 'None':
            args.weights = None
        net = load_network(args.model, args.weights)

        layer_name = model_wrapper.get_input_layer_names(net)
        log.info('Shape for input layer {0}: {1}'.format(
            layer_name,
            model_wrapper.get_input_layer_shape(net, layer_name),
        ))

        log.info('The assign of the backend to infer')
        set_backend_to_infer(net, args.backend)
        log.info(f'The backend has been assigned: {args.backend}')

        log.info('The assign of the device to infer')
        set_device_to_infer(net, args.device, args.precision)
        log.info(f'The device has been assigned: {args.device} ({args.precision})')

        log.info('Preparing input data')
        io.prepare_input(net, args.input)

        log.info(f'Starting inference ({args.number_iter} iterations)')
        result, inference_time = inference_opencv(
            net, args.input_name, args.output_names, args.number_iter, io.get_slice_input)

        log.info('Computing performance metrics')
        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time)

        report_writer.update_execution_results(**inference_result, iterations_num=args.number_iter)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Converting output tensor to print results')
                    result = prepare_output(result, args.output_names, args.task, args)

                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

        log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')

    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
