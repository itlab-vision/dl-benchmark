import argparse
import ast
import logging as log
import re
import sys
import traceback
from time import time

import numpy as np
import onnxruntime as onnx_rt

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import ONNXIOModelWrapper
from transformer import ONNXRuntimeTransformer


ORT_EXECUTION_MODE = {
    'ORT_SEQUENTIAL': onnx_rt.ExecutionMode.ORT_SEQUENTIAL,
    'ORT_PARALLEL': onnx_rt.ExecutionMode.ORT_PARALLEL,
}

ORT_EXECUTION_PROVIDERS_OPTIONS = {
    'CUDAExecutionProvider': {
        'device_id': 0,
        'arena_extend_strategy': 'kSameAsRequested',
        'cudnn_conv_algo_search': 'DEFAULT',
        'do_copy_in_default_stream': True,
        'cudnn_conv_use_max_workspace': '1',
        'cudnn_conv1d_pad_to_nc1d': '1',
    },
}


def names_arg(values):
    if values is not None:
        values = values.split(',')

    return values


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to file with a trained model.',
                        required=True,
                        type=str,
                        dest='model')
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
    parser.add_argument('--execution_providers',
                        help='Execution provider name (CPUExecutionProvider by default).',
                        default='CPUExecutionProvider',
                        type=names_arg,
                        dest='execution_providers')
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
    parser.add_argument('-in', '--input_names',
                        help='Input layer name',
                        default=None,
                        type=names_arg,
                        dest='input_names')
    parser.add_argument('-on', '--output_names',
                        help='Output layer names',
                        default=None,
                        type=names_arg,
                        dest='output_names')
    parser.add_argument('--input_scale',
                        help='Parameter input scale',
                        type=str,
                        dest='input_scale')
    parser.add_argument('--input_shapes',
                        help='Input tensor shapes',
                        default=None,
                        type=str,
                        dest='input_shapes')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=None,
                        type=str,
                        dest='mean')
    parser.add_argument('--channel_swap',
                        help='Parameter channel swap',
                        default=None,
                        type=str,
                        dest='channel_swap')
    parser.add_argument('--layout',
                        help='Parameter input layout',
                        default=None,
                        type=str,
                        dest='layout')
    parser.add_argument('-nthreads', '--number_threads',
                        help='Sets the number of threads used to parallelize the execution within nodes.',
                        default=0,
                        type=int,
                        dest='number_threads')
    parser.add_argument('--number_inter_threads',
                        help='Sets the number of threads used to parallelize the execution of the graph across nodes.',
                        default=0,
                        type=int,
                        dest='num_inter_threads')
    parser.add_argument('--execution_mode',
                        help='Sets the execution mode. Default is sequential.',
                        default='ORT_SEQUENTIAL',
                        type=str,
                        choices=['ORT_SEQUENTIAL', 'ORT_PARALLEL'],
                        dest='execution_mode')

    args = parser.parse_args()

    return args


def parse_input_arg(values, input_names):
    return_values = {}
    if values is not None:
        matches = re.findall(r'(.*?)\[(.*?)\],?', values)
        if matches:
            for i, match in enumerate(matches):
                name, value = match
                value = ast.literal_eval(value)
                if name != '':
                    return_values[name] = value
                else:
                    if input_names is None:
                        raise ValueError(f'Please set --input-names parameter'
                                         f' or use input0[value0],input1[value1] format instead {values}')
                    return_values[input_names[i]] = value
        else:
            raise ValueError(f'Unable to parse input parameter: {values}')
    return return_values


def parse_layout_arg(values, input_names):
    return_values = {}
    if values is not None:
        matches = re.findall(r'(.*?)\((.*?)\),?', values)
        if matches:
            for i, match in enumerate(matches):
                name, value = match
                if name != '':
                    return_values[name] = value
                else:
                    if input_names is None:
                        raise ValueError(f'Please set --input-names parameter'
                                         f' or use input0(value0),input1(value1) format instead {values}')
                    return_values[input_names[i]] = value
        else:
            values = values.split(',')
            return_values = dict(zip(input_names, values))
    return return_values


def set_session_options(number_threads, execution_mode, num_inter_threads):
    sess_options = onnx_rt.SessionOptions()
    sess_options.intra_op_num_threads = number_threads
    sess_options.execution_mode = ORT_EXECUTION_MODE[execution_mode]
    sess_options.graph_optimization_level = onnx_rt.GraphOptimizationLevel.ORT_ENABLE_ALL
    if execution_mode == 'ORT_PARALLEL':
        sess_options.inter_op_num_threads = num_inter_threads
    elif num_inter_threads > 0:
        log.warning('Perameter num_inter_threads is only set in ORT_PARALLEL mode')

    return sess_options


