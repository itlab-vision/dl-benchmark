import argparse
import logging as log
import sys
from time import time

import cv2

import postprocessing_data as pp
from io_adapter import IOAdapter
from io_model_wrapper import OpenCVIOModelWrapper
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
                        required=True,
                        type=str,
                        dest='weights')
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
    parser.add_argument('-in', '--input_name',
                        help='Input layer name',
                        default='_input',
                        type=str,
                        dest='input_name')
    parser.add_argument('--scalefactor',
                        help='Parameter input scale',
                        default=1.0,
                        type=float,
                        dest='scalefactor')
    parser.add_argument('--size',
                        help='Parameter size',
                        default=[224, 224],
                        type=int,
                        nargs=2,
                        dest='size')
    parser.add_argument('--mean',
                        help='Parameter mean',
                        default=[0, 0, 0],
                        type=float,
                        nargs=3,
                        dest='mean')
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

    args = parser.parse_args()

    return args


def set_backend_to_infer(net, backend):
    if backend == 'DNN':
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    elif backend == 'IE':
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
    else:
        raise ValueError('The backend is not available')


def set_device_to_infer(net, device):
    if device == 'CPU':
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    # TODO: add devices
    else:
        raise ValueError('The device is not available')


def load_network(model, weights):
    net = cv2.dnn.readNet(model, weights)
    return net


def load_images_to_network(net, input_):
    net.setInput(input_)


def inference_opencv(net, input_name, number_iter, get_slice):
    result = None
    time_infer = []
    slice_input = None

    if number_iter == 1:
        slice_input = get_slice(0)
        load_images_to_network(net, slice_input[input_name])
        t0 = time()
        result = net.forward()
        t1 = time()
        time_infer.append(t1 - t0)
    else:
        for i in range(number_iter):
            slice_input = get_slice(i)
            load_images_to_network(net, slice_input[input_name])
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
        'scalefactor': args.scalefactor,
        'size': tuple(args.size),
        'mean': tuple(args.mean),
        'swapRB': args.swapRB,
        'crop': args.crop,
    }
    return dictionary


def create_dict_for_wrapper(args):
    dictionary = {
        'input_layer_name': args.input_name,
        'input_layer_shape': [
            args.batch_size,
            args.size[0],
            args.size[1],
            len(args.mean)
        ]
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
        model_wrapper = OpenCVIOModelWrapper(create_dict_for_wrapper(args))
        data_transformer = OpenCVTransformer(create_dict_for_transformer(args))
        io = IOAdapter.get_io_adapter(args, model_wrapper, data_transformer)

        log.info('Loading network files:\n\t {0}\n\t {1}'.format(args.model, args.weights))
        net = load_network(args.model, args.weights)

        layer_name = model_wrapper.get_input_layer_names(net)
        log.info('Shape for input layer {0}: {1}'.format(
            layer_name,
            model_wrapper.get_input_layer_shape(net, layer_name),
        ))

        log.info('The assign of the backend to infer')
        set_backend_to_infer(net, args.backend)
        log.info('The backend has been assigned: {0}'.format(args.backend))

        log.info('The assign of the device to infer')
        set_device_to_infer(net, args.device)
        log.info('The device has been assigned: {0}'.format(args.device))

        log.info('Prepare input data')
        io.prepare_input(net, args.input)

        log.info(f'Starting inference ({args.number_iter} iterations)')
        result, inference_time = inference_opencv(net, args.input_name, args.number_iter, io.get_slice_input)
        average_time, latency, fps = process_result(args.batch_size, inference_time)

        if not args.raw_output:
            io.process_output(result, log)
            result_output(average_time, fps, latency, log)
        else:
            raw_result_output(average_time, fps, latency)
    except Exception as ex:
        print('ERROR! : {0}'.format(str(ex)))
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
