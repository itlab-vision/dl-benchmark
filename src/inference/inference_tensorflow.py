import argparse
import json
import logging as log
import sys
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.python.saved_model import signature_constants

import postprocessing_data as pp
from inference_tools.loop_tools import loop_inference, get_exec_time
from io_adapter import IOAdapter
from io_model_wrapper import TensorFlowIOModelWrapper
from reporter.report_writer import ReportWriter
from transformer import TensorFlowTransformer

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.model_converters.tf2tflite.tensorflow_common import (load_model, get_gpu_devices, is_gpu_available,  # noqa
                                                              get_input_operation_name, restrisct_gpu_usage)  # noqa

sys.path.append(str(Path(__file__).resolve().parents[1].joinpath('utils')))
from logger_conf import configure_logger  # noqa: E402

log = configure_logger()


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to an .pb or .meta file with a trained model.',
                        required=True,
                        type=str,
                        dest='model_path')
    parser.add_argument('-i', '--input',
                        help='Path to data',
                        required=False,
                        type=str,
                        nargs='+',
                        dest='input')
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
                        default=10,
                        type=int,
                        dest='number_top')
    parser.add_argument('-t', '--task',
                        help='Output processing method. Default: without postprocess',
                        choices=['classification', 'detection', 'yolo_tiny_voc', 'yolo_v2_coco',
                                 'yolo_v2_tiny_coco', 'yolo_v3_tf', 'mask-rcnn'],
                        default='feedforward',
                        type=str,
                        dest='task')
    parser.add_argument('--color_map',
                        help='Classes color map',
                        type=str,
                        default=None,
                        dest='color_map')
    parser.add_argument('--prob_threshold',
                        help='Probability threshold for detections filtering',
                        default=0.5,
                        type=float,
                        dest='threshold')
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
                        default=[2, 1, 0],
                        type=int,
                        nargs=3,
                        dest='channel_swap')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=[0, 0, 0],
                        type=float,
                        nargs=3,
                        dest='mean')
    parser.add_argument('--input_scale',
                        help='Parameter input scale',
                        default=1.0,
                        type=float,
                        dest='input_scale')
    parser.add_argument('-d', '--device',
                        help='Specify the target device to infer on (CPU by default)',
                        default='CPU',
                        type=str,
                        dest='device')
    parser.add_argument('--input_shape',
                        help='Input tensor shape in "height width channels" order',
                        default=None,
                        type=int,
                        nargs=3,
                        dest='input_shape')
    parser.add_argument('--input_name',
                        help='Name of the input tensor',
                        default=None,
                        type=str,
                        nargs=1,
                        dest='input_name')
    parser.add_argument('--output_names',
                        help='Name of the output tensor',
                        default=None,
                        type=str,
                        nargs='+',
                        dest='output_names')
    parser.add_argument('--num_inter_threads',
                        help='Number of threads used for parallelism between independent operations',
                        default=None,
                        type=int,
                        dest='num_inter_threads')
    parser.add_argument('--num_intra_threads',
                        help='Number of threads used within an individual op for parallelism',
                        default=None,
                        type=int,
                        dest='num_intra_threads')
    parser.add_argument('--report_path',
                        type=Path,
                        default=Path(__file__).parent / 'tf_inference_report.json',
                        dest='report_path')
    parser.add_argument('--time',
                        required=False,
                        default=0,
                        type=int,
                        dest='time',
                        help='Optional. Time in seconds to execute topology.')
    parser.add_argument('--restrisct_gpu_usage',
                        action='store_true',
                        help='Restrict TensorFlow to only use the first GPU')
    args = parser.parse_args()

    return args


def get_input_shape(io_model_wrapper, model):
    layer_shapes = {}
    layer_names = io_model_wrapper.get_input_layer_names(model)
    for input_layer in layer_names:
        shape = ''
        for dem in io_model_wrapper.get_input_layer_shape(model, input_layer):
            shape += '{0}x'.format(dem)
        shape = shape[:-1]
        layer_shapes.update({input_layer: shape})

    return layer_shapes


