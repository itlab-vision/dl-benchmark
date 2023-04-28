import argparse
import logging as log
import sys
import traceback
from time import time

import caffe

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import IntelCaffeIOModelWrapper
from transformer import IntelCaffeTransformer


def cli_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                        help='Path to an .prototxt file with a trained model.',
                        required=True,
                        type=str,
                        dest='model_prototxt')
    parser.add_argument('-w', '--weights',
                        help='Path to an .caffemodel file with a trained weights.',
                        required=True,
                        type=str,
                        dest='model_caffemodel')
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
                        choices=['classification', 'detection', 'segmentation'],
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


def set_device_to_infer(device):
    if device == 'CPU':
        caffe.set_mode_cpu()
    else:
        raise ValueError('The device is not supported')


def network_input_reshape(net, batch_size):
    for layer_input in net.inputs:
        _, c, h, w = net.blobs[layer_input].data.shape
        net.blobs[layer_input].reshape(batch_size, c, h, w)
    net.reshape()

    return net


def load_network(prototxt, caffemodel):
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    return net


def load_images_to_network(net, input_):
    for layer in input_:
        net.blobs[layer].data[...] = input_[layer]


def inference_caffe(net, number_iter, get_slice):
    result = None
    time_infer = []
    slice_input = None
    if number_iter == 1:
        slice_input = get_slice(0)
        load_images_to_network(net, slice_input)
        t0 = time()
        result = net.forward()
        t1 = time()
        time_infer.append(t1 - t0)
    else:
        for i in range(number_iter):
            slice_input = get_slice(i)
            load_images_to_network(net, slice_input)
            t0 = time()
            net.forward()
            t1 = time()
            time_infer.append(t1 - t0)

    return result, time_infer


def process_result(batch_size, inference_time):
    inference_time = pp.three_sigma_rule(inference_time)
    average_time = pp.calculate_average_time(inference_time)
    latency = pp.calculate_latency(inference_time)
    fps = pp.calculate_fps(batch_size, latency)
    return average_time, latency, fps


def result_output(average_time, fps, latency, log):
    log.info('Average time of single pass : {0:.3f}'.format(average_time))
    log.info('FPS : {0:.3f}'.format(fps))
    log.info('Latency : {0:.3f}'.format(latency))


def raw_result_output(average_time, fps, latency):
    print('{0:.3f},{1:.3f},{2:.3f}'.format(average_time, fps, latency))


def create_dict_for_transformer(args):
    dictionary = {
        'channel_swap': args.channel_swap,
        'mean': args.mean,
        'input_scale': args.input_scale,
    }
    return dictionary


def main():
    log.basicConfig(
        format='[ %(levelname)s ] %(message)s',
        level=log.INFO,
        stream=sys.stdout,
    )
    args = cli_argument_parser()
    try:
        model_wrapper = IntelCaffeIOModelWrapper()
        data_transformer = IntelCaffeTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        log.info('The assign of the device to infer')

        set_device_to_infer(args.device)

        log.info('The device has been assigned: {0}'.format(args.device))
        log.info('Loading network files:\n\t {0}\n\t {1}'.format(args.model_prototxt, args.model_caffemodel))

        net = load_network(args.model_prototxt, args.model_caffemodel)
        net = network_input_reshape(net, args.batch_size)
        input_shapes = get_input_shape(model_wrapper, net)

        for layer in input_shapes:
            log.info('Shape for input layer {0}: {1}'.format(layer, input_shapes[layer]))
        log.info('Prepare input data')

        io.prepare_input(net, args.input)

        log.info(f'Starting inference ({args.number_iter} iterations)')

        result, inference_time = inference_caffe(net, args.number_iter, io.get_slice_input)
        time, latency, fps = process_result(args.batch_size, inference_time)

        if not args.raw_output:
            io.process_output(result, log)
            result_output(time, fps, latency, log)
        else:
            raw_result_output(time, fps, latency)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
