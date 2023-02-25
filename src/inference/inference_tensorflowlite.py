import sys
import ast
import argparse
import re
import logging as log
from time import time

import tensorflow as tf
from io_adapter import IOAdapter
from io_model_wrapper import TensorFlowLiteIOModelWrapper
from transformer import TensorFlowLiteTransformer

import postprocessing_data as pp


def names_arg(values):
    if values is not None:
        values = values.split(',')

    return values


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to an .tflite with a trained model.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=True,
                        type=str,
                        nargs='+',
                        dest='input')
    parser.add_argument('-b', '--batch_size',
                        help='Size of the processed pack',
                        default=1,
                        type=int,
                        dest='batch_size')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['classification', 'detection', 'yolo_tiny_voc', 'yolo_v2_coco',
                                 'yolo_v2_tiny_coco', 'yolo_v3_tf', 'mask-rcnn'],
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
    parser.add_argument('--channel_swap',
                        help='Parameter channel swap',
                        default=None,
                        type=str,
                        dest='channel_swap')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=None,
                        type=str,
                        dest='mean')
    parser.add_argument('--input_scale',
                        help='Parameter input scale',
                        default=None,
                        type=str,
                        dest='input_scale')
    parser.add_argument('--layout',
                        help='Parameter input layout',
                        default=None,
                        type=str,
                        dest='layout')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--input_shapes',
                        help='Input tensor shapes',
                        default=None,
                        type=str,
                        dest='input_shapes')
    parser.add_argument('--input_names',
                        help='Names of the input tensors',
                        default=None,
                        type=names_arg,
                        dest='input_names')
    parser.add_argument('-nthreads', '--number_threads',
                        help='Number of threads to use for inference on the CPU. (Max by default)',
                        default=None,
                        type=int,
                        nargs=1,
                        dest='number_threads')
    parser.add_argument('--delegate_ext',
                        help='Path to delegate library',
                        default=None,
                        type=str,
                        nargs=1,
                        dest='delegate_ext')
    parser.add_argument('--delegate_options',
                        help='Delegate options, format: "option1: value1; option2: value2"',
                        default=None,
                        type=str,
                        nargs=1,
                        dest='delegate_options')

    args = parser.parse_args()

    return args


def get_input_shape(io_model_wrapper, model):
    layer_shapes = {}
    layer_names = io_model_wrapper.get_input_layer_names(model)
    for input_layer in layer_names:
        shape = ''
        for dem in io_model_wrapper.get_input_layer_shape(model, input_layer):
            shape += f'{dem}x'  # noqa: PLR1713
        shape = shape[:-1]
        layer_shapes.update({input_layer: shape})

    return layer_shapes


def load_delegates(delegate_ext, options):
    delegate_options = {}

    if options is not None:
        options = options.split(';')
        for option in options:
            try:
                key, value = option.split(':')
                delegate_options[key.strip()] = value.strip()
            except Exception:
                raise ValueError(f'Unable to parse delegate option: {option}')

    delegate = tf.lite.load_delegate(delegate_ext, delegate_options)
    return [delegate]


def load_network(tensorflow, model, number_threads, delegates):
    suffix = model.rpartition('.')[2]
    if suffix == 'tflite':
        return tensorflow.Interpreter(model_path=model, num_threads=number_threads, experimental_delegates=delegates)
    else:
        raise ValueError(f'Unsupported file format of the model: {suffix}')


def inference_tflite(interpreter, number_iter, get_slice):
    result = None
    time_infer = []
    interpreter.allocate_tensors()
    model_inputs = interpreter.get_input_details()
    input_info = {}
    for model_input in model_inputs:
        input_info[model_input['name']] = (model_input['index'], model_input['dtype'], model_input['shape'])

    outputs = interpreter.get_output_details()
    for i in range(number_iter):
        for name, data in get_slice(i).items():
            interpreter.set_tensor(input_info[name][0], data.astype(input_info[name][1]))
        t0 = time()
        interpreter.invoke()
        result = [interpreter.get_tensor(output['index']) for output in outputs]
        t1 = time()
        time_infer.append(t1 - t0)

    return result, time_infer