def prepare_output(result, outputs_name, task):
    if len(result) != len(outputs_name):
        raise ValueError('The number of output layers does not match the number of resulting tensors.')
    if task in ['yolo_tiny_voc', 'yolo_v2_coco', 'yolo_v2_tiny_coco', 'yolo_v3_tf']:
        result = [res.transpose(0, 3, 1, 2) for res in result]
    elif task in ['detection']:
        outputs_name = ['detection_output']
        batch = len(result[0])
        n = int(max(result[3]))
        new_result = np.zeros(shape=(1, 1, batch * n, 7))
        for bb in range(batch):
            num_detections = int(result[3][bb])
            for idx in range(num_detections):
                label = result[0][bb][idx]
                conf = result[1][bb][idx]
                coords = result[2][bb][idx]
                coords[0], coords[1] = coords[1], coords[0]
                coords[2], coords[3] = coords[3], coords[2]
                new_result[0][0][bb * n + idx] = [bb, label, conf, *coords]
        result = [new_result]
    elif task in ['mask-rcnn']:
        outputs_name = ['reshape_do_2d', 'masks']
        num_detections = int(result[3][0])
        detection_result = np.zeros(shape=(num_detections + 1, 7))
        mask = result[4]
        new_mask = np.zeros(shape=(num_detections, mask.shape[1], mask.shape[2], mask.shape[3]))
        for idx in range(num_detections):
            label = int(result[0][0][idx])
            conf = result[1][0][idx]
            coords = result[2][0][idx]
            coords[0], coords[1] = coords[1], coords[0]
            coords[2], coords[3] = coords[3], coords[2]
            detection_result[idx] = [0, label, conf, *coords]
            new_mask[idx][label - 1] = mask[0][idx]
        detection_result[num_detections][0] = -1
        result = [detection_result, new_mask]

    return {outputs_name[i]: result[i] for i in range(len(result))}


def inference_tensorflow(model, number_iter, get_slice, test_duration):
    result = None
    time_infer = []
    log.info(f'Starting inference ({number_iter} iterations)')

    if number_iter == 1:
        slice_input = get_slice()
        result, exec_time = infer_slice(model, slice_input)
        time_infer.append(exec_time)
    else:
        time_infer = loop_inference(number_iter, test_duration)(inference_iteration)(get_slice, model)
    log.info('Inference completed')
    return result, time_infer


def inference_iteration(get_slice, model):
    slice_input = get_slice()
    _, exec_time = infer_slice(model, slice_input)
    return exec_time


@get_exec_time()
def infer_slice(model, slice_input):
    model._num_positional_args = len(slice_input.keys())
    inputs = [tf.convert_to_tensor(value) for value in slice_input.values()]
    res = model(*inputs)
    return res


def create_dict_for_transformer(args):
    dictionary = {'channel_swap': args.channel_swap, 'mean': args.mean,
                  'input_scale': args.input_scale}

    return dictionary


def main():
    args = cli_argument_parser()
    report_writer = ReportWriter()
    report_writer.update_framework_info(name='TensorFlow', version=tf.__version__)
    report_writer.update_configuration_setup(batch_size=args.batch_size,
                                             iterations_num=args.number_iter,
                                             target_device=args.device)

    if args.device == 'NVIDIA_GPU':
        if is_gpu_available():
            if args.restrisct_gpu_usage:
                log.info('Restruct GPU usage to 1 GPU device')
                restrisct_gpu_usage()
        else:
            raise AssertionError('NVIDIA_GPU device not found on hostmachine, unable to infer on NVIDIA_GPU')

    if args.device == 'CPU' and is_gpu_available():
        log.warning(f'NVIDIA_GPU device(s) {get_gpu_devices()} available on machine,'
                    f' tensorflow will use NVIDIA_GPU by default')

    input_name = args.input_name
    input_op_name = get_input_operation_name(input_name)

    output_names = args.output_names
    model_path = Path(args.model_path)

    model_wrapper = TensorFlowIOModelWrapper(args)
    data_transformer = TensorFlowTransformer(create_dict_for_transformer(args))
    io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

    log.info(f'Loading network files:\n\t {args.model_path}')
    model_path = model_path.parent if model_path.name == 'saved_model.pb' else model_path

    model, _ = load_model(model_path,
                          input_names=input_op_name,
                          output_names=output_names,
                          const_inputs=[],
                          log=log)

    signature_key = signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY
    func = model._backref_to_saved_model.signatures[signature_key]
    graph = func.graph

    input_shapes = get_input_shape(model_wrapper, graph)

    for layer in input_shapes:
        log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))

    if args.input:
        log.info(f'Preparing input data: {args.input}')
        io.prepare_input(graph, args.input)
    else:
        io.fill_unset_inputs(graph, log, custom_shapes=input_shapes)

    inputs_names = model_wrapper.get_input_layer_names(graph)
    log.info(f'Got input names {inputs_names}')
    outputs_names = model_wrapper.get_outputs_layer_names(graph, output_names)

    result, inference_time = inference_tensorflow(model, args.number_iter,
                                                  io.get_slice_input, args.time)

    log.info('Computing performance metrics')
    inference_result = pp.calculate_performance_metrics_sync_mode(args.batch_size, inference_time)

    report_writer.update_execution_results(**inference_result)
    log.info(f'Write report to {args.report_path}')
    report_writer.write_report(args.report_path)

    if not args.raw_output:
        if args.number_iter == 1:
            result = prepare_output(result, outputs_names, args.task)
            io.process_output(result, log)

    log.info(f'Performance results:\n{json.dumps(inference_result, indent=4)}')


if __name__ == '__main__':
    sys.exit(main() or 0)