def create_inference_session(model, execution_providers, device, session_options):
    log.info(f'Setting device to {device}')
    log.info(f'Setting execution providers to {execution_providers}')

    provider_options = []
    for provider in execution_providers:
        options = ORT_EXECUTION_PROVIDERS_OPTIONS.get(provider, {})
        options['device_type'] = device
        provider_options.append(options)

    session = onnx_rt.InferenceSession(
        model, providers=execution_providers, provider_options=provider_options, sess_options=session_options,
    )
    return session


def inference_onnx_runtime(session, output_names, number_iter, get_slice):
    result = None
    time_infer = []
    slice_input = None

    if number_iter == 1:
        slice_input = get_slice(0)
        t0 = time()
        result = session.run(output_names, slice_input)
        t1 = time()
        time_infer.append(t1 - t0)
    else:
        for i in range(number_iter):
            slice_input = get_slice(i)
            t0 = time()
            session.run(output_names, slice_input)
            t1 = time()
            time_infer.append(t1 - t0)

    return result, time_infer


def process_result(batch_size, inference_time):
    inference_time = pp.three_sigma_rule(inference_time)
    average_time = pp.calculate_average_time(inference_time)
    latency = pp.calculate_latency(inference_time)
    fps = pp.calculate_fps(batch_size, latency)

    return average_time, latency, fps


def prepare_output(result, output_names, task, args):
    if task == 'feedforward':
        return {}
    if (output_names is None) or len(output_names) == 0:
        output_names = ['_output']
    if task == 'classification':
        return {output_names[0]: np.array(result).reshape(args.batch_size, -1)}
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def result_output(average_time, fps, latency, log):
    log.info('Average time of single pass : {0:.3f}'.format(average_time))
    log.info('FPS : {0:.3f}'.format(fps))
    log.info('Latency : {0:.3f}'.format(latency))


def raw_result_output(average_time, fps, latency):
    print('{0:.3f},{1:.3f},{2:.3f}'.format(average_time, fps, latency))


def create_dict_for_transformer(args):
    dictionary = {}
    for name in args.input_names:
        channel_swap = args.channel_swap.get(name, None)
        mean = args.mean.get(name, None)
        input_scale = args.input_scale.get(name, None)
        layout = args.layout.get(name, 'NCHW')
        dictionary[name] = {'channel_swap': channel_swap, 'mean': mean,
                            'input_scale': input_scale, 'layout': layout}

    return dictionary


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    try:
        args.input_shapes = parse_input_arg(args.input_shapes, args.input_names)
        model_wrapper = ONNXIOModelWrapper(args.input_shapes, args.batch_size)

        log.info('Setting inference session options')
        sess_options = set_session_options(args.number_threads, args.execution_mode, args.num_inter_threads)
        log.info(f'Creating inference session:\n\t {args.model}')
        inference_session = create_inference_session(args.model, args.execution_providers, args.device, sess_options)

        args.input_names = model_wrapper.get_input_layer_names(inference_session)

        args.mean = parse_input_arg(args.mean, args.input_names)
        args.input_scale = parse_input_arg(args.input_scale, args.input_names)
        args.channel_swap = parse_input_arg(args.channel_swap, args.input_names)
        args.layout = parse_layout_arg(args.layout, args.input_names)

        data_transformer = ONNXRuntimeTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        for layer_name in args.input_names:
            layer_shape = model_wrapper.get_input_layer_shape(inference_session, layer_name)
            log.info(f'Shape for input layer {layer_name}: {layer_shape}')

        log.info('Preparing input data')
        io.prepare_input(inference_session, args.input)
        io.fill_unset_inputs(inference_session, log)

        if args.output_names is None:
            outputs = inference_session.get_outputs()
            args.output_names = [output.name for output in outputs]

        log.info(f'Starting inference ({args.number_iter} iterations)')
        result, inference_time = inference_onnx_runtime(
            inference_session, args.output_names, args.number_iter, io.get_slice_input)

        log.info('Computing performance metrics')
        average_time, latency, fps = process_result(args.batch_size, inference_time)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Converting output tensor to print results')
                    result = prepare_output(result, args.output_names, args.task, args)

                    log.info('Inference results')
                    io.process_output(result, log)
                except Exception as ex:
                    log.warning('Error when printing inference results. {0}'.format(str(ex)))

            log.info('Performance results')
            result_output(average_time, fps, latency, log)
        else:
            raw_result_output(average_time, fps, latency)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