def reshape_model_input(io_model_wrapper, model, log):
    model_inputs = model.get_input_details()
    for model_input in model_inputs:
        shape = io_model_wrapper.get_input_layer_shape(model, model_input['name'])
        if len(model_input['shape']) == 0 or (shape != model_input['shape']).any():
            log.info(f'Reshaping model input from {model_input["shape"]} to {shape}')
            model.resize_tensor_input(model_input['index'], shape)


def process_result(batch_size, inference_time):
    inference_time = pp.three_sigma_rule(inference_time)
    average_time = pp.calculate_average_time(inference_time)
    latency = pp.calculate_latency(inference_time)
    fps = pp.calculate_fps(batch_size, latency)

    return average_time, latency, fps


def result_output(average_time, fps, latency, log):
    log.info(f'Average time of single pass : {average_time:.3f}')
    log.info(f'FPS : {fps:.3f}')
    log.info(f'Latency : {latency:.3f}')


def raw_result_output(average_time, fps, latency):
    print(f'{average_time:.3f},{fps:.3f},{latency:.3f}')


def create_dict_for_transformer(args):
    dictionary = {}
    for name in args.input_names:
        channel_swap = args.channel_swap.get(name, None)
        mean = args.mean.get(name, None)
        input_scale = args.input_scale.get(name, None)
        layout = args.layout.get(name, 'NHWC')
        dictionary[name] = {'channel_swap': channel_swap, 'mean': mean,
                            'input_scale': input_scale, 'layout': layout}

    return dictionary


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
                        raise ValueError('Please set --input-names parameter'
                                         ' or use input0[value0],input1[value1] format')
                    return_values[input_names[i]] = list(value)
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
                        raise ValueError('Please set --input-names parameter'
                                         ' or use input0(value0),input1(value1) format')
                    return_values[input_names[i]] = value
        else:
            values = values.split(',')
            return_values = dict(zip(input_names, values))
    return return_values


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)
    args = cli_argument_parser()
    try:
        args.input_shapes = parse_input_arg(args.input_shapes, args.input_names)
        model_wrapper = TensorFlowLiteIOModelWrapper(args.input_shapes, args.batch_size)

        delegate = None
        if args.delegate_ext:
            log.info(f'Loading delegate library from {args.delegate_ext}')
            delegate = load_delegates(args.delegate_ext, args.delegate_options)

        log.info(f'Loading network files:\n\t {args.model_path}')
        interpreter = load_network(tf.lite, args.model_path, args.number_threads, delegate)

        args.input_names = model_wrapper.get_input_layer_names(interpreter)

        args.mean = parse_input_arg(args.mean, args.input_names)
        args.input_scale = parse_input_arg(args.input_scale, args.input_names)
        args.channel_swap = parse_input_arg(args.channel_swap, args.input_names)
        args.layout = parse_layout_arg(args.layout, args.input_names)

        data_transformer = TensorFlowLiteTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        input_shapes = get_input_shape(model_wrapper, interpreter)
        for layer in input_shapes:
            log.info(f'Shape for input layer {layer}: {input_shapes[layer]}')

        log.info('Prepare input data')

        io.prepare_input(interpreter, args.input)
        reshape_model_input(model_wrapper, interpreter, log)

        log.info(f'Starting inference ({args.number_iter} iterations)')

        result, inference_time = inference_tflite(interpreter, args.number_iter, io.get_slice_input)

        time, latency, fps = process_result(args.batch_size, inference_time)
        if not args.raw_output:
            io.process_output(result, log)
            result_output(time, fps, latency, log)
        else:
            raw_result_output(time, fps, latency)
    except Exception as ex:
        print(f'ERROR! : {" ".join(ex)}')
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
