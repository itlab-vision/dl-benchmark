import argparse
import json
import logging as log
import sys
import traceback
from pathlib import Path

from inference_tools.loop_tools import loop_inference
from reporter.report_writer import ReportWriter

try:
    import tensorflow.lite as tflite
except ModuleNotFoundError:
    import tflite_runtime.interpreter as tflite
    log.info('Using TFLite from tflite_runtime package')
from inference_tools.loop_tools import get_exec_time

import postprocessing_data as pp
import preprocessing_data as prep
from io_adapter import IOAdapter
from io_model_wrapper import TensorFlowLiteIOModelWrapper
from transformer import TensorFlowLiteTransformer


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
                        type=prep.names_arg,
                        dest='input_names')
    parser.add_argument('-nthreads', '--number_threads',
                        help='Number of threads to use for inference on the CPU. (Max by default)',
                        default=None,
                        type=int,
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
    parser.add_argument('--output_names',
                        help='Name of the output tensor',
                        default=None,
                        type=str,
                        nargs='+',
                        dest='output_names')
    parser.add_argument('-nt', '--number_top',
                        help='Number of top results to print',
                        default=5,
                        type=int,
                        dest='number_top')
    parser.add_argument('-l', '--labels',
                        help='Labels mapping file',
                        default=None,
                        type=str,
                        dest='labels')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'tflite_inference_report.json',
                        dest='report_path')
    parser.add_argument('--time', required=False, default=0, type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')

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

    delegate = tflite.load_delegate(delegate_ext, delegate_options)
    return [delegate]


def load_network(tensorflow, model, number_threads, delegates):
    suffix = model.rpartition('.')[2]
    if suffix == 'tflite':
        return tensorflow.Interpreter(model_path=model, num_threads=number_threads, experimental_delegates=delegates)
    else:
        raise ValueError(f'Unsupported file format of the model: {suffix}')


def inference_tflite(interpreter, number_iter, get_slice, test_duration):
    result = None
    interpreter.allocate_tensors()
    model_inputs = interpreter.get_input_details()
    input_info = {}
    for model_input in model_inputs:
        input_info[model_input['name']] = (model_input['index'], model_input['dtype'], model_input['shape'])
    outputs = interpreter.get_output_details()
    if number_iter > 1:
        time_infer = loop_inference(number_iter, test_duration)(inference_iteration)(get_slice, input_info, interpreter)
    else:
        result, exec_time = inference_with_output(get_slice, input_info, interpreter, outputs)
        time_infer = [exec_time]
    return result, time_infer


def inference_iteration(get_slice, input_info, interpreter):
    for name, data in get_slice().items():
        interpreter.set_tensor(input_info[name][0], data.astype(input_info[name][1]))
    _, exec_time = infer_slice(interpreter)
    return exec_time


def inference_with_output(get_slice, input_info, interpreter, outputs):
    exec_time = inference_iteration(get_slice, input_info, interpreter)
    result = [interpreter.get_tensor(output['index']) for output in outputs]
    return result, exec_time


@get_exec_time()
def infer_slice(interpreter):
    interpreter.invoke()


def reshape_model_input(io_model_wrapper, model, log):
    model_inputs = model.get_input_details()
    for model_input in model_inputs:
        shape = io_model_wrapper.get_input_layer_shape(model, model_input['name'])
        if len(model_input['shape']) == 0 or (shape != model_input['shape']).any():
            log.info(f'Reshaping model input from {model_input["shape"]} to {shape}')
            model.resize_tensor_input(model_input['index'], shape)


def prepare_output(result, output_names, task):
    if (output_names is None) or (len(result) != len(output_names)):
        raise ValueError('The number of output tensors does not match the number of corresponding output names')
    if task == 'classification':
        return {output_names[i]: result[i] for i in range(len(result))}
    else:
        raise ValueError(f'Unsupported task {task} to print inference results')


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='TF-Lite')
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)
    try:
        args.input_shapes = prep.parse_input_arg(args.input_shapes, args.input_names)
        model_wrapper = TensorFlowLiteIOModelWrapper(args.input_shapes, args.batch_size)

        delegate = None
        if args.delegate_ext:
            log.info(f'Loading delegate library from {args.delegate_ext}')
            delegate = load_delegates(args.delegate_ext, args.delegate_options)

        log.info(f'Loading network files:\n\t {args.model_path}')
        interpreter = load_network(tflite, args.model_path, args.number_threads, delegate)

        args.input_names = model_wrapper.get_input_layer_names(interpreter)

        args.mean = prep.parse_input_arg(args.mean, args.input_names)
        args.input_scale = prep.parse_input_arg(args.input_scale, args.input_names)
        args.channel_swap = prep.parse_input_arg(args.channel_swap, args.input_names)
        args.layout = prep.parse_layout_arg(args.layout, args.input_names)

        data_transformer = TensorFlowLiteTransformer(prep.create_dict_for_transformer(args, 'NHWC'))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        input_shapes = get_input_shape(model_wrapper, interpreter)
        for layer in input_shapes:
            log.info(f'Shape for input layer {layer}: {input_shapes[layer]}')

        log.info('Preparing input data')
        io.prepare_input(interpreter, args.input)
        reshape_model_input(model_wrapper, interpreter, log)

        log.info(f'Starting inference ({args.number_iter} iterations)')
        result, inference_time = inference_tflite(interpreter, args.number_iter, io.get_slice_input, args.time)

        inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time)

        report_writer.update_execution_results(**inference_result)
        log.info(f'Write report to {args.report_path}')
        report_writer.write_report(args.report_path)

        if not args.raw_output:
            if args.number_iter == 1:
                try:
                    log.info('Converting output tensor to print results')
                    result = prepare_output(result, args.output_names, args.task)

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
